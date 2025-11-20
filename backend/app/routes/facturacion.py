"""
Rutas para el módulo de Facturación y Caja.
Endpoints: caja, facturas, convenios, cuentas por cobrar
"""

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import (
    Caja, MovimientoCaja, Factura, FacturaDetalle, Convenio,
    CuentaPorCobrar, PagoCuenta, Paciente
)
from app.services.fel_service import FELService
from app.services.reporte_service import ReporteService
from app.utils.decorators import role_required
from app.utils.pdf_generator import PDFGenerator
from datetime import datetime, timedelta

bp = Blueprint('facturacion', __name__, url_prefix='/api')

# ==================== CAJA ====================

@bp.route('/caja/apertura', methods=['POST'])
@jwt_required()
@role_required('recepcionista', 'administrador')
def abrir_caja():
    """Abre una nueva caja"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if 'monto_inicial' not in data:
        return jsonify({'success': False, 'message': 'Campo requerido: monto_inicial'}), 400
    
    # Verificar que no haya una caja abierta
    caja_abierta = Caja.query.filter_by(
        usuario_id=current_user_id,
        estado='abierta'
    ).first()
    
    if caja_abierta:
        return jsonify({'success': False, 'message': 'Ya tienes una caja abierta'}), 400
    
    # Crear nueva caja
    caja = Caja(
        usuario_id=current_user_id,
        monto_inicial=data['monto_inicial'],
        observaciones=data.get('observaciones')
    )
    
    db.session.add(caja)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Caja abierta correctamente',
        'caja': caja.to_dict()
    }), 201


@bp.route('/caja/cierre', methods=['POST'])
@jwt_required()
@role_required('recepcionista', 'administrador')
def cerrar_caja():
    """Cierra la caja actual"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if 'efectivo_contado' not in data:
        return jsonify({'success': False, 'message': 'Campo requerido: efectivo_contado'}), 400
    
    # Buscar caja abierta
    caja = Caja.query.filter_by(
        usuario_id=current_user_id,
        estado='abierta'
    ).first()
    
    if not caja:
        return jsonify({'success': False, 'message': 'No tienes una caja abierta'}), 404
    
    # Cerrar caja
    caja.cerrar_caja(
        efectivo_contado=data['efectivo_contado'],
        observaciones=data.get('observaciones')
    )
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Caja cerrada correctamente',
        'caja': caja.to_dict(incluir_movimientos=True)
    }), 200


@bp.route('/caja/estado', methods=['GET'])
@jwt_required()
def obtener_estado_caja():
    """Obtiene el estado de la caja actual del usuario"""
    current_user_id = get_jwt_identity()
    
    caja = Caja.query.filter_by(
        usuario_id=current_user_id,
        estado='abierta'
    ).first()
    
    if not caja:
        return jsonify({
            'success': True,
            'caja_abierta': False,
            'message': 'No hay caja abierta'
        }), 200
    
    return jsonify({
        'success': True,
        'caja_abierta': True,
        'caja': caja.to_dict(incluir_movimientos=True)
    }), 200


@bp.route('/caja/movimientos', methods=['GET'])
@jwt_required()
def listar_movimientos_caja():
    """Lista movimientos de caja con filtros"""
    caja_id = request.args.get('caja_id')
    tipo = request.args.get('tipo')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    query = MovimientoCaja.query
    
    if caja_id:
        query = query.filter_by(caja_id=caja_id)
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    if fecha_inicio:
        query = query.filter(MovimientoCaja.fecha_movimiento >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(MovimientoCaja.fecha_movimiento <= fecha_fin)
    
    movimientos = query.order_by(MovimientoCaja.fecha_movimiento.desc()).all()
    
    return jsonify({
        'success': True,
        'movimientos': [m.to_dict(incluir_relaciones=True) for m in movimientos],
        'total': len(movimientos)
    }), 200


@bp.route('/caja/ingresos', methods=['POST'])
@jwt_required()
@role_required('recepcionista', 'administrador')
def registrar_ingreso():
    """Registra un ingreso en caja"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    required_fields = ['categoria', 'concepto', 'monto']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Campo requerido: {field}'}), 400
    
    # Buscar caja abierta
    caja = Caja.query.filter_by(
        usuario_id=current_user_id,
        estado='abierta'
    ).first()
    
    if not caja:
        return jsonify({'success': False, 'message': 'No tienes una caja abierta'}), 404
    
    # Registrar movimiento
    movimiento = MovimientoCaja.registrar_ingreso(
        caja_id=caja.id,
        categoria=data['categoria'],
        concepto=data['concepto'],
        monto=data['monto'],
        forma_pago=data.get('forma_pago', 'efectivo'),
        paciente_id=data.get('paciente_id'),
        medico_id=data.get('medico_id'),
        referencia_id=data.get('referencia_id'),
        referencia_tipo=data.get('referencia_tipo'),
        usuario_id=current_user_id,
        observaciones=data.get('observaciones')
    )
    
    db.session.add(movimiento)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Ingreso registrado correctamente',
        'movimiento': movimiento.to_dict(incluir_relaciones=True)
    }), 201


@bp.route('/caja/egresos', methods=['POST'])
@jwt_required()
@role_required('recepcionista', 'administrador')
def registrar_egreso():
    """Registra un egreso en caja"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    required_fields = ['categoria', 'concepto', 'monto']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Campo requerido: {field}'}), 400
    
    # Buscar caja abierta
    caja = Caja.query.filter_by(
        usuario_id=current_user_id,
        estado='abierta'
    ).first()
    
    if not caja:
        return jsonify({'success': False, 'message': 'No tienes una caja abierta'}), 404
    
    # Registrar movimiento
    movimiento = MovimientoCaja.registrar_egreso(
        caja_id=caja.id,
        categoria=data['categoria'],
        concepto=data['concepto'],
        monto=data['monto'],
        forma_pago=data.get('forma_pago', 'efectivo'),
        referencia_id=data.get('referencia_id'),
        referencia_tipo=data.get('referencia_tipo'),
        usuario_id=current_user_id,
        observaciones=data.get('observaciones')
    )
    
    db.session.add(movimiento)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Egreso registrado correctamente',
        'movimiento': movimiento.to_dict(incluir_relaciones=True)
    }), 201


@bp.route('/caja/<int:id>/reporte', methods=['GET'])
@jwt_required()
def generar_reporte_arqueo(id):
    """Genera PDF de arqueo de caja"""
    caja = Caja.query.get(id)
    
    if not caja:
        return jsonify({'success': False, 'message': 'Caja no encontrada'}), 404
    
    # Generar PDF
    pdf_buffer = PDFGenerator.generar_reporte_arqueo_caja(caja)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'arqueo_caja_{caja.id}.pdf'
    )


# ==================== FACTURAS ====================

@bp.route('/facturas', methods=['GET'])
@jwt_required()
def listar_facturas():
    """Lista facturas con filtros"""
    paciente_id = request.args.get('paciente_id')
    estado = request.args.get('estado')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    query = Factura.query
    
    if paciente_id:
        query = query.filter_by(paciente_id=paciente_id)
    
    if estado:
        query = query.filter_by(estado=estado)
    
    if fecha_inicio:
        query = query.filter(Factura.fecha_emision >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(Factura.fecha_emision <= fecha_fin)
    
    facturas = query.order_by(Factura.fecha_emision.desc()).all()
    
    return jsonify({
        'success': True,
        'facturas': [f.to_dict(incluir_relaciones=True) for f in facturas],
        'total': len(facturas)
    }), 200


@bp.route('/facturas/<int:id>', methods=['GET'])
@jwt_required()
def obtener_factura(id):
    """Obtiene una factura específica"""
    factura = Factura.query.get(id)
    
    if not factura:
        return jsonify({'success': False, 'message': 'Factura no encontrada'}), 404
    
    return jsonify({
        'success': True,
        'factura': factura.to_dict(incluir_relaciones=True)
    }), 200


@bp.route('/facturas', methods=['POST'])
@jwt_required()
@role_required('recepcionista', 'administrador')
def crear_factura():
    """Crea una nueva factura"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    required_fields = ['paciente_id', 'detalles']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Campo requerido: {field}'}), 400
    
    # Verificar paciente
    paciente = Paciente.query.get(data['paciente_id'])
    if not paciente:
        return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
    
    # Crear factura
    factura = Factura(
        paciente_id=data['paciente_id'],
        convenio_id=data.get('convenio_id'),
        nit_cliente=data.get('nit_cliente'),
        nombre_cliente=data.get('nombre_cliente') or paciente.nombre_completo,
        direccion_cliente=data.get('direccion_cliente'),
        subtotal=0,
        descuento=data.get('descuento', 0),
        forma_pago=data.get('forma_pago', 'efectivo'),
        usuario_id=current_user_id,
        observaciones=data.get('observaciones')
    )
    
    # Generar número de factura
    factura.generar_numero_factura(serie=data.get('serie', 'A'))
    
    db.session.add(factura)
    db.session.flush()
    
    # Agregar detalles
    for detalle_data in data['detalles']:
        detalle = FacturaDetalle(
            factura_id=factura.id,
            descripcion=detalle_data['descripcion'],
            cantidad=detalle_data['cantidad'],
            precio_unitario=detalle_data['precio_unitario'],
            tipo_servicio=detalle_data.get('tipo_servicio'),
            referencia_id=detalle_data.get('referencia_id')
        )
        detalle.calcular_subtotal()
        db.session.add(detalle)
    
    # Calcular totales
    factura.calcular_totales()
    
    # Si es a crédito, crear cuenta por cobrar
    if factura.forma_pago == 'credito':
        factura.estado = 'credito'
        
        cuenta = CuentaPorCobrar(
            factura_id=factura.id,
            paciente_id=factura.paciente_id if not factura.convenio_id else None,
            convenio_id=factura.convenio_id,
            monto_total=factura.total,
            saldo_pendiente=factura.total,
            fecha_vencimiento=(datetime.now() + timedelta(days=30)).date()
        )
        db.session.add(cuenta)
    else:
        factura.estado = 'pagada'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Factura creada correctamente',
        'factura': factura.to_dict(incluir_relaciones=True)
    }), 201


@bp.route('/facturas/<int:id>/anular', methods=['POST'])
@jwt_required()
@role_required('administrador')
def anular_factura(id):
    """Anula una factura"""
    data = request.get_json()
    
    factura = Factura.query.get(id)
    if not factura:
        return jsonify({'success': False, 'message': 'Factura no encontrada'}), 404
    
    if factura.estado == 'anulada':
        return jsonify({'success': False, 'message': 'La factura ya está anulada'}), 400
    
    factura.anular(motivo=data.get('motivo'))
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Factura anulada correctamente',
        'factura': factura.to_dict()
    }), 200


@bp.route('/facturas/<int:id>/certificar-fel', methods=['POST'])
@jwt_required()
@role_required('administrador')
def certificar_factura_fel(id):
    """Certifica una factura con FEL (preparación Fase 7)"""
    resultado = FELService.certificar_factura(id)
    
    return jsonify({
        'success': resultado['success'],
        'message': resultado['message'],
        'datos': resultado
    }), 200 if resultado['success'] else 400


# ==================== CONVENIOS ====================

@bp.route('/convenios', methods=['GET'])
@jwt_required()
def listar_convenios():
    """Lista todos los convenios"""
    solo_activos = request.args.get('solo_activos') == 'true'
    
    query = Convenio.query
    
    if solo_activos:
        query = query.filter_by(activo=True)
    
    convenios = query.all()
    
    return jsonify({
        'success': True,
        'convenios': [c.to_dict() for c in convenios],
        'total': len(convenios)
    }), 200


@bp.route('/convenios', methods=['POST'])
@jwt_required()
@role_required('administrador')
def crear_convenio():
    """Crea un nuevo convenio"""
    data = request.get_json()
    
    required_fields = ['nombre', 'tipo']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Campo requerido: {field}'}), 400
    
    convenio = Convenio(
        nombre=data['nombre'],
        tipo=data['tipo'],
        nit=data.get('nit'),
        contacto_nombre=data.get('contacto_nombre'),
        contacto_telefono=data.get('contacto_telefono'),
        contacto_email=data.get('contacto_email'),
        porcentaje_cobertura=data.get('porcentaje_cobertura'),
        dias_credito=data.get('dias_credito', 30),
        observaciones=data.get('observaciones')
    )
    
    db.session.add(convenio)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Convenio creado correctamente',
        'convenio': convenio.to_dict()
    }), 201


# ==================== CUENTAS POR COBRAR ====================

@bp.route('/cuentas-por-cobrar', methods=['GET'])
@jwt_required()
def listar_cuentas_por_cobrar():
    """Lista cuentas por cobrar con filtros"""
    estado = request.args.get('estado')
    paciente_id = request.args.get('paciente_id')
    convenio_id = request.args.get('convenio_id')
    
    query = CuentaPorCobrar.query
    
    if estado:
        query = query.filter_by(estado=estado)
    
    if paciente_id:
        query = query.filter_by(paciente_id=paciente_id)
    
    if convenio_id:
        query = query.filter_by(convenio_id=convenio_id)
    
    cuentas = query.order_by(CuentaPorCobrar.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'cuentas': [c.to_dict(incluir_pagos=True) for c in cuentas],
        'total': len(cuentas)
    }), 200


@bp.route('/cuentas-por-cobrar/<int:id>/pagar', methods=['POST'])
@jwt_required()
@role_required('recepcionista', 'administrador')
def registrar_pago_cuenta(id):
    """Registra un pago a una cuenta por cobrar"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if 'monto' not in data:
        return jsonify({'success': False, 'message': 'Campo requerido: monto'}), 400
    
    cuenta = CuentaPorCobrar.query.get(id)
    if not cuenta:
        return jsonify({'success': False, 'message': 'Cuenta no encontrada'}), 404
    
    try:
        pago = cuenta.registrar_pago(
            monto=data['monto'],
            forma_pago=data.get('forma_pago', 'efectivo'),
            numero_recibo=data.get('numero_recibo'),
            usuario_id=current_user_id,
            observaciones=data.get('observaciones')
        )
        
        db.session.add(pago)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pago registrado correctamente',
            'cuenta': cuenta.to_dict(incluir_pagos=True)
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
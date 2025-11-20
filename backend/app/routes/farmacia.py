"""
Rutas para el módulo de Farmacia e Inventario.
Endpoints: productos, proveedores, compras, dispensación, alertas, kardex
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import (
    ProductoFarmacia, Proveedor, Compra, CompraDetalle,
    MovimientoInventario
)
from app.services.inventario_service import InventarioService
from app.utils.decorators import role_required
from datetime import datetime

bp = Blueprint('farmacia', __name__, url_prefix='/api/farmacia')

# ==================== PRODUCTOS ====================

@bp.route('/productos', methods=['GET'])
@jwt_required()
def listar_productos():
    """Lista productos de farmacia con filtros"""
    query_param = request.args.get('q')
    tipo_producto = request.args.get('tipo_producto')
    solo_con_stock = request.args.get('solo_con_stock') == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if query_param:
        productos = InventarioService.buscar_productos(
            query=query_param,
            tipo_producto=tipo_producto,
            solo_con_stock=solo_con_stock
        )
        return jsonify({
            'success': True,
            'productos': productos,
            'total': len(productos)
        }), 200
    
    query = ProductoFarmacia.query.filter_by(activo=True)
    
    if tipo_producto:
        query = query.filter_by(tipo_producto=tipo_producto)
    
    if solo_con_stock:
        query = query.filter(ProductoFarmacia.stock_actual > 0)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'productos': [p.to_dict(incluir_relaciones=True) for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@bp.route('/productos/<int:id>', methods=['GET'])
@jwt_required()
def obtener_producto(id):
    """Obtiene un producto específico"""
    producto = ProductoFarmacia.query.get(id)
    
    if not producto:
        return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
    
    return jsonify({
        'success': True,
        'producto': producto.to_dict(incluir_relaciones=True)
    }), 200


@bp.route('/productos', methods=['POST'])
@jwt_required()
@role_required('administrador', 'medico')
def crear_producto():
    """Crea un nuevo producto de farmacia"""
    data = request.get_json()
    
    # Validaciones
    required_fields = ['nombre_generico', 'tipo_producto']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Campo requerido: {field}'}), 400
    
    # Crear producto
    producto = ProductoFarmacia(
        nombre_generico=data['nombre_generico'],
        nombre_comercial=data.get('nombre_comercial'),
        presentacion=data.get('presentacion'),
        concentracion=data.get('concentracion'),
        tipo_producto=data['tipo_producto'],
        lote=data.get('lote'),
        fecha_vencimiento=datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date() if data.get('fecha_vencimiento') else None,
        proveedor_id=data.get('proveedor_id'),
        precio_compra=data.get('precio_compra'),
        precio_venta=data.get('precio_venta'),
        stock_actual=data.get('stock_actual', 0),
        stock_minimo=data.get('stock_minimo', 10),
        ubicacion=data.get('ubicacion'),
        requiere_receta=data.get('requiere_receta', False)
    )
    
    # Generar código interno si no existe
    if not data.get('codigo_interno'):
        producto.generar_codigo_interno()
    else:
        producto.codigo_interno = data['codigo_interno']
    
    db.session.add(producto)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Producto creado correctamente',
        'producto': producto.to_dict(incluir_relaciones=True)
    }), 201


@bp.route('/productos/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('administrador', 'medico')
def actualizar_producto(id):
    """Actualiza un producto existente"""
    data = request.get_json()
    
    producto = ProductoFarmacia.query.get(id)
    if not producto:
        return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
    
    # Actualizar campos
    campos_actualizables = [
        'nombre_generico', 'nombre_comercial', 'presentacion', 'concentracion',
        'lote', 'proveedor_id', 'precio_compra', 'precio_venta',
        'stock_minimo', 'ubicacion', 'requiere_receta', 'activo'
    ]
    
    for campo in campos_actualizables:
        if campo in data:
            setattr(producto, campo, data[campo])
    
    if 'fecha_vencimiento' in data and data['fecha_vencimiento']:
        producto.fecha_vencimiento = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Producto actualizado correctamente',
        'producto': producto.to_dict(incluir_relaciones=True)
    }), 200


# ==================== ALERTAS ====================

@bp.route('/alertas', methods=['GET'])
@jwt_required()
def obtener_alertas():
    """Obtiene todas las alertas de inventario"""
    alertas = InventarioService.obtener_alertas()
    
    return jsonify({
        'success': True,
        'alertas': alertas
    }), 200


@bp.route('/productos/reorden', methods=['GET'])
@jwt_required()
def productos_reorden():
    """Lista productos que necesitan reorden"""
    productos = InventarioService.obtener_productos_reorden()
    
    return jsonify({
        'success': True,
        'productos': productos,
        'total': len(productos)
    }), 200


# ==================== KARDEX ====================

@bp.route('/productos/<int:id>/kardex', methods=['GET'])
@jwt_required()
def obtener_kardex(id):
    """Obtiene el kardex de un producto"""
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    producto = ProductoFarmacia.query.get(id)
    if not producto:
        return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
    
    kardex = InventarioService.obtener_kardex(
        producto_id=id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    
    return jsonify({
        'success': True,
        'producto': producto.to_dict(),
        'kardex': kardex
    }), 200


# ==================== INVENTARIO ====================

@bp.route('/inventario/ajustar', methods=['POST'])
@jwt_required()
@role_required('administrador')
def ajustar_inventario():
    """Ajusta el inventario de un producto"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if 'producto_id' not in data or 'stock_nuevo' not in data or 'motivo' not in data:
        return jsonify({'success': False, 'message': 'Campos requeridos: producto_id, stock_nuevo, motivo'}), 400
    
    try:
        resultado = InventarioService.ajustar_inventario(
            producto_id=data['producto_id'],
            stock_nuevo=data['stock_nuevo'],
            motivo=data['motivo'],
            usuario_id=current_user_id
        )
        
        return jsonify({
            'success': True,
            'message': 'Inventario ajustado correctamente',
            'resultado': resultado
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/inventario/valorizado', methods=['GET'])
@jwt_required()
@role_required('administrador')
def inventario_valorizado():
    """Obtiene el valor total del inventario"""
    valorizado = InventarioService.obtener_inventario_valorizado()
    
    return jsonify({
        'success': True,
        'inventario': valorizado
    }), 200


# ==================== DISPENSACIÓN ====================

@bp.route('/dispensacion', methods=['POST'])
@jwt_required()
@role_required('medico', 'enfermera', 'recepcionista')
def dispensar_producto():
    """Dispensa un producto de farmacia"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if 'producto_id' not in data or 'cantidad' not in data:
        return jsonify({'success': False, 'message': 'Campos requeridos: producto_id, cantidad'}), 400
    
    try:
        resultado = InventarioService.dispensar_producto(
            producto_id=data['producto_id'],
            cantidad=data['cantidad'],
            receta_id=data.get('receta_id'),
            usuario_id=current_user_id
        )
        
        return jsonify({
            'success': True,
            'message': 'Producto dispensado correctamente',
            'resultado': resultado
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400


# ==================== PROVEEDORES ====================

@bp.route('/proveedores', methods=['GET'])
@jwt_required()
def listar_proveedores():
    """Lista todos los proveedores"""
    solo_activos = request.args.get('solo_activos') == 'true'
    
    query = Proveedor.query
    
    if solo_activos:
        query = query.filter_by(activo=True)
    
    proveedores = query.all()
    
    return jsonify({
        'success': True,
        'proveedores': [p.to_dict(incluir_estadisticas=True) for p in proveedores],
        'total': len(proveedores)
    }), 200


@bp.route('/proveedores', methods=['POST'])
@jwt_required()
@role_required('administrador')
def crear_proveedor():
    """Crea un nuevo proveedor"""
    data = request.get_json()
    
    if 'nombre' not in data:
        return jsonify({'success': False, 'message': 'Campo requerido: nombre'}), 400
    
    proveedor = Proveedor(
        nombre=data['nombre'],
        nit=data.get('nit'),
        direccion=data.get('direccion'),
        telefono=data.get('telefono'),
        email=data.get('email'),
        contacto_nombre=data.get('contacto_nombre'),
        productos_suministra=data.get('productos_suministra')
    )
    
    db.session.add(proveedor)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Proveedor creado correctamente',
        'proveedor': proveedor.to_dict()
    }), 201


# ==================== COMPRAS ====================

@bp.route('/compras', methods=['GET'])
@jwt_required()
def listar_compras():
    """Lista compras con filtros"""
    proveedor_id = request.args.get('proveedor_id')
    estado = request.args.get('estado')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    query = Compra.query
    
    if proveedor_id:
        query = query.filter_by(proveedor_id=proveedor_id)
    
    if estado:
        query = query.filter_by(estado=estado)
    
    if fecha_inicio:
        query = query.filter(Compra.fecha_compra >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(Compra.fecha_compra <= fecha_fin)
    
    compras = query.order_by(Compra.fecha_compra.desc()).all()
    
    return jsonify({
        'success': True,
        'compras': [c.to_dict(incluir_relaciones=True) for c in compras],
        'total': len(compras)
    }), 200


@bp.route('/compras', methods=['POST'])
@jwt_required()
@role_required('administrador')
def crear_compra():
    """Crea una nueva orden de compra"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if 'proveedor_id' not in data or 'detalles' not in data:
        return jsonify({'success': False, 'message': 'Campos requeridos: proveedor_id, detalles'}), 400
    
    # Crear compra
    compra = Compra(
        proveedor_id=data['proveedor_id'],
        numero_factura=data.get('numero_factura'),
        fecha_compra=datetime.now().date(),
        total=0,  # Se calcula después
        usuario_id=current_user_id,
        observaciones=data.get('observaciones')
    )
    
    db.session.add(compra)
    db.session.flush()  # Para obtener el ID
    
    # Agregar detalles
    for detalle_data in data['detalles']:
        detalle = CompraDetalle(
            compra_id=compra.id,
            producto_id=detalle_data['producto_id'],
            cantidad=detalle_data['cantidad'],
            precio_unitario=detalle_data['precio_unitario'],
            lote=detalle_data.get('lote'),
            fecha_vencimiento=datetime.strptime(detalle_data['fecha_vencimiento'], '%Y-%m-%d').date() if detalle_data.get('fecha_vencimiento') else None
        )
        detalle.calcular_subtotal()
        db.session.add(detalle)
    
    # Calcular totales
    compra.calcular_totales()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Compra creada correctamente',
        'compra': compra.to_dict(incluir_relaciones=True)
    }), 201


@bp.route('/compras/<int:id>/recibir', methods=['POST'])
@jwt_required()
@role_required('administrador')
def recibir_compra(id):
    """Marca una compra como recibida y actualiza inventario"""
    current_user_id = get_jwt_identity()
    
    compra = Compra.query.get(id)
    if not compra:
        return jsonify({'success': False, 'message': 'Compra no encontrada'}), 404
    
    if compra.estado == 'recibida':
        return jsonify({'success': False, 'message': 'La compra ya fue recibida'}), 400
    
    # Actualizar inventario con cada detalle
    for detalle in compra.detalles:
        producto = ProductoFarmacia.query.get(detalle.producto_id)
        
        if producto:
            # Registrar entrada en inventario
            movimiento = MovimientoInventario.registrar_entrada(
                producto=producto,
                cantidad=detalle.cantidad,
                motivo='Compra recibida',
                referencia_id=compra.id,
                referencia_tipo='compra',
                usuario_id=current_user_id
            )
            
            # Actualizar lote y vencimiento si vienen en el detalle
            if detalle.lote:
                producto.lote = detalle.lote
            if detalle.fecha_vencimiento:
                producto.fecha_vencimiento = detalle.fecha_vencimiento
            
            db.session.add(movimiento)
    
    # Marcar compra como recibida
    compra.marcar_como_recibida()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Compra recibida e inventario actualizado',
        'compra': compra.to_dict(incluir_relaciones=True)
    }), 200
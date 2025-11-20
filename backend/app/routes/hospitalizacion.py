"""
Rutas para el módulo de Hospitalización.
Endpoints: camas, hospitalizaciones, notas médicas, órdenes, registro enfermería
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import (
    Cama, Hospitalizacion, NotaMedica, OrdenMedica, 
    RegistroEnfermeria, Paciente, Usuario
)
from app.utils.decorators import role_required
from datetime import datetime

bp = Blueprint('hospitalizacion', __name__, url_prefix='/api/hospitalizacion')

# ==================== CAMAS ====================

@bp.route('/camas', methods=['GET'])
@jwt_required()
def listar_camas():
    """Lista todas las camas con su estado actual"""
    estado = request.args.get('estado')
    
    query = Cama.query
    
    if estado:
        query = query.filter_by(estado=estado)
    
    camas = query.all()
    
    return jsonify({
        'success': True,
        'camas': [cama.to_dict() for cama in camas],
        'total': len(camas)
    }), 200


@bp.route('/camas/<int:cama_id>', methods=['PUT'])
@jwt_required()
@role_required('medico', 'enfermera', 'administrador')
def actualizar_cama(cama_id):
    """Actualiza el estado de una cama"""
    data = request.get_json()
    
    cama = Cama.query.get(cama_id)
    if not cama:
        return jsonify({'success': False, 'message': 'Cama no encontrada'}), 404
    
    if 'estado' in data:
        cama.estado = data['estado']
    
    if 'observaciones' in data:
        cama.observaciones = data['observaciones']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cama actualizada correctamente',
        'cama': cama.to_dict()
    }), 200


# ==================== HOSPITALIZACIONES ====================

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_hospitalizaciones():
    """Lista hospitalizaciones con filtros"""
    estado = request.args.get('estado')
    paciente_id = request.args.get('paciente_id')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    query = Hospitalizacion.query
    
    if estado:
        query = query.filter_by(estado=estado)
    
    if paciente_id:
        query = query.filter_by(paciente_id=paciente_id)
    
    if fecha_inicio:
        query = query.filter(Hospitalizacion.fecha_ingreso >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(Hospitalizacion.fecha_ingreso <= fecha_fin)
    
    hospitalizaciones = query.order_by(Hospitalizacion.fecha_ingreso.desc()).all()
    
    return jsonify({
        'success': True,
        'hospitalizaciones': [h.to_dict(incluir_relaciones=True) for h in hospitalizaciones],
        'total': len(hospitalizaciones)
    }), 200


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obtener_hospitalizacion(id):
    """Obtiene una hospitalización específica con toda su información"""
    hospitalizacion = Hospitalizacion.query.get(id)
    
    if not hospitalizacion:
        return jsonify({'success': False, 'message': 'Hospitalización no encontrada'}), 404
    
    return jsonify({
        'success': True,
        'hospitalizacion': hospitalizacion.to_dict(incluir_relaciones=True),
        'notas_medicas': [nota.to_dict(incluir_relaciones=True) for nota in hospitalizacion.notas_medicas],
        'ordenes_medicas': [orden.to_dict(incluir_relaciones=True) for orden in hospitalizacion.ordenes_medicas],
        'registros_enfermeria': [reg.to_dict(incluir_relaciones=True) for reg in hospitalizacion.registros_enfermeria]
    }), 200


@bp.route('/', methods=['POST'])
@jwt_required()
@role_required('medico')
def ingresar_paciente():
    """Ingresa un paciente a hospitalización"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validaciones
    required_fields = ['paciente_id', 'cama_id', 'motivo_ingreso', 'diagnostico_ingreso']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Campo requerido: {field}'}), 400
    
    # Verificar que el paciente existe
    paciente = Paciente.query.get(data['paciente_id'])
    if not paciente:
        return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
    
    # Verificar que la cama está disponible
    cama = Cama.query.get(data['cama_id'])
    if not cama:
        return jsonify({'success': False, 'message': 'Cama no encontrada'}), 404
    
    if not cama.esta_disponible():
        return jsonify({'success': False, 'message': 'La cama no está disponible'}), 400
    
    # Crear hospitalización
    hospitalizacion = Hospitalizacion(
        paciente_id=data['paciente_id'],
        cama_id=data['cama_id'],
        medico_responsable_id=current_user_id,
        fecha_ingreso=datetime.utcnow(),
        motivo_ingreso=data['motivo_ingreso'],
        diagnostico_ingreso=data['diagnostico_ingreso'],
        observaciones=data.get('observaciones')
    )
    
    # Ocupar la cama
    cama.ocupar()
    
    db.session.add(hospitalizacion)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Paciente ingresado a hospitalización',
        'hospitalizacion': hospitalizacion.to_dict(incluir_relaciones=True)
    }), 201


@bp.route('/<int:id>/egreso', methods=['POST'])
@jwt_required()
@role_required('medico')
def egresar_paciente(id):
    """Egresa un paciente de hospitalización"""
    data = request.get_json()
    
    hospitalizacion = Hospitalizacion.query.get(id)
    if not hospitalizacion:
        return jsonify({'success': False, 'message': 'Hospitalización no encontrada'}), 404
    
    if not hospitalizacion.esta_activa():
        return jsonify({'success': False, 'message': 'La hospitalización ya no está activa'}), 400
    
    if 'diagnostico_egreso' not in data:
        return jsonify({'success': False, 'message': 'Campo requerido: diagnostico_egreso'}), 400
    
    # Egresar
    hospitalizacion.egresar(
        diagnostico_egreso=data['diagnostico_egreso'],
        observaciones=data.get('observaciones')
    )
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Paciente egresado exitosamente',
        'hospitalizacion': hospitalizacion.to_dict(incluir_relaciones=True)
    }), 200


# ==================== NOTAS MÉDICAS ====================

@bp.route('/<int:id>/notas', methods=['POST'])
@jwt_required()
@role_required('medico')
def agregar_nota_medica(id):
    """Agrega una nota médica a la hospitalización"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    hospitalizacion = Hospitalizacion.query.get(id)
    if not hospitalizacion:
        return jsonify({'success': False, 'message': 'Hospitalización no encontrada'}), 404
    
    if 'tipo_nota' not in data or 'contenido' not in data:
        return jsonify({'success': False, 'message': 'Campos requeridos: tipo_nota, contenido'}), 400
    
    nota = NotaMedica(
        hospitalizacion_id=id,
        medico_id=current_user_id,
        tipo_nota=data['tipo_nota'],
        contenido=data['contenido'],
        datos_adicionales=data.get('datos_adicionales'),
        fecha_hora=datetime.utcnow()
    )
    
    db.session.add(nota)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Nota médica agregada',
        'nota': nota.to_dict(incluir_relaciones=True)
    }), 201


# ==================== ÓRDENES MÉDICAS ====================

@bp.route('/<int:id>/ordenes', methods=['POST'])
@jwt_required()
@role_required('medico')
def agregar_orden_medica(id):
    """Agrega una orden médica a la hospitalización"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    hospitalizacion = Hospitalizacion.query.get(id)
    if not hospitalizacion:
        return jsonify({'success': False, 'message': 'Hospitalización no encontrada'}), 404
    
    if 'tipo_orden' not in data or 'descripcion' not in data:
        return jsonify({'success': False, 'message': 'Campos requeridos: tipo_orden, descripcion'}), 400
    
    orden = OrdenMedica(
        hospitalizacion_id=id,
        medico_id=current_user_id,
        tipo_orden=data['tipo_orden'],
        descripcion=data['descripcion'],
        indicaciones=data.get('indicaciones'),
        fecha_hora_orden=datetime.utcnow()
    )
    
    db.session.add(orden)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Orden médica agregada',
        'orden': orden.to_dict(incluir_relaciones=True)
    }), 201


@bp.route('/ordenes/<int:orden_id>/suspender', methods=['PUT'])
@jwt_required()
@role_required('medico')
def suspender_orden(orden_id):
    """Suspende una orden médica"""
    data = request.get_json()
    
    orden = OrdenMedica.query.get(orden_id)
    if not orden:
        return jsonify({'success': False, 'message': 'Orden no encontrada'}), 404
    
    orden.suspender(motivo=data.get('motivo'))
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Orden suspendida',
        'orden': orden.to_dict()
    }), 200


# ==================== REGISTRO ENFERMERÍA ====================

@bp.route('/<int:id>/enfermeria', methods=['POST'])
@jwt_required()
@role_required('enfermera', 'medico')
def agregar_registro_enfermeria(id):
    """Agrega un registro de enfermería"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    hospitalizacion = Hospitalizacion.query.get(id)
    if not hospitalizacion:
        return jsonify({'success': False, 'message': 'Hospitalización no encontrada'}), 404
    
    if 'tipo_registro' not in data or 'descripcion' not in data:
        return jsonify({'success': False, 'message': 'Campos requeridos: tipo_registro, descripcion'}), 400
    
    registro = RegistroEnfermeria(
        hospitalizacion_id=id,
        enfermera_id=current_user_id,
        tipo_registro=data['tipo_registro'],
        descripcion=data['descripcion'],
        datos_json=data.get('datos_json'),
        fecha_hora=datetime.utcnow()
    )
    
    db.session.add(registro)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Registro de enfermería agregado',
        'registro': registro.to_dict(incluir_relaciones=True)
    }), 201
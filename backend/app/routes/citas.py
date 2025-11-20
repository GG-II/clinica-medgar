"""
Rutas de Citas
Endpoints para gestión de agenda y citas médicas
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app.extensions import db
from app.models import Cita, TipoCita, Usuario, Paciente
from app.services.cita_service import CitaService
from app.utils.decorators import role_required

bp = Blueprint('citas', __name__, url_prefix='/api/citas')


@bp.route('', methods=['GET'])
@jwt_required()
def listar_citas():
    """
    Lista citas con filtros opcionales
    Query params:
        - fecha_inicio: YYYY-MM-DD
        - fecha_fin: YYYY-MM-DD
        - medico_id: int
        - paciente_id: int
        - estado: programada|confirmada|completada|cancelada
    """
    try:
        # Parámetros de filtro
        fecha_inicio_str = request.args.get('fecha_inicio')
        fecha_fin_str = request.args.get('fecha_fin')
        medico_id = request.args.get('medico_id', type=int)
        paciente_id = request.args.get('paciente_id', type=int)
        estado = request.args.get('estado')
        
        # Construir query
        query = Cita.query
        
        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
            query = query.filter(Cita.fecha_hora >= fecha_inicio)
        
        if fecha_fin_str:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
            query = query.filter(Cita.fecha_hora <= fecha_fin)
        
        if medico_id:
            query = query.filter(Cita.medico_id == medico_id)
        
        if paciente_id:
            query = query.filter(Cita.paciente_id == paciente_id)
        
        if estado:
            query = query.filter(Cita.estado == estado)
        
        citas = query.order_by(Cita.fecha_hora).all()
        
        return jsonify({
            'success': True,
            'data': [cita.to_dict(include_relaciones=True) for cita in citas],
            'total': len(citas)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar citas: {str(e)}'
        }), 500


@bp.route('/hoy', methods=['GET'])
@jwt_required()
def citas_hoy():
    """Obtiene las citas del día actual"""
    try:
        medico_id = request.args.get('medico_id', type=int)
        
        citas = CitaService.obtener_citas_hoy(medico_id)
        
        return jsonify({
            'success': True,
            'data': [cita.to_dict(include_relaciones=True) for cita in citas],
            'total': len(citas)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener citas de hoy: {str(e)}'
        }), 500


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obtener_cita(id):
    """Obtiene una cita por ID"""
    try:
        cita = Cita.query.get(id)
        if not cita:
            return jsonify({
                'success': False,
                'message': 'Cita no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': cita.to_dict(include_relaciones=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener cita: {str(e)}'
        }), 500


@bp.route('', methods=['POST'])
@jwt_required()
def crear_cita():
    """
    Crea una nueva cita
    Body: {
        "paciente_id": int,
        "medico_id": int,
        "tipo_cita_id": int,
        "fecha_hora": "YYYY-MM-DD HH:MM",
        "duracion_minutos": int (opcional, default 20),
        "motivo": str (opcional),
        "notas": str (opcional),
        "es_emergencia": bool (opcional, default false)
    }
    """
    try:
        data = request.get_json()
        usuario_id = get_jwt_identity()
        
        # Validar campos requeridos
        campos_requeridos = ['paciente_id', 'medico_id', 'tipo_cita_id', 'fecha_hora']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Convertir fecha_hora string a datetime
        data['fecha_hora'] = datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M')
        
        # Crear cita usando el servicio
        cita, error = CitaService.crear_cita(data, usuario_id)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Cita creada exitosamente',
            'data': cita.to_dict(include_relaciones=True)
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': 'Formato de fecha inválido. Use: YYYY-MM-DD HH:MM'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear cita: {str(e)}'
        }), 500


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_cita(id):
    """
    Actualiza una cita existente
    Body: Campos opcionales a actualizar
    """
    try:
        data = request.get_json()
        usuario_id = get_jwt_identity()
        
        # Convertir fecha_hora si viene en el request
        if 'fecha_hora' in data and isinstance(data['fecha_hora'], str):
            data['fecha_hora'] = datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M')
        
        # Actualizar usando el servicio
        cita, error = CitaService.actualizar_cita(id, data, usuario_id)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Cita actualizada exitosamente',
            'data': cita.to_dict(include_relaciones=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar cita: {str(e)}'
        }), 500


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def cancelar_cita(id):
    """
    Cancela una cita
    Body: {
        "motivo": str (opcional)
    }
    """
    try:
        data = request.get_json() or {}
        usuario_id = get_jwt_identity()
        motivo = data.get('motivo')
        
        exitoso, mensaje = CitaService.cancelar_cita(id, usuario_id, motivo)
        
        if not exitoso:
            return jsonify({
                'success': False,
                'message': mensaje
            }), 400
        
        return jsonify({
            'success': True,
            'message': mensaje
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al cancelar cita: {str(e)}'
        }), 500


@bp.route('/disponibilidad', methods=['GET'])
@jwt_required()
def verificar_disponibilidad():
    """
    Verifica disponibilidad de un médico
    Query params:
        - medico_id: int (requerido)
        - fecha: YYYY-MM-DD (requerido)
        - hora: HH:MM (opcional, si no se envía retorna todos los horarios del día)
        - duracion_minutos: int (opcional, default 20)
    """
    try:
        medico_id = request.args.get('medico_id', type=int)
        fecha_str = request.args.get('fecha')
        hora_str = request.args.get('hora')
        duracion = request.args.get('duracion_minutos', type=int, default=20)
        
        if not medico_id or not fecha_str:
            return jsonify({
                'success': False,
                'message': 'medico_id y fecha son requeridos'
            }), 400
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Si se especifica hora, verificar solo ese horario
        if hora_str:
            hora = datetime.strptime(hora_str, '%H:%M').time()
            fecha_hora = datetime.combine(fecha, hora)
            
            disponible, mensaje = CitaService.verificar_disponibilidad(
                medico_id, fecha_hora, duracion
            )
            
            return jsonify({
                'success': True,
                'disponible': disponible,
                'mensaje': mensaje
            }), 200
        
        # Si no se especifica hora, retornar todos los horarios disponibles del día
        horarios = CitaService.obtener_horarios_disponibles(medico_id, fecha, duracion)
        
        return jsonify({
            'success': True,
            'horarios_disponibles': horarios,
            'total': len(horarios)
        }), 200
        
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Formato de fecha u hora inválido'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al verificar disponibilidad: {str(e)}'
        }), 500


@bp.route('/tipos', methods=['GET'])
@jwt_required()
def listar_tipos_cita():
    """Lista todos los tipos de cita disponibles"""
    try:
        tipos = TipoCita.query.filter_by(activo=True).all()
        
        return jsonify({
            'success': True,
            'data': [tipo.to_dict() for tipo in tipos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar tipos de cita: {str(e)}'
        }), 500


@bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required('medico', 'administrador')
def estadisticas_citas():
    """
    Estadísticas de citas
    Query params:
        - fecha_inicio: YYYY-MM-DD (opcional, default: hace 30 días)
        - fecha_fin: YYYY-MM-DD (opcional, default: hoy)
        - medico_id: int (opcional)
    """
    try:
        # Parámetros
        fecha_inicio_str = request.args.get('fecha_inicio')
        fecha_fin_str = request.args.get('fecha_fin')
        medico_id = request.args.get('medico_id', type=int)
        
        # Fechas por defecto
        if not fecha_fin_str:
            fecha_fin = datetime.now()
        else:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
        
        if not fecha_inicio_str:
            fecha_inicio = fecha_fin - timedelta(days=30)
        else:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        
        # Query base
        query = Cita.query.filter(
            Cita.fecha_hora.between(fecha_inicio, fecha_fin)
        )
        
        if medico_id:
            query = query.filter(Cita.medico_id == medico_id)
        
        citas = query.all()
        
        # Calcular estadísticas
        total = len(citas)
        por_estado = {}
        por_tipo = {}
        tasa_ausentismo = 0
        
        for cita in citas:
            # Por estado
            estado = cita.estado
            por_estado[estado] = por_estado.get(estado, 0) + 1
            
            # Por tipo
            if cita.tipo_cita:
                tipo = cita.tipo_cita.nombre
                por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        
        # Calcular tasa de ausentismo
        no_asistio = por_estado.get('no_asistio', 0)
        if total > 0:
            tasa_ausentismo = round((no_asistio / total) * 100, 2)
        
        return jsonify({
            'success': True,
            'data': {
                'periodo': {
                    'inicio': fecha_inicio.strftime('%Y-%m-%d'),
                    'fin': fecha_fin.strftime('%Y-%m-%d')
                },
                'total_citas': total,
                'por_estado': por_estado,
                'por_tipo': por_tipo,
                'tasa_ausentismo': tasa_ausentismo
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }), 500
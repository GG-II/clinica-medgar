"""
Rutas de Pacientes
Endpoints para gestión de pacientes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.paciente_service import PacienteService
from app.utils.decorators import role_required

# Crear blueprint
pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/api/pacientes')


@pacientes_bp.route('/', methods=['GET'])
@jwt_required()
def listar_pacientes():
    """
    Lista todos los pacientes con paginación y búsqueda
    
    Query params:
        - page: Número de página (default: 1)
        - per_page: Cantidad por página (default: 20)
        - busqueda: Término de búsqueda
        - ordenar_por: Campo de ordenamiento (default: nombre_completo)
    
    Returns:
        200: Lista de pacientes
        500: Error del servidor
    
    Ejemplo:
        GET /api/pacientes?page=1&per_page=20&busqueda=juan
    """
    try:
        # Obtener parámetros de query
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        busqueda = request.args.get('busqueda', None, type=str)
        ordenar_por = request.args.get('ordenar_por', 'nombre_completo', type=str)
        
        # Validar parámetros
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # Obtener pacientes
        resultado = PacienteService.listar_pacientes(
            page=page,
            per_page=per_page,
            busqueda=busqueda,
            ordenar_por=ordenar_por
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar pacientes: {str(e)}'
        }), 500


@pacientes_bp.route('/buscar', methods=['GET'])
@jwt_required()
def buscar_pacientes():
    """
    Búsqueda rápida de pacientes (para autocompletar)
    
    Query params:
        - termino: Término de búsqueda (mínimo 2 caracteres)
    
    Returns:
        200: Lista de pacientes (máximo 10)
        400: Término de búsqueda muy corto
        500: Error del servidor
    
    Ejemplo:
        GET /api/pacientes/buscar?termino=juan
    """
    try:
        termino = request.args.get('termino', '', type=str)
        
        if len(termino) < 2:
            return jsonify({
                'success': False,
                'message': 'El término de búsqueda debe tener al menos 2 caracteres'
            }), 400
        
        pacientes = PacienteService.buscar_pacientes(termino)
        
        return jsonify({
            'success': True,
            'data': pacientes
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al buscar pacientes: {str(e)}'
        }), 500


@pacientes_bp.route('/<int:paciente_id>', methods=['GET'])
@jwt_required()
def obtener_paciente(paciente_id):
    """
    Obtiene un paciente específico por su ID
    
    Args:
        paciente_id: ID del paciente
    
    Returns:
        200: Datos del paciente
        404: Paciente no encontrado
        500: Error del servidor
    
    Ejemplo:
        GET /api/pacientes/1
    """
    try:
        paciente = PacienteService.obtener_paciente(paciente_id)
        
        if not paciente:
            return jsonify({
                'success': False,
                'message': 'Paciente no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': paciente.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener paciente: {str(e)}'
        }), 500


@pacientes_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('medico', 'enfermera', 'recepcionista', 'administrador')
def crear_paciente():
    """
    Crea un nuevo paciente
    
    Body (JSON):
        - nombre_completo: string (requerido)
        - fecha_nacimiento: string YYYY-MM-DD (requerido)
        - sexo: string 'M' o 'F' (requerido)
        - dpi: string (opcional)
        - direccion: string (opcional)
        - municipio: string (opcional)
        - departamento: string (opcional)
        - telefono: string (opcional)
        - telefono_alternativo: string (opcional)
        - email: string (opcional)
        - religion: string (opcional)
        - estado_civil: string (opcional)
        - tiene_igss: boolean (opcional)
        - numero_igss: string (opcional)
        - contacto_emergencia_nombre: string (opcional)
        - contacto_emergencia_telefono: string (opcional)
        - contacto_emergencia_relacion: string (opcional)
        - observaciones: string (opcional)
    
    Returns:
        201: Paciente creado exitosamente
        400: Datos inválidos
        500: Error del servidor
    
    Ejemplo:
        POST /api/pacientes
        {
            "nombre_completo": "Juan Pérez López",
            "fecha_nacimiento": "1990-05-15",
            "sexo": "M",
            "dpi": "1234567890101",
            "telefono": "12345678"
        }
    """
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se recibieron datos'
            }), 400
        
        # Obtener ID del usuario actual
        usuario_id = get_jwt_identity()
        
        # Crear paciente
        paciente, error = PacienteService.crear_paciente(data, usuario_id)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Paciente creado exitosamente',
            'data': paciente.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear paciente: {str(e)}'
        }), 500


@pacientes_bp.route('/<int:paciente_id>', methods=['PUT'])
@jwt_required()
@role_required('medico', 'enfermera', 'recepcionista', 'administrador')
def actualizar_paciente(paciente_id):
    """
    Actualiza los datos de un paciente
    
    Args:
        paciente_id: ID del paciente a actualizar
    
    Body (JSON):
        Cualquier campo del paciente (todos opcionales)
    
    Returns:
        200: Paciente actualizado
        400: Datos inválidos
        404: Paciente no encontrado
        500: Error del servidor
    
    Ejemplo:
        PUT /api/pacientes/1
        {
            "telefono": "87654321",
            "email": "nuevo@email.com"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se recibieron datos'
            }), 400
        
        usuario_id = get_jwt_identity()
        
        paciente, error = PacienteService.actualizar_paciente(paciente_id, data, usuario_id)
        
        if error:
            if 'no encontrado' in error.lower():
                return jsonify({
                    'success': False,
                    'message': error
                }), 404
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Paciente actualizado exitosamente',
            'data': paciente.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar paciente: {str(e)}'
        }), 500


@pacientes_bp.route('/<int:paciente_id>', methods=['DELETE'])
@jwt_required()
@role_required('medico', 'administrador')
def eliminar_paciente(paciente_id):
    """
    Elimina (desactiva) un paciente
    
    NOTA: No elimina físicamente, solo marca como inactivo
    
    Args:
        paciente_id: ID del paciente a eliminar
    
    Returns:
        200: Paciente eliminado
        404: Paciente no encontrado
        500: Error del servidor
    
    Ejemplo:
        DELETE /api/pacientes/1
    """
    try:
        usuario_id = get_jwt_identity()
        
        success, error = PacienteService.eliminar_paciente(paciente_id, usuario_id)
        
        if error:
            if 'no encontrado' in error.lower():
                return jsonify({
                    'success': False,
                    'message': error
                }), 404
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Paciente eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar paciente: {str(e)}'
        }), 500


@pacientes_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
def obtener_estadisticas():
    """
    Obtiene estadísticas generales de pacientes
    
    Returns:
        200: Estadísticas
        500: Error del servidor
    
    Ejemplo:
        GET /api/pacientes/estadisticas
    
    Respuesta:
        {
            "success": true,
            "data": {
                "total": 150,
                "hombres": 75,
                "mujeres": 75,
                "con_igss": 50,
                "sin_igss": 100
            }
        }
    """
    try:
        estadisticas = PacienteService.obtener_estadisticas()
        
        return jsonify({
            'success': True,
            'data': estadisticas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }), 500
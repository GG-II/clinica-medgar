from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services.auth_service import AuthService
from app.models import LogAuditoria

# Crear Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de login
    
    POST /api/auth/login
    Body: {
        "username": "admin",
        "password": "Admin123"
    }
    
    Returns:
        JSON con access_token, refresh_token y datos del usuario
    """
    data = request.get_json()
    
    # Validar que vengan los datos
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': 'Username y password son requeridos'
        }), 400
    
    # Llamar al servicio de autenticación
    success, response_data, status_code = AuthService.login(
        username_or_email=data['username'],
        password=data['password']
    )
    
    return jsonify({
        'success': success,
        **response_data
    }), status_code


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint de registro de usuario
    
    POST /api/auth/register
    Body: {
        "username": "doctor1",
        "email": "doctor1@clinica.com",
        "password": "Doctor123",
        "rol": "medico",
        "nombre_completo": "Dr. Juan Pérez",
        "telefono": "12345678"
    }
    
    Returns:
        JSON con datos del usuario creado
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'No se enviaron datos'
        }), 400
    
    # Llamar al servicio de registro
    success, response_data, status_code = AuthService.registrar_usuario(data)
    
    return jsonify({
        'success': success,
        **response_data
    }), status_code


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obtiene los datos del usuario actual (autenticado)
    
    GET /api/auth/me
    Headers: {
        "Authorization": "Bearer <access_token>"
    }
    
    Returns:
        JSON con datos del usuario
    """
    usuario_id = get_jwt_identity()
    
    success, response_data, status_code = AuthService.obtener_usuario_actual(usuario_id)
    
    return jsonify({
        'success': success,
        **response_data
    }), status_code


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresca el access token usando el refresh token
    
    POST /api/auth/refresh
    Headers: {
        "Authorization": "Bearer <refresh_token>"
    }
    
    Returns:
        JSON con nuevo access_token
    """
    usuario_id = get_jwt_identity()
    
    # Crear nuevo access token
    new_access_token = create_access_token(identity=usuario_id)
    
    # Registrar en auditoría
    LogAuditoria.registrar(
        usuario_id=usuario_id,
        accion='refresh_token',
        ip_address=request.remote_addr
    )
    
    return jsonify({
        'success': True,
        'access_token': new_access_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout del usuario (solo registra en auditoría)
    
    POST /api/auth/logout
    Headers: {
        "Authorization": "Bearer <access_token>"
    }
    
    Returns:
        JSON con mensaje de confirmación
    """
    usuario_id = get_jwt_identity()
    
    # Registrar en auditoría
    LogAuditoria.registrar(
        usuario_id=usuario_id,
        accion='logout',
        ip_address=request.remote_addr
    )
    
    return jsonify({
        'success': True,
        'message': 'Logout exitoso'
    }), 200
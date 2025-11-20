from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import Usuario


def role_required(*roles_permitidos):
    """
    Decorador para requerir roles específicos
    
    Uso:
        @role_required('medico', 'administrador')
        def mi_funcion():
            pass
    
    Args:
        roles_permitidos: Lista de roles que pueden acceder
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verificar que hay un JWT válido
            verify_jwt_in_request()
            
            # Obtener el ID del usuario del token
            usuario_id = get_jwt_identity()
            
            # Buscar el usuario en la base de datos
            usuario = Usuario.query.get(usuario_id)
            
            if not usuario:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }), 404
            
            if not usuario.activo:
                return jsonify({
                    'success': False,
                    'message': 'Usuario inactivo'
                }), 403
            
            # Verificar si el rol del usuario está en los roles permitidos
            if usuario.rol not in roles_permitidos:
                return jsonify({
                    'success': False,
                    'message': f'Acceso denegado. Se requiere uno de estos roles: {", ".join(roles_permitidos)}'
                }), 403
            
            # Si todo está bien, ejecutar la función
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(fn):
    """
    Decorador para requerir rol de administrador
    
    Uso:
        @admin_required
        def mi_funcion():
            pass
    """
    return role_required('administrador')(fn)


def medico_required(fn):
    """
    Decorador para requerir rol de médico
    
    Uso:
        @medico_required
        def mi_funcion():
            pass
    """
    return role_required('medico')(fn)


def personal_medico_required(fn):
    """
    Decorador para requerir personal médico (médico o enfermera)
    
    Uso:
        @personal_medico_required
        def mi_funcion():
            pass
    """
    return role_required('medico', 'enfermera')(fn)
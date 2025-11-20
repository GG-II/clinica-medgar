from flask import request
from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db
from app.models import Usuario, LogAuditoria
from app.utils.validators import validar_email, validar_username, validar_password, validar_telefono_guatemala, validar_rol


class AuthService:
    """Servicio de autenticación"""
    
    @staticmethod
    def login(username_or_email, password):
        """
        Autentica un usuario
        
        Args:
            username_or_email (str): Username o email
            password (str): Contraseña
            
        Returns:
            tuple: (success, data, status_code)
        """
        # Buscar usuario por username o email
        usuario = Usuario.query.filter(
            (Usuario.username == username_or_email) | (Usuario.email == username_or_email)
        ).first()
        
        if not usuario:
            return False, {'message': 'Credenciales inválidas'}, 401
        
        if not usuario.activo:
            return False, {'message': 'Usuario inactivo. Contacte al administrador'}, 403
        
        # Verificar contraseña
        if not usuario.check_password(password):
            return False, {'message': 'Credenciales inválidas'}, 401
        
        # Actualizar último acceso
        usuario.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        # Crear tokens JWT
        access_token = create_access_token(identity=usuario.id)
        refresh_token = create_refresh_token(identity=usuario.id)
        
        # Registrar en auditoría
        ip_address = request.remote_addr if request else None
        LogAuditoria.registrar(
            usuario_id=usuario.id,
            accion='login',
            ip_address=ip_address
        )
        
        return True, {
            'message': 'Login exitoso',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'usuario': usuario.to_dict()
        }, 200
    
    @staticmethod
    def registrar_usuario(data):
        """
        Registra un nuevo usuario
        
        Args:
            data (dict): Datos del usuario
            
        Returns:
            tuple: (success, data, status_code)
        """
        # Validar datos requeridos
        campos_requeridos = ['username', 'email', 'password', 'rol', 'nombre_completo']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                return False, {'message': f'El campo {campo} es requerido'}, 400
        
        # Validar username
        valido, error = validar_username(data['username'])
        if not valido:
            return False, {'message': error}, 400
        
        # Validar email
        valido, error = validar_email(data['email'])
        if not valido:
            return False, {'message': error}, 400
        
        # Validar password
        valido, error = validar_password(data['password'])
        if not valido:
            return False, {'message': error}, 400
        
        # Validar rol
        valido, error = validar_rol(data['rol'])
        if not valido:
            return False, {'message': error}, 400
        
        # Validar teléfono (opcional)
        if data.get('telefono'):
            valido, error = validar_telefono_guatemala(data['telefono'])
            if not valido:
                return False, {'message': error}, 400
        
        # Verificar que username no exista
        if Usuario.query.filter_by(username=data['username']).first():
            return False, {'message': 'El username ya está en uso'}, 400
        
        # Verificar que email no exista
        if Usuario.query.filter_by(email=data['email']).first():
            return False, {'message': 'El email ya está en uso'}, 400
        
        # Crear usuario
        nuevo_usuario = Usuario(
            username=data['username'],
            email=data['email'],
            rol=data['rol'],
            nombre_completo=data['nombre_completo'],
            telefono=data.get('telefono'),
            activo=True
        )
        nuevo_usuario.set_password(data['password'])
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Registrar en auditoría
        ip_address = request.remote_addr if request else None
        LogAuditoria.registrar(
            usuario_id=nuevo_usuario.id,
            accion='registro_usuario',
            ip_address=ip_address,
            detalles=f'Usuario {nuevo_usuario.username} registrado con rol {nuevo_usuario.rol}'
        )
        
        return True, {
            'message': 'Usuario registrado exitosamente',
            'usuario': nuevo_usuario.to_dict()
        }, 201
    
    @staticmethod
    def obtener_usuario_actual(usuario_id):
        """
        Obtiene los datos del usuario actual
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            tuple: (success, data, status_code)
        """
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return False, {'message': 'Usuario no encontrado'}, 404
        
        return True, {
            'usuario': usuario.to_dict()
        }, 200
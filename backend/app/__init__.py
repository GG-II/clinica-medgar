from flask import Flask, jsonify
from app.config import config
from app.extensions import init_extensions, db
from app.routes import auth_bp


def create_app(config_name='development'):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_name (str): Nombre de la configuración ('development', 'production', 'testing')
        
    Returns:
        Flask: Instancia de la aplicación
    """
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Registrar blueprints (NUEVO - usar la función centralizada)
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Recurso no encontrado'
        }), 404
    
    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
    
    # Manejador de errores JWT
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': 'No autorizado. Token inválido o expirado'
        }), 401
    
    # Manejador de errores de permisos
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'message': 'Acceso prohibido. No tiene permisos suficientes'
        }), 403
    
    # Ruta de prueba
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'API Clínica MEDGAR - Sistema de Gestión Clínica',
            'version': '1.0.0',
            'status': 'running'
        })
    
    # Ruta de health check
    @app.route('/api/health')
    def health():
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected' if db.engine else 'disconnected'
        })
    
    return app
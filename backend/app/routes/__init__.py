"""
Módulo de rutas de la aplicación
Registra todos los blueprints (grupos de rutas)
"""
from app.routes.auth import auth_bp
from app.routes.pacientes import pacientes_bp
from app.routes.historia_clinica import historia_bp
from app.routes.uploads import uploads_bp

def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación Flask
    
    Args:
        app: Instancia de Flask
    """
    # Rutas de autenticación
    app.register_blueprint(auth_bp)
    
    # Rutas de pacientes
    app.register_blueprint(pacientes_bp)
    
    # Rutas de historia clínica
    app.register_blueprint(historia_bp)
    
    # Rutas de uploads
    app.register_blueprint(uploads_bp)
    
    print("✅ Blueprints registrados:")
    print("   - /api/auth (Autenticación)")
    print("   - /api/pacientes (Pacientes)")
    print("   - /api/historia-clinica (Historia Clínica)")
    print("   - /api/uploads (Archivos)")
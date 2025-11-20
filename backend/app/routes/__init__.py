"""
Módulo de rutas de la aplicación
Registra todos los blueprints (grupos de rutas)
"""
from app.routes.auth import auth_bp
from app.routes.pacientes import pacientes_bp  # ← NUEVO

def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación Flask
    
    Args:
        app: Instancia de Flask
    """
    # Rutas de autenticación
    app.register_blueprint(auth_bp)
    
    # Rutas de pacientes (NUEVO)
    app.register_blueprint(pacientes_bp)
    
    print("✅ Blueprints registrados:")
    print("   - /api/auth (Autenticación)")
    print("   - /api/pacientes (Pacientes)")  # ← NUEVO
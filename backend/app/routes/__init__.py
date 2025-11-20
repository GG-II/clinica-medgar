"""
Registro de todos los blueprints (rutas)
"""
from flask import Flask

def register_blueprints(app: Flask):
    """Registra todos los blueprints en la aplicación"""
    
    # Fase 1: Autenticación
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Fase 2: Pacientes e Historia Clínica
    from app.routes.pacientes import pacientes_bp
    app.register_blueprint(pacientes_bp)
    
    from app.routes.historia_clinica import historia_bp
    app.register_blueprint(historia_bp)
    
    from app.routes.uploads import uploads_bp
    app.register_blueprint(uploads_bp)
    
    # Fase 3: Citas, Recetas y Laboratorios
    from app.routes.citas import bp as citas_bp
    app.register_blueprint(citas_bp)
    
    from app.routes.recetas import bp as recetas_bp
    app.register_blueprint(recetas_bp)
    
    from app.routes.laboratorios import bp as laboratorios_bp
    app.register_blueprint(laboratorios_bp)
    
    print("✅ Blueprints registrados:")
    print("   - /api/auth (autenticación)")
    print("   - /api/pacientes (pacientes)")
    print("   - /api/historia-clinica (historia clínica)")
    print("   - /api/uploads (archivos)")
    print("   - /api/citas (citas y agenda)")
    print("   - /api/recetas (recetas médicas)")
    print("   - /api/laboratorios (laboratorios)")
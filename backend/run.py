import os
from app import create_app
from app.extensions import db
from app.models import Usuario, LogAuditoria

# Obtener el nombre de la configuración del entorno
config_name = os.getenv('FLASK_ENV', 'development')

# Crear la aplicación
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    """
    Hace disponibles estos objetos en flask shell
    Útil para testing en consola
    """
    return {
        'db': db,
        'Usuario': Usuario,
        'LogAuditoria': LogAuditoria
    }


@app.cli.command()
def init_db():
    """
    Comando CLI para inicializar la base de datos
    Uso: flask init-db
    """
    db.create_all()
    print("✅ Base de datos inicializada correctamente")


@app.cli.command()
def crear_admin():
    """
    Comando CLI para crear un usuario administrador
    Uso: flask crear-admin
    """
    # Verificar si ya existe un admin
    admin_existente = Usuario.query.filter_by(username='admin').first()
    if admin_existente:
        print("⚠️  Ya existe un usuario 'admin'")
        return
    
    # Crear usuario admin
    admin = Usuario(
        username='admin',
        email='admin@clinica.com',
        rol='administrador',
        nombre_completo='Administrador del Sistema',
        telefono='12345678',
        activo=True
    )
    admin.set_password('Admin123')
    
    db.session.add(admin)
    db.session.commit()
    
    print("✅ Usuario administrador creado:")
    print("   Username: admin")
    print("   Password: Admin123")
    print("   Email: admin@clinica.com")


@app.cli.command()
def crear_medico():
    """
    Comando CLI para crear un usuario médico de prueba
    Uso: flask crear-medico
    """
    # Verificar si ya existe
    medico_existente = Usuario.query.filter_by(username='doctor1').first()
    if medico_existente:
        print("⚠️  Ya existe un usuario 'doctor1'")
        return
    
    # Crear usuario médico
    medico = Usuario(
        username='doctor1',
        email='doctor1@clinica.com',
        rol='medico',
        nombre_completo='Dra. Estephanny García',
        telefono='87654321',
        activo=True
    )
    medico.set_password('Doctor123')
    
    db.session.add(medico)
    db.session.commit()
    
    print("✅ Usuario médico creado:")
    print("   Username: doctor1")
    print("   Password: Doctor123")
    print("   Email: doctor1@clinica.com")


if __name__ == '__main__':
    # Ejecutar servidor de desarrollo
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
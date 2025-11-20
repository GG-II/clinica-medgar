from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Inicializar extensiones (sin app todavía)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def init_extensions(app):
    """
    Inicializa todas las extensiones con la app Flask
    
    Args:
        app: Instancia de Flask
    """
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
from app.extensions import db
from datetime import datetime
import bcrypt


class Usuario(db.Model):
    """
    Modelo de Usuario
    Representa a los usuarios del sistema (médicos, enfermeras, recepcionistas, administradores)
    """
    __tablename__ = 'usuarios'
    
    # Campos
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('medico', 'enfermera', 'recepcionista', 'administrador'), nullable=False, index=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con logs de auditoría
    logs = db.relationship('LogAuditoria', back_populates='usuario', lazy='dynamic')
    
    def __repr__(self):
        return f'<Usuario {self.username} - {self.rol}>'
    
    def set_password(self, password):
        """
        Encripta y guarda la contraseña
        
        Args:
            password (str): Contraseña en texto plano
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        """
        Verifica si la contraseña es correcta
        
        Args:
            password (str): Contraseña en texto plano
            
        Returns:
            bool: True si la contraseña es correcta
        """
        password_bytes = password.encode('utf-8')
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)
    
    def to_dict(self):
        """
        Convierte el usuario a diccionario (para JSON)
        
        Returns:
            dict: Datos del usuario (sin password)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'rol': self.rol,
            'nombre_completo': self.nombre_completo,
            'telefono': self.telefono,
            'activo': self.activo,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
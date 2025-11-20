"""
Modelo de Paciente
Representa a un paciente en el sistema de la clínica.
"""
from datetime import datetime, date
from app.extensions import db


class Paciente(db.Model):
    """
    Modelo de Paciente
    
    Almacena toda la información demográfica y de contacto de los pacientes.
    Incluye datos personales, ubicación, contactos de emergencia y foto.
    """
    __tablename__ = 'pacientes'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === DATOS PERSONALES BÁSICOS ===
    nombre_completo = db.Column(db.String(150), nullable=False, index=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False, index=True)
    sexo = db.Column(db.Enum('M', 'F', name='sexo_enum'), nullable=False)
    dpi = db.Column(db.String(20), unique=True, nullable=True, index=True)
    
    # === UBICACIÓN ===
    direccion = db.Column(db.Text, nullable=True)
    municipio = db.Column(db.String(100), nullable=True)
    departamento = db.Column(db.String(100), nullable=True)
    
    # === CONTACTO ===
    telefono = db.Column(db.String(20), nullable=True, index=True)
    telefono_alternativo = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    
    # === DATOS MÉDICOS BÁSICOS ===
    religion = db.Column(db.String(50), nullable=True)
    estado_civil = db.Column(
        db.Enum('soltero', 'casado', 'divorciado', 'viudo', 'union_libre', name='estado_civil_enum'),
        nullable=True
    )
    
    # === SEGURO MÉDICO ===
    tiene_igss = db.Column(db.Boolean, default=False)
    numero_igss = db.Column(db.String(50), nullable=True)
    
    # === CONTACTO DE EMERGENCIA ===
    contacto_emergencia_nombre = db.Column(db.String(150), nullable=True)
    contacto_emergencia_telefono = db.Column(db.String(20), nullable=True)
    contacto_emergencia_relacion = db.Column(db.String(50), nullable=True)
    
    # === FOTO ===
    foto_url = db.Column(db.String(255), nullable=True)
    
    # === OBSERVACIONES ===
    observaciones = db.Column(db.Text, nullable=True)
    
    # === ESTADO ===
    activo = db.Column(db.Boolean, default=True)
    
    # === TIMESTAMPS ===
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<Paciente {self.id}: {self.nombre_completo}>'
    
    def to_dict(self):
        """
        Convierte el objeto Paciente a un diccionario JSON-serializable
        Útil para enviar datos al frontend
        """
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'edad': self.calcular_edad(),
            'sexo': self.sexo,
            'dpi': self.dpi,
            'direccion': self.direccion,
            'municipio': self.municipio,
            'departamento': self.departamento,
            'telefono': self.telefono,
            'telefono_alternativo': self.telefono_alternativo,
            'email': self.email,
            'religion': self.religion,
            'estado_civil': self.estado_civil,
            'tiene_igss': self.tiene_igss,
            'numero_igss': self.numero_igss,
            'contacto_emergencia_nombre': self.contacto_emergencia_nombre,
            'contacto_emergencia_telefono': self.contacto_emergencia_telefono,
            'contacto_emergencia_relacion': self.contacto_emergencia_relacion,
            'foto_url': self.foto_url,
            'observaciones': self.observaciones,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def calcular_edad(self):
        """
        Calcula la edad del paciente en años
        Retorna None si no hay fecha de nacimiento
        """
        if not self.fecha_nacimiento:
            return None
        
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        
        # Ajustar si aún no ha cumplido años este año
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        
        return edad
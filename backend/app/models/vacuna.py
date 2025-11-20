"""
Modelos de Vacunas
Catálogo de vacunas y aplicaciones de vacunas a pacientes
"""
from datetime import datetime
from app.extensions import db


class Vacuna(db.Model):
    """
    Modelo de Vacuna (Catálogo)
    
    Catálogo de vacunas disponibles en Guatemala.
    """
    __tablename__ = 'vacunas'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === INFORMACIÓN DE LA VACUNA ===
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    dosis_total = db.Column(db.Integer, default=1)
    edad_recomendada_meses = db.Column(db.Integer, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    
    # === ESTADO ===
    activo = db.Column(db.Boolean, default=True)
    
    # === TIMESTAMPS ===
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # === RELACIONES ===
    aplicaciones = db.relationship('AplicacionVacuna', backref='vacuna', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<Vacuna {self.nombre}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'dosis_total': self.dosis_total,
            'edad_recomendada_meses': self.edad_recomendada_meses,
            'observaciones': self.observaciones,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AplicacionVacuna(db.Model):
    """
    Modelo de Aplicación de Vacuna
    
    Registro de vacunas aplicadas a pacientes.
    """
    __tablename__ = 'aplicaciones_vacunas'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === RELACIONES ===
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False, index=True)
    vacuna_id = db.Column(db.Integer, db.ForeignKey('vacunas.id'), nullable=False)
    
    # === INFORMACIÓN DE LA APLICACIÓN ===
    numero_dosis = db.Column(db.Integer, nullable=False)
    fecha_aplicacion = db.Column(db.Date, nullable=False, index=True)
    lote = db.Column(db.String(50), nullable=True)
    aplicada_por = db.Column(db.String(100), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    
    # === TIMESTAMPS ===
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # === RELACIONES ===
    paciente = db.relationship('Paciente', backref=db.backref('vacunas_aplicadas', lazy='dynamic', cascade='all, delete-orphan'))
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<AplicacionVacuna Paciente ID: {self.paciente_id} - Vacuna ID: {self.vacuna_id}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'vacuna_id': self.vacuna_id,
            'vacuna_nombre': self.vacuna.nombre if self.vacuna else None,
            'numero_dosis': self.numero_dosis,
            'fecha_aplicacion': self.fecha_aplicacion.isoformat() if self.fecha_aplicacion else None,
            'lote': self.lote,
            'aplicada_por': self.aplicada_por,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
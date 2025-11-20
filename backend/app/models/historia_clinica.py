"""
Modelo de Historia Clínica
Representa la historia clínica de un paciente
"""
from datetime import datetime
from app.extensions import db


class HistoriaClinica(db.Model):
    """
    Modelo de Historia Clínica
    
    Relación uno a uno con Paciente.
    Almacena información médica general del paciente.
    """
    __tablename__ = 'historias_clinicas'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === RELACIÓN CON PACIENTE (UNO A UNO) ===
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    # === DATOS MÉDICOS GENERALES ===
    tipo_sangre = db.Column(
        db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', name='tipo_sangre_enum'),
        nullable=True
    )
    
    # === TIMESTAMPS ===
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELACIONES ===
    paciente = db.relationship('Paciente', backref=db.backref('historia_clinica', uselist=False, cascade='all, delete-orphan'))
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<HistoriaClinica Paciente ID: {self.paciente_id}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'tipo_sangre': self.tipo_sangre,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
"""
Modelo de Antecedentes
Representa los antecedentes médicos, quirúrgicos, traumáticos, alérgicos, etc.
"""
from datetime import datetime
from app.extensions import db


class Antecedente(db.Model):
    """
    Modelo de Antecedente
    
    Almacena diferentes tipos de antecedentes del paciente.
    """
    __tablename__ = 'antecedentes'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === RELACIÓN CON PACIENTE ===
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # === TIPO DE ANTECEDENTE ===
    tipo = db.Column(
        db.Enum('medicos', 'quirurgicos', 'traumaticos', 'alergicos', 'ginecologicos', 'obstetricos', name='tipo_antecedente_enum'),
        nullable=False,
        index=True
    )
    
    # === DESCRIPCIÓN ===
    descripcion = db.Column(db.Text, nullable=False)
    
    # === FECHA DEL EVENTO (OPCIONAL) ===
    fecha_evento = db.Column(db.Date, nullable=True)
    
    # === RELEVANCIA ===
    relevancia = db.Column(
        db.Enum('alta', 'media', 'baja', name='relevancia_enum'),
        default='media'
    )
    
    # === ESTADO ===
    activo = db.Column(db.Boolean, default=True)
    
    # === TIMESTAMPS ===
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELACIONES ===
    paciente = db.relationship('Paciente', backref=db.backref('antecedentes', lazy='dynamic', cascade='all, delete-orphan'))
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<Antecedente {self.tipo} - Paciente ID: {self.paciente_id}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'fecha_evento': self.fecha_evento.isoformat() if self.fecha_evento else None,
            'relevancia': self.relevancia,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
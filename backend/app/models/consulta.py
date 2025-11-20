"""
Modelo de Consulta
Representa una consulta médica realizada a un paciente
"""
from datetime import datetime
from app.extensions import db


class Consulta(db.Model):
    """
    Modelo de Consulta
    
    Registra cada consulta médica realizada.
    """
    __tablename__ = 'consultas'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === RELACIONES ===
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False, index=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    
    # === FECHA Y HORA ===
    fecha_consulta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # === INFORMACIÓN DE LA CONSULTA ===
    motivo_consulta = db.Column(db.Text, nullable=False)
    historia_enfermedad_actual = db.Column(db.Text, nullable=True)
    examen_fisico = db.Column(db.Text, nullable=True)
    diagnostico = db.Column(db.Text, nullable=True)
    plan_tratamiento = db.Column(db.Text, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    
    # === ESPECIALIDAD ===
    especialidad = db.Column(
        db.Enum('medicina_general', 'pediatria', 'ginecologia', 'medicina_interna', 'cirugia', 'traumatologia', name='especialidad_enum'),
        nullable=True
    )
    
    # === TIMESTAMPS ===
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # === RELACIONES ===
    paciente = db.relationship('Paciente', backref=db.backref('consultas', lazy='dynamic', cascade='all, delete-orphan'))
    medico = db.relationship('Usuario', backref='consultas_realizadas')
    signos_vitales = db.relationship('SignosVitales', backref='consulta', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<Consulta {self.id} - Paciente: {self.paciente_id}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'fecha_consulta': self.fecha_consulta.isoformat() if self.fecha_consulta else None,
            'motivo_consulta': self.motivo_consulta,
            'historia_enfermedad_actual': self.historia_enfermedad_actual,
            'examen_fisico': self.examen_fisico,
            'diagnostico': self.diagnostico,
            'plan_tratamiento': self.plan_tratamiento,
            'observaciones': self.observaciones,
            'especialidad': self.especialidad,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
"""
Modelo de Signos Vitales
Representa los signos vitales registrados en cada consulta
"""
from datetime import datetime
from app.extensions import db


class SignosVitales(db.Model):
    """
    Modelo de Signos Vitales
    
    Se registran en cada consulta médica.
    """
    __tablename__ = 'signos_vitales'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === RELACIONES ===
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id', ondelete='CASCADE'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    
    # === FECHA DE REGISTRO ===
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # === SIGNOS VITALES ESTÁNDAR ===
    presion_sistolica = db.Column(db.Integer, nullable=True)  # mmHg
    presion_diastolica = db.Column(db.Integer, nullable=True)  # mmHg
    frecuencia_cardiaca = db.Column(db.Integer, nullable=True)  # latidos/min
    temperatura = db.Column(db.Numeric(4, 2), nullable=True)  # °C
    saturacion_oxigeno = db.Column(db.Integer, nullable=True)  # %
    frecuencia_respiratoria = db.Column(db.Integer, nullable=True)  # respiraciones/min
    
    # === MEDIDAS ANTROPOMÉTRICAS ===
    peso = db.Column(db.Numeric(6, 2), nullable=True)  # kg
    talla = db.Column(db.Numeric(5, 2), nullable=True)  # cm
    imc = db.Column(db.Numeric(5, 2), nullable=True)  # calculado automáticamente
    perimetro_cefalico = db.Column(db.Numeric(5, 2), nullable=True)  # cm (para pediatría)
    
    # === SIGNOS VITALES ESPECIALES ===
    frecuencia_cardiaca_fetal = db.Column(db.Integer, nullable=True)  # latidos/min (embarazo)
    
    # === OBSERVACIONES ===
    observaciones = db.Column(db.Text, nullable=True)
    
    # === TIMESTAMPS ===
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # === RELACIONES ===
    paciente = db.relationship('Paciente', backref=db.backref('signos_vitales', lazy='dynamic', cascade='all, delete-orphan'))
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<SignosVitales Paciente ID: {self.paciente_id} - {self.fecha_registro}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'consulta_id': self.consulta_id,
            'paciente_id': self.paciente_id,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'presion_sistolica': self.presion_sistolica,
            'presion_diastolica': self.presion_diastolica,
            'frecuencia_cardiaca': self.frecuencia_cardiaca,
            'temperatura': float(self.temperatura) if self.temperatura else None,
            'saturacion_oxigeno': self.saturacion_oxigeno,
            'frecuencia_respiratoria': self.frecuencia_respiratoria,
            'peso': float(self.peso) if self.peso else None,
            'talla': float(self.talla) if self.talla else None,
            'imc': float(self.imc) if self.imc else None,
            'perimetro_cefalico': float(self.perimetro_cefalico) if self.perimetro_cefalico else None,
            'frecuencia_cardiaca_fetal': self.frecuencia_cardiaca_fetal,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
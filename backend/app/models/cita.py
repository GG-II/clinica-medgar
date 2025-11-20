"""
Modelo de Citas
Maneja las citas médicas con calendario por médico
"""
from datetime import datetime
from app.extensions import db

class TipoCita(db.Model):
    """Catálogo de tipos de cita"""
    __tablename__ = 'tipos_cita'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_minutos = db.Column(db.Integer, default=20)
    color = db.Column(db.String(7))  # Color hexadecimal para el calendario
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con citas
    citas = db.relationship('Cita', back_populates='tipo_cita', lazy='dynamic')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'duracion_minutos': self.duracion_minutos,
            'color': self.color,
            'activo': self.activo
        }


class Cita(db.Model):
    """Modelo de Citas Médicas"""
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_cita_id = db.Column(db.Integer, db.ForeignKey('tipos_cita.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # Datos de la cita
    fecha_hora = db.Column(db.DateTime, nullable=False, index=True)
    duracion_minutos = db.Column(db.Integer, default=20)
    motivo = db.Column(db.Text)
    estado = db.Column(
        db.Enum('programada', 'confirmada', 'en_curso', 'completada', 'cancelada', 'no_asistio', 
                name='estado_cita'),
        default='programada',
        nullable=False,
        index=True
    )
    notas = db.Column(db.Text)
    es_emergencia = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    paciente = db.relationship('Paciente', back_populates='citas')
    medico = db.relationship('Usuario', foreign_keys=[medico_id], backref='citas_medico')
    creador = db.relationship('Usuario', foreign_keys=[created_by])
    tipo_cita = db.relationship('TipoCita', back_populates='citas')
    recordatorios = db.relationship('Recordatorio', back_populates='cita', cascade='all, delete-orphan')
    
    def to_dict(self, include_relaciones=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'tipo_cita_id': self.tipo_cita_id,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'duracion_minutos': self.duracion_minutos,
            'motivo': self.motivo,
            'estado': self.estado,
            'notas': self.notas,
            'es_emergencia': self.es_emergencia,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relaciones:
            data['paciente'] = {
                'id': self.paciente.id,
                'nombre_completo': self.paciente.nombre_completo,
                'telefono': self.paciente.telefono
            } if self.paciente else None
            
            data['medico'] = {
                'id': self.medico.id,
                'nombre_completo': self.medico.nombre_completo
            } if self.medico else None
            
            data['tipo_cita'] = self.tipo_cita.to_dict() if self.tipo_cita else None
        
        return data
    
    def __repr__(self):
        return f'<Cita {self.id} - {self.paciente.nombre_completo if self.paciente else "Sin paciente"} - {self.fecha_hora}>'
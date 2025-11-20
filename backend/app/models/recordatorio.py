"""
Modelo de Recordatorios
Maneja los recordatorios por WhatsApp/SMS para las citas
"""
from datetime import datetime
from app.extensions import db

class Recordatorio(db.Model):
    """Modelo de Recordatorios de Citas"""
    __tablename__ = 'recordatorios'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con cita
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id', ondelete='CASCADE'), nullable=False)
    
    # Datos del recordatorio
    tipo = db.Column(
        db.Enum('whatsapp', 'sms', 'email', name='tipo_recordatorio'),
        nullable=False
    )
    telefono_destinatario = db.Column(db.String(20))
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime)
    estado = db.Column(
        db.Enum('pendiente', 'enviado', 'fallido', 'confirmado', name='estado_recordatorio'),
        default='pendiente',
        nullable=False,
        index=True
    )
    respuesta_paciente = db.Column(db.Text)
    dias_anticipacion = db.Column(db.Integer)  # 7 o 1 día antes
    
    # Información del envío
    sid_twilio = db.Column(db.String(100))  # ID de Twilio para tracking
    error_mensaje = db.Column(db.Text)  # Si hubo error al enviar
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    cita = db.relationship('Cita', back_populates='recordatorios')
    
    def to_dict(self, include_cita=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'cita_id': self.cita_id,
            'tipo': self.tipo,
            'telefono_destinatario': self.telefono_destinatario,
            'mensaje': self.mensaje,
            'fecha_envio': self.fecha_envio.isoformat() if self.fecha_envio else None,
            'estado': self.estado,
            'respuesta_paciente': self.respuesta_paciente,
            'dias_anticipacion': self.dias_anticipacion,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_cita and self.cita:
            data['cita'] = {
                'id': self.cita.id,
                'fecha_hora': self.cita.fecha_hora.isoformat() if self.cita.fecha_hora else None,
                'paciente_nombre': self.cita.paciente.nombre_completo if self.cita.paciente else None,
                'medico_nombre': self.cita.medico.nombre_completo if self.cita.medico else None
            }
        
        return data
    
    def __repr__(self):
        return f'<Recordatorio {self.id} - {self.tipo} - {self.estado}>'
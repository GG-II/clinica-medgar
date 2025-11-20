from app.extensions import db
from datetime import datetime


class LogAuditoria(db.Model):
    """
    Modelo de Log de Auditoría
    Registra todas las acciones importantes del sistema para cumplimiento legal
    """
    __tablename__ = 'logs_auditoria'
    
    # Campos
    id = db.Column(db.BigInteger, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    accion = db.Column(db.String(100), nullable=False)
    tabla_afectada = db.Column(db.String(50), index=True)
    registro_id = db.Column(db.Integer)
    detalles = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relación con Usuario
    usuario = db.relationship('Usuario', back_populates='logs')
    
    def __repr__(self):
        return f'<LogAuditoria {self.id} - {self.accion} por Usuario {self.usuario_id}>'
    
    def to_dict(self):
        """
        Convierte el log a diccionario
        
        Returns:
            dict: Datos del log
        """
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'accion': self.accion,
            'tabla_afectada': self.tabla_afectada,
            'registro_id': self.registro_id,
            'detalles': self.detalles,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @staticmethod
    def registrar(usuario_id, accion, ip_address=None, tabla_afectada=None, registro_id=None, detalles=None):
        """
        Método estático para crear un log de auditoría fácilmente
        
        Args:
            usuario_id (int): ID del usuario que realiza la acción
            accion (str): Descripción de la acción (ej: "login", "acceso_historia_clinica")
            ip_address (str): IP desde donde se realizó la acción
            tabla_afectada (str): Nombre de la tabla afectada
            registro_id (int): ID del registro afectado
            detalles (str): Información adicional
            
        Returns:
            LogAuditoria: Instancia del log creado
        """
        log = LogAuditoria(
            usuario_id=usuario_id,
            accion=accion,
            ip_address=ip_address,
            tabla_afectada=tabla_afectada,
            registro_id=registro_id,
            detalles=detalles
        )
        db.session.add(log)
        db.session.commit()
        return log
"""
Modelo de Archivo de Paciente
Representa archivos multimedia asociados a pacientes
"""
from datetime import datetime
from app.extensions import db


class ArchivoPaciente(db.Model):
    """
    Modelo de Archivo de Paciente
    
    Almacena información sobre archivos subidos (fotos, PDFs, videos).
    """
    __tablename__ = 'archivos_paciente'
    
    # === CLAVE PRIMARIA ===
    id = db.Column(db.Integer, primary_key=True)
    
    # === RELACIÓN CON PACIENTE ===
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # === INFORMACIÓN DEL ARCHIVO ===
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    tipo_archivo = db.Column(db.String(50), nullable=True)  # image/jpeg, application/pdf, etc.
    
    # === CATEGORÍA ===
    categoria = db.Column(
        db.Enum('laboratorios', 'imagenes', 'recetas', 'ekg', 'otros', name='categoria_archivo_enum'),
        nullable=False,
        index=True
    )
    
    # === TAMAÑO ===
    tamanio_bytes = db.Column(db.BigInteger, nullable=True)
    
    # === DESCRIPCIÓN ===
    descripcion = db.Column(db.Text, nullable=True)
    
    # === USUARIO QUE SUBIÓ ===
    subido_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    # === TIMESTAMPS ===
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    # === RELACIONES ===
    paciente = db.relationship('Paciente', backref=db.backref('archivos', lazy='dynamic', cascade='all, delete-orphan'))
    usuario = db.relationship('Usuario', backref='archivos_subidos')
    
    def __repr__(self):
        """Representación del objeto para debugging"""
        return f'<ArchivoPaciente {self.nombre_archivo} - Paciente ID: {self.paciente_id}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'nombre_archivo': self.nombre_archivo,
            'ruta_archivo': self.ruta_archivo,
            'tipo_archivo': self.tipo_archivo,
            'categoria': self.categoria,
            'tamanio_bytes': self.tamanio_bytes,
            'tamanio_mb': round(self.tamanio_bytes / (1024 * 1024), 2) if self.tamanio_bytes else None,
            'descripcion': self.descripcion,
            'subido_por': self.subido_por,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None
        }
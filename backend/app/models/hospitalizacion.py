"""
Modelos para el módulo de Hospitalización.
Incluye: Cama y Hospitalización
"""

from app.extensions import db
from datetime import datetime

class Cama(db.Model):
    """
    Modelo para gestión de las 8 camas de la clínica.
    Estados: disponible, ocupada, limpieza, mantenimiento
    """
    __tablename__ = 'camas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_cama = db.Column(db.String(10), unique=True, nullable=False)
    ubicacion = db.Column(db.String(100))
    estado = db.Column(
        db.Enum('disponible', 'ocupada', 'limpieza', 'mantenimiento', name='estado_cama'),
        default='disponible',
        nullable=False
    )
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con hospitalizaciones
    hospitalizaciones = db.relationship('Hospitalizacion', back_populates='cama', lazy='dynamic')
    
    def __repr__(self):
        return f'<Cama {self.numero_cama} - {self.estado}>'
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'numero_cama': self.numero_cama,
            'ubicacion': self.ubicacion,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def esta_disponible(self):
        """Verifica si la cama está disponible para asignar"""
        return self.estado == 'disponible'
    
    def ocupar(self):
        """Marca la cama como ocupada"""
        self.estado = 'ocupada'
        self.updated_at = datetime.utcnow()
    
    def liberar(self):
        """Marca la cama como disponible"""
        self.estado = 'disponible'
        self.updated_at = datetime.utcnow()


class Hospitalizacion(db.Model):
    """
    Modelo para registros de hospitalización de pacientes.
    Relaciona: paciente, cama, médico responsable
    """
    __tablename__ = 'hospitalizaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    cama_id = db.Column(db.Integer, db.ForeignKey('camas.id'), nullable=False)
    medico_responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    fecha_egreso = db.Column(db.DateTime)
    motivo_ingreso = db.Column(db.Text, nullable=False)
    diagnostico_ingreso = db.Column(db.Text, nullable=False)
    diagnostico_egreso = db.Column(db.Text)
    estado = db.Column(
        db.Enum('activo', 'egresado', 'transferido', name='estado_hospitalizacion'),
        default='activo',
        nullable=False
    )
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    paciente = db.relationship('Paciente', backref=db.backref('hospitalizaciones', lazy='dynamic'))
    cama = db.relationship('Cama', back_populates='hospitalizaciones')
    medico_responsable = db.relationship('Usuario', foreign_keys=[medico_responsable_id])
    notas_medicas = db.relationship('NotaMedica', back_populates='hospitalizacion', lazy='dynamic', cascade='all, delete-orphan')
    ordenes_medicas = db.relationship('OrdenMedica', back_populates='hospitalizacion', lazy='dynamic', cascade='all, delete-orphan')
    registros_enfermeria = db.relationship('RegistroEnfermeria', back_populates='hospitalizacion', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Hospitalizacion {self.id} - Paciente {self.paciente_id} - {self.estado}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'cama_id': self.cama_id,
            'medico_responsable_id': self.medico_responsable_id,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'fecha_egreso': self.fecha_egreso.isoformat() if self.fecha_egreso else None,
            'motivo_ingreso': self.motivo_ingreso,
            'diagnostico_ingreso': self.diagnostico_ingreso,
            'diagnostico_egreso': self.diagnostico_egreso,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if incluir_relaciones:
            data['paciente'] = self.paciente.to_dict() if self.paciente else None
            data['cama'] = self.cama.to_dict() if self.cama else None
            data['medico_responsable'] = {
                'id': self.medico_responsable.id,
                'nombre_completo': self.medico_responsable.nombre_completo
            } if self.medico_responsable else None
            data['dias_estancia'] = self.calcular_dias_estancia()
        
        return data
    
    def calcular_dias_estancia(self):
        """Calcula los días de estancia hospitalaria"""
        if self.fecha_egreso:
            delta = self.fecha_egreso - self.fecha_ingreso
        else:
            delta = datetime.utcnow() - self.fecha_ingreso
        return delta.days
    
    def egresar(self, diagnostico_egreso, observaciones=None):
        """Marca la hospitalización como egresada"""
        self.estado = 'egresado'
        self.fecha_egreso = datetime.utcnow()
        self.diagnostico_egreso = diagnostico_egreso
        if observaciones:
            self.observaciones = observaciones
        
        # Liberar la cama
        if self.cama:
            self.cama.liberar()
    
    def esta_activa(self):
        """Verifica si la hospitalización está activa"""
        return self.estado == 'activo'
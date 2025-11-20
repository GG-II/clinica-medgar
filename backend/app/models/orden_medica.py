"""
Modelo para Órdenes Médicas en Hospitalización.
Tipos: medicamento, dieta, signos_vitales, laboratorio, imagen, interconsulta, cuidados, otro
"""

from app.extensions import db
from datetime import datetime

class OrdenMedica(db.Model):
    """
    Modelo para órdenes médicas durante hospitalización.
    Estados: activa, suspendida, completada, cancelada
    """
    __tablename__ = 'ordenes_medicas'
    
    id = db.Column(db.Integer, primary_key=True)
    hospitalizacion_id = db.Column(db.Integer, db.ForeignKey('hospitalizaciones.id', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_hora_orden = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo_orden = db.Column(
        db.Enum('medicamento', 'dieta', 'signos_vitales', 'laboratorio', 'imagen', 
                'interconsulta', 'cuidados', 'otro', name='tipo_orden_medica'),
        nullable=False
    )
    descripcion = db.Column(db.Text, nullable=False)
    indicaciones = db.Column(db.Text)
    estado = db.Column(
        db.Enum('activa', 'suspendida', 'completada', 'cancelada', name='estado_orden'),
        default='activa',
        nullable=False
    )
    fecha_suspension = db.Column(db.DateTime)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    hospitalizacion = db.relationship('Hospitalizacion', back_populates='ordenes_medicas')
    medico = db.relationship('Usuario', foreign_keys=[medico_id])
    
    def __repr__(self):
        return f'<OrdenMedica {self.id} - {self.tipo_orden} - {self.estado}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'hospitalizacion_id': self.hospitalizacion_id,
            'medico_id': self.medico_id,
            'fecha_hora_orden': self.fecha_hora_orden.isoformat() if self.fecha_hora_orden else None,
            'tipo_orden': self.tipo_orden,
            'descripcion': self.descripcion,
            'indicaciones': self.indicaciones,
            'estado': self.estado,
            'fecha_suspension': self.fecha_suspension.isoformat() if self.fecha_suspension else None,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if incluir_relaciones:
            data['medico'] = {
                'id': self.medico.id,
                'nombre_completo': self.medico.nombre_completo
            } if self.medico else None
        
        return data
    
    def suspender(self, motivo=None):
        """Suspende la orden médica"""
        self.estado = 'suspendida'
        self.fecha_suspension = datetime.utcnow()
        if motivo:
            self.observaciones = f"Suspendida: {motivo}"
    
    def completar(self, observaciones=None):
        """Marca la orden como completada"""
        self.estado = 'completada'
        if observaciones:
            self.observaciones = observaciones
    
    def cancelar(self, motivo=None):
        """Cancela la orden médica"""
        self.estado = 'cancelada'
        if motivo:
            self.observaciones = f"Cancelada: {motivo}"
    
    def esta_activa(self):
        """Verifica si la orden está activa"""
        return self.estado == 'activa'
    
    @staticmethod
    def crear_orden_medicamento(hospitalizacion_id, medico_id, medicamento, 
                                dosis, frecuencia, via, duracion=None):
        """
        Método helper para crear orden de medicamento.
        """
        descripcion = f"""
Medicamento: {medicamento}
Dosis: {dosis}
Frecuencia: {frecuencia}
Vía: {via}
        """.strip()
        
        if duracion:
            descripcion += f"\nDuración: {duracion}"
        
        return OrdenMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_orden='medicamento',
            descripcion=descripcion,
            indicaciones=f"Administrar {medicamento} {dosis} {frecuencia} vía {via}"
        )
    
    @staticmethod
    def crear_orden_dieta(hospitalizacion_id, medico_id, tipo_dieta, restricciones=None):
        """
        Método helper para crear orden de dieta.
        """
        descripcion = f"Dieta: {tipo_dieta}"
        if restricciones:
            descripcion += f"\nRestricciones: {restricciones}"
        
        return OrdenMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_orden='dieta',
            descripcion=descripcion
        )
    
    @staticmethod
    def crear_orden_signos_vitales(hospitalizacion_id, medico_id, frecuencia):
        """
        Método helper para crear orden de signos vitales.
        """
        return OrdenMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_orden='signos_vitales',
            descripcion=f"Control de signos vitales {frecuencia}",
            indicaciones=f"Tomar presión arterial, frecuencia cardíaca, temperatura, saturación O2, frecuencia respiratoria {frecuencia}"
        )
    
    @staticmethod
    def crear_orden_laboratorio(hospitalizacion_id, medico_id, estudios, urgencia=False):
        """
        Método helper para crear orden de laboratorio.
        """
        descripcion = "Estudios de laboratorio:\n" + estudios
        if urgencia:
            descripcion = "⚠️ URGENTE\n" + descripcion
        
        return OrdenMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_orden='laboratorio',
            descripcion=descripcion
        )
    
    @staticmethod
    def crear_orden_interconsulta(hospitalizacion_id, medico_id, especialidad, motivo):
        """
        Método helper para crear orden de interconsulta.
        """
        return OrdenMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_orden='interconsulta',
            descripcion=f"Interconsulta a {especialidad}",
            indicaciones=f"Motivo: {motivo}"
        )
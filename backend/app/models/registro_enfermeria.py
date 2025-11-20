"""
Modelo para Registro de Enfermería en Hospitalización.
Tipos: signos_vitales, medicamento, curacion, nota, otro
"""

from app.extensions import db
from datetime import datetime

class RegistroEnfermeria(db.Model):
    """
    Modelo para registros de enfermería durante hospitalización.
    Documenta todas las acciones realizadas por enfermería.
    """
    __tablename__ = 'registro_enfermeria'
    
    id = db.Column(db.Integer, primary_key=True)
    hospitalizacion_id = db.Column(db.Integer, db.ForeignKey('hospitalizaciones.id', ondelete='CASCADE'), nullable=False)
    enfermera_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo_registro = db.Column(
        db.Enum('signos_vitales', 'medicamento', 'curacion', 'nota', 'otro', name='tipo_registro_enfermeria'),
        nullable=False
    )
    descripcion = db.Column(db.Text, nullable=False)
    datos_json = db.Column(db.JSON)  # Para datos estructurados (signos vitales, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    hospitalizacion = db.relationship('Hospitalizacion', back_populates='registros_enfermeria')
    enfermera = db.relationship('Usuario', foreign_keys=[enfermera_id])
    
    def __repr__(self):
        return f'<RegistroEnfermeria {self.id} - {self.tipo_registro} - Hosp {self.hospitalizacion_id}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'hospitalizacion_id': self.hospitalizacion_id,
            'enfermera_id': self.enfermera_id,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'tipo_registro': self.tipo_registro,
            'descripcion': self.descripcion,
            'datos_json': self.datos_json,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if incluir_relaciones:
            data['enfermera'] = {
                'id': self.enfermera.id,
                'nombre_completo': self.enfermera.nombre_completo
            } if self.enfermera else None
        
        return data
    
    @staticmethod
    def registrar_signos_vitales(hospitalizacion_id, enfermera_id, signos_vitales):
        """
        Método helper para registrar signos vitales.
        
        Args:
            signos_vitales (dict): {
                'presion_sistolica': 120,
                'presion_diastolica': 80,
                'frecuencia_cardiaca': 72,
                'temperatura': 36.5,
                'saturacion_oxigeno': 98,
                'frecuencia_respiratoria': 18
            }
        """
        descripcion = f"""
Signos Vitales:
- Presión arterial: {signos_vitales.get('presion_sistolica', 'N/A')}/{signos_vitales.get('presion_diastolica', 'N/A')} mmHg
- Frecuencia cardíaca: {signos_vitales.get('frecuencia_cardiaca', 'N/A')} lpm
- Temperatura: {signos_vitales.get('temperatura', 'N/A')} °C
- Saturación O2: {signos_vitales.get('saturacion_oxigeno', 'N/A')}%
- Frecuencia respiratoria: {signos_vitales.get('frecuencia_respiratoria', 'N/A')} rpm
        """.strip()
        
        return RegistroEnfermeria(
            hospitalizacion_id=hospitalizacion_id,
            enfermera_id=enfermera_id,
            tipo_registro='signos_vitales',
            descripcion=descripcion,
            datos_json=signos_vitales
        )
    
    @staticmethod
    def registrar_administracion_medicamento(hospitalizacion_id, enfermera_id, 
                                            medicamento, dosis, via, hora_administracion=None):
        """
        Método helper para registrar administración de medicamento.
        """
        if not hora_administracion:
            hora_administracion = datetime.utcnow().strftime('%H:%M')
        
        descripcion = f"""
Medicamento Administrado:
- Nombre: {medicamento}
- Dosis: {dosis}
- Vía: {via}
- Hora: {hora_administracion}
        """.strip()
        
        datos_json = {
            'medicamento': medicamento,
            'dosis': dosis,
            'via': via,
            'hora_administracion': hora_administracion
        }
        
        return RegistroEnfermeria(
            hospitalizacion_id=hospitalizacion_id,
            enfermera_id=enfermera_id,
            tipo_registro='medicamento',
            descripcion=descripcion,
            datos_json=datos_json
        )
    
    @staticmethod
    def registrar_curacion(hospitalizacion_id, enfermera_id, tipo_curacion, 
                          localizacion, materiales_usados, observaciones=None):
        """
        Método helper para registrar curación.
        """
        descripcion = f"""
Curación Realizada:
- Tipo: {tipo_curacion}
- Localización: {localizacion}
- Materiales: {materiales_usados}
        """.strip()
        
        if observaciones:
            descripcion += f"\n- Observaciones: {observaciones}"
        
        datos_json = {
            'tipo_curacion': tipo_curacion,
            'localizacion': localizacion,
            'materiales_usados': materiales_usados,
            'observaciones': observaciones
        }
        
        return RegistroEnfermeria(
            hospitalizacion_id=hospitalizacion_id,
            enfermera_id=enfermera_id,
            tipo_registro='curacion',
            descripcion=descripcion,
            datos_json=datos_json
        )
    
    @staticmethod
    def registrar_nota(hospitalizacion_id, enfermera_id, nota):
        """
        Método helper para registrar nota de observación.
        """
        return RegistroEnfermeria(
            hospitalizacion_id=hospitalizacion_id,
            enfermera_id=enfermera_id,
            tipo_registro='nota',
            descripcion=nota
        )
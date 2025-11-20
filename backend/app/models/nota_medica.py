"""
Modelo para Notas Médicas en Hospitalización.
5 tipos: ingreso, evolución, procedimiento, operatoria, egreso
"""

from app.extensions import db
from datetime import datetime

class NotaMedica(db.Model):
    """
    Modelo para notas médicas durante hospitalización.
    Soporta 5 tipos de notas con datos adicionales en JSON.
    """
    __tablename__ = 'notas_medicas'
    
    id = db.Column(db.Integer, primary_key=True)
    hospitalizacion_id = db.Column(db.Integer, db.ForeignKey('hospitalizaciones.id', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_nota = db.Column(
        db.Enum('ingreso', 'evolucion', 'procedimiento', 'operatoria', 'egreso', name='tipo_nota_medica'),
        nullable=False
    )
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contenido = db.Column(db.Text, nullable=False)
    datos_adicionales = db.Column(db.JSON)  # Para campos específicos por tipo de nota
    firma_digital = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    hospitalizacion = db.relationship('Hospitalizacion', back_populates='notas_medicas')
    medico = db.relationship('Usuario', foreign_keys=[medico_id])
    
    def __repr__(self):
        return f'<NotaMedica {self.id} - {self.tipo_nota} - Hosp {self.hospitalizacion_id}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'hospitalizacion_id': self.hospitalizacion_id,
            'medico_id': self.medico_id,
            'tipo_nota': self.tipo_nota,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'contenido': self.contenido,
            'datos_adicionales': self.datos_adicionales,
            'firma_digital': self.firma_digital,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if incluir_relaciones:
            data['medico'] = {
                'id': self.medico.id,
                'nombre_completo': self.medico.nombre_completo
            } if self.medico else None
        
        return data
    
    @staticmethod
    def crear_nota_ingreso(hospitalizacion_id, medico_id, motivo, resumen_caso, 
                          antecedentes, examen_fisico, diagnostico, plan):
        """
        Método helper para crear nota de ingreso con estructura estándar.
        """
        contenido = f"""
MOTIVO DE HOSPITALIZACIÓN:
{motivo}

RESUMEN DEL CASO:
{resumen_caso}

ANTECEDENTES RELEVANTES:
{antecedentes}

EXAMEN FÍSICO DE INGRESO:
{examen_fisico}

DIAGNÓSTICO DE INGRESO:
{diagnostico}

PLAN DE MANEJO:
{plan}
        """.strip()
        
        datos_adicionales = {
            'motivo': motivo,
            'resumen_caso': resumen_caso,
            'antecedentes': antecedentes,
            'examen_fisico': examen_fisico,
            'diagnostico': diagnostico,
            'plan': plan
        }
        
        return NotaMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_nota='ingreso',
            contenido=contenido,
            datos_adicionales=datos_adicionales
        )
    
    @staticmethod
    def crear_nota_evolucion(hospitalizacion_id, medico_id, subjetivo, objetivo, 
                            analisis, plan):
        """
        Método helper para crear nota de evolución (SOAP).
        """
        contenido = f"""
SUBJETIVO (cómo se siente el paciente):
{subjetivo}

OBJETIVO (signos vitales, examen físico):
{objetivo}

ANÁLISIS:
{analisis}

PLAN:
{plan}
        """.strip()
        
        datos_adicionales = {
            'subjetivo': subjetivo,
            'objetivo': objetivo,
            'analisis': analisis,
            'plan': plan
        }
        
        return NotaMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_nota='evolucion',
            contenido=contenido,
            datos_adicionales=datos_adicionales
        )
    
    @staticmethod
    def crear_nota_procedimiento(hospitalizacion_id, medico_id, tipo_procedimiento,
                                 indicacion, descripcion, hallazgos, complicaciones, 
                                 plan_post):
        """
        Método helper para crear nota de procedimiento.
        """
        contenido = f"""
TIPO DE PROCEDIMIENTO:
{tipo_procedimiento}

INDICACIÓN:
{indicacion}

DESCRIPCIÓN DEL PROCEDIMIENTO:
{descripcion}

HALLAZGOS:
{hallazgos}

COMPLICACIONES:
{complicaciones if complicaciones else 'Ninguna'}

PLAN POST-PROCEDIMIENTO:
{plan_post}
        """.strip()
        
        datos_adicionales = {
            'tipo_procedimiento': tipo_procedimiento,
            'indicacion': indicacion,
            'descripcion': descripcion,
            'hallazgos': hallazgos,
            'complicaciones': complicaciones,
            'plan_post': plan_post
        }
        
        return NotaMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_nota='procedimiento',
            contenido=contenido,
            datos_adicionales=datos_adicionales
        )
    
    @staticmethod
    def crear_nota_operatoria(hospitalizacion_id, medico_id, cirugia_realizada,
                             cirujano, ayudantes, anestesiologo, tipo_anestesia,
                             diagnostico_pre, diagnostico_post, descripcion,
                             hallazgos, complicaciones, sangrado, especimenes, 
                             pronostico):
        """
        Método helper para crear nota operatoria completa.
        """
        contenido = f"""
CIRUGÍA REALIZADA:
{cirugia_realizada}

EQUIPO QUIRÚRGICO:
Cirujano: {cirujano}
Ayudantes: {ayudantes}
Anestesiólogo: {anestesiologo}
Tipo de anestesia: {tipo_anestesia}

DIAGNÓSTICO PREOPERATORIO:
{diagnostico_pre}

DIAGNÓSTICO POSTOPERATORIO:
{diagnostico_post}

DESCRIPCIÓN DEL PROCEDIMIENTO:
{descripcion}

HALLAZGOS:
{hallazgos}

COMPLICACIONES:
{complicaciones if complicaciones else 'Ninguna'}

SANGRADO ESTIMADO:
{sangrado}

ESPECÍMENES ENVIADOS A PATOLOGÍA:
{especimenes if especimenes else 'Ninguno'}

PRONÓSTICO:
{pronostico}
        """.strip()
        
        datos_adicionales = {
            'cirugia_realizada': cirugia_realizada,
            'cirujano': cirujano,
            'ayudantes': ayudantes,
            'anestesiologo': anestesiologo,
            'tipo_anestesia': tipo_anestesia,
            'diagnostico_pre': diagnostico_pre,
            'diagnostico_post': diagnostico_post,
            'descripcion': descripcion,
            'hallazgos': hallazgos,
            'complicaciones': complicaciones,
            'sangrado': sangrado,
            'especimenes': especimenes,
            'pronostico': pronostico
        }
        
        return NotaMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_nota='operatoria',
            contenido=contenido,
            datos_adicionales=datos_adicionales
        )
    
    @staticmethod
    def crear_nota_egreso(hospitalizacion_id, medico_id, dias_estancia, 
                         resumen_hospitalizacion, diagnostico_final, 
                         procedimientos, condicion_egreso, tratamiento_alta, 
                         indicaciones, cita_control):
        """
        Método helper para crear nota de egreso.
        """
        contenido = f"""
DÍAS DE ESTANCIA:
{dias_estancia}

RESUMEN DE HOSPITALIZACIÓN:
{resumen_hospitalizacion}

DIAGNÓSTICO FINAL:
{diagnostico_final}

PROCEDIMIENTOS REALIZADOS:
{procedimientos}

CONDICIÓN DE EGRESO:
{condicion_egreso}

TRATAMIENTO AL ALTA:
{tratamiento_alta}

INDICACIONES:
{indicaciones}

CITA DE CONTROL:
{cita_control}
        """.strip()
        
        datos_adicionales = {
            'dias_estancia': dias_estancia,
            'resumen_hospitalizacion': resumen_hospitalizacion,
            'diagnostico_final': diagnostico_final,
            'procedimientos': procedimientos,
            'condicion_egreso': condicion_egreso,
            'tratamiento_alta': tratamiento_alta,
            'indicaciones': indicaciones,
            'cita_control': cita_control
        }
        
        return NotaMedica(
            hospitalizacion_id=hospitalizacion_id,
            medico_id=medico_id,
            tipo_nota='egreso',
            contenido=contenido,
            datos_adicionales=datos_adicionales
        )
"""
Modelo de Recetas
Maneja las recetas médicas y sus detalles
"""
from datetime import datetime
from app.extensions import db

class Receta(db.Model):
    """Modelo de Recetas Médicas"""
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'))
    
    # Datos de la receta
    fecha_emision = db.Column(db.Date, nullable=False, index=True)
    indicaciones_generales = db.Column(db.Text)
    diagnostico = db.Column(db.String(255))
    activa = db.Column(db.Boolean, default=True)  # Si todavía es válida para dispensar
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    paciente = db.relationship('Paciente', backref='recetas')
    medico = db.relationship('Usuario', backref='recetas_emitidas')
    consulta = db.relationship('Consulta', backref='recetas')
    medicamentos = db.relationship('RecetaDetalle', back_populates='receta', cascade='all, delete-orphan')
    
    def to_dict(self, include_medicamentos=True):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'consulta_id': self.consulta_id,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'indicaciones_generales': self.indicaciones_generales,
            'diagnostico': self.diagnostico,
            'activa': self.activa,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paciente': {
                'id': self.paciente.id,
                'nombre_completo': self.paciente.nombre_completo,
                'edad': self.paciente.edad,
                'dpi': self.paciente.dpi
            } if self.paciente else None,
            'medico': {
                'id': self.medico.id,
                'nombre_completo': self.medico.nombre_completo
            } if self.medico else None
        }
        
        if include_medicamentos:
            data['medicamentos'] = [med.to_dict() for med in self.medicamentos]
        
        return data
    
    def validar_alergias(self):
        """
        Validar si algún medicamento de la receta tiene interacción
        con las alergias del paciente
        """
        alergias = []
        
        if self.paciente and self.paciente.historia_clinica:
            # Obtener antecedentes alérgicos
            antecedentes_alergicos = [
                ant for ant in self.paciente.historia_clinica.antecedentes 
                if ant.tipo == 'alergicos' and ant.activo
            ]
            
            for medicamento_receta in self.medicamentos:
                medicamento = medicamento_receta.medicamento
                
                # Revisar si alguna alergia menciona este medicamento
                for alergia in antecedentes_alergicos:
                    if medicamento.nombre_generico.lower() in alergia.descripcion.lower():
                        alergias.append({
                            'medicamento': medicamento.nombre_generico,
                            'alergia': alergia.descripcion
                        })
        
        return alergias
    
    def __repr__(self):
        return f'<Receta {self.id} - {self.paciente.nombre_completo if self.paciente else "Sin paciente"}>'


class RecetaDetalle(db.Model):
    """Detalle de medicamentos en una receta"""
    __tablename__ = 'recetas_detalle'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id', ondelete='CASCADE'), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)
    
    # Indicaciones del medicamento
    dosis = db.Column(db.String(100), nullable=False)  # "1 tableta", "10 ml"
    frecuencia = db.Column(db.String(100), nullable=False)  # "cada 8 horas", "3 veces al día"
    duracion = db.Column(db.String(50))  # "7 días", "1 mes"
    via_administracion = db.Column(db.String(50))  # "Oral", "Tópica"
    indicaciones_especificas = db.Column(db.Text)  # "Tomar con alimentos"
    cantidad_prescrita = db.Column(db.Integer)  # Cantidad de unidades a dispensar
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    receta = db.relationship('Receta', back_populates='medicamentos')
    medicamento = db.relationship('Medicamento', back_populates='recetas_detalle')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'receta_id': self.receta_id,
            'medicamento_id': self.medicamento_id,
            'medicamento': self.medicamento.to_dict_simple() if self.medicamento else None,
            'dosis': self.dosis,
            'frecuencia': self.frecuencia,
            'duracion': self.duracion,
            'via_administracion': self.via_administracion,
            'indicaciones_especificas': self.indicaciones_especificas,
            'cantidad_prescrita': self.cantidad_prescrita
        }
    
    def __repr__(self):
        return f'<RecetaDetalle {self.id} - {self.medicamento.nombre_generico if self.medicamento else "Sin medicamento"}>'
"""
Modelo de Laboratorios
Maneja tipos de estudios y resultados de laboratorio
"""
from datetime import datetime
from app.extensions import db

class TipoLaboratorio(db.Model):
    """Catálogo de tipos de estudios de laboratorio"""
    __tablename__ = 'tipos_laboratorio'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))  # Hematología, Química, etc.
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    laboratorios = db.relationship('Laboratorio', back_populates='tipo_laboratorio', lazy='dynamic')
    valores_referencia = db.relationship('ValorReferencia', back_populates='tipo_laboratorio', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'activo': self.activo
        }
    
    def __repr__(self):
        return f'<TipoLaboratorio {self.id} - {self.nombre}>'


class Laboratorio(db.Model):
    """Modelo de Estudios de Laboratorio"""
    __tablename__ = 'laboratorios'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_laboratorio_id = db.Column(db.Integer, db.ForeignKey('tipos_laboratorio.id'), nullable=False)
    
    # Datos del laboratorio
    fecha_solicitud = db.Column(db.Date, nullable=False, index=True)
    fecha_resultado = db.Column(db.Date, index=True)
    laboratorio_externo = db.Column(db.String(100))  # Nombre del laboratorio que procesó
    
    # Resultados (guardados como JSON para flexibilidad)
    resultados = db.Column(db.JSON)
    """
    Ejemplo de estructura JSON:
    {
        "hemoglobina": {"valor": 12.5, "unidad": "g/dL", "normal": true},
        "leucocitos": {"valor": 8500, "unidad": "/mm³", "normal": true},
        "glucosa": {"valor": 95, "unidad": "mg/dL", "normal": true}
    }
    """
    
    interpretacion = db.Column(db.Text)  # Interpretación del médico
    observaciones = db.Column(db.Text)
    archivo_url = db.Column(db.String(255))  # Ruta del PDF/imagen del resultado
    
    estado = db.Column(
        db.Enum('solicitado', 'en_proceso', 'completado', 'cancelado', name='estado_laboratorio'),
        default='solicitado',
        nullable=False,
        index=True
    )
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    paciente = db.relationship('Paciente', backref='laboratorios')
    medico = db.relationship('Usuario', backref='laboratorios_solicitados')
    tipo_laboratorio = db.relationship('TipoLaboratorio', back_populates='laboratorios')
    
    def to_dict(self, include_relaciones=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'tipo_laboratorio_id': self.tipo_laboratorio_id,
            'fecha_solicitud': self.fecha_solicitud.isoformat() if self.fecha_solicitud else None,
            'fecha_resultado': self.fecha_resultado.isoformat() if self.fecha_resultado else None,
            'laboratorio_externo': self.laboratorio_externo,
            'resultados': self.resultados,
            'interpretacion': self.interpretacion,
            'observaciones': self.observaciones,
            'archivo_url': self.archivo_url,
            'estado': self.estado,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relaciones:
            data['paciente'] = {
                'id': self.paciente.id,
                'nombre_completo': self.paciente.nombre_completo,
                'edad': self.paciente.edad,
                'sexo': self.paciente.sexo
            } if self.paciente else None
            
            data['medico'] = {
                'id': self.medico.id,
                'nombre_completo': self.medico.nombre_completo
            } if self.medico else None
            
            data['tipo'] = self.tipo_laboratorio.to_dict() if self.tipo_laboratorio else None
        
        return data
    
    def verificar_valores_criticos(self):
        """
        Verifica si hay valores críticos en los resultados
        Retorna lista de alertas
        """
        alertas = []
        
        if not self.resultados:
            return alertas
        
        # Valores críticos comunes
        valores_criticos = {
            'hemoglobina': {'min': 7, 'max': 20},
            'leucocitos': {'min': 2000, 'max': 30000},
            'plaquetas': {'min': 50000, 'max': 1000000},
            'glucosa': {'min': 40, 'max': 400},
            'creatinina': {'min': 0, 'max': 5},
            'potasio': {'min': 2.5, 'max': 6.5}
        }
        
        for parametro, limites in valores_criticos.items():
            if parametro in self.resultados:
                valor = self.resultados[parametro].get('valor')
                if valor:
                    if valor < limites['min'] or valor > limites['max']:
                        alertas.append({
                            'parametro': parametro,
                            'valor': valor,
                            'limite_min': limites['min'],
                            'limite_max': limites['max'],
                            'severidad': 'critico'
                        })
        
        return alertas
    
    def __repr__(self):
        return f'<Laboratorio {self.id} - {self.tipo_laboratorio.nombre if self.tipo_laboratorio else "Sin tipo"}>'


class ValorReferencia(db.Model):
    """Valores de referencia para cada tipo de laboratorio"""
    __tablename__ = 'valores_referencia'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación
    tipo_laboratorio_id = db.Column(db.Integer, db.ForeignKey('tipos_laboratorio.id'), nullable=False)
    
    # Parámetro
    parametro = db.Column(db.String(100), nullable=False)  # "hemoglobina", "glucosa"
    valor_minimo = db.Column(db.Numeric(10, 2))
    valor_maximo = db.Column(db.Numeric(10, 2))
    unidad = db.Column(db.String(20))  # "g/dL", "mg/dL"
    
    # Rangos por edad y sexo
    rango_edad_min = db.Column(db.Integer)  # Edad mínima en años
    rango_edad_max = db.Column(db.Integer)  # Edad máxima en años
    sexo = db.Column(
        db.Enum('M', 'F', 'ambos', name='sexo_valor_referencia'),
        default='ambos'
    )
    
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    tipo_laboratorio = db.relationship('TipoLaboratorio', back_populates='valores_referencia')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'tipo_laboratorio_id': self.tipo_laboratorio_id,
            'parametro': self.parametro,
            'valor_minimo': float(self.valor_minimo) if self.valor_minimo else None,
            'valor_maximo': float(self.valor_maximo) if self.valor_maximo else None,
            'unidad': self.unidad,
            'rango_edad_min': self.rango_edad_min,
            'rango_edad_max': self.rango_edad_max,
            'sexo': self.sexo,
            'observaciones': self.observaciones
        }
    
    @staticmethod
    def obtener_referencia(tipo_laboratorio_id, parametro, edad, sexo):
        """
        Obtiene el valor de referencia apropiado según edad y sexo
        """
        return ValorReferencia.query.filter(
            ValorReferencia.tipo_laboratorio_id == tipo_laboratorio_id,
            ValorReferencia.parametro == parametro,
            db.or_(
                ValorReferencia.rango_edad_min.is_(None),
                ValorReferencia.rango_edad_min <= edad
            ),
            db.or_(
                ValorReferencia.rango_edad_max.is_(None),
                ValorReferencia.rango_edad_max >= edad
            ),
            db.or_(
                ValorReferencia.sexo == 'ambos',
                ValorReferencia.sexo == sexo
            )
        ).first()
    
    def __repr__(self):
        return f'<ValorReferencia {self.parametro} - {self.valor_minimo}-{self.valor_maximo} {self.unidad}>'
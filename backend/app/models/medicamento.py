"""
Modelo de Medicamentos
Catálogo de medicamentos disponibles en Guatemala
"""
from datetime import datetime
from app.extensions import db

class Medicamento(db.Model):
    """Modelo de Catálogo de Medicamentos"""
    __tablename__ = 'medicamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información básica
    nombre_generico = db.Column(db.String(200), nullable=False, index=True)
    nombre_comercial = db.Column(db.String(200), index=True)
    presentacion = db.Column(db.String(100))  # Tableta, jarabe, inyectable, etc.
    concentracion = db.Column(db.String(50))  # 500mg, 10mg/ml, etc.
    via_administracion = db.Column(db.String(50))  # Oral, IV, IM, tópica, etc.
    
    # Información clínica
    interacciones = db.Column(db.Text)  # Interacciones medicamentosas conocidas
    contraindicaciones = db.Column(db.Text)  # Contraindicaciones
    observaciones = db.Column(db.Text)
    
    # Control
    activo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    recetas_detalle = db.relationship('RecetaDetalle', back_populates='medicamento', lazy='dynamic')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre_generico': self.nombre_generico,
            'nombre_comercial': self.nombre_comercial,
            'presentacion': self.presentacion,
            'concentracion': self.concentracion,
            'via_administracion': self.via_administracion,
            'interacciones': self.interacciones,
            'contraindicaciones': self.contraindicaciones,
            'observaciones': self.observaciones,
            'activo': self.activo
        }
    
    def to_dict_simple(self):
        """Versión simplificada para búsquedas rápidas"""
        return {
            'id': self.id,
            'nombre_generico': self.nombre_generico,
            'nombre_comercial': self.nombre_comercial,
            'presentacion': self.presentacion,
            'concentracion': self.concentracion
        }
    
    @staticmethod
    def buscar(query, limit=10):
        """
        Búsqueda predictiva de medicamentos
        Busca en nombre genérico y comercial
        """
        if not query:
            return []
        
        query_pattern = f"%{query}%"
        
        return Medicamento.query.filter(
            db.and_(
                Medicamento.activo == True,
                db.or_(
                    Medicamento.nombre_generico.ilike(query_pattern),
                    Medicamento.nombre_comercial.ilike(query_pattern)
                )
            )
        ).limit(limit).all()
    
    def __repr__(self):
        return f'<Medicamento {self.id} - {self.nombre_generico}>'
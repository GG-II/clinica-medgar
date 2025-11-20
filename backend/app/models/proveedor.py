"""
Modelo para Proveedores de Farmacia.
Gestiona empresas que suministran medicamentos e insumos médicos.
"""

from app.extensions import db
from datetime import datetime

class Proveedor(db.Model):
    """
    Modelo para proveedores de medicamentos e insumos médicos.
    """
    __tablename__ = 'proveedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    nit = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    contacto_nombre = db.Column(db.String(100))
    productos_suministra = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    productos = db.relationship('ProductoFarmacia', back_populates='proveedor', lazy='dynamic')
    compras = db.relationship('Compra', back_populates='proveedor', lazy='dynamic')
    
    def __repr__(self):
        return f'<Proveedor {self.id} - {self.nombre}>'
    
    def to_dict(self, incluir_estadisticas=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'nit': self.nit,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'contacto_nombre': self.contacto_nombre,
            'productos_suministra': self.productos_suministra,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if incluir_estadisticas:
            data['total_productos'] = self.productos.count()
            data['total_compras'] = self.compras.count()
        
        return data
    
    def desactivar(self):
        """Desactiva el proveedor"""
        self.activo = False
        self.updated_at = datetime.utcnow()
    
    def activar(self):
        """Activa el proveedor"""
        self.activo = True
        self.updated_at = datetime.utcnow()
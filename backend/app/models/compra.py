"""
Modelos para Compras de Farmacia.
Incluye: Compra y CompraDetalle
"""

from app.extensions import db
from datetime import datetime

class Compra(db.Model):
    """
    Modelo para órdenes de compra a proveedores.
    Estados: pendiente, recibida, parcial, cancelada
    """
    __tablename__ = 'compras'
    
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    numero_factura = db.Column(db.String(50))
    fecha_compra = db.Column(db.Date, nullable=False)
    fecha_recepcion = db.Column(db.Date)
    subtotal = db.Column(db.Numeric(10, 2))
    impuestos = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(
        db.Enum('pendiente', 'recibida', 'parcial', 'cancelada', name='estado_compra'),
        default='pendiente',
        nullable=False
    )
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    proveedor = db.relationship('Proveedor', back_populates='compras')
    usuario = db.relationship('Usuario')
    detalles = db.relationship('CompraDetalle', back_populates='compra', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Compra {self.id} - Proveedor {self.proveedor_id} - {self.estado}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'proveedor_id': self.proveedor_id,
            'numero_factura': self.numero_factura,
            'fecha_compra': self.fecha_compra.isoformat() if self.fecha_compra else None,
            'fecha_recepcion': self.fecha_recepcion.isoformat() if self.fecha_recepcion else None,
            'subtotal': float(self.subtotal) if self.subtotal else None,
            'impuestos': float(self.impuestos) if self.impuestos else None,
            'total': float(self.total) if self.total else None,
            'estado': self.estado,
            'usuario_id': self.usuario_id,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if incluir_relaciones:
            data['proveedor'] = self.proveedor.to_dict() if self.proveedor else None
            data['usuario'] = {
                'id': self.usuario.id,
                'nombre_completo': self.usuario.nombre_completo
            } if self.usuario else None
            data['detalles'] = [detalle.to_dict() for detalle in self.detalles]
            data['cantidad_productos'] = self.detalles.count()
        
        return data
    
    def calcular_totales(self):
        """Calcula subtotal e impuestos basado en los detalles"""
        subtotal = sum(detalle.subtotal for detalle in self.detalles)
        self.subtotal = subtotal
        self.impuestos = subtotal * 0.12  # IVA 12% Guatemala
        self.total = self.subtotal + self.impuestos
    
    def marcar_como_recibida(self, fecha_recepcion=None):
        """Marca la compra como recibida"""
        self.estado = 'recibida'
        self.fecha_recepcion = fecha_recepcion or datetime.now().date()
    
    def cancelar(self, motivo=None):
        """Cancela la compra"""
        self.estado = 'cancelada'
        if motivo:
            self.observaciones = f"Cancelada: {motivo}"


class CompraDetalle(db.Model):
    """
    Modelo para detalle de compras (productos comprados).
    """
    __tablename__ = 'compras_detalle'
    
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id', ondelete='CASCADE'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos_farmacia.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    lote = db.Column(db.String(50))
    fecha_vencimiento = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    compra = db.relationship('Compra', back_populates='detalles')
    producto = db.relationship('ProductoFarmacia')
    
    def __repr__(self):
        return f'<CompraDetalle {self.id} - Compra {self.compra_id} - Producto {self.producto_id}>'
    
    def to_dict(self, incluir_producto=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'compra_id': self.compra_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal': float(self.subtotal),
            'lote': self.lote,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if incluir_producto:
            data['producto'] = {
                'id': self.producto.id,
                'codigo_interno': self.producto.codigo_interno,
                'nombre_generico': self.producto.nombre_generico,
                'nombre_comercial': self.producto.nombre_comercial,
                'presentacion': self.producto.presentacion
            } if self.producto else None
        
        return data
    
    def calcular_subtotal(self):
        """Calcula el subtotal del detalle"""
        self.subtotal = self.cantidad * self.precio_unitario
        return self.subtotal
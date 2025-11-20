"""
Modelo para Movimientos de Inventario (Kardex).
Tipos: entrada, salida, ajuste, devolucion
"""

from app.extensions import db
from datetime import datetime

class MovimientoInventario(db.Model):
    """
    Modelo para kardex de inventario.
    Registra todas las entradas y salidas de productos.
    """
    __tablename__ = 'movimientos_inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos_farmacia.id'), nullable=False)
    tipo_movimiento = db.Column(
        db.Enum('entrada', 'salida', 'ajuste', 'devolucion', name='tipo_movimiento_inventario'),
        nullable=False
    )
    cantidad = db.Column(db.Integer, nullable=False)
    stock_anterior = db.Column(db.Integer, nullable=False)
    stock_nuevo = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(100))
    referencia_id = db.Column(db.Integer)  # ID de compra, venta, etc.
    referencia_tipo = db.Column(db.String(50))  # 'compra', 'venta', 'dispensacion', etc.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_movimiento = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)
    
    # Relaciones
    producto = db.relationship('ProductoFarmacia', back_populates='movimientos')
    usuario = db.relationship('Usuario')
    
    def __repr__(self):
        return f'<MovimientoInventario {self.id} - {self.tipo_movimiento} - Producto {self.producto_id}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'producto_id': self.producto_id,
            'tipo_movimiento': self.tipo_movimiento,
            'cantidad': self.cantidad,
            'stock_anterior': self.stock_anterior,
            'stock_nuevo': self.stock_nuevo,
            'motivo': self.motivo,
            'referencia_id': self.referencia_id,
            'referencia_tipo': self.referencia_tipo,
            'usuario_id': self.usuario_id,
            'fecha_movimiento': self.fecha_movimiento.isoformat() if self.fecha_movimiento else None,
            'observaciones': self.observaciones
        }
        
        if incluir_relaciones:
            data['producto'] = {
                'id': self.producto.id,
                'codigo_interno': self.producto.codigo_interno,
                'nombre_generico': self.producto.nombre_generico,
                'nombre_comercial': self.producto.nombre_comercial
            } if self.producto else None
            
            data['usuario'] = {
                'id': self.usuario.id,
                'nombre_completo': self.usuario.nombre_completo
            } if self.usuario else None
        
        return data
    
    @staticmethod
    def registrar_entrada(producto, cantidad, motivo, referencia_id=None, 
                         referencia_tipo=None, usuario_id=None, observaciones=None):
        """
        Método helper para registrar entrada de inventario.
        """
        stock_anterior = producto.stock_actual
        producto.aumentar_stock(cantidad)
        stock_nuevo = producto.stock_actual
        
        movimiento = MovimientoInventario(
            producto_id=producto.id,
            tipo_movimiento='entrada',
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo=motivo,
            referencia_id=referencia_id,
            referencia_tipo=referencia_tipo,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        return movimiento
    
    @staticmethod
    def registrar_salida(producto, cantidad, motivo, referencia_id=None, 
                        referencia_tipo=None, usuario_id=None, observaciones=None):
        """
        Método helper para registrar salida de inventario.
        """
        stock_anterior = producto.stock_actual
        producto.disminuir_stock(cantidad)  # Lanza excepción si no hay stock
        stock_nuevo = producto.stock_actual
        
        movimiento = MovimientoInventario(
            producto_id=producto.id,
            tipo_movimiento='salida',
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo=motivo,
            referencia_id=referencia_id,
            referencia_tipo=referencia_tipo,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        return movimiento
    
    @staticmethod
    def registrar_ajuste(producto, cantidad_nueva, motivo, usuario_id=None, observaciones=None):
        """
        Método helper para registrar ajuste de inventario.
        cantidad_nueva: el nuevo stock total (no la diferencia)
        """
        stock_anterior = producto.stock_actual
        diferencia = cantidad_nueva - stock_anterior
        
        producto.stock_actual = cantidad_nueva
        producto.updated_at = datetime.utcnow()
        
        movimiento = MovimientoInventario(
            producto_id=producto.id,
            tipo_movimiento='ajuste',
            cantidad=abs(diferencia),
            stock_anterior=stock_anterior,
            stock_nuevo=cantidad_nueva,
            motivo=motivo,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        return movimiento
    
    @staticmethod
    def registrar_devolucion(producto, cantidad, motivo, referencia_id=None,
                            referencia_tipo=None, usuario_id=None, observaciones=None):
        """
        Método helper para registrar devolución (aumenta stock).
        """
        stock_anterior = producto.stock_actual
        producto.aumentar_stock(cantidad)
        stock_nuevo = producto.stock_actual
        
        movimiento = MovimientoInventario(
            producto_id=producto.id,
            tipo_movimiento='devolucion',
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo=motivo,
            referencia_id=referencia_id,
            referencia_tipo=referencia_tipo,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        return movimiento
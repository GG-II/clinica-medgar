"""
Modelo para Productos de Farmacia e Inventario.
Tipos: medicamento, insumo_medico, material_curacion, solucion_iv, equipo
"""

from app.extensions import db
from datetime import datetime, timedelta

class ProductoFarmacia(db.Model):
    """
    Modelo para productos de farmacia e inventario.
    Gestiona medicamentos, insumos médicos y material de curación.
    """
    __tablename__ = 'productos_farmacia'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.String(50), unique=True)
    nombre_generico = db.Column(db.String(200), nullable=False)
    nombre_comercial = db.Column(db.String(200))
    presentacion = db.Column(db.String(100))
    concentracion = db.Column(db.String(50))
    tipo_producto = db.Column(
        db.Enum('medicamento', 'insumo_medico', 'material_curacion', 'solucion_iv', 'equipo', 
                name='tipo_producto_farmacia'),
        nullable=False
    )
    lote = db.Column(db.String(50))
    fecha_vencimiento = db.Column(db.Date)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    precio_compra = db.Column(db.Numeric(10, 2))
    precio_venta = db.Column(db.Numeric(10, 2))
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=10)
    ubicacion = db.Column(db.String(100))
    requiere_receta = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    proveedor = db.relationship('Proveedor', back_populates='productos')
    movimientos = db.relationship('MovimientoInventario', back_populates='producto', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ProductoFarmacia {self.codigo_interno} - {self.nombre_generico}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'codigo_interno': self.codigo_interno,
            'nombre_generico': self.nombre_generico,
            'nombre_comercial': self.nombre_comercial,
            'presentacion': self.presentacion,
            'concentracion': self.concentracion,
            'tipo_producto': self.tipo_producto,
            'lote': self.lote,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'proveedor_id': self.proveedor_id,
            'precio_compra': float(self.precio_compra) if self.precio_compra else None,
            'precio_venta': float(self.precio_venta) if self.precio_venta else None,
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'ubicacion': self.ubicacion,
            'requiere_receta': self.requiere_receta,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if incluir_relaciones:
            data['proveedor'] = self.proveedor.to_dict() if self.proveedor else None
            data['alertas'] = self.obtener_alertas()
        
        return data
    
    def obtener_alertas(self):
        """
        Genera alertas automáticas del producto.
        Retorna lista de alertas activas.
        """
        alertas = []
        
        # Alerta stock mínimo
        if self.stock_actual <= self.stock_minimo:
            alertas.append({
                'tipo': 'stock_minimo',
                'severidad': 'alta' if self.stock_actual == 0 else 'media',
                'mensaje': f'Stock bajo: {self.stock_actual} unidades (mínimo: {self.stock_minimo})'
            })
        
        # Alerta vencimiento
        if self.fecha_vencimiento:
            dias_para_vencer = (self.fecha_vencimiento - datetime.now().date()).days
            
            if dias_para_vencer < 0:
                alertas.append({
                    'tipo': 'vencido',
                    'severidad': 'critica',
                    'mensaje': f'Producto VENCIDO desde hace {abs(dias_para_vencer)} días'
                })
            elif dias_para_vencer <= 30:
                alertas.append({
                    'tipo': 'por_vencer',
                    'severidad': 'alta',
                    'mensaje': f'Vence en {dias_para_vencer} días'
                })
            elif dias_para_vencer <= 60:
                alertas.append({
                    'tipo': 'proximo_vencer',
                    'severidad': 'media',
                    'mensaje': f'Vence en {dias_para_vencer} días'
                })
        
        return alertas
    
    def tiene_stock_suficiente(self, cantidad):
        """Verifica si hay stock suficiente para dispensar"""
        return self.stock_actual >= cantidad
    
    def aumentar_stock(self, cantidad, precio_compra=None):
        """Aumenta el stock del producto (entrada)"""
        self.stock_actual += cantidad
        if precio_compra:
            self.precio_compra = precio_compra
        self.updated_at = datetime.utcnow()
    
    def disminuir_stock(self, cantidad):
        """Disminuye el stock del producto (salida)"""
        if not self.tiene_stock_suficiente(cantidad):
            raise ValueError(f'Stock insuficiente. Disponible: {self.stock_actual}, Solicitado: {cantidad}')
        
        self.stock_actual -= cantidad
        self.updated_at = datetime.utcnow()
    
    def calcular_margen_utilidad(self):
        """Calcula el margen de utilidad porcentual"""
        if not self.precio_compra or self.precio_compra == 0:
            return None
        
        margen = ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100
        return round(float(margen), 2)
    
    def esta_vencido(self):
        """Verifica si el producto está vencido"""
        if not self.fecha_vencimiento:
            return False
        return self.fecha_vencimiento < datetime.now().date()
    
    def dias_hasta_vencimiento(self):
        """Calcula días hasta el vencimiento"""
        if not self.fecha_vencimiento:
            return None
        return (self.fecha_vencimiento - datetime.now().date()).days
    
    def necesita_reorden(self):
        """Verifica si necesita reorden (stock bajo)"""
        return self.stock_actual <= self.stock_minimo
    
    def generar_codigo_interno(self):
        """
        Genera código interno automático si no existe.
        Formato: TIPO-NUMERO
        Ejemplo: MED-001, INS-042
        """
        if self.codigo_interno:
            return self.codigo_interno
        
        prefijos = {
            'medicamento': 'MED',
            'insumo_medico': 'INS',
            'material_curacion': 'MAT',
            'solucion_iv': 'SOL',
            'equipo': 'EQP'
        }
        
        prefijo = prefijos.get(self.tipo_producto, 'PRD')
        
        # Buscar el último código de este tipo
        ultimo = ProductoFarmacia.query.filter(
            ProductoFarmacia.codigo_interno.like(f'{prefijo}-%')
        ).order_by(ProductoFarmacia.id.desc()).first()
        
        if ultimo and ultimo.codigo_interno:
            try:
                numero = int(ultimo.codigo_interno.split('-')[1]) + 1
            except:
                numero = 1
        else:
            numero = 1
        
        self.codigo_interno = f'{prefijo}-{numero:03d}'
        return self.codigo_interno
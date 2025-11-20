"""
Servicio para gestión de inventario de farmacia.
Incluye: alertas, control de stock, dispensación
"""

from app.extensions import db
from app.models import ProductoFarmacia, MovimientoInventario, Receta
from datetime import datetime, timedelta
from sqlalchemy import or_

class InventarioService:
    """Servicio para gestión de inventario"""
    
    @staticmethod
    def obtener_alertas():
        """
        Obtiene todas las alertas activas de inventario.
        Retorna: {
            'stock_minimo': [],
            'vencidos': [],
            'por_vencer': []
        }
        """
        productos = ProductoFarmacia.query.filter_by(activo=True).all()
        
        alertas = {
            'stock_minimo': [],
            'vencidos': [],
            'por_vencer_30': [],
            'por_vencer_60': []
        }
        
        hoy = datetime.now().date()
        
        for producto in productos:
            # Alertas de stock
            if producto.stock_actual <= producto.stock_minimo:
                alertas['stock_minimo'].append({
                    'producto': producto.to_dict(),
                    'severidad': 'critica' if producto.stock_actual == 0 else 'alta',
                    'mensaje': f'Stock bajo: {producto.stock_actual} unidades (mínimo: {producto.stock_minimo})'
                })
            
            # Alertas de vencimiento
            if producto.fecha_vencimiento:
                dias_para_vencer = (producto.fecha_vencimiento - hoy).days
                
                if dias_para_vencer < 0:
                    alertas['vencidos'].append({
                        'producto': producto.to_dict(),
                        'severidad': 'critica',
                        'mensaje': f'Producto VENCIDO desde hace {abs(dias_para_vencer)} días'
                    })
                elif dias_para_vencer <= 30:
                    alertas['por_vencer_30'].append({
                        'producto': producto.to_dict(),
                        'severidad': 'alta',
                        'mensaje': f'Vence en {dias_para_vencer} días'
                    })
                elif dias_para_vencer <= 60:
                    alertas['por_vencer_60'].append({
                        'producto': producto.to_dict(),
                        'severidad': 'media',
                        'mensaje': f'Vence en {dias_para_vencer} días'
                    })
        
        return alertas
    
    @staticmethod
    def obtener_productos_reorden():
        """
        Obtiene lista de productos que necesitan reorden.
        """
        productos = ProductoFarmacia.query.filter(
            ProductoFarmacia.activo == True,
            ProductoFarmacia.stock_actual <= ProductoFarmacia.stock_minimo
        ).all()
        
        return [p.to_dict(incluir_relaciones=True) for p in productos]
    
    @staticmethod
    def dispensar_producto(producto_id, cantidad, receta_id=None, usuario_id=None):
        """
        Dispensa producto de farmacia.
        Valida stock y receta si es requerida.
        """
        producto = ProductoFarmacia.query.get(producto_id)
        
        if not producto:
            raise ValueError('Producto no encontrado')
        
        if not producto.activo:
            raise ValueError('Producto inactivo')
        
        # Validar si requiere receta
        if producto.requiere_receta and not receta_id:
            raise ValueError('Este producto requiere receta médica')
        
        # Validar receta activa
        if receta_id:
            receta = Receta.query.get(receta_id)
            if not receta or not receta.activa:
                raise ValueError('Receta inválida o inactiva')
        
        # Validar stock suficiente
        if not producto.tiene_stock_suficiente(cantidad):
            raise ValueError(f'Stock insuficiente. Disponible: {producto.stock_actual}')
        
        # Registrar movimiento de salida
        movimiento = MovimientoInventario.registrar_salida(
            producto=producto,
            cantidad=cantidad,
            motivo='Dispensación',
            referencia_id=receta_id,
            referencia_tipo='receta',
            usuario_id=usuario_id
        )
        
        db.session.add(movimiento)
        db.session.commit()
        
        return {
            'producto': producto.to_dict(),
            'movimiento': movimiento.to_dict()
        }
    
    @staticmethod
    def obtener_kardex(producto_id, fecha_inicio=None, fecha_fin=None):
        """
        Obtiene el kardex (historial de movimientos) de un producto.
        """
        query = MovimientoInventario.query.filter_by(producto_id=producto_id)
        
        if fecha_inicio:
            query = query.filter(MovimientoInventario.fecha_movimiento >= fecha_inicio)
        
        if fecha_fin:
            query = query.filter(MovimientoInventario.fecha_movimiento <= fecha_fin)
        
        movimientos = query.order_by(MovimientoInventario.fecha_movimiento.desc()).all()
        
        return [m.to_dict(incluir_relaciones=True) for m in movimientos]
    
    @staticmethod
    def ajustar_inventario(producto_id, stock_nuevo, motivo, usuario_id=None):
        """
        Ajusta el inventario de un producto (corrección de stock).
        """
        producto = ProductoFarmacia.query.get(producto_id)
        
        if not producto:
            raise ValueError('Producto no encontrado')
        
        movimiento = MovimientoInventario.registrar_ajuste(
            producto=producto,
            cantidad_nueva=stock_nuevo,
            motivo=motivo,
            usuario_id=usuario_id
        )
        
        db.session.add(movimiento)
        db.session.commit()
        
        return {
            'producto': producto.to_dict(),
            'movimiento': movimiento.to_dict()
        }
    
    @staticmethod
    def buscar_productos(query, tipo_producto=None, solo_con_stock=False):
        """
        Búsqueda predictiva de productos.
        """
        search = ProductoFarmacia.query.filter_by(activo=True)
        
        if query:
            search = search.filter(
                or_(
                    ProductoFarmacia.nombre_generico.ilike(f'%{query}%'),
                    ProductoFarmacia.nombre_comercial.ilike(f'%{query}%'),
                    ProductoFarmacia.codigo_interno.ilike(f'%{query}%')
                )
            )
        
        if tipo_producto:
            search = search.filter_by(tipo_producto=tipo_producto)
        
        if solo_con_stock:
            search = search.filter(ProductoFarmacia.stock_actual > 0)
        
        productos = search.limit(20).all()
        
        return [p.to_dict(incluir_relaciones=True) for p in productos]
    
    @staticmethod
    def obtener_inventario_valorizado():
        """
        Calcula el valor total del inventario actual.
        """
        productos = ProductoFarmacia.query.filter_by(activo=True).all()
        
        total_costo = 0
        total_venta = 0
        
        for producto in productos:
            if producto.precio_compra:
                total_costo += float(producto.precio_compra) * producto.stock_actual
            if producto.precio_venta:
                total_venta += float(producto.precio_venta) * producto.stock_actual
        
        return {
            'total_productos': len(productos),
            'valor_costo': round(total_costo, 2),
            'valor_venta': round(total_venta, 2),
            'utilidad_potencial': round(total_venta - total_costo, 2)
        }
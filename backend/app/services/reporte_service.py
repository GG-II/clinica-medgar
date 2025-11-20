"""
Servicio para generación de reportes y estadísticas.
Incluye: reportes operativos, financieros, inventario
"""

from app.extensions import db
from app.models import (
    Paciente, Cita, Hospitalizacion, ProductoFarmacia,
    Factura, MovimientoCaja, Caja, Compra
)
from sqlalchemy import func, extract
from datetime import datetime, timedelta

class ReporteService:
    """Servicio para generación de reportes"""
    
    @staticmethod
    def reporte_pacientes_atendidos(fecha_inicio, fecha_fin, medico_id=None):
        """
        Reporte de pacientes atendidos en un período.
        """
        query = Cita.query.filter(
            Cita.fecha_hora.between(fecha_inicio, fecha_fin),
            Cita.estado.in_(['completada', 'en_curso'])
        )
        
        if medico_id:
            query = query.filter_by(medico_id=medico_id)
        
        citas = query.all()
        
        # Estadísticas
        total_citas = len(citas)
        pacientes_unicos = len(set([cita.paciente_id for cita in citas]))
        
        # Por tipo de cita
        por_tipo = db.session.query(
            Cita.tipo_cita_id,
            func.count(Cita.id)
        ).filter(
            Cita.fecha_hora.between(fecha_inicio, fecha_fin),
            Cita.estado.in_(['completada', 'en_curso'])
        ).group_by(Cita.tipo_cita_id).all()
        
        return {
            'periodo': {
                'inicio': fecha_inicio.isoformat(),
                'fin': fecha_fin.isoformat()
            },
            'total_citas': total_citas,
            'pacientes_unicos': pacientes_unicos,
            'por_tipo_cita': [
                {'tipo_cita_id': tipo, 'cantidad': cantidad}
                for tipo, cantidad in por_tipo
            ]
        }
    
    @staticmethod
    def reporte_ocupacion_hospitalaria(fecha_inicio, fecha_fin):
        """
        Reporte de ocupación de camas hospitalarias.
        """
        hospitalizaciones = Hospitalizacion.query.filter(
            Hospitalizacion.fecha_ingreso.between(fecha_inicio, fecha_fin)
        ).all()
        
        total_ingresos = len(hospitalizaciones)
        total_egresos = len([h for h in hospitalizaciones if h.estado == 'egresado'])
        actualmente_hospitalizados = len([h for h in hospitalizaciones if h.estado == 'activo'])
        
        # Promedio días de estancia
        dias_estancia = [h.calcular_dias_estancia() for h in hospitalizaciones if h.estado == 'egresado']
        promedio_estancia = sum(dias_estancia) / len(dias_estancia) if dias_estancia else 0
        
        return {
            'periodo': {
                'inicio': fecha_inicio.isoformat(),
                'fin': fecha_fin.isoformat()
            },
            'total_ingresos': total_ingresos,
            'total_egresos': total_egresos,
            'actualmente_hospitalizados': actualmente_hospitalizados,
            'promedio_dias_estancia': round(promedio_estancia, 1)
        }
    
    @staticmethod
    def reporte_ingresos_egresos(fecha_inicio, fecha_fin):
        """
        Reporte de ingresos y egresos de caja.
        """
        # Cajas en el período
        cajas = Caja.query.filter(
            Caja.fecha_apertura.between(fecha_inicio, fecha_fin)
        ).all()
        
        total_ingresos = sum([float(caja.total_ingresos or 0) for caja in cajas])
        total_egresos = sum([float(caja.total_egresos or 0) for caja in cajas])
        
        # Ingresos por categoría
        ingresos_categoria = db.session.query(
            MovimientoCaja.categoria,
            func.sum(MovimientoCaja.monto)
        ).join(Caja).filter(
            Caja.fecha_apertura.between(fecha_inicio, fecha_fin),
            MovimientoCaja.tipo == 'ingreso'
        ).group_by(MovimientoCaja.categoria).all()
        
        # Egresos por categoría
        egresos_categoria = db.session.query(
            MovimientoCaja.categoria,
            func.sum(MovimientoCaja.monto)
        ).join(Caja).filter(
            Caja.fecha_apertura.between(fecha_inicio, fecha_fin),
            MovimientoCaja.tipo == 'egreso'
        ).group_by(MovimientoCaja.categoria).all()
        
        return {
            'periodo': {
                'inicio': fecha_inicio.isoformat(),
                'fin': fecha_fin.isoformat()
            },
            'total_ingresos': round(total_ingresos, 2),
            'total_egresos': round(total_egresos, 2),
            'utilidad': round(total_ingresos - total_egresos, 2),
            'ingresos_por_categoria': [
                {'categoria': cat, 'monto': float(monto)}
                for cat, monto in ingresos_categoria
            ],
            'egresos_por_categoria': [
                {'categoria': cat, 'monto': float(monto)}
                for cat, monto in egresos_categoria
            ]
        }
    
    @staticmethod
    def reporte_facturacion(fecha_inicio, fecha_fin):
        """
        Reporte de facturación del período.
        """
        facturas = Factura.query.filter(
            Factura.fecha_emision.between(fecha_inicio, fecha_fin)
        ).all()
        
        total_facturado = sum([float(f.total) for f in facturas])
        total_pagadas = sum([float(f.total) for f in facturas if f.estado == 'pagada'])
        total_pendientes = sum([float(f.total) for f in facturas if f.estado in ['pendiente', 'credito']])
        
        # Por forma de pago
        por_forma_pago = db.session.query(
            Factura.forma_pago,
            func.count(Factura.id),
            func.sum(Factura.total)
        ).filter(
            Factura.fecha_emision.between(fecha_inicio, fecha_fin)
        ).group_by(Factura.forma_pago).all()
        
        return {
            'periodo': {
                'inicio': fecha_inicio.isoformat(),
                'fin': fecha_fin.isoformat()
            },
            'total_facturas': len(facturas),
            'total_facturado': round(total_facturado, 2),
            'total_pagadas': round(total_pagadas, 2),
            'total_pendientes': round(total_pendientes, 2),
            'por_forma_pago': [
                {
                    'forma_pago': forma,
                    'cantidad': cantidad,
                    'monto': float(monto)
                }
                for forma, cantidad, monto in por_forma_pago
            ]
        }
    
    @staticmethod
    def reporte_inventario():
        """
        Reporte de estado actual del inventario.
        """
        productos = ProductoFarmacia.query.filter_by(activo=True).all()
        
        total_productos = len(productos)
        valor_costo = sum([
            float(p.precio_compra or 0) * p.stock_actual 
            for p in productos
        ])
        valor_venta = sum([
            float(p.precio_venta or 0) * p.stock_actual 
            for p in productos
        ])
        
        # Productos con stock bajo
        stock_bajo = len([p for p in productos if p.stock_actual <= p.stock_minimo])
        
        # Productos próximos a vencer (30 días)
        hoy = datetime.now().date()
        proximos_vencer = len([
            p for p in productos 
            if p.fecha_vencimiento and (p.fecha_vencimiento - hoy).days <= 30
        ])
        
        return {
            'total_productos': total_productos,
            'valor_inventario_costo': round(valor_costo, 2),
            'valor_inventario_venta': round(valor_venta, 2),
            'utilidad_potencial': round(valor_venta - valor_costo, 2),
            'alertas': {
                'stock_bajo': stock_bajo,
                'proximos_vencer': proximos_vencer
            }
        }
    
    @staticmethod
    def reporte_compras(fecha_inicio, fecha_fin):
        """
        Reporte de compras realizadas.
        """
        compras = Compra.query.filter(
            Compra.fecha_compra.between(fecha_inicio, fecha_fin)
        ).all()
        
        total_compras = len(compras)
        total_invertido = sum([float(c.total) for c in compras])
        
        # Por proveedor
        por_proveedor = db.session.query(
            Compra.proveedor_id,
            func.count(Compra.id),
            func.sum(Compra.total)
        ).filter(
            Compra.fecha_compra.between(fecha_inicio, fecha_fin)
        ).group_by(Compra.proveedor_id).all()
        
        return {
            'periodo': {
                'inicio': fecha_inicio.isoformat(),
                'fin': fecha_fin.isoformat()
            },
            'total_compras': total_compras,
            'total_invertido': round(total_invertido, 2),
            'por_proveedor': [
                {
                    'proveedor_id': prov_id,
                    'cantidad_compras': cantidad,
                    'monto_total': float(monto)
                }
                for prov_id, cantidad, monto in por_proveedor
            ]
        }
    
    @staticmethod
    def dashboard_general():
        """
        Datos para dashboard principal (resumen general).
        """
        hoy = datetime.now().date()
        inicio_mes = hoy.replace(day=1)
        
        # Pacientes atendidos hoy
        citas_hoy = Cita.query.filter(
            func.date(Cita.fecha_hora) == hoy,
            Cita.estado.in_(['completada', 'en_curso'])
        ).count()
        
        # Pacientes atendidos este mes
        citas_mes = Cita.query.filter(
            func.date(Cita.fecha_hora) >= inicio_mes,
            Cita.estado.in_(['completada', 'en_curso'])
        ).count()
        
        # Pacientes hospitalizados
        hospitalizados = Hospitalizacion.query.filter_by(estado='activo').count()
        
        # Ingresos del día
        caja_hoy = Caja.query.filter(
            func.date(Caja.fecha_apertura) == hoy
        ).first()
        ingresos_hoy = float(caja_hoy.total_ingresos or 0) if caja_hoy else 0
        
        # Ingresos del mes
        cajas_mes = Caja.query.filter(
            Caja.fecha_apertura >= inicio_mes
        ).all()
        ingresos_mes = sum([float(c.total_ingresos or 0) for c in cajas_mes])
        
        return {
            'fecha': hoy.isoformat(),
            'pacientes_hoy': citas_hoy,
            'pacientes_mes': citas_mes,
            'pacientes_hospitalizados': hospitalizados,
            'ingresos_hoy': round(ingresos_hoy, 2),
            'ingresos_mes': round(ingresos_mes, 2)
        }
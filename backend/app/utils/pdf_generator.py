"""
Utilidad para generación de PDFs de reportes.
Usa ReportLab para crear documentos PDF profesionales.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from datetime import datetime

class PDFGenerator:
    """Generador de PDFs para reportes del sistema"""
    
    @staticmethod
    def generar_reporte_arqueo_caja(caja):
        """
        Genera PDF de arqueo de caja.
        
        Args:
            caja: Objeto Caja con sus movimientos
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado
        style_title = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#8B5CF6'),  # Lila
            alignment=TA_CENTER
        )
        
        # Título
        story.append(Paragraph("CLÍNICA MÉDICA DRA. ESTEPHANNY GARCÍA", style_title))
        story.append(Paragraph("Reporte de Arqueo de Caja", styles['Heading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Información de la caja
        info_data = [
            ['Fecha Apertura:', caja.fecha_apertura.strftime('%d/%m/%Y %H:%M')],
            ['Fecha Cierre:', caja.fecha_cierre.strftime('%d/%m/%Y %H:%M') if caja.fecha_cierre else 'No cerrada'],
            ['Usuario:', caja.usuario.nombre_completo],
            ['Estado:', caja.estado.upper()]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E9D5FF')),  # Lila claro
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Resumen financiero
        story.append(Paragraph("Resumen Financiero", styles['Heading3']))
        
        resumen_data = [
            ['Concepto', 'Monto (Q)'],
            ['Monto Inicial', f'{float(caja.monto_inicial):,.2f}'],
            ['Total Ingresos', f'{float(caja.total_ingresos or 0):,.2f}'],
            ['Total Egresos', f'{float(caja.total_egresos or 0):,.2f}'],
            ['Monto Esperado', f'{float(caja.calcular_monto_esperado()):,.2f}'],
            ['Efectivo Contado', f'{float(caja.efectivo_contado or 0):,.2f}'],
            ['Diferencia', f'{float(caja.diferencia or 0):,.2f}']
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FEF3C7'))  # Amarillo claro para diferencia
        ]))
        
        story.append(resumen_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Detalle de movimientos
        story.append(Paragraph("Detalle de Movimientos", styles['Heading3']))
        
        movimientos_data = [['Hora', 'Tipo', 'Categoría', 'Concepto', 'Monto (Q)']]
        
        for mov in caja.movimientos.order_by('fecha_movimiento'):
            movimientos_data.append([
                mov.fecha_movimiento.strftime('%H:%M'),
                mov.tipo.upper(),
                mov.categoria,
                mov.concepto[:40] + '...' if len(mov.concepto) > 40 else mov.concepto,
                f'{float(mov.monto):,.2f}'
            ])
        
        if len(movimientos_data) > 1:
            movimientos_table = Table(movimientos_data, colWidths=[0.8*inch, 0.8*inch, 1.2*inch, 2.5*inch, 1*inch])
            movimientos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F4F6')])
            ]))
            story.append(movimientos_table)
        else:
            story.append(Paragraph("No hay movimientos registrados", styles['Normal']))
        
        # Pie de página
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_reporte_inventario(productos, alertas):
        """
        Genera PDF de reporte de inventario.
        
        Args:
            productos: Lista de productos
            alertas: Diccionario con alertas
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        style_title = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#8B5CF6'),
            alignment=TA_CENTER
        )
        
        # Título
        story.append(Paragraph("CLÍNICA MÉDICA DRA. ESTEPHANNY GARCÍA", style_title))
        story.append(Paragraph("Reporte de Inventario", styles['Heading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Resumen de alertas
        story.append(Paragraph("Resumen de Alertas", styles['Heading3']))
        
        alertas_data = [
            ['Tipo de Alerta', 'Cantidad'],
            ['Stock Mínimo', str(len(alertas.get('stock_minimo', [])))],
            ['Productos Vencidos', str(len(alertas.get('vencidos', [])))],
            ['Por Vencer (30 días)', str(len(alertas.get('por_vencer_30', [])))],
        ]
        
        alertas_table = Table(alertas_data, colWidths=[3*inch, 2*inch])
        alertas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(alertas_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Listado de productos
        story.append(Paragraph("Listado de Productos", styles['Heading3']))
        
        productos_data = [['Código', 'Producto', 'Stock', 'P. Venta', 'Total']]
        
        total_valor = 0
        for prod in productos[:50]:  # Primeros 50 productos
            valor_total = float(prod.get('precio_venta', 0) or 0) * prod.get('stock_actual', 0)
            total_valor += valor_total
            
            productos_data.append([
                prod.get('codigo_interno', ''),
                prod.get('nombre_generico', '')[:30],
                str(prod.get('stock_actual', 0)),
                f"Q{prod.get('precio_venta', 0):,.2f}",
                f"Q{valor_total:,.2f}"
            ])
        
        productos_data.append(['', '', '', 'TOTAL:', f'Q{total_valor:,.2f}'])
        
        productos_table = Table(productos_data, colWidths=[1*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
        productos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F3F4F6')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FEF3C7'))
        ]))
        
        story.append(productos_table)
        
        # Pie de página
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        
        if len(productos) > 50:
            story.append(Paragraph(f"Mostrando 50 de {len(productos)} productos", styles['Normal']))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
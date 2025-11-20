"""
Servicio para generación de recetas médicas.
Incluye: creación, validación de alergias, generación de PDF
"""

from app.extensions import db
from app.models import Receta, RecetaDetalle, Medicamento, Paciente, Usuario, Antecedente
from datetime import datetime
from io import BytesIO

# ReportLab para PDFs
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class RecetaService:
    """Servicio para gestión de recetas médicas"""
    
    @staticmethod
    def crear_receta(paciente_id, medico_id, diagnostico, indicaciones_generales, 
                     medicamentos_lista, consulta_id=None):
        """
        Crea una nueva receta médica con sus medicamentos.
        
        Args:
            paciente_id: ID del paciente
            medico_id: ID del médico
            diagnostico: Diagnóstico del paciente
            indicaciones_generales: Indicaciones adicionales
            medicamentos_lista: Lista de diccionarios con medicamento_id, dosis, frecuencia, etc.
            consulta_id: ID de la consulta (opcional)
        """
        # Validar alergias
        alertas = RecetaService._validar_alergias(paciente_id, medicamentos_lista)
        
        # Crear receta
        receta = Receta(
            paciente_id=paciente_id,
            medico_id=medico_id,
            consulta_id=consulta_id,
            fecha_emision=datetime.now().date(),
            indicaciones_generales=indicaciones_generales,
            diagnostico=diagnostico,
            activa=True
        )
        
        db.session.add(receta)
        db.session.flush()  # Para obtener el ID de la receta
        
        # Agregar detalles
        for med_data in medicamentos_lista:
            detalle = RecetaDetalle(
                receta_id=receta.id,
                medicamento_id=med_data['medicamento_id'],
                dosis=med_data['dosis'],
                frecuencia=med_data['frecuencia'],
                duracion=med_data.get('duracion'),
                via_administracion=med_data.get('via_administracion'),
                indicaciones_especificas=med_data.get('indicaciones_especificas'),
                cantidad_prescrita=med_data.get('cantidad_prescrita')
            )
            db.session.add(detalle)
        
        db.session.commit()
        
        return {
            'receta': receta.to_dict(incluir_relaciones=True),
            'alertas': alertas
        }
    
    @staticmethod
    def _validar_alergias(paciente_id, medicamentos_lista):
        """
        Valida si algún medicamento tiene conflicto con las alergias del paciente.
        """
        alertas = []
        
        # Obtener alergias del paciente
        alergias = Antecedente.query.filter_by(
            paciente_id=paciente_id,
            tipo='alergicos',
            activo=True
        ).all()
        
        if not alergias:
            return alertas
        
        # Verificar cada medicamento
        for med_data in medicamentos_lista:
            medicamento = Medicamento.query.get(med_data['medicamento_id'])
            
            if medicamento:
                for alergia in alergias:
                    # Buscar coincidencias (básico)
                    if (alergia.descripcion.lower() in medicamento.nombre_generico.lower() or
                        alergia.descripcion.lower() in (medicamento.nombre_comercial or '').lower()):
                        
                        alertas.append({
                            'tipo': 'alergia',
                            'severidad': 'alta',
                            'medicamento': medicamento.nombre_generico,
                            'mensaje': f'ALERTA: Paciente tiene alergia registrada a {alergia.descripcion}'
                        })
        
        return alertas
    
    @staticmethod
    def generar_pdf(receta_id):
        """
        Genera PDF de la receta médica.
        """
        receta = Receta.query.get(receta_id)
        
        if not receta:
            raise ValueError('Receta no encontrada')
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        style_title = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#8B5CF6'),  # Lila
            alignment=TA_CENTER,
            spaceAfter=10
        )
        
        style_subtitle = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        style_rx = ParagraphStyle(
            'RxStyle',
            parent=styles['Heading2'],
            fontSize=24,
            textColor=colors.HexColor('#8B5CF6'),
            spaceAfter=10
        )
        
        # Encabezado
        story.append(Paragraph("CLÍNICA FAMILIAR MEDGAR", style_title))
        story.append(Paragraph("Dirección de la clínica • Tel: (502) 0000-0000", style_subtitle))
        story.append(Spacer(1, 0.2*inch))
        
        # Información del médico
        medico = receta.medico
        info_medico = f"<b>Dr(a). {medico.nombre_completo}</b><br/>"
        info_medico += f"Registro Médico: [Número]<br/>"
        
        story.append(Paragraph(info_medico, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Información del paciente
        paciente = receta.paciente
        info_data = [
            ['Fecha:', receta.fecha_emision.strftime('%d/%m/%Y')],
            ['Paciente:', paciente.nombre_completo],
            ['Edad:', f'{paciente.calcular_edad()} años'],
            ['DPI:', paciente.dpi or 'No especificado']
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Símbolo Rx
        story.append(Paragraph("℞", style_rx))
        story.append(Spacer(1, 0.1*inch))
        
        # Medicamentos
        contador = 1
        for detalle in receta.detalles:
            med = detalle.medicamento
            
            med_text = f"<b>{contador}. {med.nombre_generico}"
            if med.nombre_comercial:
                med_text += f" ({med.nombre_comercial})"
            med_text += f"</b><br/>"
            med_text += f"   {med.presentacion or ''} {med.concentracion or ''}<br/>"
            med_text += f"   <b>Dosis:</b> {detalle.dosis}<br/>"
            med_text += f"   <b>Frecuencia:</b> {detalle.frecuencia}<br/>"
            
            if detalle.duracion:
                med_text += f"   <b>Duración:</b> {detalle.duracion}<br/>"
            
            if detalle.via_administracion:
                med_text += f"   <b>Vía:</b> {detalle.via_administracion}<br/>"
            
            if detalle.indicaciones_especificas:
                med_text += f"   <i>{detalle.indicaciones_especificas}</i><br/>"
            
            story.append(Paragraph(med_text, styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
            contador += 1
        
        # Indicaciones generales
        if receta.indicaciones_generales:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("<b>INDICACIONES GENERALES:</b>", styles['Heading3']))
            story.append(Paragraph(receta.indicaciones_generales, styles['Normal']))
        
        # Espacio para firma
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("_" * 40, styles['Normal']))
        story.append(Paragraph("Firma y sello del médico", styles['Normal']))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def desactivar_receta(receta_id, motivo=None):
        """Desactiva una receta (ya no se puede dispensar)"""
        receta = Receta.query.get(receta_id)
        
        if not receta:
            raise ValueError('Receta no encontrada')
        
        receta.activa = False
        
        if motivo:
            receta.indicaciones_generales = f"{receta.indicaciones_generales}\n\nDESACTIVADA: {motivo}"
        
        db.session.commit()
        
        return receta.to_dict()
    
    @staticmethod
    def obtener_recetas_paciente(paciente_id, solo_activas=False):
        """Obtiene historial de recetas de un paciente"""
        query = Receta.query.filter_by(paciente_id=paciente_id)
        
        if solo_activas:
            query = query.filter_by(activa=True)
        
        recetas = query.order_by(Receta.fecha_emision.desc()).all()
        
        return [r.to_dict(incluir_relaciones=True) for r in recetas]
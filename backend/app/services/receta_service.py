"""
Servicio de Recetas
Lógica para generación de recetas médicas en PDF
"""
from datetime import datetime, date
from app.extensions import db
from app.models import Receta, RecetaDetalle, Medicamento, Paciente, Usuario
from app.models.auditoria import LogAuditoria
import os

# Importar WeasyPrint para PDF (opcional)
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_DISPONIBLE = True
except ImportError:
    WEASYPRINT_DISPONIBLE = False
    print("⚠️  WeasyPrint no está instalado. Instalar con: pip install weasyprint")


class RecetaService:
    """Servicio para gestión de recetas médicas"""
    
    @staticmethod
    def crear_receta(data, usuario_id):
        """
        Crea una nueva receta con sus medicamentos
        
        Args:
            data: {
                'paciente_id': int,
                'medico_id': int,
                'consulta_id': int (opcional),
                'diagnostico': str,
                'indicaciones_generales': str,
                'medicamentos': [
                    {
                        'medicamento_id': int,
                        'dosis': str,
                        'frecuencia': str,
                        'duracion': str,
                        'via_administracion': str,
                        'indicaciones_especificas': str,
                        'cantidad_prescrita': int
                    }
                ]
            }
            usuario_id: ID del usuario que crea
        
        Returns:
            (Receta, str): (receta, error)
        """
        try:
            # Validar paciente y médico
            paciente = Paciente.query.get(data['paciente_id'])
            if not paciente:
                return None, "Paciente no encontrado"
            
            medico = Usuario.query.get(data['medico_id'])
            if not medico or medico.rol != 'medico':
                return None, "Médico no válido"
            
            # Crear receta
            receta = Receta(
                paciente_id=data['paciente_id'],
                medico_id=data['medico_id'],
                consulta_id=data.get('consulta_id'),
                fecha_emision=date.today(),
                diagnostico=data.get('diagnostico'),
                indicaciones_generales=data.get('indicaciones_generales'),
                activa=True
            )
            
            db.session.add(receta)
            db.session.flush()  # Para obtener el ID
            
            # Agregar medicamentos
            if 'medicamentos' not in data or not data['medicamentos']:
                return None, "Debe incluir al menos un medicamento"
            
            for med_data in data['medicamentos']:
                medicamento = Medicamento.query.get(med_data['medicamento_id'])
                if not medicamento:
                    db.session.rollback()
                    return None, f"Medicamento {med_data['medicamento_id']} no encontrado"
                
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
            
            # Validar alergias
            alertas = receta.validar_alergias()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='crear_receta',
                tabla_afectada='recetas',
                registro_id=receta.id,
                detalles=f"Receta creada para paciente {paciente.nombre_completo}"
            )
            db.session.add(log)
            db.session.commit()
            
            # Retornar receta con alertas si las hay
            if alertas:
                return receta, f"⚠️ ALERTAS DE ALERGIAS: {alertas}"
            
            return receta, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def generar_pdf(receta_id):
        """
        Genera PDF de la receta
        
        Returns:
            (bytes, str): (pdf_bytes, error)
        """
        try:
            receta = Receta.query.get(receta_id)
            if not receta:
                return None, "Receta no encontrada"
            
            # Generar HTML de la receta
            html_content = RecetaService._generar_html(receta)
            
            if not WEASYPRINT_DISPONIBLE:
                # Modo desarrollo: retornar HTML
                return html_content.encode('utf-8'), None
            
            # Generar PDF con WeasyPrint
            pdf = HTML(string=html_content).write_pdf()
            
            return pdf, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def _generar_html(receta):
        """
        Genera HTML de la receta con diseño profesional
        """
        paciente = receta.paciente
        medico = receta.medico
        
        # Cabecera
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: letter;
                    margin: 2cm;
                }}
                body {{
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    line-height: 1.6;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #B8A9D4;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .clinic-name {{
                    color: #B8A9D4;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .doctor-info {{
                    font-size: 14px;
                    color: #666;
                }}
                .section {{
                    margin-bottom: 25px;
                }}
                .section-title {{
                    background-color: #F5F3F9;
                    color: #6B5B95;
                    padding: 8px 12px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    border-left: 4px solid #B8A9D4;
                }}
                .patient-data {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 10px;
                }}
                .data-row {{
                    margin: 5px 0;
                }}
                .label {{
                    font-weight: bold;
                    color: #6B5B95;
                }}
                .rx-symbol {{
                    font-size: 48px;
                    color: #B8A9D4;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .medicamento {{
                    margin-bottom: 20px;
                    padding: 15px;
                    background-color: #FAFAFA;
                    border-left: 3px solid #B8A9D4;
                }}
                .med-nombre {{
                    font-size: 16px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 8px;
                }}
                .med-detalle {{
                    margin: 4px 0;
                    padding-left: 15px;
                }}
                .indicaciones {{
                    margin-top: 30px;
                    padding: 15px;
                    background-color: #F5F3F9;
                    border-radius: 5px;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    border-top: 2px solid #E0E0E0;
                    padding-top: 20px;
                }}
                .firma {{
                    margin-top: 60px;
                    text-align: center;
                }}
                .firma-linea {{
                    border-top: 2px solid #333;
                    width: 250px;
                    margin: 0 auto 10px;
                }}
            </style>
        </head>
        <body>
            <!-- Cabecera -->
            <div class="header">
                <div class="clinic-name">CLÍNICA MÉDICA MEDGAR</div>
                <div class="doctor-info">
                    {medico.nombre_completo}<br>
                    Registro Médico: {medico.id}<br>
                    Especialidad: Medicina General
                </div>
            </div>
            
            <!-- Fecha -->
            <div style="text-align: right; margin-bottom: 20px;">
                <strong>Fecha:</strong> {receta.fecha_emision.strftime('%d de %B de %Y')}
            </div>
            
            <!-- Datos del Paciente -->
            <div class="section">
                <div class="section-title">DATOS DEL PACIENTE</div>
                <div class="data-row">
                    <span class="label">Nombre:</span> {paciente.nombre_completo}
                </div>
                <div class="data-row">
                    <span class="label">Edad:</span> {paciente.edad} años
                </div>
                <div class="data-row">
                    <span class="label">DPI:</span> {paciente.dpi or 'N/A'}
                </div>
            </div>
            
            <!-- Diagnóstico -->
            {"<div class='section'><div class='section-title'>DIAGNÓSTICO</div><p>" + receta.diagnostico + "</p></div>" if receta.diagnostico else ""}
            
            <!-- Símbolo Rx -->
            <div class="rx-symbol">℞</div>
            
            <!-- Medicamentos -->
            <div class="section">
        """
        
        # Agregar cada medicamento
        for i, detalle in enumerate(receta.medicamentos, 1):
            med = detalle.medicamento
            html += f"""
                <div class="medicamento">
                    <div class="med-nombre">{i}. {med.nombre_generico.upper()}</div>
                    <div class="med-detalle"><strong>Presentación:</strong> {med.presentacion} {med.concentracion}</div>
                    <div class="med-detalle"><strong>Dosis:</strong> {detalle.dosis}</div>
                    <div class="med-detalle"><strong>Frecuencia:</strong> {detalle.frecuencia}</div>
                    {"<div class='med-detalle'><strong>Duración:</strong> " + detalle.duracion + "</div>" if detalle.duracion else ""}
                    {"<div class='med-detalle'><strong>Vía:</strong> " + detalle.via_administracion + "</div>" if detalle.via_administracion else ""}
                    {"<div class='med-detalle' style='font-style: italic; margin-top: 5px;'>" + detalle.indicaciones_especificas + "</div>" if detalle.indicaciones_especificas else ""}
                </div>
            """
        
        html += """
            </div>
        """
        
        # Indicaciones generales
        if receta.indicaciones_generales:
            html += f"""
                <div class="indicaciones">
                    <div class="section-title">INDICACIONES GENERALES</div>
                    <p>{receta.indicaciones_generales}</p>
                </div>
            """
        
        # Firma
        html += f"""
            <div class="firma">
                <div class="firma-linea"></div>
                <strong>{medico.nombre_completo}</strong><br>
                Registro Médico: {medico.id}
            </div>
            
            <div class="footer">
                <small>Esta receta es válida por 30 días desde su emisión</small>
            </div>
        </body>
        </html>
        """
        
        return html
    
    @staticmethod
    def desactivar_receta(receta_id, usuario_id):
        """
        Desactiva una receta (ya no se puede dispensar)
        """
        try:
            receta = Receta.query.get(receta_id)
            if not receta:
                return False, "Receta no encontrada"
            
            receta.activa = False
            db.session.commit()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='desactivar_receta',
                tabla_afectada='recetas',
                registro_id=receta.id,
                detalles=f"Receta {receta_id} desactivada"
            )
            db.session.add(log)
            db.session.commit()
            
            return True, "Receta desactivada"
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def obtener_recetas_paciente(paciente_id, solo_activas=False):
        """Obtiene todas las recetas de un paciente"""
        query = Receta.query.filter_by(paciente_id=paciente_id)
        
        if solo_activas:
            query = query.filter_by(activa=True)
        
        return query.order_by(Receta.fecha_emision.desc()).all()
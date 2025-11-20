"""
Servicio de Recordatorios
Lógica para envío de recordatorios por WhatsApp/SMS usando Twilio
"""
from datetime import datetime, timedelta
from app.extensions import db
from app.models import Recordatorio, Cita
from app.models.auditoria import LogAuditoria
import os

# Importar Twilio (opcional, solo si está instalado)
try:
    from twilio.rest import Client
    TWILIO_DISPONIBLE = True
except ImportError:
    TWILIO_DISPONIBLE = False
    print("⚠️  Twilio no está instalado. Instalar con: pip install twilio")


class RecordatorioService:
    """Servicio para gestión de recordatorios"""
    
    def __init__(self):
        """Inicializar cliente de Twilio"""
        self.twilio_client = None
        self.twilio_phone = None
        self.twilio_whatsapp = None
        
        if TWILIO_DISPONIBLE:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            self.twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
            self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
            
            if account_sid and auth_token:
                try:
                    self.twilio_client = Client(account_sid, auth_token)
                except Exception as e:
                    print(f"❌ Error inicializando Twilio: {str(e)}")
    
    def crear_recordatorio(self, cita_id, tipo='whatsapp', dias_anticipacion=1):
        """
        Crea un recordatorio para una cita
        
        Args:
            cita_id: ID de la cita
            tipo: 'whatsapp', 'sms' o 'email'
            dias_anticipacion: Días antes de la cita (1 o 7)
        
        Returns:
            (Recordatorio, str): (recordatorio, error)
        """
        try:
            cita = Cita.query.get(cita_id)
            if not cita:
                return None, "Cita no encontrada"
            
            if not cita.paciente or not cita.paciente.telefono:
                return None, "Paciente no tiene teléfono registrado"
            
            # Calcular fecha de envío
            fecha_envio = cita.fecha_hora - timedelta(days=dias_anticipacion)
            
            # Generar mensaje
            mensaje = self._generar_mensaje(cita, dias_anticipacion)
            
            # Crear recordatorio
            recordatorio = Recordatorio(
                cita_id=cita_id,
                tipo=tipo,
                telefono_destinatario=cita.paciente.telefono,
                mensaje=mensaje,
                fecha_envio=fecha_envio,
                dias_anticipacion=dias_anticipacion,
                estado='pendiente'
            )
            
            db.session.add(recordatorio)
            db.session.commit()
            
            return recordatorio, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    def enviar_recordatorio(self, recordatorio_id, usuario_id=None):
        """
        Envía un recordatorio por WhatsApp o SMS
        
        Args:
            recordatorio_id: ID del recordatorio
            usuario_id: ID del usuario que ejecuta (para auditoría)
        
        Returns:
            (bool, str): (exitoso, mensaje)
        """
        try:
            recordatorio = Recordatorio.query.get(recordatorio_id)
            if not recordatorio:
                return False, "Recordatorio no encontrado"
            
            if recordatorio.estado == 'enviado':
                return False, "Recordatorio ya fue enviado"
            
            # Validar cliente Twilio
            if not self.twilio_client:
                # Modo simulación (desarrollo)
                recordatorio.estado = 'enviado'
                recordatorio.fecha_envio = datetime.utcnow()
                recordatorio.sid_twilio = 'SIM' + str(datetime.utcnow().timestamp())
                db.session.commit()
                
                print(f"📱 [SIMULADO] Recordatorio enviado:")
                print(f"   Tipo: {recordatorio.tipo}")
                print(f"   Destino: {recordatorio.telefono_destinatario}")
                print(f"   Mensaje: {recordatorio.mensaje}")
                
                return True, "Recordatorio enviado (modo simulación)"
            
            # Enviar real con Twilio
            try:
                if recordatorio.tipo == 'whatsapp':
                    resultado = self._enviar_whatsapp(recordatorio)
                elif recordatorio.tipo == 'sms':
                    resultado = self._enviar_sms(recordatorio)
                else:
                    return False, "Tipo de recordatorio no soportado"
                
                if resultado:
                    recordatorio.estado = 'enviado'
                    recordatorio.fecha_envio = datetime.utcnow()
                    recordatorio.sid_twilio = resultado
                    db.session.commit()
                    
                    # Auditoría
                    if usuario_id:
                        log = LogAuditoria(
                            usuario_id=usuario_id,
                            accion='enviar_recordatorio',
                            tabla_afectada='recordatorios',
                            registro_id=recordatorio.id,
                            detalles=f"Recordatorio {recordatorio.tipo} enviado a {recordatorio.telefono_destinatario}"
                        )
                        db.session.add(log)
                        db.session.commit()
                    
                    return True, "Recordatorio enviado exitosamente"
                else:
                    return False, "Error al enviar recordatorio"
                    
            except Exception as e:
                recordatorio.estado = 'fallido'
                recordatorio.error_mensaje = str(e)
                db.session.commit()
                return False, f"Error en envío: {str(e)}"
                
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def _enviar_whatsapp(self, recordatorio):
        """Envía mensaje por WhatsApp usando Twilio"""
        try:
            # Formatear número para WhatsApp
            numero_destino = recordatorio.telefono_destinatario
            if not numero_destino.startswith('whatsapp:'):
                # Formato Guatemala: +502 XXXXXXXX
                if not numero_destino.startswith('+'):
                    numero_destino = f"+502{numero_destino}"
                numero_destino = f"whatsapp:{numero_destino}"
            
            message = self.twilio_client.messages.create(
                from_=self.twilio_whatsapp,
                to=numero_destino,
                body=recordatorio.mensaje
            )
            
            return message.sid
            
        except Exception as e:
            print(f"❌ Error enviando WhatsApp: {str(e)}")
            raise e
    
    def _enviar_sms(self, recordatorio):
        """Envía mensaje por SMS usando Twilio"""
        try:
            # Formatear número para SMS
            numero_destino = recordatorio.telefono_destinatario
            if not numero_destino.startswith('+'):
                # Formato Guatemala: +502 XXXXXXXX
                numero_destino = f"+502{numero_destino}"
            
            message = self.twilio_client.messages.create(
                from_=self.twilio_phone,
                to=numero_destino,
                body=recordatorio.mensaje
            )
            
            return message.sid
            
        except Exception as e:
            print(f"❌ Error enviando SMS: {str(e)}")
            raise e
    
    def _generar_mensaje(self, cita, dias_anticipacion):
        """
        Genera el mensaje del recordatorio
        
        Template personalizable
        """
        nombre_paciente = cita.paciente.nombre_completo if cita.paciente else "Paciente"
        nombre_medico = cita.medico.nombre_completo if cita.medico else "Doctor"
        fecha = cita.fecha_hora.strftime('%d/%m/%Y')
        hora = cita.fecha_hora.strftime('%I:%M %p')
        
        if dias_anticipacion == 7:
            mensaje = (
                f"Hola {nombre_paciente},\n\n"
                f"Le recordamos su cita en Clínica Dra. García "
                f"el {fecha} a las {hora} con {nombre_medico}.\n\n"
                f"Por favor confirme su asistencia respondiendo SÍ.\n\n"
                f"¡Gracias!"
            )
        else:  # 1 día antes
            mensaje = (
                f"Hola {nombre_paciente},\n\n"
                f"Su cita es MAÑANA {fecha} a las {hora} con {nombre_medico}.\n\n"
                f"Por favor confirme respondiendo SÍ.\n\n"
                f"Clínica Dra. García"
            )
        
        return mensaje
    
    def procesar_respuesta(self, telefono, respuesta_texto):
        """
        Procesa respuesta del paciente (webhook de Twilio)
        
        Args:
            telefono: Número que responde
            respuesta_texto: Texto de la respuesta
        
        Returns:
            bool: True si se procesó correctamente
        """
        try:
            # Limpiar teléfono
            telefono_limpio = telefono.replace('whatsapp:', '').replace('+502', '')
            
            # Buscar recordatorio pendiente
            recordatorio = Recordatorio.query.filter(
                Recordatorio.telefono_destinatario.contains(telefono_limpio),
                Recordatorio.estado == 'enviado'
            ).order_by(Recordatorio.fecha_envio.desc()).first()
            
            if not recordatorio:
                return False
            
            # Procesar respuesta
            respuesta_lower = respuesta_texto.lower().strip()
            if respuesta_lower in ['si', 'sí', 'yes', 'confirmo', 'ok']:
                recordatorio.estado = 'confirmado'
                recordatorio.respuesta_paciente = respuesta_texto
                
                # Actualizar estado de la cita
                if recordatorio.cita:
                    recordatorio.cita.estado = 'confirmada'
                
                db.session.commit()
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error procesando respuesta: {str(e)}")
            return False
    
    @staticmethod
    def obtener_recordatorios_pendientes():
        """
        Obtiene recordatorios pendientes de envío
        Para ejecutar en cron job
        """
        ahora = datetime.utcnow()
        
        return Recordatorio.query.filter(
            Recordatorio.estado == 'pendiente',
            Recordatorio.fecha_envio <= ahora
        ).all()
    
    @staticmethod
    def crear_recordatorios_automaticos():
        """
        Crea recordatorios automáticos para citas próximas
        Ejecutar diariamente en cron job
        
        Crea 2 recordatorios por cita:
        - 7 días antes
        - 1 día antes
        """
        try:
            ahora = datetime.utcnow()
            
            # Buscar citas en los próximos 8 días sin recordatorios
            fecha_inicio = ahora
            fecha_fin = ahora + timedelta(days=8)
            
            citas = Cita.query.filter(
                Cita.fecha_hora.between(fecha_inicio, fecha_fin),
                Cita.estado.in_(['programada', 'confirmada'])
            ).all()
            
            servicio = RecordatorioService()
            recordatorios_creados = 0
            
            for cita in citas:
                # Verificar si ya tiene recordatorios
                tiene_recordatorio_7 = Recordatorio.query.filter(
                    Recordatorio.cita_id == cita.id,
                    Recordatorio.dias_anticipacion == 7
                ).first()
                
                tiene_recordatorio_1 = Recordatorio.query.filter(
                    Recordatorio.cita_id == cita.id,
                    Recordatorio.dias_anticipacion == 1
                ).first()
                
                # Crear recordatorio 7 días antes
                dias_para_cita = (cita.fecha_hora.date() - ahora.date()).days
                
                if not tiene_recordatorio_7 and dias_para_cita >= 7:
                    servicio.crear_recordatorio(cita.id, 'whatsapp', 7)
                    recordatorios_creados += 1
                
                # Crear recordatorio 1 día antes
                if not tiene_recordatorio_1 and dias_para_cita >= 1:
                    servicio.crear_recordatorio(cita.id, 'whatsapp', 1)
                    recordatorios_creados += 1
            
            return recordatorios_creados, None
            
        except Exception as e:
            return 0, str(e)
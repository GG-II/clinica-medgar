"""
Servicio de Citas
Lógica de negocio para gestión de citas médicas
"""
from datetime import datetime, timedelta, time
from sqlalchemy import and_, or_
from app.extensions import db
from app.models import Cita, TipoCita, Usuario, Paciente
from app.models.auditoria import LogAuditoria

class CitaService:
    """Servicio para gestión de citas"""
    
    @staticmethod
    def verificar_disponibilidad(medico_id, fecha_hora, duracion_minutos=20, excluir_cita_id=None):
        """
        Verifica si un médico está disponible en una fecha/hora específica
        
        Args:
            medico_id: ID del médico
            fecha_hora: datetime de la cita propuesta
            duracion_minutos: duración de la cita
            excluir_cita_id: ID de cita a excluir (para ediciones)
        
        Returns:
            (bool, str): (disponible, mensaje)
        """
        # Verificar que sea día laborable
        if not CitaService._es_dia_laborable(fecha_hora):
            return False, "No se programan citas en este día"
        
        # Verificar horario de atención
        if not CitaService._en_horario_atencion(fecha_hora):
            return False, "Fuera del horario de atención"
        
        # Calcular rango de la cita propuesta
        inicio_propuesto = fecha_hora
        fin_propuesto = fecha_hora + timedelta(minutes=duracion_minutos)
        
        # Buscar citas conflictivas
        query = Cita.query.filter(
            Cita.medico_id == medico_id,
            Cita.estado.in_(['programada', 'confirmada', 'en_curso']),
            Cita.fecha_hora >= fecha_hora.date()  # Mismo día
        )
        
        if excluir_cita_id:
            query = query.filter(Cita.id != excluir_cita_id)
        
        citas_existentes = query.all()
        
        for cita in citas_existentes:
            inicio_existente = cita.fecha_hora
            fin_existente = cita.fecha_hora + timedelta(minutes=cita.duracion_minutos)
            
            # Verificar solapamiento
            if not (fin_propuesto <= inicio_existente or inicio_propuesto >= fin_existente):
                return False, f"El médico tiene otra cita a las {cita.fecha_hora.strftime('%H:%M')}"
        
        return True, "Horario disponible"
    
    @staticmethod
    def _es_dia_laborable(fecha):
        """Verifica si es día laborable (Lunes-Sábado)"""
        dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
        return dia_semana != 6  # No es domingo
    
    @staticmethod
    def _en_horario_atencion(fecha_hora):
        """
        Verifica si está dentro del horario de atención
        Lunes-Viernes: 8AM-5PM
        Sábado: 8AM-1PM
        """
        dia_semana = fecha_hora.weekday()
        hora = fecha_hora.time()
        
        if dia_semana < 5:  # Lunes a Viernes
            return time(8, 0) <= hora <= time(17, 0)
        elif dia_semana == 5:  # Sábado
            return time(8, 0) <= hora <= time(13, 0)
        else:  # Domingo
            return False
    
    @staticmethod
    def obtener_horarios_disponibles(medico_id, fecha, duracion_minutos=20):
        """
        Obtiene lista de horarios disponibles para un médico en una fecha
        
        Returns:
            list: Lista de horarios disponibles en formato HH:MM
        """
        if not CitaService._es_dia_laborable(fecha):
            return []
        
        # Determinar horarios según día
        dia_semana = fecha.weekday()
        if dia_semana < 5:  # Lunes-Viernes
            hora_inicio = time(8, 0)
            hora_fin = time(17, 0)
        else:  # Sábado
            hora_inicio = time(8, 0)
            hora_fin = time(13, 0)
        
        # Generar slots cada 20 minutos
        horarios = []
        hora_actual = datetime.combine(fecha, hora_inicio)
        hora_limite = datetime.combine(fecha, hora_fin)
        
        while hora_actual < hora_limite:
            disponible, _ = CitaService.verificar_disponibilidad(
                medico_id, 
                hora_actual, 
                duracion_minutos
            )
            
            if disponible:
                horarios.append(hora_actual.strftime('%H:%M'))
            
            hora_actual += timedelta(minutes=20)
        
        return horarios
    
    @staticmethod
    def crear_cita(data, usuario_id):
        """
        Crea una nueva cita
        
        Args:
            data: Diccionario con datos de la cita
            usuario_id: ID del usuario que crea la cita
        
        Returns:
            (Cita, str): (cita_creada, mensaje_error)
        """
        try:
            # Validar disponibilidad
            disponible, mensaje = CitaService.verificar_disponibilidad(
                data['medico_id'],
                data['fecha_hora'],
                data.get('duracion_minutos', 20)
            )
            
            if not disponible and not data.get('es_emergencia', False):
                return None, mensaje
            
            # Crear cita
            cita = Cita(
                paciente_id=data['paciente_id'],
                medico_id=data['medico_id'],
                tipo_cita_id=data['tipo_cita_id'],
                fecha_hora=data['fecha_hora'],
                duracion_minutos=data.get('duracion_minutos', 20),
                motivo=data.get('motivo'),
                notas=data.get('notas'),
                es_emergencia=data.get('es_emergencia', False),
                estado='programada',
                created_by=usuario_id
            )
            
            db.session.add(cita)
            db.session.commit()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='crear_cita',
                tabla_afectada='citas',
                registro_id=cita.id,
                detalles=f"Cita creada para paciente {cita.paciente_id} con médico {cita.medico_id}"
            )
            db.session.add(log)
            db.session.commit()
            
            return cita, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def actualizar_cita(cita_id, data, usuario_id):
        """Actualiza una cita existente"""
        try:
            cita = Cita.query.get(cita_id)
            if not cita:
                return None, "Cita no encontrada"
            
            # Si cambia fecha/hora, verificar disponibilidad
            if 'fecha_hora' in data:
                disponible, mensaje = CitaService.verificar_disponibilidad(
                    cita.medico_id,
                    data['fecha_hora'],
                    data.get('duracion_minutos', cita.duracion_minutos),
                    excluir_cita_id=cita_id
                )
                
                if not disponible and not data.get('es_emergencia', False):
                    return None, mensaje
            
            # Actualizar campos
            for key, value in data.items():
                if hasattr(cita, key):
                    setattr(cita, key, value)
            
            db.session.commit()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='actualizar_cita',
                tabla_afectada='citas',
                registro_id=cita.id,
                detalles=f"Cita {cita_id} actualizada"
            )
            db.session.add(log)
            db.session.commit()
            
            return cita, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def cancelar_cita(cita_id, usuario_id, motivo=None):
        """Cancela una cita"""
        try:
            cita = Cita.query.get(cita_id)
            if not cita:
                return False, "Cita no encontrada"
            
            cita.estado = 'cancelada'
            if motivo:
                cita.notas = f"{cita.notas or ''}\nMotivo cancelación: {motivo}".strip()
            
            db.session.commit()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='cancelar_cita',
                tabla_afectada='citas',
                registro_id=cita.id,
                detalles=f"Cita {cita_id} cancelada. Motivo: {motivo}"
            )
            db.session.add(log)
            db.session.commit()
            
            return True, "Cita cancelada exitosamente"
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def obtener_citas_por_fecha(fecha_inicio, fecha_fin=None, medico_id=None, paciente_id=None):
        """
        Obtiene citas en un rango de fechas
        """
        query = Cita.query.filter(
            Cita.fecha_hora >= fecha_inicio
        )
        
        if fecha_fin:
            query = query.filter(Cita.fecha_hora <= fecha_fin)
        
        if medico_id:
            query = query.filter(Cita.medico_id == medico_id)
        
        if paciente_id:
            query = query.filter(Cita.paciente_id == paciente_id)
        
        return query.order_by(Cita.fecha_hora).all()
    
    @staticmethod
    def obtener_citas_hoy(medico_id=None):
        """Obtiene las citas del día actual"""
        hoy = datetime.now().date()
        inicio = datetime.combine(hoy, time.min)
        fin = datetime.combine(hoy, time.max)
        
        return CitaService.obtener_citas_por_fecha(inicio, fin, medico_id)
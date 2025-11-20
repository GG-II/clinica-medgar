"""
Servicio de Laboratorios
Lógica para gestión de estudios de laboratorio
"""
from datetime import datetime, date
from app.extensions import db
from app.models import Laboratorio, TipoLaboratorio, ValorReferencia, Paciente, Usuario
from app.models.auditoria import LogAuditoria


class LaboratorioService:
    """Servicio para gestión de laboratorios"""
    
    @staticmethod
    def solicitar_laboratorio(data, usuario_id):
        """
        Crea solicitud de laboratorio
        
        Args:
            data: {
                'paciente_id': int,
                'medico_id': int,
                'tipo_laboratorio_id': int,
                'fecha_solicitud': date,
                'observaciones': str
            }
            usuario_id: ID del usuario que solicita
        
        Returns:
            (Laboratorio, str): (laboratorio, error)
        """
        try:
            # Validar paciente y médico
            paciente = Paciente.query.get(data['paciente_id'])
            if not paciente:
                return None, "Paciente no encontrado"
            
            medico = Usuario.query.get(data['medico_id'])
            if not medico or medico.rol != 'medico':
                return None, "Médico no válido"
            
            tipo = TipoLaboratorio.query.get(data['tipo_laboratorio_id'])
            if not tipo:
                return None, "Tipo de laboratorio no encontrado"
            
            # Crear laboratorio
            laboratorio = Laboratorio(
                paciente_id=data['paciente_id'],
                medico_id=data['medico_id'],
                tipo_laboratorio_id=data['tipo_laboratorio_id'],
                fecha_solicitud=data.get('fecha_solicitud', date.today()),
                observaciones=data.get('observaciones'),
                estado='solicitado'
            )
            
            db.session.add(laboratorio)
            db.session.commit()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='solicitar_laboratorio',
                tabla_afectada='laboratorios',
                registro_id=laboratorio.id,
                detalles=f"Laboratorio {tipo.nombre} solicitado para {paciente.nombre_completo}"
            )
            db.session.add(log)
            db.session.commit()
            
            return laboratorio, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def registrar_resultados(laboratorio_id, data, usuario_id):
        """
        Registra resultados de laboratorio
        
        Args:
            laboratorio_id: ID del laboratorio
            data: {
                'fecha_resultado': date,
                'resultados': dict,  # JSON con los valores
                'interpretacion': str,
                'laboratorio_externo': str,
                'archivo_url': str
            }
            usuario_id: ID del usuario que registra
        
        Returns:
            (Laboratorio, list, str): (laboratorio, alertas, error)
        """
        try:
            laboratorio = Laboratorio.query.get(laboratorio_id)
            if not laboratorio:
                return None, [], "Laboratorio no encontrado"
            
            # Actualizar datos
            laboratorio.fecha_resultado = data.get('fecha_resultado', date.today())
            laboratorio.resultados = data.get('resultados', {})
            laboratorio.interpretacion = data.get('interpretacion')
            laboratorio.laboratorio_externo = data.get('laboratorio_externo')
            laboratorio.archivo_url = data.get('archivo_url')
            laboratorio.estado = 'completado'
            
            # Procesar resultados y agregar indicadores de normalidad
            if laboratorio.resultados:
                laboratorio.resultados = LaboratorioService._procesar_resultados(
                    laboratorio.resultados,
                    laboratorio.tipo_laboratorio_id,
                    laboratorio.paciente.edad if laboratorio.paciente else None,
                    laboratorio.paciente.sexo if laboratorio.paciente else None
                )
            
            db.session.commit()
            
            # Verificar valores críticos
            alertas = laboratorio.verificar_valores_criticos()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='registrar_resultados_laboratorio',
                tabla_afectada='laboratorios',
                registro_id=laboratorio.id,
                detalles=f"Resultados registrados para laboratorio {laboratorio_id}"
            )
            db.session.add(log)
            db.session.commit()
            
            return laboratorio, alertas, None
            
        except Exception as e:
            db.session.rollback()
            return None, [], str(e)
    
    @staticmethod
    def _procesar_resultados(resultados, tipo_laboratorio_id, edad, sexo):
        """
        Procesa resultados y agrega indicadores de normalidad
        
        Args:
            resultados: dict con valores {'parametro': {'valor': X, 'unidad': 'Y'}}
            tipo_laboratorio_id: ID del tipo de laboratorio
            edad: Edad del paciente
            sexo: Sexo del paciente ('M' o 'F')
        
        Returns:
            dict: Resultados procesados con indicador 'normal'
        """
        procesados = {}
        
        for parametro, datos in resultados.items():
            valor = datos.get('valor')
            unidad = datos.get('unidad')
            
            # Buscar valor de referencia
            referencia = ValorReferencia.obtener_referencia(
                tipo_laboratorio_id,
                parametro,
                edad,
                sexo
            )
            
            # Determinar si está en rango normal
            normal = True
            estado = 'normal'
            
            if referencia and valor is not None:
                valor_float = float(valor)
                
                if referencia.valor_minimo and valor_float < float(referencia.valor_minimo):
                    normal = False
                    estado = 'bajo'
                elif referencia.valor_maximo and valor_float > float(referencia.valor_maximo):
                    normal = False
                    estado = 'alto'
            
            procesados[parametro] = {
                'valor': valor,
                'unidad': unidad,
                'normal': normal,
                'estado': estado,
                'referencia': {
                    'min': float(referencia.valor_minimo) if referencia and referencia.valor_minimo else None,
                    'max': float(referencia.valor_maximo) if referencia and referencia.valor_maximo else None,
                    'unidad': referencia.unidad if referencia else unidad
                } if referencia else None
            }
        
        return procesados
    
    @staticmethod
    def obtener_historico_parametro(paciente_id, tipo_laboratorio_id, parametro, limite=10):
        """
        Obtiene histórico de un parámetro específico para gráficas
        
        Returns:
            list: [{'fecha': date, 'valor': float}, ...]
        """
        laboratorios = Laboratorio.query.filter(
            Laboratorio.paciente_id == paciente_id,
            Laboratorio.tipo_laboratorio_id == tipo_laboratorio_id,
            Laboratorio.estado == 'completado',
            Laboratorio.resultados.isnot(None)
        ).order_by(Laboratorio.fecha_resultado.desc()).limit(limite).all()
        
        historico = []
        
        for lab in laboratorios:
            if lab.resultados and parametro in lab.resultados:
                historico.append({
                    'fecha': lab.fecha_resultado.isoformat() if lab.fecha_resultado else None,
                    'valor': lab.resultados[parametro].get('valor')
                })
        
        return list(reversed(historico))  # Ordenar cronológicamente
    
    @staticmethod
    def comparar_resultados(paciente_id, tipo_laboratorio_id):
        """
        Compara últimos 3 resultados del mismo tipo de laboratorio
        Para ver evolución del paciente
        """
        laboratorios = Laboratorio.query.filter(
            Laboratorio.paciente_id == paciente_id,
            Laboratorio.tipo_laboratorio_id == tipo_laboratorio_id,
            Laboratorio.estado == 'completado'
        ).order_by(Laboratorio.fecha_resultado.desc()).limit(3).all()
        
        if len(laboratorios) < 2:
            return None, "Se necesitan al menos 2 estudios para comparar"
        
        comparacion = {
            'laboratorios': [],
            'tendencias': {}
        }
        
        # Agregar cada laboratorio
        for lab in laboratorios:
            comparacion['laboratorios'].append({
                'id': lab.id,
                'fecha': lab.fecha_resultado.isoformat() if lab.fecha_resultado else None,
                'resultados': lab.resultados
            })
        
        # Calcular tendencias (si hay parámetros comunes)
        if laboratorios[0].resultados and laboratorios[1].resultados:
            parametros_comunes = set(laboratorios[0].resultados.keys()) & set(laboratorios[1].resultados.keys())
            
            for parametro in parametros_comunes:
                valor_actual = laboratorios[0].resultados[parametro].get('valor')
                valor_anterior = laboratorios[1].resultados[parametro].get('valor')
                
                if valor_actual is not None and valor_anterior is not None:
                    diferencia = float(valor_actual) - float(valor_anterior)
                    porcentaje = (diferencia / float(valor_anterior)) * 100 if valor_anterior != 0 else 0
                    
                    if diferencia > 0:
                        tendencia = 'aumentó'
                    elif diferencia < 0:
                        tendencia = 'disminuyó'
                    else:
                        tendencia = 'se mantuvo'
                    
                    comparacion['tendencias'][parametro] = {
                        'tendencia': tendencia,
                        'diferencia': round(diferencia, 2),
                        'porcentaje': round(porcentaje, 2),
                        'valor_actual': valor_actual,
                        'valor_anterior': valor_anterior
                    }
        
        return comparacion, None
    
    @staticmethod
    def obtener_laboratorios_paciente(paciente_id, solo_completados=False):
        """Obtiene todos los laboratorios de un paciente"""
        query = Laboratorio.query.filter_by(paciente_id=paciente_id)
        
        if solo_completados:
            query = query.filter_by(estado='completado')
        
        return query.order_by(Laboratorio.fecha_solicitud.desc()).all()
    
    @staticmethod
    def cancelar_laboratorio(laboratorio_id, usuario_id, motivo=None):
        """Cancela un laboratorio solicitado"""
        try:
            laboratorio = Laboratorio.query.get(laboratorio_id)
            if not laboratorio:
                return False, "Laboratorio no encontrado"
            
            if laboratorio.estado != 'solicitado':
                return False, "Solo se pueden cancelar laboratorios en estado 'solicitado'"
            
            laboratorio.estado = 'cancelado'
            if motivo:
                laboratorio.observaciones = f"{laboratorio.observaciones or ''}\nMotivo cancelación: {motivo}".strip()
            
            db.session.commit()
            
            # Auditoría
            log = LogAuditoria(
                usuario_id=usuario_id,
                accion='cancelar_laboratorio',
                tabla_afectada='laboratorios',
                registro_id=laboratorio.id,
                detalles=f"Laboratorio {laboratorio_id} cancelado. Motivo: {motivo}"
            )
            db.session.add(log)
            db.session.commit()
            
            return True, "Laboratorio cancelado"
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
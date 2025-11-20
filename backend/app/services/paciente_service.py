"""
Servicio de Pacientes
Contiene toda la lógica de negocio relacionada con pacientes
"""
from app.extensions import db
from app.models.paciente import Paciente
from app.models.auditoria import LogAuditoria
from app.utils.helpers import calcular_edad, validar_dpi_guatemala, formatear_nombre, formatear_telefono_guatemala
from sqlalchemy import or_
from datetime import datetime


class PacienteService:
    """
    Servicio para gestionar pacientes
    Separa la lógica de negocio de las rutas
    """
    
    @staticmethod
    def crear_paciente(data, usuario_id):
        """
        Crea un nuevo paciente en el sistema
        
        Args:
            data (dict): Datos del paciente
            usuario_id (int): ID del usuario que crea el paciente
        
        Returns:
            tuple: (paciente, error)
                - paciente: Objeto Paciente creado, o None si hay error
                - error: Mensaje de error, o None si todo está bien
        
        Validaciones:
            - Nombre completo obligatorio
            - Fecha de nacimiento obligatoria
            - Sexo obligatorio
            - DPI único (si se proporciona)
        """
        try:
            # === VALIDACIONES ===
            
            # Validar campos obligatorios
            if not data.get('nombre_completo'):
                return None, "El nombre completo es obligatorio"
            
            if not data.get('fecha_nacimiento'):
                return None, "La fecha de nacimiento es obligatoria"
            
            if not data.get('sexo') or data.get('sexo') not in ['M', 'F']:
                return None, "El sexo debe ser 'M' o 'F'"
            
            # Validar DPI si se proporciona
            dpi = data.get('dpi')
            if dpi:
                # Validar formato
                if not validar_dpi_guatemala(dpi):
                    return None, "El DPI debe tener 13 dígitos"
                
                # Validar que sea único
                paciente_existente = Paciente.query.filter_by(dpi=dpi, activo=True).first()
                if paciente_existente:
                    return None, f"Ya existe un paciente con el DPI {dpi}"
            
            # === CREAR PACIENTE ===
            
            paciente = Paciente(
                nombre_completo=formatear_nombre(data.get('nombre_completo')),
                fecha_nacimiento=datetime.strptime(data.get('fecha_nacimiento'), '%Y-%m-%d').date(),
                sexo=data.get('sexo'),
                dpi=dpi,
                direccion=data.get('direccion'),
                municipio=data.get('municipio'),
                departamento=data.get('departamento'),
                telefono=data.get('telefono'),
                telefono_alternativo=data.get('telefono_alternativo'),
                email=data.get('email'),
                religion=data.get('religion'),
                estado_civil=data.get('estado_civil'),
                tiene_igss=data.get('tiene_igss', False),
                numero_igss=data.get('numero_igss'),
                contacto_emergencia_nombre=data.get('contacto_emergencia_nombre'),
                contacto_emergencia_telefono=data.get('contacto_emergencia_telefono'),
                contacto_emergencia_relacion=data.get('contacto_emergencia_relacion'),
                foto_url=data.get('foto_url'),
                observaciones=data.get('observaciones'),
                activo=True
            )
            
            db.session.add(paciente)
            db.session.commit()
            
            # Registrar en auditoría
            LogAuditoria.registrar(
                usuario_id=usuario_id,
                accion='crear_paciente',
                tabla_afectada='pacientes',
                registro_id=paciente.id,
                detalles=f"Paciente creado: {paciente.nombre_completo}"
            )
            
            return paciente, None
            
        except ValueError as e:
            db.session.rollback()
            return None, f"Error en el formato de fecha: {str(e)}"
        except Exception as e:
            db.session.rollback()
            return None, f"Error al crear paciente: {str(e)}"
    
    @staticmethod
    def obtener_paciente(paciente_id):
        """
        Obtiene un paciente por su ID
        
        Args:
            paciente_id (int): ID del paciente
        
        Returns:
            Paciente: Objeto paciente, o None si no existe
        """
        return Paciente.query.filter_by(id=paciente_id, activo=True).first()
    
    @staticmethod
    def listar_pacientes(page=1, per_page=20, busqueda=None, ordenar_por='nombre_completo'):
        """
        Lista pacientes con paginación y búsqueda
        
        Args:
            page (int): Número de página (default: 1)
            per_page (int): Cantidad por página (default: 20)
            busqueda (str): Término de búsqueda (busca en nombre, DPI, teléfono)
            ordenar_por (str): Campo por el cual ordenar
        
        Returns:
            dict: {
                'pacientes': [...],
                'total': int,
                'page': int,
                'per_page': int,
                'total_pages': int
            }
        """
        query = Paciente.query.filter_by(activo=True)
        
        # Aplicar búsqueda si existe
        if busqueda:
            busqueda_like = f"%{busqueda}%"
            query = query.filter(
                or_(
                    Paciente.nombre_completo.ilike(busqueda_like),
                    Paciente.dpi.ilike(busqueda_like),
                    Paciente.telefono.ilike(busqueda_like)
                )
            )
        
        # Aplicar ordenamiento
        if ordenar_por == 'nombre_completo':
            query = query.order_by(Paciente.nombre_completo.asc())
        elif ordenar_por == 'fecha_nacimiento':
            query = query.order_by(Paciente.fecha_nacimiento.desc())
        elif ordenar_por == 'created_at':
            query = query.order_by(Paciente.created_at.desc())
        
        # Paginar
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'pacientes': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages
        }
    
    @staticmethod
    def buscar_pacientes(termino):
        """
        Búsqueda rápida de pacientes (para autocompletar)
        
        Args:
            termino (str): Término de búsqueda
        
        Returns:
            list: Lista de pacientes que coinciden (máximo 10)
        """
        if not termino or len(termino) < 2:
            return []
        
        termino_like = f"%{termino}%"
        pacientes = Paciente.query.filter(
            Paciente.activo == True,
            or_(
                Paciente.nombre_completo.ilike(termino_like),
                Paciente.dpi.ilike(termino_like),
                Paciente.telefono.ilike(termino_like)
            )
        ).limit(10).all()
        
        return [p.to_dict() for p in pacientes]
    
    @staticmethod
    def actualizar_paciente(paciente_id, data, usuario_id):
        """
        Actualiza los datos de un paciente
        
        Args:
            paciente_id (int): ID del paciente a actualizar
            data (dict): Datos a actualizar
            usuario_id (int): ID del usuario que actualiza
        
        Returns:
            tuple: (paciente, error)
        """
        try:
            paciente = Paciente.query.filter_by(id=paciente_id, activo=True).first()
            
            if not paciente:
                return None, "Paciente no encontrado"
            
            # Validar DPI si se está actualizando
            if 'dpi' in data and data['dpi'] != paciente.dpi:
                if not validar_dpi_guatemala(data['dpi']):
                    return None, "El DPI debe tener 13 dígitos"
                
                # Verificar que no exista otro paciente con ese DPI
                otro_paciente = Paciente.query.filter(
                    Paciente.dpi == data['dpi'],
                    Paciente.id != paciente_id,
                    Paciente.activo == True
                ).first()
                
                if otro_paciente:
                    return None, f"Ya existe otro paciente con el DPI {data['dpi']}"
            
            # Actualizar campos
            campos_actualizables = [
                'nombre_completo', 'fecha_nacimiento', 'sexo', 'dpi',
                'direccion', 'municipio', 'departamento',
                'telefono', 'telefono_alternativo', 'email',
                'religion', 'estado_civil',
                'tiene_igss', 'numero_igss',
                'contacto_emergencia_nombre', 'contacto_emergencia_telefono',
                'contacto_emergencia_relacion',
                'foto_url', 'observaciones'
            ]
            
            for campo in campos_actualizables:
                if campo in data:
                    if campo == 'nombre_completo':
                        setattr(paciente, campo, formatear_nombre(data[campo]))
                    elif campo == 'fecha_nacimiento' and isinstance(data[campo], str):
                        setattr(paciente, campo, datetime.strptime(data[campo], '%Y-%m-%d').date())
                    else:
                        setattr(paciente, campo, data[campo])
            
            paciente.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Registrar en auditoría
            LogAuditoria.registrar(
                usuario_id=usuario_id,
                accion='actualizar_paciente',
                tabla_afectada='pacientes',
                registro_id=paciente.id,
                detalles=f"Paciente actualizado: {paciente.nombre_completo}"
            )
            
            return paciente, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error al actualizar paciente: {str(e)}"
    
    @staticmethod
    def eliminar_paciente(paciente_id, usuario_id):
        """
        Elimina (desactiva) un paciente
        
        NOTA: No se elimina físicamente, solo se marca como inactivo
        
        Args:
            paciente_id (int): ID del paciente
            usuario_id (int): ID del usuario que elimina
        
        Returns:
            tuple: (success, error)
        """
        try:
            paciente = Paciente.query.filter_by(id=paciente_id, activo=True).first()
            
            if not paciente:
                return False, "Paciente no encontrado"
            
            paciente.activo = False
            paciente.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Registrar en auditoría
            LogAuditoria.registrar(
                usuario_id=usuario_id,
                accion='eliminar_paciente',
                tabla_afectada='pacientes',
                registro_id=paciente.id,
                detalles=f"Paciente eliminado (desactivado): {paciente.nombre_completo}"
            )
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error al eliminar paciente: {str(e)}"
    
    @staticmethod
    def obtener_estadisticas():
        """
        Obtiene estadísticas generales de pacientes
        
        Returns:
            dict: Estadísticas de pacientes
        """
        total_pacientes = Paciente.query.filter_by(activo=True).count()
        pacientes_hombres = Paciente.query.filter_by(activo=True, sexo='M').count()
        pacientes_mujeres = Paciente.query.filter_by(activo=True, sexo='F').count()
        pacientes_con_igss = Paciente.query.filter_by(activo=True, tiene_igss=True).count()
        
        return {
            'total': total_pacientes,
            'hombres': pacientes_hombres,
            'mujeres': pacientes_mujeres,
            'con_igss': pacientes_con_igss,
            'sin_igss': total_pacientes - pacientes_con_igss
        }
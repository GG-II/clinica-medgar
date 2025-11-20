"""
Servicio de Archivos
Maneja la subida, descarga y gestión de archivos de pacientes
"""
import os
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.archivo_paciente import ArchivoPaciente
from app.models.auditoria import LogAuditoria
from datetime import datetime


class ArchivoService:
    """
    Servicio para gestionar archivos de pacientes
    """
    
    # Configuración de archivos permitidos
    ALLOWED_EXTENSIONS = {
        'images': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
        'documents': {'pdf'},
        'videos': {'mp4', 'avi', 'mov'}
    }
    
    # Tamaños máximos (en bytes)
    MAX_FILE_SIZE = {
        'images': 5 * 1024 * 1024,      # 5 MB
        'documents': 5 * 1024 * 1024,   # 5 MB
        'videos': 50 * 1024 * 1024      # 50 MB
    }
    
    @staticmethod
    def validar_extension(filename, categoria):
        """
        Valida que la extensión del archivo sea permitida
        
        Args:
            filename (str): Nombre del archivo
            categoria (str): Categoría del archivo
        
        Returns:
            bool: True si es válido, False si no
        """
        if '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        
        # Determinar tipo según extensión
        if extension in ArchivoService.ALLOWED_EXTENSIONS['images']:
            return True
        elif extension in ArchivoService.ALLOWED_EXTENSIONS['documents']:
            return True
        elif extension in ArchivoService.ALLOWED_EXTENSIONS['videos']:
            return True
        
        return False
    
    @staticmethod
    def validar_tamanio(file_size, filename):
        """
        Valida que el tamaño del archivo no exceda el máximo
        
        Args:
            file_size (int): Tamaño del archivo en bytes
            filename (str): Nombre del archivo
        
        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        extension = filename.rsplit('.', 1)[1].lower()
        
        # Determinar límite según tipo
        if extension in ArchivoService.ALLOWED_EXTENSIONS['images']:
            max_size = ArchivoService.MAX_FILE_SIZE['images']
            tipo = 'imagen'
        elif extension in ArchivoService.ALLOWED_EXTENSIONS['documents']:
            max_size = ArchivoService.MAX_FILE_SIZE['documents']
            tipo = 'documento'
        elif extension in ArchivoService.ALLOWED_EXTENSIONS['videos']:
            max_size = ArchivoService.MAX_FILE_SIZE['videos']
            tipo = 'video'
        else:
            return False, "Tipo de archivo no permitido"
        
        if file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            return False, f"El {tipo} no debe superar {max_mb} MB"
        
        return True, None
    
    @staticmethod
    def guardar_archivo(file, paciente_id, categoria, descripcion=None, usuario_id=None):
        """
        Guarda un archivo en el sistema de archivos y registra en BD
        
        Args:
            file: Archivo de Flask
            paciente_id (int): ID del paciente
            categoria (str): Categoría del archivo
            descripcion (str): Descripción opcional
            usuario_id (int): ID del usuario que sube el archivo
        
        Returns:
            tuple: (archivo, error)
        """
        try:
            # Validar que hay archivo
            if not file or file.filename == '':
                return None, "No se proporcionó archivo"
            
            filename = secure_filename(file.filename)
            
            # Validar extensión
            if not ArchivoService.validar_extension(filename, categoria):
                return None, "Tipo de archivo no permitido"
            
            # Crear directorio si no existe
            upload_folder = os.path.join('uploads', 'pacientes', str(paciente_id), categoria)
            os.makedirs(upload_folder, exist_ok=True)
            
            # Generar nombre único
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            extension = filename.rsplit('.', 1)[1].lower()
            nuevo_nombre = f"{timestamp}_{filename}"
            ruta_completa = os.path.join(upload_folder, nuevo_nombre)
            
            # Guardar archivo
            file.save(ruta_completa)
            
            # Obtener tamaño
            tamanio = os.path.getsize(ruta_completa)
            
            # Validar tamaño
            valido, error_tamanio = ArchivoService.validar_tamanio(tamanio, filename)
            if not valido:
                # Eliminar archivo si es muy grande
                os.remove(ruta_completa)
                return None, error_tamanio
            
            # Registrar en base de datos
            archivo = ArchivoPaciente(
                paciente_id=paciente_id,
                nombre_archivo=filename,
                ruta_archivo=ruta_completa,
                tipo_archivo=file.content_type,
                categoria=categoria,
                tamanio_bytes=tamanio,
                descripcion=descripcion,
                subido_por=usuario_id
            )
            
            db.session.add(archivo)
            db.session.commit()
            
            # Registrar en auditoría
            if usuario_id:
                LogAuditoria.registrar(
                    usuario_id=usuario_id,
                    accion='subir_archivo',
                    tabla_afectada='archivos_paciente',
                    registro_id=archivo.id,
                    detalles=f"Archivo subido: {filename} para paciente {paciente_id}"
                )
            
            return archivo, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error al guardar archivo: {str(e)}"
    
    @staticmethod
    def obtener_archivos_paciente(paciente_id, categoria=None):
        """
        Obtiene los archivos de un paciente
        
        Args:
            paciente_id (int): ID del paciente
            categoria (str): Filtrar por categoría (opcional)
        
        Returns:
            list: Lista de archivos
        """
        query = ArchivoPaciente.query.filter_by(paciente_id=paciente_id)
        
        if categoria:
            query = query.filter_by(categoria=categoria)
        
        query = query.order_by(ArchivoPaciente.fecha_subida.desc())
        
        return [archivo.to_dict() for archivo in query.all()]
    
    @staticmethod
    def eliminar_archivo(archivo_id, usuario_id=None):
        """
        Elimina un archivo del sistema
        
        Args:
            archivo_id (int): ID del archivo
            usuario_id (int): ID del usuario que elimina
        
        Returns:
            tuple: (success, error)
        """
        try:
            archivo = ArchivoPaciente.query.get(archivo_id)
            
            if not archivo:
                return False, "Archivo no encontrado"
            
            # Eliminar archivo físico
            if os.path.exists(archivo.ruta_archivo):
                os.remove(archivo.ruta_archivo)
            
            # Eliminar registro de BD
            db.session.delete(archivo)
            db.session.commit()
            
            # Registrar en auditoría
            if usuario_id:
                LogAuditoria.registrar(
                    usuario_id=usuario_id,
                    accion='eliminar_archivo',
                    tabla_afectada='archivos_paciente',
                    registro_id=archivo_id,
                    detalles=f"Archivo eliminado: {archivo.nombre_archivo}"
                )
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error al eliminar archivo: {str(e)}"
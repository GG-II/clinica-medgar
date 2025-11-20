"""
Utilidades para manejo de archivos
Funciones auxiliares para trabajar con archivos
"""
import os
from PIL import Image
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):
    """
    Verifica si la extensión del archivo es permitida
    
    Args:
        filename (str): Nombre del archivo
        allowed_extensions (set): Set de extensiones permitidas
    
    Returns:
        bool: True si es permitido, False si no
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def resize_image(image_path, max_width=800, max_height=800, quality=85):
    """
    Redimensiona una imagen manteniendo la proporción
    
    Args:
        image_path (str): Ruta de la imagen
        max_width (int): Ancho máximo
        max_height (int): Alto máximo
        quality (int): Calidad de compresión (1-100)
    
    Returns:
        bool: True si se redimensionó exitosamente
    """
    try:
        with Image.open(image_path) as img:
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Calcular nuevas dimensiones manteniendo proporción
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Guardar con compresión
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            
            return True
    except Exception as e:
        print(f"Error al redimensionar imagen: {str(e)}")
        return False


def get_file_size_mb(file_path):
    """
    Obtiene el tamaño de un archivo en MB
    
    Args:
        file_path (str): Ruta del archivo
    
    Returns:
        float: Tamaño en MB
    """
    if not os.path.exists(file_path):
        return 0
    
    size_bytes = os.path.getsize(file_path)
    return round(size_bytes / (1024 * 1024), 2)


def create_thumbnail(image_path, thumbnail_path, size=(150, 150)):
    """
    Crea una miniatura de una imagen
    
    Args:
        image_path (str): Ruta de la imagen original
        thumbnail_path (str): Ruta donde guardar la miniatura
        size (tuple): Tamaño de la miniatura (ancho, alto)
    
    Returns:
        bool: True si se creó exitosamente
    """
    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=75)
            
            return True
    except Exception as e:
        print(f"Error al crear miniatura: {str(e)}")
        return False
import re
from email_validator import validate_email, EmailNotValidError


def validar_email(email):
    """
    Valida que un email sea válido
    
    Args:
        email (str): Email a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validar_telefono_guatemala(telefono):
    """
    Valida formato de teléfono guatemalteco
    Formatos aceptados:
    - 8 dígitos: 12345678
    - Con código país: +502 12345678 o +50212345678
    - Con guiones: 1234-5678
    
    Args:
        telefono (str): Teléfono a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    if not telefono:
        return True, None  # Teléfono es opcional
    
    # Limpiar espacios y guiones
    telefono_limpio = telefono.replace(' ', '').replace('-', '')
    
    # Patrón: opcional +502, luego 8 dígitos
    patron = r'^(\+502)?[2-9]\d{7}$'
    
    if re.match(patron, telefono_limpio):
        return True, None
    else:
        return False, "Formato de teléfono inválido. Use 8 dígitos (ej: 12345678) o con código +502"


def validar_username(username):
    """
    Valida que el username sea válido
    - Solo letras, números, guiones bajos y puntos
    - Entre 3 y 50 caracteres
    
    Args:
        username (str): Username a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    if not username:
        return False, "El username es requerido"
    
    if len(username) < 3:
        return False, "El username debe tener al menos 3 caracteres"
    
    if len(username) > 50:
        return False, "El username no puede tener más de 50 caracteres"
    
    patron = r'^[a-zA-Z0-9._]+$'
    if not re.match(patron, username):
        return False, "El username solo puede contener letras, números, puntos y guiones bajos"
    
    return True, None


def validar_password(password):
    """
    Valida que la contraseña sea segura
    - Al menos 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    
    Args:
        password (str): Contraseña a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    if not password:
        return False, "La contraseña es requerida"
    
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe tener al menos una letra mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe tener al menos una letra minúscula"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe tener al menos un número"
    
    return True, None


def validar_rol(rol):
    """
    Valida que el rol sea uno de los permitidos
    
    Args:
        rol (str): Rol a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    roles_validos = ['medico', 'enfermera', 'recepcionista', 'administrador']
    
    if rol not in roles_validos:
        return False, f"Rol inválido. Debe ser uno de: {', '.join(roles_validos)}"
    
    return True, None
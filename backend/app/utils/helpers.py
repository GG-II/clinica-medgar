"""
Funciones auxiliares (helpers)
Funciones útiles que se usan en varios lugares del sistema
"""
from datetime import date, datetime


def calcular_edad(fecha_nacimiento):
    """
    Calcula la edad en años a partir de una fecha de nacimiento
    
    Args:
        fecha_nacimiento (date): Fecha de nacimiento del paciente
    
    Returns:
        int: Edad en años, o None si la fecha es inválida
    
    Ejemplos:
        >>> calcular_edad(date(2000, 1, 1))
        24  # (si estamos en 2024)
    """
    if not fecha_nacimiento:
        return None
    
    # Si recibimos un string, convertirlo a date
    if isinstance(fecha_nacimiento, str):
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        except ValueError:
            return None
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    
    # Ajustar si aún no ha cumplido años este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    return edad


def calcular_imc(peso_kg, talla_cm):
    """
    Calcula el Índice de Masa Corporal (IMC)
    
    Args:
        peso_kg (float): Peso en kilogramos
        talla_cm (float): Talla en centímetros
    
    Returns:
        float: IMC calculado, redondeado a 2 decimales
        None: Si los datos son inválidos
    
    Fórmula: IMC = peso (kg) / (talla (m))²
    
    Ejemplos:
        >>> calcular_imc(70, 170)
        24.22
    """
    if not peso_kg or not talla_cm or peso_kg <= 0 or talla_cm <= 0:
        return None
    
    # Convertir talla de cm a metros
    talla_m = talla_cm / 100
    
    # Calcular IMC
    imc = peso_kg / (talla_m ** 2)
    
    # Redondear a 2 decimales
    return round(imc, 2)


def interpretar_imc(imc):
    """
    Interpreta el valor del IMC según estándares de la OMS
    
    Args:
        imc (float): Valor del IMC
    
    Returns:
        str: Interpretación del IMC
    
    Clasificación OMS:
        - Bajo peso: < 18.5
        - Normal: 18.5 - 24.9
        - Sobrepeso: 25.0 - 29.9
        - Obesidad I: 30.0 - 34.9
        - Obesidad II: 35.0 - 39.9
        - Obesidad III: >= 40.0
    """
    if not imc:
        return "No calculado"
    
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25.0:
        return "Normal"
    elif imc < 30.0:
        return "Sobrepeso"
    elif imc < 35.0:
        return "Obesidad I"
    elif imc < 40.0:
        return "Obesidad II"
    else:
        return "Obesidad III"


def validar_dpi_guatemala(dpi):
    """
    Valida que el DPI tenga formato válido de Guatemala
    
    Formato válido: 13 dígitos sin espacios ni guiones
    Ejemplo: 1234567890101
    
    Args:
        dpi (str): Número de DPI a validar
    
    Returns:
        bool: True si es válido, False si no lo es
    """
    if not dpi:
        return False
    
    # Remover espacios y guiones
    dpi = dpi.replace(' ', '').replace('-', '')
    
    # Debe tener exactamente 13 dígitos
    if len(dpi) != 13:
        return False
    
    # Debe contener solo números
    if not dpi.isdigit():
        return False
    
    return True


def formatear_telefono_guatemala(telefono):
    """
    Formatea un número de teléfono de Guatemala
    
    Formato: +502 1234-5678
    
    Args:
        telefono (str): Número de teléfono sin formato
    
    Returns:
        str: Teléfono formateado, o el original si no es válido
    
    Ejemplos:
        >>> formatear_telefono_guatemala("12345678")
        "+502 1234-5678"
        >>> formatear_telefono_guatemala("50212345678")
        "+502 1234-5678"
    """
    if not telefono:
        return telefono
    
    # Remover espacios, guiones y el símbolo +
    telefono_limpio = telefono.replace(' ', '').replace('-', '').replace('+', '')
    
    # Si empieza con 502, removerlo
    if telefono_limpio.startswith('502'):
        telefono_limpio = telefono_limpio[3:]
    
    # Debe tener 8 dígitos
    if len(telefono_limpio) != 8 or not telefono_limpio.isdigit():
        return telefono  # Retornar original si no es válido
    
    # Formatear: +502 1234-5678
    return f"+502 {telefono_limpio[:4]}-{telefono_limpio[4:]}"


def edad_a_meses(fecha_nacimiento):
    """
    Calcula la edad en meses (útil para pediatría)
    
    Args:
        fecha_nacimiento (date): Fecha de nacimiento
    
    Returns:
        int: Edad en meses completos
    """
    if not fecha_nacimiento:
        return None
    
    hoy = date.today()
    meses = (hoy.year - fecha_nacimiento.year) * 12 + (hoy.month - fecha_nacimiento.month)
    
    # Ajustar si aún no ha llegado al día del mes
    if hoy.day < fecha_nacimiento.day:
        meses -= 1
    
    return meses


def formatear_nombre(nombre):
    """
    Formatea un nombre: primera letra de cada palabra en mayúscula
    
    Args:
        nombre (str): Nombre sin formatear
    
    Returns:
        str: Nombre formateado
    
    Ejemplos:
        >>> formatear_nombre("juan PÉREZ lópez")
        "Juan Pérez López"
    """
    if not nombre:
        return nombre
    
    return nombre.strip().title()
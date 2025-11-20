"""
Módulo de modelos de la aplicación
Exporta todos los modelos para facilitar su importación
"""
from app.models.usuario import Usuario
from app.models.auditoria import LogAuditoria
from app.models.paciente import Paciente  # ← NUEVO

# Exportar todos los modelos para poder importarlos fácilmente
__all__ = [
    'Usuario',
    'LogAuditoria',
    'Paciente'  # ← NUEVO
]
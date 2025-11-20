"""
Módulo de modelos de la aplicación
Exporta todos los modelos para facilitar su importación
"""
from app.models.usuario import Usuario
from app.models.auditoria import LogAuditoria
from app.models.paciente import Paciente
from app.models.consulta import Consulta  # ← AGREGAR
from app.models.historia_clinica import HistoriaClinica
from app.models.signos_vitales import SignosVitales
from app.models.antecedentes import Antecedente
from app.models.vacuna import Vacuna, AplicacionVacuna
from app.models.archivo_paciente import ArchivoPaciente

# Exportar todos los modelos para poder importarlos fácilmente
__all__ = [
    'Usuario',
    'LogAuditoria',
    'Paciente',
    'Consulta',  # ← AGREGAR
    'HistoriaClinica',
    'SignosVitales',
    'Antecedente',
    'Vacuna',
    'AplicacionVacuna',
    'ArchivoPaciente'
]
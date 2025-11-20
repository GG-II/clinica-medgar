"""
Exportación de todos los modelos
"""
from app.models.usuario import Usuario
from app.models.auditoria import LogAuditoria
from app.models.paciente import Paciente
from app.models.historia_clinica import HistoriaClinica
from app.models.consulta import Consulta
from app.models.signos_vitales import SignosVitales
from app.models.antecedentes import Antecedente
from app.models.vacuna import Vacuna, AplicacionVacuna
from app.models.archivo_paciente import ArchivoPaciente

# Nuevos modelos Fase 3
from app.models.cita import Cita, TipoCita
from app.models.recordatorio import Recordatorio
from app.models.medicamento import Medicamento
from app.models.receta import Receta, RecetaDetalle
from app.models.laboratorio import Laboratorio, TipoLaboratorio, ValorReferencia

__all__ = [
    # Fase 1
    'Usuario',
    'LogAuditoria',
    
    # Fase 2
    'Paciente',
    'HistoriaClinica',
    'Consulta',
    'SignosVitales',
    'Antecedente',
    'Vacuna',
    'AplicacionVacuna',
    'ArchivoPaciente',
    
    # Fase 3
    'Cita',
    'TipoCita',
    'Recordatorio',
    'Medicamento',
    'Receta',
    'RecetaDetalle',
    'Laboratorio',
    'TipoLaboratorio',
    'ValorReferencia'
]
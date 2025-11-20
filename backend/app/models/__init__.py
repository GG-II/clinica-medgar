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

# Modelos Fase 3
from app.models.cita import Cita, TipoCita
from app.models.recordatorio import Recordatorio
from app.models.medicamento import Medicamento
from app.models.receta import Receta, RecetaDetalle
from app.models.laboratorio import Laboratorio, TipoLaboratorio, ValorReferencia

# Modelos Fase 4 - Hospitalización
from app.models.hospitalizacion import Cama, Hospitalizacion
from app.models.nota_medica import NotaMedica
from app.models.orden_medica import OrdenMedica
from app.models.registro_enfermeria import RegistroEnfermeria

# Modelos Fase 4 - Farmacia
from app.models.proveedor import Proveedor
from app.models.producto_farmacia import ProductoFarmacia
from app.models.movimiento_inventario import MovimientoInventario
from app.models.compra import Compra, CompraDetalle

# Modelos Fase 4 - Facturación y Caja
from app.models.caja import Caja, MovimientoCaja
from app.models.factura import Convenio, Factura, FacturaDetalle, CuentaPorCobrar, PagoCuenta

__all__ = [
    # Fase 1 - Autenticación
    'Usuario',
    'LogAuditoria',
    
    # Fase 2 - Pacientes e Historia Clínica
    'Paciente',
    'HistoriaClinica',
    'Consulta',
    'SignosVitales',
    'Antecedente',
    'Vacuna',
    'AplicacionVacuna',
    'ArchivoPaciente',
    
    # Fase 3 - Agenda, Recetas y Laboratorios
    'Cita',
    'TipoCita',
    'Recordatorio',
    'Medicamento',
    'Receta',
    'RecetaDetalle',
    'Laboratorio',
    'TipoLaboratorio',
    'ValorReferencia',
    
    # Fase 4 - Hospitalización
    'Cama',
    'Hospitalizacion',
    'NotaMedica',
    'OrdenMedica',
    'RegistroEnfermeria',
    
    # Fase 4 - Farmacia
    'Proveedor',
    'ProductoFarmacia',
    'MovimientoInventario',
    'Compra',
    'CompraDetalle',
    
    # Fase 4 - Facturación y Caja
    'Caja',
    'MovimientoCaja',
    'Convenio',
    'Factura',
    'FacturaDetalle',
    'CuentaPorCobrar',
    'PagoCuenta'
]
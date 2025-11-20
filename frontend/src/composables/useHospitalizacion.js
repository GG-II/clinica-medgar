import { ref, computed } from 'vue'
import { useHospitalizacionStore } from '@/stores/hospitalizacion'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de hospitalización
 * Proporciona métodos y estado reactivo para componentes
 */
export function useHospitalizacion() {
  const store = useHospitalizacionStore()
  const router = useRouter()

  // ==========================================
  // COMPUTED PROPERTIES (desde el store)
  // ==========================================
  
  // Camas
  const camas = computed(() => store.camas)
  const loadingCamas = computed(() => store.loadingCamas)
  const camasDisponibles = computed(() => store.camasDisponibles)
  const camasOcupadas = computed(() => store.camasOcupadas)
  const camasEnLimpieza = computed(() => store.camasEnLimpieza)
  const camasEnMantenimiento = computed(() => store.camasEnMantenimiento)
  const totalCamas = computed(() => store.totalCamas)
  const porcentajeOcupacion = computed(() => store.porcentajeOcupacion)
  
  // Hospitalizaciones
  const hospitalizaciones = computed(() => store.hospitalizaciones)
  const hospitalizacionActual = computed(() => store.hospitalizacionActual)
  const loadingHospitalizaciones = computed(() => store.loadingHospitalizaciones)
  const hospitalizacionesActivas = computed(() => store.hospitalizacionesActivas)
  const hospitalizacionesEgresadas = computed(() => store.hospitalizacionesEgresadas)
  const totalHospitalizaciones = computed(() => store.totalHospitalizaciones)
  
  // Notas, Órdenes, Registros
  const notasMedicas = computed(() => store.notasMedicas)
  const ordenesMedicas = computed(() => store.ordenesMedicas)
  const registrosEnfermeria = computed(() => store.registrosEnfermeria)
  const ordenesActivas = computed(() => store.ordenesActivas)
  
  // General
  const loading = computed(() => store.loading)
  const error = computed(() => store.error)
  const filters = computed(() => store.filters)

  // ==========================================
  // MÉTODOS - CAMAS
  // ==========================================

  /**
   * Cargar camas
   */
  async function loadCamas(params = {}) {
    try {
      await store.fetchCamas(params)
    } catch (err) {
      console.error('Error al cargar camas:', err)
    }
  }

  /**
   * Actualizar estado de cama
   */
  async function actualizarCama(id, estado, observaciones = null) {
    try {
      const data = { estado }
      if (observaciones) {
        data.observaciones = observaciones
      }
      
      const result = await store.updateCama(id, data)
      return result
    } catch (err) {
      console.error('Error al actualizar cama:', err)
      throw err
    }
  }

  // ==========================================
  // MÉTODOS - HOSPITALIZACIONES
  // ==========================================

  /**
   * Cargar hospitalizaciones
   */
  async function loadHospitalizaciones(params = {}) {
    try {
      await store.fetchHospitalizaciones(params)
    } catch (err) {
      console.error('Error al cargar hospitalizaciones:', err)
    }
  }

  /**
   * Cargar una hospitalización específica
   */
  async function loadHospitalizacion(id) {
    try {
      await store.fetchHospitalizacionById(id)
    } catch (err) {
      console.error('Error al cargar hospitalización:', err)
    }
  }

  /**
   * Ingresar paciente
   */
  async function ingresarPaciente(data) {
    try {
      const result = await store.ingresarPaciente(data)
      
      if (result.success) {
        return result
      }
    } catch (err) {
      console.error('Error al ingresar paciente:', err)
      throw err
    }
  }

  /**
   * Egresar paciente con confirmación
   */
  async function egresarPaciente(id, diagnosticoEgreso, observaciones = null, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm(
        '¿Está seguro de egresar a este paciente? Esta acción liberará la cama.'
      )
      if (!confirmado) return false
    }
    
    try {
      const data = { diagnostico_egreso: diagnosticoEgreso }
      if (observaciones) {
        data.observaciones = observaciones
      }
      
      const result = await store.egresarPaciente(id, data)
      return result
    } catch (err) {
      console.error('Error al egresar paciente:', err)
      throw err
    }
  }

  // ==========================================
  // MÉTODOS - NOTAS MÉDICAS
  // ==========================================

  /**
   * Agregar nota médica
   */
  async function agregarNota(hospitalizacionId, tipoNota, contenido, datosAdicionales = null) {
    try {
      const data = {
        tipo_nota: tipoNota,
        contenido
      }
      
      if (datosAdicionales) {
        data.datos_adicionales = datosAdicionales
      }
      
      const result = await store.agregarNotaMedica(hospitalizacionId, data)
      return result
    } catch (err) {
      console.error('Error al agregar nota médica:', err)
      throw err
    }
  }

  // ==========================================
  // MÉTODOS - ÓRDENES MÉDICAS
  // ==========================================

  /**
   * Agregar orden médica
   */
  async function agregarOrden(hospitalizacionId, tipoOrden, descripcion, indicaciones = null) {
    try {
      const data = {
        tipo_orden: tipoOrden,
        descripcion
      }
      
      if (indicaciones) {
        data.indicaciones = indicaciones
      }
      
      const result = await store.agregarOrdenMedica(hospitalizacionId, data)
      return result
    } catch (err) {
      console.error('Error al agregar orden médica:', err)
      throw err
    }
  }

  /**
   * Suspender orden con confirmación
   */
  async function suspenderOrden(ordenId, motivo = null, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm(
        '¿Está seguro de suspender esta orden médica?'
      )
      if (!confirmado) return false
    }
    
    try {
      const result = await store.suspenderOrden(ordenId, motivo)
      return result
    } catch (err) {
      console.error('Error al suspender orden:', err)
      throw err
    }
  }

  // ==========================================
  // MÉTODOS - REGISTRO ENFERMERÍA
  // ==========================================

  /**
   * Agregar registro de enfermería
   */
  async function agregarRegistro(hospitalizacionId, tipoRegistro, descripcion, datosJson = null) {
    try {
      const data = {
        tipo_registro: tipoRegistro,
        descripcion
      }
      
      if (datosJson) {
        data.datos_json = datosJson
      }
      
      const result = await store.agregarRegistroEnfermeria(hospitalizacionId, data)
      return result
    } catch (err) {
      console.error('Error al agregar registro de enfermería:', err)
      throw err
    }
  }

  // ==========================================
  // FILTROS
  // ==========================================

  /**
   * Aplicar filtros
   */
  async function aplicarFiltros(newFilters) {
    try {
      await store.setFilters(newFilters)
    } catch (err) {
      console.error('Error al aplicar filtros:', err)
    }
  }

  /**
   * Limpiar filtros
   */
  async function limpiarFiltros() {
    try {
      await store.clearFilters()
    } catch (err) {
      console.error('Error al limpiar filtros:', err)
    }
  }

  // ==========================================
  // UTILIDADES - CAMAS
  // ==========================================

  /**
   * Obtener badge del estado de cama
   */
  function obtenerBadgeEstadoCama(estado) {
    const badges = {
      'disponible': { text: 'Disponible', variant: 'success' },
      'ocupada': { text: 'Ocupada', variant: 'danger' },
      'limpieza': { text: 'Limpieza', variant: 'warning' },
      'mantenimiento': { text: 'Mantenimiento', variant: 'secondary' }
    }
    return badges[estado] || { text: estado, variant: 'secondary' }
  }

  /**
   * Obtener color del estado de cama
   */
  function obtenerColorEstadoCama(estado) {
    const colores = {
      'disponible': 'text-green-600',
      'ocupada': 'text-red-600',
      'limpieza': 'text-yellow-600',
      'mantenimiento': 'text-gray-600'
    }
    return colores[estado] || 'text-gray-600'
  }

  /**
   * Obtener icono del estado de cama
   */
  function obtenerIconoCama(estado) {
    const iconos = {
      'disponible': '✅',
      'ocupada': '🛏️',
      'limpieza': '🧹',
      'mantenimiento': '🔧'
    }
    return iconos[estado] || '📋'
  }

  // ==========================================
  // UTILIDADES - HOSPITALIZACIONES
  // ==========================================

  /**
   * Obtener badge del estado de hospitalización
   */
  function obtenerBadgeEstadoHospitalizacion(estado) {
    const badges = {
      'activo': { text: 'Activo', variant: 'success' },
      'egresado': { text: 'Egresado', variant: 'secondary' },
      'transferido': { text: 'Transferido', variant: 'info' }
    }
    return badges[estado] || { text: estado, variant: 'secondary' }
  }

  /**
   * Calcular días de estancia
   */
  function calcularDiasEstancia(hospitalizacion) {
    if (!hospitalizacion.fecha_ingreso) return 0
    
    const fechaIngreso = new Date(hospitalizacion.fecha_ingreso)
    const fechaFin = hospitalizacion.fecha_egreso 
      ? new Date(hospitalizacion.fecha_egreso)
      : new Date()
    
    const diferencia = fechaFin - fechaIngreso
    const dias = Math.ceil(diferencia / (1000 * 60 * 60 * 24))
    
    return dias
  }

  /**
   * Verificar si hospitalización está activa
   */
  function estaActiva(hospitalizacion) {
    return hospitalizacion.estado === 'activo'
  }

  // ==========================================
  // UTILIDADES - NOTAS MÉDICAS
  // ==========================================

  /**
   * Obtener badge del tipo de nota
   */
  function obtenerBadgeTipoNota(tipo) {
    const badges = {
      'ingreso': { text: 'Ingreso', variant: 'primary' },
      'evolucion': { text: 'Evolución', variant: 'info' },
      'procedimiento': { text: 'Procedimiento', variant: 'warning' },
      'operatoria': { text: 'Operatoria', variant: 'danger' },
      'egreso': { text: 'Egreso', variant: 'success' }
    }
    return badges[tipo] || { text: tipo, variant: 'secondary' }
  }

  /**
   * Obtener icono del tipo de nota
   */
  function obtenerIconoNota(tipo) {
    const iconos = {
      'ingreso': '📝',
      'evolucion': '📈',
      'procedimiento': '🔬',
      'operatoria': '⚕️',
      'egreso': '✅'
    }
    return iconos[tipo] || '📋'
  }

  // ==========================================
  // UTILIDADES - ÓRDENES MÉDICAS
  // ==========================================

  /**
   * Obtener badge del tipo de orden
   */
  function obtenerBadgeTipoOrden(tipo) {
    const badges = {
      'medicamento': { text: 'Medicamento', variant: 'primary' },
      'dieta': { text: 'Dieta', variant: 'success' },
      'signos_vitales': { text: 'Signos Vitales', variant: 'info' },
      'laboratorio': { text: 'Laboratorio', variant: 'warning' },
      'imagen': { text: 'Imagen', variant: 'secondary' },
      'interconsulta': { text: 'Interconsulta', variant: 'info' },
      'cuidados': { text: 'Cuidados', variant: 'success' },
      'otro': { text: 'Otro', variant: 'secondary' }
    }
    return badges[tipo] || { text: tipo, variant: 'secondary' }
  }

  /**
   * Obtener badge del estado de orden
   */
  function obtenerBadgeEstadoOrden(estado) {
    const badges = {
      'activa': { text: 'Activa', variant: 'success' },
      'suspendida': { text: 'Suspendida', variant: 'warning' },
      'completada': { text: 'Completada', variant: 'info' },
      'cancelada': { text: 'Cancelada', variant: 'danger' }
    }
    return badges[estado] || { text: estado, variant: 'secondary' }
  }

  /**
   * Obtener icono del tipo de orden
   */
  function obtenerIconoOrden(tipo) {
    const iconos = {
      'medicamento': '💊',
      'dieta': '🍽️',
      'signos_vitales': '❤️',
      'laboratorio': '🔬',
      'imagen': '📷',
      'interconsulta': '👨‍⚕️',
      'cuidados': '🩺',
      'otro': '📋'
    }
    return iconos[tipo] || '📋'
  }

  // ==========================================
  // UTILIDADES - REGISTRO ENFERMERÍA
  // ==========================================

  /**
   * Obtener badge del tipo de registro
   */
  function obtenerBadgeTipoRegistro(tipo) {
    const badges = {
      'signos_vitales': { text: 'Signos Vitales', variant: 'info' },
      'medicamento': { text: 'Medicamento', variant: 'primary' },
      'curacion': { text: 'Curación', variant: 'warning' },
      'nota': { text: 'Nota', variant: 'success' },
      'otro': { text: 'Otro', variant: 'secondary' }
    }
    return badges[tipo] || { text: tipo, variant: 'secondary' }
  }

  /**
   * Obtener icono del tipo de registro
   */
  function obtenerIconoRegistro(tipo) {
    const iconos = {
      'signos_vitales': '❤️',
      'medicamento': '💉',
      'curacion': '🩹',
      'nota': '📝',
      'otro': '📋'
    }
    return iconos[tipo] || '📋'
  }

  // ==========================================
  // UTILIDADES - FECHAS
  // ==========================================

  /**
   * Formatear fecha
   */
  function formatearFecha(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    return date.toLocaleDateString('es-GT', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  /**
   * Formatear fecha corta
   */
  function formatearFechaCorta(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    return date.toLocaleDateString('es-GT', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  }

  /**
   * Formatear fecha y hora
   */
  function formatearFechaHora(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    return date.toLocaleString('es-GT', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================

  return {
    // Estado - Camas
    camas,
    loadingCamas,
    camasDisponibles,
    camasOcupadas,
    camasEnLimpieza,
    camasEnMantenimiento,
    totalCamas,
    porcentajeOcupacion,
    
    // Estado - Hospitalizaciones
    hospitalizaciones,
    hospitalizacionActual,
    loadingHospitalizaciones,
    hospitalizacionesActivas,
    hospitalizacionesEgresadas,
    totalHospitalizaciones,
    
    // Estado - Notas, Órdenes, Registros
    notasMedicas,
    ordenesMedicas,
    registrosEnfermeria,
    ordenesActivas,
    
    // Estado - General
    loading,
    error,
    filters,
    
    // Métodos - Camas
    loadCamas,
    actualizarCama,
    
    // Métodos - Hospitalizaciones
    loadHospitalizaciones,
    loadHospitalizacion,
    ingresarPaciente,
    egresarPaciente,
    
    // Métodos - Notas
    agregarNota,
    
    // Métodos - Órdenes
    agregarOrden,
    suspenderOrden,
    
    // Métodos - Enfermería
    agregarRegistro,
    
    // Filtros
    aplicarFiltros,
    limpiarFiltros,
    
    // Utilidades - Camas
    obtenerBadgeEstadoCama,
    obtenerColorEstadoCama,
    obtenerIconoCama,
    
    // Utilidades - Hospitalizaciones
    obtenerBadgeEstadoHospitalizacion,
    calcularDiasEstancia,
    estaActiva,
    
    // Utilidades - Notas
    obtenerBadgeTipoNota,
    obtenerIconoNota,
    
    // Utilidades - Órdenes
    obtenerBadgeTipoOrden,
    obtenerBadgeEstadoOrden,
    obtenerIconoOrden,
    
    // Utilidades - Registros
    obtenerBadgeTipoRegistro,
    obtenerIconoRegistro,
    
    // Utilidades - Fechas
    formatearFecha,
    formatearFechaCorta,
    formatearFechaHora
  }
}
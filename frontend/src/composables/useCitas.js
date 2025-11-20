import { ref, computed } from 'vue'
import { useCitasStore } from '@/stores/citas'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de citas
 * Proporciona métodos y estado reactivo para componentes
 */
export function useCitas() {
  const store = useCitasStore()
  const router = useRouter()

  // ==========================================
  // COMPUTED PROPERTIES (desde el store)
  // ==========================================
  
  const citas = computed(() => store.citas)
  const citaActual = computed(() => store.citaActual)
  const tiposCita = computed(() => store.tiposCita)
  const horariosDisponibles = computed(() => store.horariosDisponibles)
  const loading = computed(() => store.loading)
  const error = computed(() => store.error)
  const filters = computed(() => store.filters)
  const hasCitas = computed(() => store.hasCitas)
  const hasActiveFilters = computed(() => store.hasActiveFilters)

  // ==========================================
  // MÉTODOS BÁSICOS (delegan al store)
  // ==========================================

  /**
   * Cargar lista de citas con filtros
   */
  async function loadCitas(params = {}) {
    try {
      await store.fetchCitas(params)
    } catch (err) {
      console.error('Error al cargar citas:', err)
    }
  }

  /**
   * Cargar citas del día actual
   */
  async function loadCitasHoy(medicoId = null) {
    try {
      await store.fetchCitasHoy(medicoId)
    } catch (err) {
      console.error('Error al cargar citas de hoy:', err)
    }
  }

  /**
   * Cargar una cita específica
   */
  async function loadCita(id) {
    try {
      await store.fetchCitaById(id)
    } catch (err) {
      console.error('Error al cargar cita:', err)
    }
  }

  /**
   * Crear nueva cita y opcionalmente redirigir
   */
  async function crearCita(data, redirigir = false) {
    try {
      const result = await store.createCita(data)
      
      if (result.success && redirigir) {
        router.push('/agenda')
      }
      
      return result
    } catch (err) {
      console.error('Error al crear cita:', err)
      throw err
    }
  }

  /**
   * Actualizar cita existente
   */
  async function actualizarCita(id, data) {
    try {
      const result = await store.updateCita(id, data)
      return result
    } catch (err) {
      console.error('Error al actualizar cita:', err)
      throw err
    }
  }

  /**
   * Cancelar cita con confirmación
   */
  async function cancelarCita(id, motivo = null, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm('¿Está seguro de cancelar esta cita?')
      if (!confirmado) return false
    }
    
    try {
      const result = await store.cancelarCita(id, motivo)
      return result
    } catch (err) {
      console.error('Error al cancelar cita:', err)
      throw err
    }
  }

  /**
   * Verificar disponibilidad de un médico
   */
  async function verificarDisponibilidad(medicoId, fecha, hora, duracionMinutos = 20) {
    try {
      const result = await store.verificarDisponibilidad(medicoId, fecha, hora, duracionMinutos)
      return result
    } catch (err) {
      console.error('Error al verificar disponibilidad:', err)
      return { disponible: false, mensaje: 'Error al verificar disponibilidad' }
    }
  }

  /**
   * Obtener horarios disponibles de un médico
   */
  async function cargarHorariosDisponibles(medicoId, fecha, duracionMinutos = 20) {
    try {
      const horarios = await store.fetchHorariosDisponibles(medicoId, fecha, duracionMinutos)
      return horarios
    } catch (err) {
      console.error('Error al cargar horarios:', err)
      return []
    }
  }

  /**
   * Cargar tipos de cita
   */
  async function cargarTiposCita() {
    try {
      await store.fetchTiposCita()
    } catch (err) {
      console.error('Error al cargar tipos de cita:', err)
    }
  }

  /**
   * Cargar estadísticas
   */
  async function cargarEstadisticas(params = {}) {
    try {
      const stats = await store.fetchEstadisticas(params)
      return stats
    } catch (err) {
      console.error('Error al cargar estadísticas:', err)
      return null
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

  /**
   * Filtrar citas por fecha
   */
  async function filtrarPorFecha(fechaInicio, fechaFin = null) {
    await aplicarFiltros({
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin
    })
  }

  /**
   * Filtrar citas por médico
   */
  async function filtrarPorMedico(medicoId) {
    await aplicarFiltros({ medico_id: medicoId })
  }

  /**
   * Filtrar citas por paciente
   */
  async function filtrarPorPaciente(pacienteId) {
    await aplicarFiltros({ paciente_id: pacienteId })
  }

  /**
   * Filtrar citas por estado
   */
  async function filtrarPorEstado(estado) {
    await aplicarFiltros({ estado })
  }

  // ==========================================
  // UTILIDADES DE FORMATO
  // ==========================================

  /**
   * Formatear fecha y hora para mostrar
   * @param {string} fechaHora - ISO string "2025-11-25T10:00:00"
   * @returns {string} - "25/11/2025 10:00"
   */
  function formatearFechaHora(fechaHora) {
    if (!fechaHora) return ''
    
    const fecha = new Date(fechaHora)
    const dia = fecha.getDate().toString().padStart(2, '0')
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0')
    const anio = fecha.getFullYear()
    const hora = fecha.getHours().toString().padStart(2, '0')
    const minutos = fecha.getMinutes().toString().padStart(2, '0')
    
    return `${dia}/${mes}/${anio} ${hora}:${minutos}`
  }

  /**
   * Formatear solo la fecha
   * @param {string} fechaHora - ISO string
   * @returns {string} - "25/11/2025"
   */
  function formatearFecha(fechaHora) {
    if (!fechaHora) return ''
    
    const fecha = new Date(fechaHora)
    const dia = fecha.getDate().toString().padStart(2, '0')
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0')
    const anio = fecha.getFullYear()
    
    return `${dia}/${mes}/${anio}`
  }

  /**
   * Formatear solo la hora
   * @param {string} fechaHora - ISO string
   * @returns {string} - "10:00"
   */
  function formatearHora(fechaHora) {
    if (!fechaHora) return ''
    
    const fecha = new Date(fechaHora)
    const hora = fecha.getHours().toString().padStart(2, '0')
    const minutos = fecha.getMinutes().toString().padStart(2, '0')
    
    return `${hora}:${minutos}`
  }

  /**
   * Convertir fecha y hora separadas a formato ISO para el backend
   * @param {string} fecha - "2025-11-25"
   * @param {string} hora - "10:00"
   * @returns {string} - "2025-11-25 10:00"
   */
  function combinarFechaHora(fecha, hora) {
    if (!fecha || !hora) return null
    return `${fecha} ${hora}`
  }

  /**
   * Obtener fecha de hoy en formato YYYY-MM-DD
   */
  function getFechaHoy() {
    const hoy = new Date()
    const anio = hoy.getFullYear()
    const mes = (hoy.getMonth() + 1).toString().padStart(2, '0')
    const dia = hoy.getDate().toString().padStart(2, '0')
    
    return `${anio}-${mes}-${dia}`
  }

  /**
   * Obtener nombre del estado de cita
   */
  function obtenerNombreEstado(estado) {
    const nombres = {
      'programada': 'Programada',
      'confirmada': 'Confirmada',
      'en_curso': 'En Curso',
      'completada': 'Completada',
      'cancelada': 'Cancelada',
      'no_asistio': 'No Asistió'
    }
    return nombres[estado] || estado
  }

  /**
   * Obtener variante de badge según estado
   */
  function obtenerVarianteEstado(estado) {
    const variantes = {
      'programada': 'info',      // Azul
      'confirmada': 'success',   // Verde
      'en_curso': 'warning',     // Amarillo
      'completada': 'secondary', // Gris
      'cancelada': 'error',      // Rojo
      'no_asistio': 'warning'    // Naranja
    }
    return variantes[estado] || 'secondary'
  }

  /**
   * Obtener color del tipo de cita
   */
  function obtenerColorTipoCita(tipoCitaId) {
    const tipo = store.getTipoCitaById(tipoCitaId)
    return tipo?.color || '#9333ea' // Lila por defecto
  }

  /**
   * Obtener nombre del tipo de cita
   */
  function obtenerNombreTipoCita(tipoCitaId) {
    const tipo = store.getTipoCitaById(tipoCitaId)
    return tipo?.nombre || 'Sin tipo'
  }

  // ==========================================
  // VALIDACIONES
  // ==========================================

  /**
   * Validar que la fecha no sea pasada
   */
  function validarFechaFutura(fecha) {
    const fechaCita = new Date(fecha)
    const hoy = new Date()
    hoy.setHours(0, 0, 0, 0)
    
    return fechaCita >= hoy
  }

  /**
   * Validar que la hora esté en formato correcto
   */
  function validarFormatoHora(hora) {
    const regex = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/
    return regex.test(hora)
  }

  /**
   * Validar que sea día laborable (Lunes-Sábado)
   */
  function esDiaLaborable(fecha) {
    // Asegurarse de que la fecha sea un objeto Date válido
    const date = new Date(fecha + 'T00:00:00') // Agregar hora para evitar problemas de zona horaria
    const diaSemana = date.getDay() // 0=Domingo, 1=Lunes, ..., 6=Sábado
    return diaSemana !== 0 // No es domingo
  }

  /**
   * Validar horario de atención
   * L-V: 8AM-5PM, Sábado: 8AM-1PM
   */
  function estaEnHorarioAtencion(fecha, hora) {
    // Asegurarse de que la fecha sea un objeto Date válido
    const date = new Date(fecha + 'T00:00:00')
    const diaSemana = date.getDay() // 0=Domingo, 1=Lunes, ..., 6=Sábado
    
    const [horas, minutos] = hora.split(':').map(Number)
    const horaDecimal = horas + minutos / 60
    
    if (diaSemana >= 1 && diaSemana <= 5) {
      // Lunes a Viernes: 8AM - 5PM
      return horaDecimal >= 8 && horaDecimal <= 17
    } else if (diaSemana === 6) {
      // Sábado: 8AM - 1PM
      return horaDecimal >= 8 && horaDecimal <= 13
    }
    
    return false // Domingo
  }

  // ==========================================
  // UTILIDADES DE CALENDARIO
  // ==========================================

  /**
   * Obtener eventos para FullCalendar
   */
  function getEventosCalendario() {
    return citas.value.map(cita => ({
      id: cita.id,
      title: cita.paciente?.nombre_completo || 'Sin paciente',
      start: cita.fecha_hora,
      end: calcularFechaFin(cita.fecha_hora, cita.duracion_minutos),
      backgroundColor: obtenerColorTipoCita(cita.tipo_cita_id),
      borderColor: obtenerColorTipoCita(cita.tipo_cita_id),
      extendedProps: {
        pacienteId: cita.paciente_id,
        medicoId: cita.medico_id,
        estado: cita.estado,
        motivo: cita.motivo,
        tipo: cita.tipo_cita?.nombre
      }
    }))
  }

  /**
   * Calcular fecha/hora de fin de la cita
   */
  function calcularFechaFin(fechaInicio, duracionMinutos) {
    const inicio = new Date(fechaInicio)
    const fin = new Date(inicio.getTime() + duracionMinutos * 60000)
    return fin.toISOString()
  }

  /**
   * Obtener nombre del día de la semana
   */
  function obtenerNombreDia(fecha) {
    const date = new Date(fecha + 'T00:00:00')
    const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    return dias[date.getDay()]
  }

  /**
   * Verificar si una cita puede ser editada
   */
  function puedeEditarCita(cita) {
    // No se pueden editar citas completadas o muy antiguas
    if (cita.estado === 'completada') return false
    if (cita.estado === 'cancelada') return false
    
    const fechaCita = new Date(cita.fecha_hora)
    const ahora = new Date()
    
    // No editar citas pasadas
    return fechaCita >= ahora
  }

  /**
   * Verificar si una cita puede ser cancelada
   */
  function puedeCancelarCita(cita) {
    return cita.estado === 'programada' || cita.estado === 'confirmada'
  }

  /**
   * Verificar si una cita está próxima (dentro de 1 hora)
   */
  function esCitaProxima(cita) {
    const fechaCita = new Date(cita.fecha_hora)
    const ahora = new Date()
    const diferenciaMs = fechaCita - ahora
    const diferenciaHoras = diferenciaMs / (1000 * 60 * 60)
    
    return diferenciaHoras > 0 && diferenciaHoras <= 1
  }

  // ==========================================
  // ESTADÍSTICAS RÁPIDAS
  // ==========================================

  /**
   * Contar citas por estado
   */
  function contarPorEstado(estado) {
    return citas.value.filter(c => c.estado === estado).length
  }

  /**
   * Obtener citas del día
   */
  function getCitasDelDia(fecha = null) {
    const fechaBuscar = fecha || getFechaHoy()
    return citas.value.filter(c => {
      const fechaCita = c.fecha_hora.split('T')[0]
      return fechaCita === fechaBuscar
    })
  }

  /**
   * Obtener próximas citas (ordenadas por fecha)
   */
  function getProximasCitas(limite = 5) {
    const ahora = new Date()
    return citas.value
      .filter(c => new Date(c.fecha_hora) >= ahora && c.estado !== 'cancelada')
      .sort((a, b) => new Date(a.fecha_hora) - new Date(b.fecha_hora))
      .slice(0, limite)
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================

  return {
    // Estado
    citas,
    citaActual,
    tiposCita,
    horariosDisponibles,
    loading,
    error,
    filters,
    hasCitas,
    hasActiveFilters,
    
    // CRUD
    loadCitas,
    loadCitasHoy,
    loadCita,
    crearCita,
    actualizarCita,
    cancelarCita,
    
    // Disponibilidad
    verificarDisponibilidad,
    cargarHorariosDisponibles,
    cargarTiposCita,
    cargarEstadisticas,
    
    // Filtros
    aplicarFiltros,
    limpiarFiltros,
    filtrarPorFecha,
    filtrarPorMedico,
    filtrarPorPaciente,
    filtrarPorEstado,
    
    // Formato
    formatearFechaHora,
    formatearFecha,
    formatearHora,
    combinarFechaHora,
    getFechaHoy,
    obtenerNombreEstado,
    obtenerVarianteEstado,
    obtenerColorTipoCita,
    obtenerNombreTipoCita,
    
    // Validaciones
    validarFechaFutura,
    validarFormatoHora,
    esDiaLaborable,
    estaEnHorarioAtencion,
    
    // Calendario
    getEventosCalendario,
    calcularFechaFin,
    obtenerNombreDia,
    puedeEditarCita,
    puedeCancelarCita,
    esCitaProxima,
    
    // Estadísticas
    contarPorEstado,
    getCitasDelDia,
    getProximasCitas
  }
}
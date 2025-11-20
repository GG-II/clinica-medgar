import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { citasAPI } from '@/api/citas.api'

export const useCitasStore = defineStore('citas', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  const citas = ref([])
  const citaActual = ref(null)
  const tiposCita = ref([])
  const horariosDisponibles = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // Filtros activos
  const filters = ref({
    fecha_inicio: null,
    fecha_fin: null,
    medico_id: null,
    paciente_id: null,
    estado: null
  })

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Obtener cita por ID desde la lista en memoria
   */
  const getCitaById = computed(() => {
    return (id) => {
      return citas.value.find(c => c.id === parseInt(id))
    }
  })
  
  /**
   * Obtener solo citas activas (no canceladas)
   */
  const getCitasActivas = computed(() => {
    return citas.value.filter(c => c.estado !== 'cancelada')
  })
  
  /**
   * Obtener citas por estado
   */
  const getCitasByEstado = computed(() => {
    return (estado) => {
      return citas.value.filter(c => c.estado === estado)
    }
  })
  
  /**
   * Obtener citas de hoy
   */
  const getCitasHoy = computed(() => {
    const hoy = new Date().toISOString().split('T')[0]
    return citas.value.filter(c => {
      if (!c.fecha_hora) return false
      const fechaCita = c.fecha_hora.split('T')[0]
      return fechaCita === hoy
    })
  })
  
  /**
   * Total de citas
   */
  const totalCitas = computed(() => citas.value.length)
  
  /**
   * Verificar si hay citas cargadas
   */
  const hasCitas = computed(() => citas.value.length > 0)
  
  /**
   * Verificar si hay filtros activos
   */
  const hasActiveFilters = computed(() => {
    return filters.value.fecha_inicio !== null ||
           filters.value.fecha_fin !== null ||
           filters.value.medico_id !== null ||
           filters.value.paciente_id !== null ||
           filters.value.estado !== null
  })

  /**
   * Obtener tipo de cita por ID
   */
  const getTipoCitaById = computed(() => {
    return (id) => {
      return tiposCita.value.find(t => t.id === parseInt(id))
    }
  })

  // ==========================================
  // ACTIONS (Métodos)
  // ==========================================

  /**
   * Obtener lista de citas con filtros
   */
  async function fetchCitas(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      // Combinar filtros activos con parámetros adicionales
      const queryParams = {
        ...filters.value,
        ...params
      }
      
      // Limpiar parámetros null/undefined
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === undefined) {
          delete queryParams[key]
        }
      })
      
      const response = await citasAPI.getAll(queryParams)
      
      if (response.data.success) {
        citas.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar citas'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener citas del día actual
   */
  async function fetchCitasHoy(medicoId = null) {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.getHoy(medicoId)
      
      if (response.data.success) {
        citas.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar citas de hoy'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener una cita específica por ID
   */
  async function fetchCitaById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.getById(id)
      
      if (response.data.success) {
        citaActual.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar cita'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear una nueva cita
   */
  async function createCita(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.create(data)
      
      if (response.data.success) {
        // Agregar la nueva cita a la lista local
        citas.value.push(response.data.data)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear cita'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar una cita existente
   */
  async function updateCita(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.update(id, data)
      
      if (response.data.success) {
        // Actualizar en la lista local
        const index = citas.value.findIndex(c => c.id === parseInt(id))
        if (index !== -1) {
          citas.value[index] = response.data.data
        }
        
        // Actualizar cita actual si es la misma
        if (citaActual.value?.id === parseInt(id)) {
          citaActual.value = response.data.data
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar cita'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Cancelar una cita
   */
  async function cancelarCita(id, motivo = null) {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.delete(id, motivo)
      
      if (response.data.success) {
        // Actualizar estado en lista local
        const index = citas.value.findIndex(c => c.id === parseInt(id))
        if (index !== -1) {
          citas.value[index].estado = 'cancelada'
        }
        
        // Actualizar cita actual si es la misma
        if (citaActual.value?.id === parseInt(id)) {
          citaActual.value.estado = 'cancelada'
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cancelar cita'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Verificar disponibilidad de un médico en una hora específica
   */
  async function verificarDisponibilidad(medicoId, fecha, hora, duracionMinutos = 20) {
    try {
      const response = await citasAPI.verificarDisponibilidad(medicoId, fecha, hora, duracionMinutos)
      
      if (response.data.success) {
        return {
          disponible: response.data.disponible,
          mensaje: response.data.mensaje
        }
      }
      
      return { disponible: false, mensaje: 'Error al verificar disponibilidad' }
    } catch (err) {
      console.error('Error al verificar disponibilidad:', err)
      return { disponible: false, mensaje: 'Error al verificar disponibilidad' }
    }
  }

  /**
   * Obtener horarios disponibles de un médico en una fecha
   */
  async function fetchHorariosDisponibles(medicoId, fecha, duracionMinutos = 20) {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.getHorariosDisponibles(medicoId, fecha, duracionMinutos)
      
      if (response.data.success) {
        horariosDisponibles.value = response.data.horarios_disponibles
        return response.data.horarios_disponibles
      }
      
      return []
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar horarios'
      horariosDisponibles.value = []
      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener tipos de cita
   */
  async function fetchTiposCita() {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.getTipos()
      
      if (response.data.success) {
        tiposCita.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar tipos de cita'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener estadísticas de citas
   */
  async function fetchEstadisticas(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await citasAPI.getEstadisticas(params)
      
      if (response.data.success) {
        return response.data.data
      }
      
      return null
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar estadísticas'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Aplicar filtros y recargar lista
   */
  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    await fetchCitas()
  }

  /**
   * Limpiar todos los filtros
   */
  async function clearFilters() {
    filters.value = {
      fecha_inicio: null,
      fecha_fin: null,
      medico_id: null,
      paciente_id: null,
      estado: null
    }
    await fetchCitas()
  }

  /**
   * Limpiar horarios disponibles
   */
  function clearHorariosDisponibles() {
    horariosDisponibles.value = []
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    citas.value = []
    citaActual.value = null
    tiposCita.value = []
    horariosDisponibles.value = []
    loading.value = false
    error.value = null
    filters.value = {
      fecha_inicio: null,
      fecha_fin: null,
      medico_id: null,
      paciente_id: null,
      estado: null
    }
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State
    citas,
    citaActual,
    tiposCita,
    horariosDisponibles,
    loading,
    error,
    filters,
    
    // Getters
    getCitaById,
    getCitasActivas,
    getCitasByEstado,
    getCitasHoy,
    totalCitas,
    hasCitas,
    hasActiveFilters,
    getTipoCitaById,
    
    // Actions
    fetchCitas,
    fetchCitasHoy,
    fetchCitaById,
    createCita,
    updateCita,
    cancelarCita,
    verificarDisponibilidad,
    fetchHorariosDisponibles,
    fetchTiposCita,
    fetchEstadisticas,
    setFilters,
    clearFilters,
    clearHorariosDisponibles,
    resetStore
  }
})
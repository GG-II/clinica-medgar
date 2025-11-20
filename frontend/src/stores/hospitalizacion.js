import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { hospitalizacionAPI } from '@/api/hospitalizacion.api'

export const useHospitalizacionStore = defineStore('hospitalizacion', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  // Camas
  const camas = ref([])
  const loadingCamas = ref(false)
  
  // Hospitalizaciones
  const hospitalizaciones = ref([])
  const hospitalizacionActual = ref(null)
  const loadingHospitalizaciones = ref(false)
  
  // Notas médicas
  const notasMedicas = ref([])
  
  // Órdenes médicas
  const ordenesMedicas = ref([])
  
  // Registros de enfermería
  const registrosEnfermeria = ref([])
  
  // General
  const loading = ref(false)
  const error = ref(null)
  
  // Filtros
  const filters = ref({
    estado: null,
    paciente_id: null,
    fecha_inicio: null,
    fecha_fin: null
  })

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Obtener camas disponibles
   */
  const camasDisponibles = computed(() => {
    return camas.value.filter(c => c.estado === 'disponible')
  })
  
  /**
   * Obtener camas ocupadas
   */
  const camasOcupadas = computed(() => {
    return camas.value.filter(c => c.estado === 'ocupada')
  })
  
  /**
   * Obtener camas en limpieza
   */
  const camasEnLimpieza = computed(() => {
    return camas.value.filter(c => c.estado === 'limpieza')
  })
  
  /**
   * Obtener camas en mantenimiento
   */
  const camasEnMantenimiento = computed(() => {
    return camas.value.filter(c => c.estado === 'mantenimiento')
  })
  
  /**
   * Total de camas
   */
  const totalCamas = computed(() => camas.value.length)
  
  /**
   * Porcentaje de ocupación
   */
  const porcentajeOcupacion = computed(() => {
    if (totalCamas.value === 0) return 0
    return Math.round((camasOcupadas.value.length / totalCamas.value) * 100)
  })
  
  /**
   * Obtener hospitalizaciones activas
   */
  const hospitalizacionesActivas = computed(() => {
    return hospitalizaciones.value.filter(h => h.estado === 'activo')
  })
  
  /**
   * Obtener hospitalizaciones egresadas
   */
  const hospitalizacionesEgresadas = computed(() => {
    return hospitalizaciones.value.filter(h => h.estado === 'egresado')
  })
  
  /**
   * Total de hospitalizaciones
   */
  const totalHospitalizaciones = computed(() => hospitalizaciones.value.length)
  
  /**
   * Obtener cama por ID
   */
  const getCamaById = computed(() => {
    return (id) => {
      return camas.value.find(c => c.id === parseInt(id))
    }
  })
  
  /**
   * Obtener hospitalización por ID
   */
  const getHospitalizacionById = computed(() => {
    return (id) => {
      return hospitalizaciones.value.find(h => h.id === parseInt(id))
    }
  })
  
  /**
   * Obtener órdenes médicas activas
   */
  const ordenesActivas = computed(() => {
    return ordenesMedicas.value.filter(o => o.estado === 'activa')
  })
  
  /**
   * Obtener notas médicas por tipo
   */
  const getNotasByTipo = computed(() => {
    return (tipo) => {
      return notasMedicas.value.filter(n => n.tipo_nota === tipo)
    }
  })

  // ==========================================
  // ACTIONS - CAMAS
  // ==========================================

  /**
   * Obtener lista de camas
   */
  async function fetchCamas(params = {}) {
    loadingCamas.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.getCamas(params)
      
      if (response.data.success) {
        camas.value = response.data.camas || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar camas'
      throw err
    } finally {
      loadingCamas.value = false
    }
  }

  /**
   * Actualizar estado de una cama
   */
  async function updateCama(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.updateCama(id, data)
      
      if (response.data.success) {
        // Actualizar en la lista local
        const index = camas.value.findIndex(c => c.id === parseInt(id))
        if (index !== -1) {
          camas.value[index] = response.data.cama
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar cama'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - HOSPITALIZACIONES
  // ==========================================

  /**
   * Obtener lista de hospitalizaciones
   */
  async function fetchHospitalizaciones(params = {}) {
    loadingHospitalizaciones.value = true
    error.value = null
    
    try {
      const queryParams = {
        ...filters.value,
        ...params
      }
      
      const response = await hospitalizacionAPI.getHospitalizaciones(queryParams)
      
      if (response.data.success) {
        hospitalizaciones.value = response.data.hospitalizaciones || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar hospitalizaciones'
      throw err
    } finally {
      loadingHospitalizaciones.value = false
    }
  }

  /**
   * Obtener una hospitalización específica
   */
  async function fetchHospitalizacionById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.getHospitalizacionById(id)
      
      if (response.data.success) {
        hospitalizacionActual.value = response.data.hospitalizacion
        notasMedicas.value = response.data.notas_medicas || []
        ordenesMedicas.value = response.data.ordenes_medicas || []
        registrosEnfermeria.value = response.data.registros_enfermeria || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar hospitalización'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Ingresar paciente a hospitalización
   */
  async function ingresarPaciente(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.ingresarPaciente(data)
      
      if (response.data.success) {
        // Agregar a la lista local
        hospitalizaciones.value.unshift(response.data.hospitalizacion)
        
        // Actualizar la cama ocupada
        const cama = camas.value.find(c => c.id === data.cama_id)
        if (cama) {
          cama.estado = 'ocupada'
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al ingresar paciente'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Egresar paciente de hospitalización
   */
  async function egresarPaciente(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.egresarPaciente(id, data)
      
      if (response.data.success) {
        const hospitalizacion = response.data.hospitalizacion
        
        // Actualizar en la lista local
        const index = hospitalizaciones.value.findIndex(h => h.id === parseInt(id))
        if (index !== -1) {
          hospitalizaciones.value[index] = hospitalizacion
        }
        
        // Actualizar hospitalización actual si es la misma
        if (hospitalizacionActual.value?.id === parseInt(id)) {
          hospitalizacionActual.value = hospitalizacion
        }
        
        // Liberar la cama
        const cama = camas.value.find(c => c.id === hospitalizacion.cama_id)
        if (cama) {
          cama.estado = 'disponible'
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al egresar paciente'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - NOTAS MÉDICAS
  // ==========================================

  /**
   * Agregar nota médica
   */
  async function agregarNotaMedica(hospitalizacionId, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.agregarNotaMedica(hospitalizacionId, data)
      
      if (response.data.success) {
        // Agregar a la lista local
        notasMedicas.value.unshift(response.data.nota)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al agregar nota médica'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - ÓRDENES MÉDICAS
  // ==========================================

  /**
   * Agregar orden médica
   */
  async function agregarOrdenMedica(hospitalizacionId, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.agregarOrdenMedica(hospitalizacionId, data)
      
      if (response.data.success) {
        // Agregar a la lista local
        ordenesMedicas.value.unshift(response.data.orden)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al agregar orden médica'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Suspender orden médica
   */
  async function suspenderOrden(ordenId, motivo = null) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.suspenderOrden(ordenId, { motivo })
      
      if (response.data.success) {
        // Actualizar en la lista local
        const index = ordenesMedicas.value.findIndex(o => o.id === parseInt(ordenId))
        if (index !== -1) {
          ordenesMedicas.value[index] = response.data.orden
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al suspender orden'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - REGISTRO ENFERMERÍA
  // ==========================================

  /**
   * Agregar registro de enfermería
   */
  async function agregarRegistroEnfermeria(hospitalizacionId, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await hospitalizacionAPI.agregarRegistroEnfermeria(hospitalizacionId, data)
      
      if (response.data.success) {
        // Agregar a la lista local
        registrosEnfermeria.value.unshift(response.data.registro)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al agregar registro de enfermería'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - FILTROS Y UTILIDADES
  // ==========================================

  /**
   * Aplicar filtros
   */
  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    await fetchHospitalizaciones()
  }

  /**
   * Limpiar filtros
   */
  async function clearFilters() {
    filters.value = {
      estado: null,
      paciente_id: null,
      fecha_inicio: null,
      fecha_fin: null
    }
    await fetchHospitalizaciones()
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    camas.value = []
    hospitalizaciones.value = []
    hospitalizacionActual.value = null
    notasMedicas.value = []
    ordenesMedicas.value = []
    registrosEnfermeria.value = []
    error.value = null
    clearFilters()
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State - Camas
    camas,
    loadingCamas,
    
    // State - Hospitalizaciones
    hospitalizaciones,
    hospitalizacionActual,
    loadingHospitalizaciones,
    
    // State - Notas, Órdenes, Registros
    notasMedicas,
    ordenesMedicas,
    registrosEnfermeria,
    
    // State - General
    loading,
    error,
    filters,
    
    // Getters - Camas
    camasDisponibles,
    camasOcupadas,
    camasEnLimpieza,
    camasEnMantenimiento,
    totalCamas,
    porcentajeOcupacion,
    getCamaById,
    
    // Getters - Hospitalizaciones
    hospitalizacionesActivas,
    hospitalizacionesEgresadas,
    totalHospitalizaciones,
    getHospitalizacionById,
    
    // Getters - Órdenes y Notas
    ordenesActivas,
    getNotasByTipo,
    
    // Actions - Camas
    fetchCamas,
    updateCama,
    
    // Actions - Hospitalizaciones
    fetchHospitalizaciones,
    fetchHospitalizacionById,
    ingresarPaciente,
    egresarPaciente,
    
    // Actions - Notas
    agregarNotaMedica,
    
    // Actions - Órdenes
    agregarOrdenMedica,
    suspenderOrden,
    
    // Actions - Enfermería
    agregarRegistroEnfermeria,
    
    // Actions - Utilidades
    setFilters,
    clearFilters,
    resetStore
  }
})
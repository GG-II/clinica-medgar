import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { laboratoriosAPI } from '@/api/laboratorios.api'

export const useLaboratoriosStore = defineStore('laboratorios', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  const laboratorios = ref([])
  const laboratorioActual = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Tipos y catálogos
  const tipos = ref([])
  const tiposPorCategoria = ref({})
  const categorias = ref([])
  const valoresReferencia = ref([])
  
  // Histórico y comparaciones
  const historicoParametro = ref([])
  const comparacion = ref(null)
  
  // Filtros activos
  const filters = ref({
    paciente_id: null,
    medico_id: null,
    estado: null,
    tipo_laboratorio_id: null
  })

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Obtener laboratorio por ID desde la lista en memoria
   */
  const getLaboratorioById = computed(() => {
    return (id) => {
      return laboratorios.value.find(l => l.id === parseInt(id))
    }
  })
  
  /**
   * Obtener solo laboratorios completados
   */
  const getLaboratoriosCompletados = computed(() => {
    return laboratorios.value.filter(l => l.estado === 'completado')
  })
  
  /**
   * Obtener solo laboratorios solicitados
   */
  const getLaboratoriosSolicitados = computed(() => {
    return laboratorios.value.filter(l => l.estado === 'solicitado')
  })
  
  /**
   * Obtener solo laboratorios en proceso
   */
  const getLaboratoriosEnProceso = computed(() => {
    return laboratorios.value.filter(l => l.estado === 'en_proceso')
  })
  
  /**
   * Total de laboratorios
   */
  const totalLaboratorios = computed(() => laboratorios.value.length)
  
  /**
   * Verificar si hay laboratorios cargados
   */
  const hasLaboratorios = computed(() => laboratorios.value.length > 0)
  
  /**
   * Verificar si hay filtros activos
   */
  const hasActiveFilters = computed(() => {
    return filters.value.paciente_id !== null ||
           filters.value.medico_id !== null ||
           filters.value.estado !== null ||
           filters.value.tipo_laboratorio_id !== null
  })
  
  /**
   * Obtener tipos agrupados por categoría
   */
  const getTiposPorCategoria = computed(() => tiposPorCategoria.value)

  // ==========================================
  // ACTIONS - CRUD BÁSICO
  // ==========================================

  /**
   * Obtener lista de laboratorios con filtros
   */
  async function fetchLaboratorios(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      // Combinar filtros activos con parámetros adicionales
      const queryParams = {
        ...filters.value,
        ...params
      }
      
      const response = await laboratoriosAPI.getAll(queryParams)
      
      if (response.data.success) {
        laboratorios.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar laboratorios'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener un laboratorio específico por ID
   */
  async function fetchLaboratorioById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.getById(id)
      
      if (response.data.success) {
        laboratorioActual.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar laboratorio'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Solicitar un nuevo laboratorio
   */
  async function createLaboratorio(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.create(data)
      
      if (response.data.success) {
        // Agregar el nuevo laboratorio a la lista local
        laboratorios.value.unshift(response.data.data)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al solicitar laboratorio'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Registrar resultados de un laboratorio
   */
  async function registrarResultados(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.registrarResultados(id, data)
      
      if (response.data.success) {
        // Actualizar en la lista local
        const index = laboratorios.value.findIndex(l => l.id === parseInt(id))
        if (index !== -1) {
          laboratorios.value[index] = response.data.data
        }
        
        // Actualizar laboratorio actual si es el mismo
        if (laboratorioActual.value?.id === parseInt(id)) {
          laboratorioActual.value = response.data.data
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrar resultados'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Cancelar un laboratorio
   */
  async function cancelarLaboratorio(id, motivo = null) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.cancelar(id, { motivo })
      
      if (response.data.success) {
        // Actualizar estado en la lista local
        const index = laboratorios.value.findIndex(l => l.id === parseInt(id))
        if (index !== -1) {
          laboratorios.value[index].estado = 'cancelado'
        }
        
        // Actualizar laboratorio actual si es el mismo
        if (laboratorioActual.value?.id === parseInt(id)) {
          laboratorioActual.value.estado = 'cancelado'
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cancelar laboratorio'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - HISTORIAL Y COMPARACIÓN
  // ==========================================

  /**
   * Obtener historial de laboratorios de un paciente
   */
  async function fetchLaboratoriosPaciente(pacienteId, soloCompletados = false) {
    loading.value = true
    error.value = null
    
    try {
      const params = soloCompletados ? { completados: true } : {}
      const response = await laboratoriosAPI.getByPaciente(pacienteId, params)
      
      if (response.data.success) {
        laboratorios.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al obtener historial'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener histórico de un parámetro para gráficas
   */
  async function fetchHistoricoParametro(pacienteId, tipoLaboratorioId, parametro, limite = 10) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.getHistoricoParametro(
        pacienteId,
        tipoLaboratorioId,
        parametro,
        { limite }
      )
      
      if (response.data.success) {
        historicoParametro.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al obtener histórico'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Comparar últimos 3 resultados
   */
  async function fetchComparacion(pacienteId, tipoLaboratorioId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.comparar(pacienteId, tipoLaboratorioId)
      
      if (response.data.success) {
        comparacion.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al comparar resultados'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - TIPOS Y CATÁLOGOS
  // ==========================================

  /**
   * Obtener tipos de laboratorio
   */
  async function fetchTipos(categoria = null) {
    loading.value = true
    error.value = null
    
    try {
      const params = categoria ? { categoria } : {}
      const response = await laboratoriosAPI.getTipos(params)
      
      if (response.data.success) {
        tipos.value = response.data.data
        tiposPorCategoria.value = response.data.por_categoria || {}
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar tipos'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener un tipo específico con valores de referencia
   */
  async function fetchTipoById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.getTipoById(id)
      
      if (response.data.success) {
        valoresReferencia.value = response.data.data.valores_referencia || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar tipo'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener valores de referencia
   */
  async function fetchValoresReferencia(params) {
    loading.value = true
    error.value = null
    
    try {
      const response = await laboratoriosAPI.getValoresReferencia(params)
      
      if (response.data.success) {
        valoresReferencia.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al obtener valores de referencia'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener categorías disponibles
   */
  async function fetchCategorias() {
    try {
      const response = await laboratoriosAPI.getCategorias()
      
      if (response.data.success) {
        categorias.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      console.error('Error al obtener categorías:', err)
      return null
    }
  }

  // ==========================================
  // ACTIONS - FILTROS
  // ==========================================

  /**
   * Aplicar filtros y recargar lista
   */
  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    await fetchLaboratorios()
  }

  /**
   * Limpiar todos los filtros
   */
  async function clearFilters() {
    filters.value = {
      paciente_id: null,
      medico_id: null,
      estado: null,
      tipo_laboratorio_id: null
    }
    await fetchLaboratorios()
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    laboratorios.value = []
    laboratorioActual.value = null
    loading.value = false
    error.value = null
    tipos.value = []
    tiposPorCategoria.value = {}
    categorias.value = []
    valoresReferencia.value = []
    historicoParametro.value = []
    comparacion.value = null
    filters.value = {
      paciente_id: null,
      medico_id: null,
      estado: null,
      tipo_laboratorio_id: null
    }
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State
    laboratorios,
    laboratorioActual,
    loading,
    error,
    tipos,
    tiposPorCategoria,
    categorias,
    valoresReferencia,
    historicoParametro,
    comparacion,
    filters,
    
    // Getters
    getLaboratorioById,
    getLaboratoriosCompletados,
    getLaboratoriosSolicitados,
    getLaboratoriosEnProceso,
    totalLaboratorios,
    hasLaboratorios,
    hasActiveFilters,
    getTiposPorCategoria,
    
    // Actions - CRUD
    fetchLaboratorios,
    fetchLaboratorioById,
    createLaboratorio,
    registrarResultados,
    cancelarLaboratorio,
    
    // Actions - Historial
    fetchLaboratoriosPaciente,
    fetchHistoricoParametro,
    fetchComparacion,
    
    // Actions - Catálogos
    fetchTipos,
    fetchTipoById,
    fetchValoresReferencia,
    fetchCategorias,
    
    // Actions - Filtros
    setFilters,
    clearFilters,
    resetStore
  }
})
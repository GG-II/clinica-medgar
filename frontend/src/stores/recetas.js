import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { recetasAPI } from '@/api/recetas.api'

export const useRecetasStore = defineStore('recetas', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  const recetas = ref([])
  const recetaActual = ref(null)
  const medicamentos = ref([])
  const medicamentoActual = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Filtros activos
  const filters = ref({
    paciente_id: null,
    medico_id: null,
    activas: null
  })

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Obtener receta por ID desde la lista en memoria
   */
  const getRecetaById = computed(() => {
    return (id) => {
      return recetas.value.find(r => r.id === parseInt(id))
    }
  })
  
  /**
   * Obtener solo recetas activas
   */
  const getRecetasActivas = computed(() => {
    return recetas.value.filter(r => r.activa)
  })
  
  /**
   * Obtener medicamento por ID desde la lista en memoria
   */
  const getMedicamentoById = computed(() => {
    return (id) => {
      return medicamentos.value.find(m => m.id === parseInt(id))
    }
  })
  
  /**
   * Total de recetas
   */
  const totalRecetas = computed(() => recetas.value.length)
  
  /**
   * Verificar si hay recetas cargadas
   */
  const hasRecetas = computed(() => recetas.value.length > 0)
  
  /**
   * Verificar si hay filtros activos
   */
  const hasActiveFilters = computed(() => {
    return filters.value.paciente_id !== null ||
           filters.value.medico_id !== null ||
           filters.value.activas !== null
  })

  // ==========================================
  // ACTIONS (Métodos)
  // ==========================================

  /**
   * Obtener lista de recetas con filtros
   */
  async function fetchRecetas(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      // Combinar filtros activos con parámetros adicionales
      const queryParams = {
        ...filters.value,
        ...params
      }
      
      const response = await recetasAPI.getAll(queryParams)
      
      if (response.data.success) {
        recetas.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar recetas'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener una receta específica por ID
   */
  async function fetchRecetaById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await recetasAPI.getById(id)
      
      if (response.data.success) {
        recetaActual.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar receta'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear una nueva receta
   */
  async function createReceta(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await recetasAPI.create(data)
      
      if (response.data.success) {
        // Agregar la nueva receta a la lista local
        recetas.value.unshift(response.data.data)
        
        // Guardar warnings de alergias si existen
        if (response.data.warning) {
          return {
            ...response.data,
            hasWarning: true
          }
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear receta'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Descargar PDF de una receta
   */
  async function downloadPDF(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await recetasAPI.downloadPDF(id)
      
      // Crear un blob URL para descargar el archivo
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `receta_${id}.pdf`
      link.click()
      window.URL.revokeObjectURL(url)
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al descargar PDF'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Desactivar una receta
   */
  async function desactivarReceta(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await recetasAPI.desactivar(id)
      
      if (response.data.success) {
        // Actualizar en la lista local
        const index = recetas.value.findIndex(r => r.id === parseInt(id))
        if (index !== -1) {
          recetas.value[index].activa = false
        }
        
        // Actualizar receta actual si es la misma
        if (recetaActual.value?.id === parseInt(id)) {
          recetaActual.value.activa = false
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al desactivar receta'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener historial de recetas de un paciente
   */
  async function fetchRecetasByPaciente(pacienteId, soloActivas = false) {
    loading.value = true
    error.value = null
    
    try {
      const params = soloActivas ? { activas: true } : {}
      const response = await recetasAPI.getByPaciente(pacienteId, params)
      
      if (response.data.success) {
        recetas.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar historial de recetas'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Buscar medicamentos (para autocomplete)
   */
  async function searchMedicamentos(query, limit = 10) {
    if (!query || query.length < 2) {
      return []
    }
    
    try {
      const response = await recetasAPI.searchMedicamentos(query, limit)
      
      if (response.data.success) {
        medicamentos.value = response.data.data
        return response.data.data
      }
      
      return []
    } catch (err) {
      console.error('Error en búsqueda de medicamentos:', err)
      return []
    }
  }

  /**
   * Obtener información completa de un medicamento
   */
  async function fetchMedicamentoById(id) {
    try {
      const response = await recetasAPI.getMedicamentoById(id)
      
      if (response.data.success) {
        medicamentoActual.value = response.data.data
        return response.data.data
      }
      
      return null
    } catch (err) {
      console.error('Error al obtener medicamento:', err)
      return null
    }
  }

  /**
   * Crear un medicamento personalizado
   */
  async function createMedicamento(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await recetasAPI.createMedicamento(data)
      
      if (response.data.success) {
        // Agregar el nuevo medicamento a la lista local
        medicamentos.value.unshift(response.data.data)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear medicamento'
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
    await fetchRecetas()
  }

  /**
   * Limpiar todos los filtros
   */
  async function clearFilters() {
    filters.value = {
      paciente_id: null,
      medico_id: null,
      activas: null
    }
    await fetchRecetas()
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    recetas.value = []
    recetaActual.value = null
    medicamentos.value = []
    medicamentoActual.value = null
    loading.value = false
    error.value = null
    filters.value = {
      paciente_id: null,
      medico_id: null,
      activas: null
    }
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State
    recetas,
    recetaActual,
    medicamentos,
    medicamentoActual,
    loading,
    error,
    filters,
    
    // Getters
    getRecetaById,
    getRecetasActivas,
    getMedicamentoById,
    totalRecetas,
    hasRecetas,
    hasActiveFilters,
    
    // Actions
    fetchRecetas,
    fetchRecetaById,
    createReceta,
    downloadPDF,
    desactivarReceta,
    fetchRecetasByPaciente,
    searchMedicamentos,
    fetchMedicamentoById,
    createMedicamento,
    setFilters,
    clearFilters,
    resetStore
  }
})
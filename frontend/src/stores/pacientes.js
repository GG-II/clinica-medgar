import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { pacientesAPI } from '@/api/pacientes.api'

export const usePacientesStore = defineStore('pacientes', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  const pacientes = ref([])
  const pacienteActual = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Paginación
  const pagination = ref({
    page: 1,
    perPage: 25,
    total: 0,
    totalPages: 0
  })
  
  // Filtros activos
  const filters = ref({
    search: '',
    sexo: null,
    tieneIGSS: null,
    edadMin: null,
    edadMax: null
  })

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Obtener paciente por ID desde la lista en memoria
   */
  const getPacienteById = computed(() => {
    return (id) => {
      return pacientes.value.find(p => p.id === parseInt(id))
    }
  })
  
  /**
   * Obtener solo pacientes activos
   */
  const getPacientesActivos = computed(() => {
    return pacientes.value.filter(p => p.activo)
  })
  
  /**
   * Total de pacientes
   */
  const totalPacientes = computed(() => pagination.value.total)
  
  /**
   * Verificar si hay pacientes cargados
   */
  const hasPacientes = computed(() => pacientes.value.length > 0)
  
  /**
   * Verificar si hay filtros activos
   */
  const hasActiveFilters = computed(() => {
    return filters.value.search !== '' ||
           filters.value.sexo !== null ||
           filters.value.tieneIGSS !== null ||
           filters.value.edadMin !== null ||
           filters.value.edadMax !== null
  })

  // ==========================================
  // ACTIONS (Métodos)
  // ==========================================

  /**
 * Obtener lista de pacientes con paginación
 */
async function fetchPacientes(params = {}) {
  loading.value = true
  error.value = null
  
  try {
    // Combinar parámetros de paginación y filtros
    const queryParams = {
      page: pagination.value.page,
      per_page: pagination.value.perPage,
      ...filters.value,
      ...params
    }
    
    const response = await pacientesAPI.getAll(queryParams)
    
    if (response.data.success) {
      // ✅ ACTUALIZAR: El backend devuelve la estructura dentro de "data"
      const resultado = response.data.data
      pacientes.value = resultado.pacientes
      pagination.value = {
        page: resultado.page,
        perPage: resultado.per_page,
        total: resultado.total,
        totalPages: Math.ceil(resultado.total / resultado.per_page)
      }
    }
    
    return response.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al cargar pacientes'
    throw err
  } finally {
    loading.value = false
  }
}

  /**
   * Obtener un paciente específico por ID
   */
  async function fetchPacienteById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await pacientesAPI.getById(id)
      
      if (response.data.success) {
        pacienteActual.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar paciente'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear un nuevo paciente
   */
  async function createPaciente(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await pacientesAPI.create(data)
      
      if (response.data.success) {
        // Agregar el nuevo paciente a la lista local
        pacientes.value.unshift(response.data.data)
        pagination.value.total += 1
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear paciente'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar un paciente existente
   */
  async function updatePaciente(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await pacientesAPI.update(id, data)
      
      if (response.data.success) {
        // Actualizar en la lista local
        const index = pacientes.value.findIndex(p => p.id === parseInt(id))
        if (index !== -1) {
          pacientes.value[index] = response.data.data
        }
        
        // Actualizar paciente actual si es el mismo
        if (pacienteActual.value?.id === parseInt(id)) {
          pacienteActual.value = response.data.data
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar paciente'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Eliminar un paciente
   */
  async function deletePaciente(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await pacientesAPI.delete(id)
      
      if (response.data.success) {
        // Remover de la lista local
        const index = pacientes.value.findIndex(p => p.id === parseInt(id))
        if (index !== -1) {
          pacientes.value.splice(index, 1)
          pagination.value.total -= 1
        }
        
        // Limpiar paciente actual si es el mismo
        if (pacienteActual.value?.id === parseInt(id)) {
          pacienteActual.value = null
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al eliminar paciente'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Buscar pacientes (para autocomplete)
   */
  async function searchPacientes(query) {
    if (!query || query.length < 2) {
      return []
    }
    
    try {
      const response = await pacientesAPI.search(query)
      
      if (response.data.success) {
        return response.data.data
      }
      
      return []
    } catch (err) {
      console.error('Error en búsqueda:', err)
      return []
    }
  }

  /**
   * Obtener estadísticas de pacientes
   */
  async function fetchStats() {
    try {
      const response = await pacientesAPI.getStats()
      
      if (response.data.success) {
        return response.data.data
      }
      
      return null
    } catch (err) {
      console.error('Error al obtener estadísticas:', err)
      return null
    }
  }

  /**
   * Subir archivo para un paciente
   */
  async function uploadArchivo(pacienteId, file, categoria) {
    loading.value = true
    error.value = null
    
    try {
      const formData = new FormData()
      formData.append('archivo', file)
      formData.append('categoria', categoria)
      
      const response = await pacientesAPI.uploadFile(pacienteId, formData)
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al subir archivo'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener archivos de un paciente
   */
  async function fetchArchivos(pacienteId) {
    try {
      const response = await pacientesAPI.getFiles(pacienteId)
      
      if (response.data.success) {
        return response.data.data
      }
      
      return []
    } catch (err) {
      console.error('Error al obtener archivos:', err)
      return []
    }
  }

  /**
   * Aplicar filtros y recargar lista
   */
  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1 // Resetear a primera página
    await fetchPacientes()
  }

  /**
   * Limpiar todos los filtros
   */
  async function clearFilters() {
    filters.value = {
      search: '',
      sexo: null,
      tieneIGSS: null,
      edadMin: null,
      edadMax: null
    }
    pagination.value.page = 1
    await fetchPacientes()
  }

  /**
   * Cambiar página
   */
  async function setPage(page) {
    pagination.value.page = page
    await fetchPacientes()
  }

  /**
   * Cambiar items por página
   */
  async function setPerPage(perPage) {
    pagination.value.perPage = perPage
    pagination.value.page = 1
    await fetchPacientes()
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    pacientes.value = []
    pacienteActual.value = null
    loading.value = false
    error.value = null
    pagination.value = {
      page: 1,
      perPage: 25,
      total: 0,
      totalPages: 0
    }
    filters.value = {
      search: '',
      sexo: null,
      tieneIGSS: null,
      edadMin: null,
      edadMax: null
    }
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State
    pacientes,
    pacienteActual,
    loading,
    error,
    pagination,
    filters,
    
    // Getters
    getPacienteById,
    getPacientesActivos,
    totalPacientes,
    hasPacientes,
    hasActiveFilters,
    
    // Actions
    fetchPacientes,
    fetchPacienteById,
    createPaciente,
    updatePaciente,
    deletePaciente,
    searchPacientes,
    fetchStats,
    uploadArchivo,
    fetchArchivos,
    setFilters,
    clearFilters,
    setPage,
    setPerPage,
    resetStore
  }
})
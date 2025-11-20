import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { historiaClinicaAPI } from '@/api/historiaClinica.api'

export const useHistoriaClinicaStore = defineStore('historiaClinica', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  const historiaActual = ref(null)
  const signosVitales = ref([])
  const antecedentes = ref([])
  const vacunasAplicadas = ref([])
  const catalogoVacunas = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // Estado del paciente actual (para referencia)
  const pacienteActual = ref(null)

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Obtener signos vitales más recientes
   */
  const signosVitalesRecientes = computed(() => {
    return signosVitales.value.slice(0, 5)
  })
  
  /**
   * Obtener antecedentes por tipo
   */
  const getAntecedentesByTipo = computed(() => {
    return (tipo) => {
      return antecedentes.value.filter(ant => ant.tipo === tipo && ant.activo)
    }
  })
  
  /**
   * Obtener tipos de antecedentes disponibles
   */
  const tiposAntecedentes = computed(() => {
    return [
      { value: 'medicos', label: 'Médicos', icon: '🏥' },
      { value: 'quirurgicos', label: 'Quirúrgicos', icon: '🔪' },
      { value: 'traumaticos', label: 'Traumáticos', icon: '🤕' },
      { value: 'alergicos', label: 'Alérgicos', icon: '⚠️' },
      { value: 'ginecologicos', label: 'Ginecológicos', icon: '👩' },
      { value: 'obstetricos', label: 'Obstétricos', icon: '🤰' }
    ]
  })
  
  /**
   * Verificar si hay datos de historia clínica cargados
   */
  const hasHistoriaClinica = computed(() => {
    return historiaActual.value !== null
  })
  
  /**
   * Verificar si hay signos vitales
   */
  const hasSignosVitales = computed(() => {
    return signosVitales.value.length > 0
  })
  
  /**
   * Verificar si hay antecedentes
   */
  const hasAntecedentes = computed(() => {
    return antecedentes.value.filter(ant => ant.activo).length > 0
  })
  
  /**
   * Verificar si hay vacunas aplicadas
   */
  const hasVacunas = computed(() => {
    return vacunasAplicadas.value.length > 0
  })
  
  /**
   * Obtener último IMC registrado
   */
  const ultimoIMC = computed(() => {
    const ultimoSigno = signosVitales.value.find(sv => sv.imc)
    return ultimoSigno?.imc || null
  })
  
  /**
   * Obtener último peso registrado
   */
  const ultimoPeso = computed(() => {
    const ultimoSigno = signosVitales.value.find(sv => sv.peso)
    return ultimoSigno?.peso || null
  })

  // ==========================================
  // ACTIONS (Métodos)
  // ==========================================

  /**
   * Cargar historia clínica completa de un paciente
   */
  async function fetchHistoriaCompleta(pacienteId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await historiaClinicaAPI.getHistoriaCompleta(pacienteId)
      
      if (response.data.success) {
        const data = response.data.data
        
        // Guardar todos los datos en el store
        pacienteActual.value = data.paciente
        historiaActual.value = data.historia_clinica
        signosVitales.value = data.signos_vitales || []
        antecedentes.value = data.antecedentes || []
        vacunasAplicadas.value = data.vacunas_aplicadas || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar historia clínica'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar tipo de sangre
   */
  async function updateTipoSangre(pacienteId, tipoSangre) {
    loading.value = true
    error.value = null
    
    try {
      const response = await historiaClinicaAPI.updateHistoria(pacienteId, {
        tipo_sangre: tipoSangre
      })
      
      if (response.data.success) {
        historiaActual.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar tipo de sangre'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Registrar signos vitales
   */
  async function registrarSignosVitales(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await historiaClinicaAPI.registrarSignosVitales(data)
      
      if (response.data.success) {
        // Agregar al inicio de la lista local (más reciente primero)
        signosVitales.value.unshift(response.data.data)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrar signos vitales'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Registrar antecedente
   */
  async function registrarAntecedente(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await historiaClinicaAPI.registrarAntecedente(data)
      
      if (response.data.success) {
        // Agregar a la lista local
        antecedentes.value.push(response.data.data)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrar antecedente'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Eliminar antecedente
   */
  async function eliminarAntecedente(antecedenteId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await historiaClinicaAPI.eliminarAntecedente(antecedenteId)
      
      if (response.data.success) {
        // Marcar como inactivo en la lista local
        const index = antecedentes.value.findIndex(ant => ant.id === antecedenteId)
        if (index !== -1) {
          antecedentes.value[index].activo = false
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al eliminar antecedente'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Cargar catálogo de vacunas
   */
  async function fetchCatalogoVacunas() {
    loading.value = true
    error.value = null
    
    try {
      const response = await historiaClinicaAPI.getCatalogoVacunas()
      
      if (response.data.success) {
        catalogoVacunas.value = response.data.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar catálogo de vacunas'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Aplicar vacuna a paciente
   */
  async function aplicarVacuna(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await historiaClinicaAPI.aplicarVacuna(data)
      
      if (response.data.success) {
        // Agregar a la lista local de vacunas aplicadas
        vacunasAplicadas.value.unshift(response.data.data)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al aplicar vacuna'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener vacuna por ID del catálogo
   */
  function getVacunaById(vacunaId) {
    return catalogoVacunas.value.find(vac => vac.id === parseInt(vacunaId))
  }

  /**
   * Obtener nombre del tipo de antecedente
   */
  function getNombreTipoAntecedente(tipo) {
    const tipoObj = tiposAntecedentes.value.find(t => t.value === tipo)
    return tipoObj?.label || tipo
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    historiaActual.value = null
    signosVitales.value = []
    antecedentes.value = []
    vacunasAplicadas.value = []
    catalogoVacunas.value = []
    pacienteActual.value = null
    loading.value = false
    error.value = null
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State
    historiaActual,
    signosVitales,
    antecedentes,
    vacunasAplicadas,
    catalogoVacunas,
    pacienteActual,
    loading,
    error,
    
    // Getters
    signosVitalesRecientes,
    getAntecedentesByTipo,
    tiposAntecedentes,
    hasHistoriaClinica,
    hasSignosVitales,
    hasAntecedentes,
    hasVacunas,
    ultimoIMC,
    ultimoPeso,
    
    // Actions
    fetchHistoriaCompleta,
    updateTipoSangre,
    registrarSignosVitales,
    registrarAntecedente,
    eliminarAntecedente,
    fetchCatalogoVacunas,
    aplicarVacuna,
    getVacunaById,
    getNombreTipoAntecedente,
    resetStore
  }
})
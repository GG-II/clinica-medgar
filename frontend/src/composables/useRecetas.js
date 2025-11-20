import { ref, computed, watch } from 'vue'
import { useRecetasStore } from '@/stores/recetas'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de recetas médicas
 * Proporciona métodos y estado reactivo para componentes
 */
export function useRecetas() {
  const store = useRecetasStore()
  const router = useRouter()

  // ==========================================
  // ESTADO LOCAL DEL COMPOSABLE
  // ==========================================
  
  const searchQuery = ref('')
  const searchResults = ref([])
  const searchLoading = ref(false)
  const debounceTimer = ref(null)

  // ==========================================
  // COMPUTED PROPERTIES (desde el store)
  // ==========================================
  
  const recetas = computed(() => store.recetas)
  const recetaActual = computed(() => store.recetaActual)
  const medicamentos = computed(() => store.medicamentos)
  const medicamentoActual = computed(() => store.medicamentoActual)
  const loading = computed(() => store.loading)
  const error = computed(() => store.error)
  const filters = computed(() => store.filters)
  const hasRecetas = computed(() => store.hasRecetas)
  const hasActiveFilters = computed(() => store.hasActiveFilters)

  // ==========================================
  // MÉTODOS BÁSICOS (delegan al store)
  // ==========================================

  /**
   * Cargar lista de recetas
   */
  async function loadRecetas(params = {}) {
    try {
      await store.fetchRecetas(params)
    } catch (err) {
      console.error('Error al cargar recetas:', err)
    }
  }

  /**
   * Cargar una receta específica
   */
  async function loadReceta(id) {
    try {
      await store.fetchRecetaById(id)
    } catch (err) {
      console.error('Error al cargar receta:', err)
    }
  }

  /**
   * Crear nueva receta
   */
  async function crearReceta(data) {
    try {
      const result = await store.createReceta(data)
      
      if (result.success) {
        // Si hay warnings de alergias, retornarlos para mostrar al usuario
        if (result.hasWarning) {
          return {
            success: true,
            warning: result.warning,
            data: result.data
          }
        }
        
        return result
      }
    } catch (err) {
      console.error('Error al crear receta:', err)
      throw err
    }
  }

  /**
   * Descargar PDF de receta
   */
  async function descargarPDF(id) {
    try {
      await store.downloadPDF(id)
    } catch (err) {
      console.error('Error al descargar PDF:', err)
      throw err
    }
  }

  /**
   * Desactivar receta con confirmación
   */
  async function desactivarReceta(id, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm('¿Está seguro de desactivar esta receta? Ya no podrá ser dispensada.')
      if (!confirmado) return false
    }
    
    try {
      const result = await store.desactivarReceta(id)
      return result
    } catch (err) {
      console.error('Error al desactivar receta:', err)
      throw err
    }
  }

  /**
   * Cargar historial de recetas de un paciente
   */
  async function loadRecetasPaciente(pacienteId, soloActivas = false) {
    try {
      await store.fetchRecetasByPaciente(pacienteId, soloActivas)
    } catch (err) {
      console.error('Error al cargar historial de recetas:', err)
    }
  }

  // ==========================================
  // BÚSQUEDA DE MEDICAMENTOS CON DEBOUNCE
  // ==========================================

  /**
   * Buscar medicamentos con debounce (espera 300ms después de dejar de escribir)
   */
  function buscarMedicamentos(query) {
    searchQuery.value = query
    
    // Limpiar timer anterior
    if (debounceTimer.value) {
      clearTimeout(debounceTimer.value)
    }
    
    // Si la búsqueda está vacía, limpiar resultados
    if (!query || query.length < 2) {
      searchResults.value = []
      return
    }
    
    // Nuevo timer con debounce de 300ms
    searchLoading.value = true
    debounceTimer.value = setTimeout(async () => {
      try {
        const results = await store.searchMedicamentos(query)
        searchResults.value = results
      } catch (err) {
        console.error('Error en búsqueda:', err)
        searchResults.value = []
      } finally {
        searchLoading.value = false
      }
    }, 300)
  }

  /**
   * Limpiar búsqueda
   */
  function limpiarBusqueda() {
    searchQuery.value = ''
    searchResults.value = []
    if (debounceTimer.value) {
      clearTimeout(debounceTimer.value)
    }
  }

  /**
   * Obtener información completa de un medicamento
   */
  async function obtenerMedicamento(id) {
    try {
      return await store.fetchMedicamentoById(id)
    } catch (err) {
      console.error('Error al obtener medicamento:', err)
      return null
    }
  }

  /**
   * Crear medicamento personalizado
   */
  async function crearMedicamento(data) {
    try {
      const result = await store.createMedicamento(data)
      return result
    } catch (err) {
      console.error('Error al crear medicamento:', err)
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
  // UTILIDADES DE FORMATO
  // ==========================================

  /**
   * Formatear fecha de emisión de receta
   */
  function formatearFechaEmision(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    const opciones = { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }
    
    return date.toLocaleDateString('es-GT', opciones)
  }

  /**
   * Formatear fecha corta (DD/MM/YYYY)
   */
  function formatearFechaCorta(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    const dia = String(date.getDate()).padStart(2, '0')
    const mes = String(date.getMonth() + 1).padStart(2, '0')
    const anio = date.getFullYear()
    
    return `${dia}/${mes}/${anio}`
  }

  /**
   * Formatear nombre de medicamento (genérico + comercial)
   */
  function formatearNombreMedicamento(medicamento) {
    if (!medicamento) return ''
    
    let nombre = medicamento.nombre_generico
    
    if (medicamento.nombre_comercial) {
      nombre += ` (${medicamento.nombre_comercial})`
    }
    
    return nombre
  }

  /**
   * Formatear presentación completa del medicamento
   */
  function formatearPresentacionMedicamento(medicamento) {
    if (!medicamento) return ''
    
    const partes = []
    
    if (medicamento.presentacion) {
      partes.push(medicamento.presentacion)
    }
    
    if (medicamento.concentracion) {
      partes.push(medicamento.concentracion)
    }
    
    return partes.join(' - ')
  }

  /**
   * Formatear dosis completa para mostrar
   */
  function formatearDosisCompleta(detalle) {
    if (!detalle) return ''
    
    const partes = []
    
    // Dosis
    if (detalle.dosis) {
      partes.push(detalle.dosis)
    }
    
    // Frecuencia
    if (detalle.frecuencia) {
      partes.push(detalle.frecuencia)
    }
    
    // Duración
    if (detalle.duracion) {
      partes.push(`por ${detalle.duracion}`)
    }
    
    return partes.join(', ')
  }

  /**
   * Obtener badge de estado de receta
   */
  function obtenerBadgeEstado(receta) {
    if (!receta) return { text: 'Desconocido', variant: 'secondary' }
    
    if (receta.activa) {
      return {
        text: 'Activa',
        variant: 'success'
      }
    } else {
      return {
        text: 'Inactiva',
        variant: 'danger'
      }
    }
  }

  /**
   * Verificar si una receta está activa
   */
  function esRecetaActiva(receta) {
    return receta && receta.activa === true
  }

  /**
   * Verificar si una receta puede ser dispensada
   */
  function puedeDispensarse(receta) {
    return esRecetaActiva(receta)
  }

  // ==========================================
  // VALIDACIONES
  // ==========================================

  /**
   * Validar datos de receta antes de crear
   */
  function validarReceta(data) {
    const errores = []
    
    if (!data.paciente_id) {
      errores.push('Debe seleccionar un paciente')
    }
    
    if (!data.medico_id) {
      errores.push('Debe seleccionar un médico')
    }
    
    if (!data.medicamentos || data.medicamentos.length === 0) {
      errores.push('Debe agregar al menos un medicamento')
    }
    
    // Validar cada medicamento
    if (data.medicamentos) {
      data.medicamentos.forEach((med, index) => {
        if (!med.medicamento_id) {
          errores.push(`Medicamento ${index + 1}: Debe seleccionar un medicamento`)
        }
        
        if (!med.dosis) {
          errores.push(`Medicamento ${index + 1}: Debe especificar la dosis`)
        }
        
        if (!med.frecuencia) {
          errores.push(`Medicamento ${index + 1}: Debe especificar la frecuencia`)
        }
      })
    }
    
    return {
      valido: errores.length === 0,
      errores
    }
  }

  /**
   * Validar datos de medicamento antes de crear
   */
  function validarMedicamento(data) {
    const errores = []
    
    if (!data.nombre_generico || data.nombre_generico.trim() === '') {
      errores.push('El nombre genérico es requerido')
    }
    
    return {
      valido: errores.length === 0,
      errores
    }
  }

  // ==========================================
  // UTILIDADES DE MEDICAMENTOS
  // ==========================================

  /**
   * Obtener vías de administración comunes
   */
  function getViasAdministracion() {
    return [
      { value: 'Oral', label: 'Oral' },
      { value: 'Tópica', label: 'Tópica' },
      { value: 'Intravenosa', label: 'Intravenosa (IV)' },
      { value: 'Intramuscular', label: 'Intramuscular (IM)' },
      { value: 'Subcutánea', label: 'Subcutánea' },
      { value: 'Rectal', label: 'Rectal' },
      { value: 'Oftálmica', label: 'Oftálmica' },
      { value: 'Ótica', label: 'Ótica' },
      { value: 'Nasal', label: 'Nasal' },
      { value: 'Inhalatoria', label: 'Inhalatoria' }
    ]
  }

  /**
   * Obtener frecuencias comunes de dosificación
   */
  function getFrecuenciasDosificacion() {
    return [
      { value: 'cada 4 horas', label: 'Cada 4 horas' },
      { value: 'cada 6 horas', label: 'Cada 6 horas' },
      { value: 'cada 8 horas', label: 'Cada 8 horas (3 veces al día)' },
      { value: 'cada 12 horas', label: 'Cada 12 horas (2 veces al día)' },
      { value: 'cada 24 horas', label: 'Cada 24 horas (1 vez al día)' },
      { value: '1 vez al día', label: '1 vez al día' },
      { value: '2 veces al día', label: '2 veces al día' },
      { value: '3 veces al día', label: '3 veces al día' },
      { value: '4 veces al día', label: '4 veces al día' },
      { value: 'antes de cada comida', label: 'Antes de cada comida' },
      { value: 'después de cada comida', label: 'Después de cada comida' },
      { value: 'al acostarse', label: 'Al acostarse' },
      { value: 'en ayunas', label: 'En ayunas' }
    ]
  }

  /**
   * Obtener duraciones comunes de tratamiento
   */
  function getDuracionesTratamiento() {
    return [
      { value: '3 días', label: '3 días' },
      { value: '5 días', label: '5 días' },
      { value: '7 días', label: '7 días' },
      { value: '10 días', label: '10 días' },
      { value: '14 días', label: '14 días' },
      { value: '1 mes', label: '1 mes' },
      { value: '2 meses', label: '2 meses' },
      { value: '3 meses', label: '3 meses' },
      { value: '6 meses', label: '6 meses' },
      { value: 'continuo', label: 'Tratamiento continuo' }
    ]
  }

  /**
   * Obtener presentaciones comunes de medicamentos
   */
  function getPresentacionesComunes() {
    return [
      { value: 'Tableta', label: 'Tableta' },
      { value: 'Cápsula', label: 'Cápsula' },
      { value: 'Jarabe', label: 'Jarabe' },
      { value: 'Suspensión', label: 'Suspensión' },
      { value: 'Solución', label: 'Solución' },
      { value: 'Inyectable', label: 'Inyectable (ampolla)' },
      { value: 'Crema', label: 'Crema' },
      { value: 'Ungüento', label: 'Ungüento' },
      { value: 'Gel', label: 'Gel' },
      { value: 'Gotas', label: 'Gotas' },
      { value: 'Spray', label: 'Spray' },
      { value: 'Inhalador', label: 'Inhalador' },
      { value: 'Supositorio', label: 'Supositorio' },
      { value: 'Óvulo', label: 'Óvulo' },
      { value: 'Parche', label: 'Parche transdérmico' }
    ]
  }

  /**
   * Generar texto de ejemplo para dosis
   */
  function generarEjemploDosis(presentacion) {
    const ejemplos = {
      'Tableta': '1 tableta',
      'Cápsula': '1 cápsula',
      'Jarabe': '10 ml',
      'Suspensión': '5 ml',
      'Inyectable': '1 ampolla',
      'Crema': 'Aplicar cantidad suficiente',
      'Gotas': '2 gotas'
    }
    
    return ejemplos[presentacion] || '1 unidad'
  }

  // ==========================================
  // UTILIDADES AVANZADAS
  // ==========================================

  /**
   * Contar medicamentos en una receta
   */
  function contarMedicamentos(receta) {
    if (!receta || !receta.medicamentos) return 0
    return receta.medicamentos.length
  }

  /**
   * Verificar si hay alertas de alergias en la respuesta
   */
  function tieneAlertasAlergias(resultado) {
    return resultado && resultado.warning && resultado.warning.includes('ALERTAS')
  }

  /**
   * Parsear alertas de alergias del warning
   */
  function parsearAlertasAlergias(warning) {
    if (!warning) return []
    
    // El warning viene en formato texto, lo parseamos
    const alertas = []
    const lineas = warning.split('\n')
    
    lineas.forEach(linea => {
      if (linea.includes('ALERTA:')) {
        alertas.push(linea.trim())
      }
    })
    
    return alertas
  }

  /**
   * Verificar si un medicamento tiene interacciones registradas
   */
  function tieneInteracciones(medicamento) {
    return medicamento && medicamento.interacciones && medicamento.interacciones.trim() !== ''
  }

  /**
   * Verificar si un medicamento tiene contraindicaciones registradas
   */
  function tieneContraindicaciones(medicamento) {
    return medicamento && medicamento.contraindicaciones && medicamento.contraindicaciones.trim() !== ''
  }

  // ==========================================
  // WATCH (Observadores)
  // ==========================================

  // Limpiar timer cuando el composable se destruye
  watch(() => null, () => {
    if (debounceTimer.value) {
      clearTimeout(debounceTimer.value)
    }
  })

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================

  return {
    // Estado
    recetas,
    recetaActual,
    medicamentos,
    medicamentoActual,
    loading,
    error,
    filters,
    hasRecetas,
    hasActiveFilters,
    
    // Búsqueda de medicamentos
    searchQuery,
    searchResults,
    searchLoading,
    buscarMedicamentos,
    limpiarBusqueda,
    
    // CRUD de recetas
    loadRecetas,
    loadReceta,
    crearReceta,
    descargarPDF,
    desactivarReceta,
    loadRecetasPaciente,
    
    // CRUD de medicamentos
    obtenerMedicamento,
    crearMedicamento,
    
    // Filtros
    aplicarFiltros,
    limpiarFiltros,
    
    // Utilidades de formato
    formatearFechaEmision,
    formatearFechaCorta,
    formatearNombreMedicamento,
    formatearPresentacionMedicamento,
    formatearDosisCompleta,
    obtenerBadgeEstado,
    esRecetaActiva,
    puedeDispensarse,
    
    // Validaciones
    validarReceta,
    validarMedicamento,
    
    // Catálogos
    getViasAdministracion,
    getFrecuenciasDosificacion,
    getDuracionesTratamiento,
    getPresentacionesComunes,
    generarEjemploDosis,
    
    // Utilidades avanzadas
    contarMedicamentos,
    tieneAlertasAlergias,
    parsearAlertasAlergias,
    tieneInteracciones,
    tieneContraindicaciones
  }
}
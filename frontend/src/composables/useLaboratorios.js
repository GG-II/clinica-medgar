import { ref, computed } from 'vue'
import { useLaboratoriosStore } from '@/stores/laboratorios'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de laboratorios
 * Proporciona métodos y estado reactivo para componentes
 */
export function useLaboratorios() {
  const store = useLaboratoriosStore()
  const router = useRouter()

  // ==========================================
  // ESTADO LOCAL DEL COMPOSABLE
  // ==========================================
  
  const alertas = ref([])
  const procesandoResultados = ref(false)

  // ==========================================
  // COMPUTED PROPERTIES (desde el store)
  // ==========================================
  
  const laboratorios = computed(() => store.laboratorios)
  const laboratorioActual = computed(() => store.laboratorioActual)
  const loading = computed(() => store.loading)
  const error = computed(() => store.error)
  const tipos = computed(() => store.tipos)
  const tiposPorCategoria = computed(() => store.tiposPorCategoria)
  const categorias = computed(() => store.categorias)
  const valoresReferencia = computed(() => store.valoresReferencia)
  const historicoParametro = computed(() => store.historicoParametro)
  const comparacion = computed(() => store.comparacion)
  const filters = computed(() => store.filters)
  const hasLaboratorios = computed(() => store.hasLaboratorios)
  const hasActiveFilters = computed(() => store.hasActiveFilters)

  // ==========================================
  // MÉTODOS BÁSICOS (delegan al store)
  // ==========================================

  /**
   * Cargar lista de laboratorios
   */
  async function loadLaboratorios(params = {}) {
    try {
      await store.fetchLaboratorios(params)
    } catch (err) {
      console.error('Error al cargar laboratorios:', err)
    }
  }

  /**
   * Cargar un laboratorio específico
   */
  async function loadLaboratorio(id) {
    try {
      const result = await store.fetchLaboratorioById(id)
      
      // Guardar alertas si existen
      if (result.data?.alertas) {
        alertas.value = result.data.alertas
      }
      
      return result
    } catch (err) {
      console.error('Error al cargar laboratorio:', err)
    }
  }

  /**
   * Solicitar nuevo laboratorio
   */
  async function solicitarLaboratorio(data) {
    try {
      const result = await store.createLaboratorio(data)
      
      if (result.success) {
        // Redirigir al detalle del laboratorio recién creado (opcional)
        // router.push(`/laboratorios/${result.data.id}`)
        return result
      }
    } catch (err) {
      console.error('Error al solicitar laboratorio:', err)
      throw err
    }
  }

  /**
   * Registrar resultados de un laboratorio
   */
  async function registrarResultados(id, data) {
    procesandoResultados.value = true
    alertas.value = []
    
    try {
      const result = await store.registrarResultados(id, data)
      
      if (result.success) {
        // Guardar alertas si existen
        if (result.alertas) {
          alertas.value = result.alertas
        }
      }
      
      return result
    } catch (err) {
      console.error('Error al registrar resultados:', err)
      throw err
    } finally {
      procesandoResultados.value = false
    }
  }

  /**
   * Cancelar laboratorio con confirmación
   */
  async function cancelarLaboratorio(id, motivo = null, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm('¿Está seguro de cancelar este laboratorio?')
      if (!confirmado) return false
    }
    
    try {
      const result = await store.cancelarLaboratorio(id, motivo)
      return result
    } catch (err) {
      console.error('Error al cancelar laboratorio:', err)
      throw err
    }
  }

  // ==========================================
  // HISTORIAL Y COMPARACIÓN
  // ==========================================

  /**
   * Cargar historial de laboratorios de un paciente
   */
  async function loadHistorialPaciente(pacienteId, soloCompletados = false) {
    try {
      await store.fetchLaboratoriosPaciente(pacienteId, soloCompletados)
    } catch (err) {
      console.error('Error al cargar historial:', err)
    }
  }

  /**
   * Cargar histórico de un parámetro para gráficas
   */
  async function loadHistoricoParametro(pacienteId, tipoLaboratorioId, parametro, limite = 10) {
    try {
      await store.fetchHistoricoParametro(pacienteId, tipoLaboratorioId, parametro, limite)
    } catch (err) {
      console.error('Error al cargar histórico de parámetro:', err)
    }
  }

  /**
   * Cargar comparación de últimos resultados
   */
  async function loadComparacion(pacienteId, tipoLaboratorioId) {
    try {
      await store.fetchComparacion(pacienteId, tipoLaboratorioId)
    } catch (err) {
      console.error('Error al cargar comparación:', err)
    }
  }

  // ==========================================
  // CATÁLOGOS
  // ==========================================

  /**
   * Cargar tipos de laboratorio
   */
  async function loadTipos(categoria = null) {
    try {
      await store.fetchTipos(categoria)
    } catch (err) {
      console.error('Error al cargar tipos:', err)
    }
  }

  /**
   * Cargar un tipo específico con valores de referencia
   */
  async function loadTipoById(id) {
    try {
      await store.fetchTipoById(id)
    } catch (err) {
      console.error('Error al cargar tipo:', err)
    }
  }

  /**
   * Cargar valores de referencia
   */
  async function loadValoresReferencia(params) {
    try {
      await store.fetchValoresReferencia(params)
    } catch (err) {
      console.error('Error al cargar valores de referencia:', err)
    }
  }

  /**
   * Cargar categorías
   */
  async function loadCategorias() {
    try {
      await store.fetchCategorias()
    } catch (err) {
      console.error('Error al cargar categorías:', err)
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
  // UTILIDADES
  // ==========================================

  /**
   * Obtener nombre del estado con estilo
   */
  function obtenerEstadoBadge(estado) {
    const badges = {
      'solicitado': { text: 'Solicitado', variant: 'warning' },
      'en_proceso': { text: 'En Proceso', variant: 'info' },
      'completado': { text: 'Completado', variant: 'success' },
      'cancelado': { text: 'Cancelado', variant: 'danger' }
    }
    return badges[estado] || { text: estado, variant: 'secondary' }
  }

  /**
   * Verificar si un resultado está en rango normal
   */
  function esNormal(resultado) {
    return resultado?.normal === true && resultado?.estado === 'normal'
  }

  /**
   * Obtener color según estado del resultado
   */
  function obtenerColorResultado(resultado) {
    if (!resultado || !resultado.estado) return 'text-gray-600'
    
    const colores = {
      'normal': 'text-green-600',
      'bajo': 'text-blue-600',
      'alto': 'text-red-600'
    }
    
    return colores[resultado.estado] || 'text-gray-600'
  }

  /**
   * Obtener ícono según estado del resultado
   */
  function obtenerIconoResultado(resultado) {
    if (!resultado || !resultado.estado) return '•'
    
    const iconos = {
      'normal': '✓',
      'bajo': '↓',
      'alto': '↑'
    }
    
    return iconos[resultado.estado] || '•'
  }

  /**
   * Formatear valor con unidad
   */
  function formatearValorConUnidad(resultado) {
    if (!resultado) return ''
    
    const valor = resultado.valor
    const unidad = resultado.unidad || ''
    
    return `${valor} ${unidad}`.trim()
  }

  /**
   * Obtener texto de rango de referencia
   */
  function obtenerRangoReferencia(resultado) {
    if (!resultado?.referencia) return ''
    
    const ref = resultado.referencia
    
    if (ref.min !== null && ref.max !== null) {
      return `${ref.min} - ${ref.max} ${ref.unidad || ''}`.trim()
    } else if (ref.min !== null) {
      return `> ${ref.min} ${ref.unidad || ''}`.trim()
    } else if (ref.max !== null) {
      return `< ${ref.max} ${ref.unidad || ''}`.trim()
    }
    
    return ''
  }

  /**
   * Verificar si hay alertas críticas
   */
  function tieneAlertasCriticas() {
    return alertas.value.some(alerta => alerta.severidad === 'critico')
  }

  /**
   * Obtener cantidad de alertas
   */
  const cantidadAlertas = computed(() => alertas.value.length)

  /**
   * Formatear fecha de laboratorio
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
   * Obtener tendencia en texto legible
   */
  function obtenerTextoTendencia(tendencia) {
    const textos = {
      'aumentó': '↑ Aumentó',
      'disminuyó': '↓ Disminuyó',
      'se mantuvo': '→ Se mantuvo'
    }
    return textos[tendencia] || tendencia
  }

  /**
   * Obtener color de tendencia
   */
  function obtenerColorTendencia(tendencia, esMejor) {
    if (tendencia === 'se mantuvo') return 'text-gray-600'
    
    // Por defecto: aumento = rojo, disminución = azul
    // Pero depende del parámetro (por ejemplo, glucosa alta es mala)
    if (esMejor === undefined) {
      return tendencia === 'aumentó' ? 'text-red-600' : 'text-blue-600'
    }
    
    return esMejor ? 'text-green-600' : 'text-red-600'
  }

  /**
   * Limpiar alertas
   */
  function limpiarAlertas() {
    alertas.value = []
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================

  return {
    // Estado
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
    hasLaboratorios,
    hasActiveFilters,
    alertas,
    procesandoResultados,
    cantidadAlertas,
    
    // CRUD
    loadLaboratorios,
    loadLaboratorio,
    solicitarLaboratorio,
    registrarResultados,
    cancelarLaboratorio,
    
    // Historial y comparación
    loadHistorialPaciente,
    loadHistoricoParametro,
    loadComparacion,
    
    // Catálogos
    loadTipos,
    loadTipoById,
    loadValoresReferencia,
    loadCategorias,
    
    // Filtros
    aplicarFiltros,
    limpiarFiltros,
    
    // Utilidades
    obtenerEstadoBadge,
    esNormal,
    obtenerColorResultado,
    obtenerIconoResultado,
    formatearValorConUnidad,
    obtenerRangoReferencia,
    tieneAlertasCriticas,
    formatearFecha,
    formatearFechaCorta,
    obtenerTextoTendencia,
    obtenerColorTendencia,
    limpiarAlertas
  }
}
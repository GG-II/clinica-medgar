import { ref, computed, watch } from 'vue'
import { usePacientesStore } from '@/stores/pacientes'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de pacientes
 * Proporciona métodos y estado reactivo para componentes
 */
export function usePacientes() {
  const store = usePacientesStore()
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
  
  const pacientes = computed(() => store.pacientes)
  const pacienteActual = computed(() => store.pacienteActual)
  const loading = computed(() => store.loading)
  const error = computed(() => store.error)
  const pagination = computed(() => store.pagination)
  const filters = computed(() => store.filters)
  const hasPacientes = computed(() => store.hasPacientes)
  const hasActiveFilters = computed(() => store.hasActiveFilters)

  // ==========================================
  // MÉTODOS BÁSICOS (delegan al store)
  // ==========================================

  /**
   * Cargar lista de pacientes
   */
  async function loadPacientes(params = {}) {
    try {
      await store.fetchPacientes(params)
    } catch (err) {
      console.error('Error al cargar pacientes:', err)
    }
  }

  /**
   * Cargar un paciente específico
   */
  async function loadPaciente(id) {
    try {
      await store.fetchPacienteById(id)
    } catch (err) {
      console.error('Error al cargar paciente:', err)
    }
  }

  /**
   * Crear nuevo paciente y redirigir al detalle
   */
  async function crearPaciente(data) {
    try {
      const result = await store.createPaciente(data)
      
      if (result.success) {
        // Redirigir al detalle del paciente recién creado
        router.push(`/pacientes/${result.data.id}`)
        return result
      }
    } catch (err) {
      console.error('Error al crear paciente:', err)
      throw err
    }
  }

  /**
   * Actualizar paciente existente
   */
  async function actualizarPaciente(id, data) {
    try {
      const result = await store.updatePaciente(id, data)
      return result
    } catch (err) {
      console.error('Error al actualizar paciente:', err)
      throw err
    }
  }

  /**
   * Eliminar paciente con confirmación
   */
  async function eliminarPaciente(id, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm('¿Está seguro de eliminar este paciente?')
      if (!confirmado) return false
    }
    
    try {
      const result = await store.deletePaciente(id)
      
      if (result.success) {
        // Redirigir a lista si estamos en el detalle
        if (router.currentRoute.value.name === 'PacienteDetalle') {
          router.push('/pacientes')
        }
      }
      
      return result
    } catch (err) {
      console.error('Error al eliminar paciente:', err)
      throw err
    }
  }

  // ==========================================
  // BÚSQUEDA CON DEBOUNCE
  // ==========================================

  /**
   * Buscar pacientes con debounce (espera 300ms después de dejar de escribir)
   */
  function buscarPacientes(query) {
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
        const results = await store.searchPacientes(query)
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
  // PAGINACIÓN
  // ==========================================

  /**
   * Ir a una página específica
   */
  async function irAPagina(page) {
    try {
      await store.setPage(page)
    } catch (err) {
      console.error('Error al cambiar página:', err)
    }
  }

  /**
   * Cambiar items por página
   */
  async function cambiarItemsPorPagina(perPage) {
    try {
      await store.setPerPage(perPage)
    } catch (err) {
      console.error('Error al cambiar items por página:', err)
    }
  }

  /**
   * Ir a página anterior
   */
  async function paginaAnterior() {
    if (pagination.value.page > 1) {
      await irAPagina(pagination.value.page - 1)
    }
  }

  /**
   * Ir a página siguiente
   */
  async function paginaSiguiente() {
    if (pagination.value.page < pagination.value.totalPages) {
      await irAPagina(pagination.value.page + 1)
    }
  }

  // ==========================================
  // ARCHIVOS
  // ==========================================

  /**
   * Subir foto del paciente
   */
  async function subirFoto(pacienteId, file) {
    try {
      const result = await store.uploadArchivo(pacienteId, file, 'foto_perfil')
      
      // Recargar paciente actual para actualizar la foto
      if (pacienteActual.value?.id === pacienteId) {
        await loadPaciente(pacienteId)
      }
      
      return result
    } catch (err) {
      console.error('Error al subir foto:', err)
      throw err
    }
  }

  /**
   * Subir documento del paciente
   */
  async function subirDocumento(pacienteId, file, categoria = 'documentos') {
    try {
      const result = await store.uploadArchivo(pacienteId, file, categoria)
      return result
    } catch (err) {
      console.error('Error al subir documento:', err)
      throw err
    }
  }

  /**
   * Obtener archivos del paciente
   */
  async function obtenerArchivos(pacienteId) {
    try {
      const archivos = await store.fetchArchivos(pacienteId)
      return archivos
    } catch (err) {
      console.error('Error al obtener archivos:', err)
      return []
    }
  }

  // ==========================================
  // UTILIDADES
  // ==========================================

  /**
   * Calcular edad a partir de fecha de nacimiento
   */
  function calcularEdad(fechaNacimiento) {
    if (!fechaNacimiento) return null
    
    const hoy = new Date()
    const nacimiento = new Date(fechaNacimiento)
    let edad = hoy.getFullYear() - nacimiento.getFullYear()
    const mes = hoy.getMonth() - nacimiento.getMonth()
    
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--
    }
    
    return edad
  }

  /**
   * Formatear teléfono guatemalteco
   */
  function formatearTelefono(telefono) {
    if (!telefono) return ''
    
    // Remover caracteres no numéricos
    const numeros = telefono.replace(/\D/g, '')
    
    // Formato: XXXX-XXXX
    if (numeros.length === 8) {
      return `${numeros.slice(0, 4)}-${numeros.slice(4)}`
    }
    
    return telefono
  }

  /**
   * Obtener nombre de sexo
   */
  function obtenerNombreSexo(sexo) {
    const nombres = {
      'M': 'Masculino',
      'F': 'Femenino'
    }
    return nombres[sexo] || sexo
  }

  /**
   * Obtener badge de sexo
   */
  function obtenerBadgeSexo(sexo) {
    const badges = {
      'M': { text: 'Masculino', variant: 'info' },
      'F': { text: 'Femenino', variant: 'pink' }
    }
    return badges[sexo] || { text: sexo, variant: 'secondary' }
  }

  /**
   * Validar DPI guatemalteco (13 dígitos)
   */
  function validarDPI(dpi) {
    if (!dpi) return true // Opcional
    
    const numeros = dpi.replace(/\D/g, '')
    return numeros.length === 13
  }

  /**
   * Formatear DPI guatemalteco
   */
  function formatearDPI(dpi) {
    if (!dpi) return ''
    
    const numeros = dpi.replace(/\D/g, '')
    
    // Formato: XXXX XXXXX XXXX
    if (numeros.length === 13) {
      return `${numeros.slice(0, 4)} ${numeros.slice(4, 9)} ${numeros.slice(9)}`
    }
    
    return dpi
  }

  /**
   * Verificar si el paciente es menor de edad
   */
  function esMenorDeEdad(fechaNacimiento) {
    const edad = calcularEdad(fechaNacimiento)
    return edad !== null && edad < 18
  }

  /**
   * Verificar si el paciente es adulto mayor
   */
  function esAdultoMayor(fechaNacimiento) {
    const edad = calcularEdad(fechaNacimiento)
    return edad !== null && edad >= 65
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
    pacientes,
    pacienteActual,
    loading,
    error,
    pagination,
    filters,
    hasPacientes,
    hasActiveFilters,
    
    // Búsqueda
    searchQuery,
    searchResults,
    searchLoading,
    buscarPacientes,
    limpiarBusqueda,
    
    // CRUD
    loadPacientes,
    loadPaciente,
    crearPaciente,
    actualizarPaciente,
    eliminarPaciente,
    
    // Filtros
    aplicarFiltros,
    limpiarFiltros,
    
    // Paginación
    irAPagina,
    cambiarItemsPorPagina,
    paginaAnterior,
    paginaSiguiente,
    
    // Archivos
    subirFoto,
    subirDocumento,
    obtenerArchivos,
    
    // Utilidades
    calcularEdad,
    formatearTelefono,
    formatearDPI,
    validarDPI,
    obtenerNombreSexo,
    obtenerBadgeSexo,
    esMenorDeEdad,
    esAdultoMayor
  }
}

import { ref, computed } from 'vue'
import { useHistoriaClinicaStore } from '@/stores/historiaClinica'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de Historia Clínica
 * Proporciona métodos y estado reactivo para componentes
 */
export function useHistoriaClinica() {
  const store = useHistoriaClinicaStore()
  const router = useRouter()

  // ==========================================
  // COMPUTED PROPERTIES (desde el store)
  // ==========================================
  
  const historiaActual = computed(() => store.historiaActual)
  const signosVitales = computed(() => store.signosVitales)
  const antecedentes = computed(() => store.antecedentes)
  const vacunasAplicadas = computed(() => store.vacunasAplicadas)
  const catalogoVacunas = computed(() => store.catalogoVacunas)
  const pacienteActual = computed(() => store.pacienteActual)
  const loading = computed(() => store.loading)
  const error = computed(() => store.error)
  const signosVitalesRecientes = computed(() => store.signosVitalesRecientes)
  const tiposAntecedentes = computed(() => store.tiposAntecedentes)
  const hasHistoriaClinica = computed(() => store.hasHistoriaClinica)
  const hasSignosVitales = computed(() => store.hasSignosVitales)
  const hasAntecedentes = computed(() => store.hasAntecedentes)
  const hasVacunas = computed(() => store.hasVacunas)
  const ultimoIMC = computed(() => store.ultimoIMC)
  const ultimoPeso = computed(() => store.ultimoPeso)

  // ==========================================
  // MÉTODOS BÁSICOS (delegan al store)
  // ==========================================

  /**
   * Cargar historia clínica completa de un paciente
   */
  async function cargarHistoriaCompleta(pacienteId) {
    try {
      await store.fetchHistoriaCompleta(pacienteId)
    } catch (err) {
      console.error('Error al cargar historia clínica:', err)
      throw err
    }
  }

  /**
   * Actualizar tipo de sangre
   */
  async function actualizarTipoSangre(pacienteId, tipoSangre) {
    try {
      const result = await store.updateTipoSangre(pacienteId, tipoSangre)
      return result
    } catch (err) {
      console.error('Error al actualizar tipo de sangre:', err)
      throw err
    }
  }

  /**
   * Registrar signos vitales
   */
  async function registrarSignosVitales(data) {
    try {
      const result = await store.registrarSignosVitales(data)
      return result
    } catch (err) {
      console.error('Error al registrar signos vitales:', err)
      throw err
    }
  }

  /**
   * Registrar antecedente
   */
  async function registrarAntecedente(data) {
    try {
      const result = await store.registrarAntecedente(data)
      return result
    } catch (err) {
      console.error('Error al registrar antecedente:', err)
      throw err
    }
  }

  /**
   * Eliminar antecedente con confirmación
   */
  async function eliminarAntecedente(antecedenteId, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm('¿Está seguro de eliminar este antecedente?')
      if (!confirmado) return false
    }
    
    try {
      const result = await store.eliminarAntecedente(antecedenteId)
      return result
    } catch (err) {
      console.error('Error al eliminar antecedente:', err)
      throw err
    }
  }

  /**
   * Cargar catálogo de vacunas
   */
  async function cargarCatalogoVacunas() {
    try {
      await store.fetchCatalogoVacunas()
    } catch (err) {
      console.error('Error al cargar catálogo de vacunas:', err)
    }
  }

  /**
   * Aplicar vacuna
   */
  async function aplicarVacuna(data) {
    try {
      const result = await store.aplicarVacuna(data)
      return result
    } catch (err) {
      console.error('Error al aplicar vacuna:', err)
      throw err
    }
  }

  // ==========================================
  // UTILIDADES - SIGNOS VITALES
  // ==========================================

  /**
   * Calcular IMC (Índice de Masa Corporal)
   * @param {number} peso - Peso en kg
   * @param {number} talla - Talla en cm
   * @returns {number|null} IMC calculado
   */
  function calcularIMC(peso, talla) {
    if (!peso || !talla || talla === 0) return null
    
    // Convertir talla de cm a metros
    const tallaMetros = talla / 100
    const imc = peso / (tallaMetros * tallaMetros)
    
    return Math.round(imc * 100) / 100 // Redondear a 2 decimales
  }

  /**
   * Clasificar IMC según OMS
   * @param {number} imc - Índice de Masa Corporal
   * @returns {Object} { categoria, color, descripcion }
   */
  function clasificarIMC(imc) {
    if (!imc) return { categoria: 'No disponible', color: 'gray', descripcion: '' }
    
    if (imc < 18.5) {
      return {
        categoria: 'Bajo peso',
        color: 'warning',
        descripcion: 'Por debajo del peso normal'
      }
    } else if (imc >= 18.5 && imc < 25) {
      return {
        categoria: 'Normal',
        color: 'success',
        descripcion: 'Peso saludable'
      }
    } else if (imc >= 25 && imc < 30) {
      return {
        categoria: 'Sobrepeso',
        color: 'warning',
        descripcion: 'Por encima del peso normal'
      }
    } else if (imc >= 30 && imc < 35) {
      return {
        categoria: 'Obesidad I',
        color: 'danger',
        descripcion: 'Obesidad leve'
      }
    } else if (imc >= 35 && imc < 40) {
      return {
        categoria: 'Obesidad II',
        color: 'danger',
        descripcion: 'Obesidad moderada'
      }
    } else {
      return {
        categoria: 'Obesidad III',
        color: 'danger',
        descripcion: 'Obesidad mórbida'
      }
    }
  }

  /**
   * Validar presión arterial
   * @param {number} sistolica - Presión sistólica
   * @param {number} diastolica - Presión diastólica
   * @returns {Object} { nivel, color, descripcion }
   */
  function validarPresionArterial(sistolica, diastolica) {
    if (!sistolica || !diastolica) {
      return { nivel: 'No disponible', color: 'gray', descripcion: '' }
    }
    
    if (sistolica < 90 || diastolica < 60) {
      return {
        nivel: 'Baja',
        color: 'warning',
        descripcion: 'Hipotensión'
      }
    } else if (sistolica < 120 && diastolica < 80) {
      return {
        nivel: 'Normal',
        color: 'success',
        descripcion: 'Presión arterial óptima'
      }
    } else if (sistolica < 130 && diastolica < 85) {
      return {
        nivel: 'Normal-Alta',
        color: 'info',
        descripcion: 'Rango normal alto'
      }
    } else if (sistolica < 140 && diastolica < 90) {
      return {
        nivel: 'Prehipertensión',
        color: 'warning',
        descripcion: 'Riesgo de hipertensión'
      }
    } else if (sistolica < 160 && diastolica < 100) {
      return {
        nivel: 'Hipertensión Grado 1',
        color: 'danger',
        descripcion: 'Hipertensión leve'
      }
    } else if (sistolica < 180 && diastolica < 110) {
      return {
        nivel: 'Hipertensión Grado 2',
        color: 'danger',
        descripcion: 'Hipertensión moderada'
      }
    } else {
      return {
        nivel: 'Hipertensión Grado 3',
        color: 'danger',
        descripcion: 'Hipertensión severa'
      }
    }
  }

  /**
   * Validar frecuencia cardíaca
   * @param {number} fc - Frecuencia cardíaca
   * @param {number} edad - Edad del paciente
   * @returns {Object} { nivel, color, descripcion }
   */
  function validarFrecuenciaCardiaca(fc, edad = null) {
    if (!fc) return { nivel: 'No disponible', color: 'gray', descripcion: '' }
    
    // Valores normales para adultos
    if (fc < 60) {
      return {
        nivel: 'Bradicardia',
        color: 'warning',
        descripcion: 'Frecuencia cardíaca baja'
      }
    } else if (fc >= 60 && fc <= 100) {
      return {
        nivel: 'Normal',
        color: 'success',
        descripcion: 'Frecuencia cardíaca normal'
      }
    } else if (fc > 100 && fc <= 120) {
      return {
        nivel: 'Taquicardia leve',
        color: 'warning',
        descripcion: 'Frecuencia cardíaca elevada'
      }
    } else {
      return {
        nivel: 'Taquicardia',
        color: 'danger',
        descripcion: 'Frecuencia cardíaca muy elevada'
      }
    }
  }

  /**
   * Validar temperatura corporal
   * @param {number} temperatura - Temperatura en °C
   * @returns {Object} { nivel, color, descripcion }
   */
  function validarTemperatura(temperatura) {
    if (!temperatura) return { nivel: 'No disponible', color: 'gray', descripcion: '' }
    
    if (temperatura < 35) {
      return {
        nivel: 'Hipotermia',
        color: 'info',
        descripcion: 'Temperatura muy baja'
      }
    } else if (temperatura >= 35 && temperatura < 36) {
      return {
        nivel: 'Baja',
        color: 'info',
        descripcion: 'Temperatura por debajo del rango normal'
      }
    } else if (temperatura >= 36 && temperatura < 37.5) {
      return {
        nivel: 'Normal',
        color: 'success',
        descripcion: 'Temperatura normal'
      }
    } else if (temperatura >= 37.5 && temperatura < 38) {
      return {
        nivel: 'Febrícula',
        color: 'warning',
        descripcion: 'Temperatura ligeramente elevada'
      }
    } else if (temperatura >= 38 && temperatura < 39) {
      return {
        nivel: 'Fiebre moderada',
        color: 'warning',
        descripcion: 'Fiebre presente'
      }
    } else {
      return {
        nivel: 'Fiebre alta',
        color: 'danger',
        descripcion: 'Temperatura muy elevada'
      }
    }
  }

  /**
   * Validar saturación de oxígeno
   * @param {number} saturacion - Saturación en %
   * @returns {Object} { nivel, color, descripcion }
   */
  function validarSaturacionOxigeno(saturacion) {
    if (!saturacion) return { nivel: 'No disponible', color: 'gray', descripcion: '' }
    
    if (saturacion < 90) {
      return {
        nivel: 'Crítica',
        color: 'danger',
        descripcion: 'Hipoxemia severa'
      }
    } else if (saturacion >= 90 && saturacion < 95) {
      return {
        nivel: 'Baja',
        color: 'warning',
        descripcion: 'Saturación por debajo del rango normal'
      }
    } else if (saturacion >= 95 && saturacion <= 100) {
      return {
        nivel: 'Normal',
        color: 'success',
        descripcion: 'Saturación óptima'
      }
    } else {
      return {
        nivel: 'Inválida',
        color: 'gray',
        descripcion: 'Valor fuera de rango'
      }
    }
  }

  /**
   * Formatear presión arterial
   * @param {number} sistolica - Presión sistólica
   * @param {number} diastolica - Presión diastólica
   * @returns {string} Formato: "120/80 mmHg"
   */
  function formatearPresionArterial(sistolica, diastolica) {
    if (!sistolica || !diastolica) return 'N/A'
    return `${sistolica}/${diastolica} mmHg`
  }

  /**
   * Formatear temperatura
   * @param {number} temperatura - Temperatura en °C
   * @returns {string} Formato: "37.5 °C"
   */
  function formatearTemperatura(temperatura) {
    if (!temperatura) return 'N/A'
    return `${temperatura} °C`
  }

  /**
   * Formatear fecha de signos vitales
   * @param {string} fecha - Fecha ISO
   * @returns {string} Formato: "20 Nov 2024, 10:30"
   */
  function formatearFechaSignosVitales(fecha) {
    if (!fecha) return 'N/A'
    
    const date = new Date(fecha)
    const options = { 
      day: '2-digit', 
      month: 'short', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }
    
    return date.toLocaleDateString('es-GT', options)
  }

  // ==========================================
  // UTILIDADES - ANTECEDENTES
  // ==========================================

  /**
   * Obtener antecedentes por tipo
   * @param {string} tipo - Tipo de antecedente
   * @returns {Array} Lista de antecedentes del tipo especificado
   */
  function obtenerAntecedentesPorTipo(tipo) {
    return store.getAntecedentesByTipo(tipo)
  }

  /**
   * Obtener nombre del tipo de antecedente
   * @param {string} tipo - Tipo de antecedente
   * @returns {string} Nombre legible
   */
  function obtenerNombreTipoAntecedente(tipo) {
    return store.getNombreTipoAntecedente(tipo)
  }

  /**
   * Obtener icono del tipo de antecedente
   * @param {string} tipo - Tipo de antecedente
   * @returns {string} Emoji del icono
   */
  function obtenerIconoTipoAntecedente(tipo) {
    const tipoObj = tiposAntecedentes.value.find(t => t.value === tipo)
    return tipoObj?.icon || '📋'
  }

  /**
   * Obtener badge de relevancia
   * @param {string} relevancia - Nivel de relevancia
   * @returns {Object} { text, variant }
   */
  function obtenerBadgeRelevancia(relevancia) {
    const badges = {
      'alta': { text: 'Alta', variant: 'danger' },
      'media': { text: 'Media', variant: 'warning' },
      'baja': { text: 'Baja', variant: 'info' }
    }
    return badges[relevancia] || { text: relevancia, variant: 'secondary' }
  }

  /**
   * Formatear fecha de antecedente
   * @param {string} fecha - Fecha ISO
   * @returns {string} Formato: "20 Nov 2024"
   */
  function formatearFechaAntecedente(fecha) {
    if (!fecha) return 'Fecha no especificada'
    
    const date = new Date(fecha)
    const options = { day: '2-digit', month: 'short', year: 'numeric' }
    
    return date.toLocaleDateString('es-GT', options)
  }

  // ==========================================
  // UTILIDADES - VACUNAS
  // ==========================================

  /**
   * Obtener vacuna por ID
   * @param {number} vacunaId - ID de la vacuna
   * @returns {Object|null} Datos de la vacuna
   */
  function obtenerVacunaPorId(vacunaId) {
    return store.getVacunaById(vacunaId)
  }

  /**
   * Verificar si una vacuna está completa
   * @param {number} vacunaId - ID de la vacuna
   * @returns {boolean} true si todas las dosis fueron aplicadas
   */
  function vacunaCompleta(vacunaId) {
    const vacuna = obtenerVacunaPorId(vacunaId)
    if (!vacuna) return false
    
    const aplicaciones = vacunasAplicadas.value.filter(
      v => v.vacuna_id === vacunaId
    )
    
    return aplicaciones.length >= vacuna.dosis_total
  }

  /**
   * Obtener próxima dosis de una vacuna
   * @param {number} vacunaId - ID de la vacuna
   * @returns {number} Número de la próxima dosis
   */
  function obtenerProximaDosis(vacunaId) {
    const aplicaciones = vacunasAplicadas.value.filter(
      v => v.vacuna_id === vacunaId
    )
    
    if (aplicaciones.length === 0) return 1
    
    const ultimaDosis = Math.max(...aplicaciones.map(a => a.numero_dosis))
    return ultimaDosis + 1
  }

  /**
   * Formatear fecha de vacuna
   * @param {string} fecha - Fecha ISO
   * @returns {string} Formato: "20 Nov 2024"
   */
  function formatearFechaVacuna(fecha) {
    if (!fecha) return 'N/A'
    
    const date = new Date(fecha)
    const options = { day: '2-digit', month: 'short', year: 'numeric' }
    
    return date.toLocaleDateString('es-GT', options)
  }

  /**
   * Obtener badge de estado de vacunación
   * @param {number} vacunaId - ID de la vacuna
   * @returns {Object} { text, variant }
   */
  function obtenerBadgeEstadoVacuna(vacunaId) {
    const completa = vacunaCompleta(vacunaId)
    
    if (completa) {
      return { text: 'Completa', variant: 'success' }
    } else {
      const aplicaciones = vacunasAplicadas.value.filter(v => v.vacuna_id === vacunaId)
      if (aplicaciones.length > 0) {
        return { text: 'En proceso', variant: 'warning' }
      } else {
        return { text: 'Pendiente', variant: 'secondary' }
      }
    }
  }

  // ==========================================
  // UTILIDADES - TIPOS DE SANGRE
  // ==========================================

  /**
   * Obtener tipos de sangre disponibles
   * @returns {Array} Lista de tipos de sangre
   */
  function obtenerTiposSangre() {
    return [
      { value: 'A+', label: 'A+' },
      { value: 'A-', label: 'A-' },
      { value: 'B+', label: 'B+' },
      { value: 'B-', label: 'B-' },
      { value: 'AB+', label: 'AB+' },
      { value: 'AB-', label: 'AB-' },
      { value: 'O+', label: 'O+' },
      { value: 'O-', label: 'O-' }
    ]
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================

  return {
    // Estado
    historiaActual,
    signosVitales,
    antecedentes,
    vacunasAplicadas,
    catalogoVacunas,
    pacienteActual,
    loading,
    error,
    signosVitalesRecientes,
    tiposAntecedentes,
    hasHistoriaClinica,
    hasSignosVitales,
    hasAntecedentes,
    hasVacunas,
    ultimoIMC,
    ultimoPeso,
    
    // Métodos CRUD
    cargarHistoriaCompleta,
    actualizarTipoSangre,
    registrarSignosVitales,
    registrarAntecedente,
    eliminarAntecedente,
    cargarCatalogoVacunas,
    aplicarVacuna,
    
    // Utilidades - Signos Vitales
    calcularIMC,
    clasificarIMC,
    validarPresionArterial,
    validarFrecuenciaCardiaca,
    validarTemperatura,
    validarSaturacionOxigeno,
    formatearPresionArterial,
    formatearTemperatura,
    formatearFechaSignosVitales,
    
    // Utilidades - Antecedentes
    obtenerAntecedentesPorTipo,
    obtenerNombreTipoAntecedente,
    obtenerIconoTipoAntecedente,
    obtenerBadgeRelevancia,
    formatearFechaAntecedente,
    
    // Utilidades - Vacunas
    obtenerVacunaPorId,
    vacunaCompleta,
    obtenerProximaDosis,
    formatearFechaVacuna,
    obtenerBadgeEstadoVacuna,
    
    // Utilidades - Tipos de Sangre
    obtenerTiposSangre
  }
}
import axios from './axios'

export const laboratoriosAPI = {
  // ==========================================
  // CRUD BÁSICO DE LABORATORIOS
  // ==========================================

  /**
   * Obtener lista de laboratorios con filtros
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.paciente_id - ID del paciente
   * @param {number} params.medico_id - ID del médico
   * @param {string} params.estado - Estado (solicitado|en_proceso|completado|cancelado)
   * @param {number} params.tipo_laboratorio_id - ID del tipo de laboratorio
   * @returns {Promise} Response con { laboratorios, total }
   */
  getAll(params = {}) {
    return axios.get('/laboratorios', { params })
  },

  /**
   * Obtener un laboratorio por ID (incluye alertas si está completado)
   * @param {number} id - ID del laboratorio
   * @returns {Promise} Response con datos completos + alertas
   */
  getById(id) {
    return axios.get(`/laboratorios/${id}`)
  },

  /**
   * Solicitar un nuevo estudio de laboratorio (solo médicos)
   * @param {Object} data - Datos de la solicitud
   * @param {number} data.paciente_id - ID del paciente
   * @param {number} data.medico_id - ID del médico
   * @param {number} data.tipo_laboratorio_id - ID del tipo
   * @param {string} data.fecha_solicitud - Fecha (opcional, default hoy)
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con el laboratorio creado
   */
  create(data) {
    return axios.post('/laboratorios', data)
  },

  /**
   * Registrar resultados de un laboratorio
   * @param {number} id - ID del laboratorio
   * @param {Object} data - Datos de los resultados
   * @param {string} data.fecha_resultado - Fecha (opcional, default hoy)
   * @param {Object} data.resultados - JSON con valores {parametro: {valor, unidad}}
   * @param {string} data.interpretacion - Interpretación médica (opcional)
   * @param {string} data.laboratorio_externo - Nombre del lab externo (opcional)
   * @param {string} data.archivo_url - URL del PDF/imagen (opcional)
   * @returns {Promise} Response con laboratorio actualizado + alertas
   */
  registrarResultados(id, data) {
    return axios.put(`/laboratorios/${id}/resultados`, data)
  },

  /**
   * Cancelar un laboratorio solicitado
   * @param {number} id - ID del laboratorio
   * @param {Object} data - Datos de cancelación
   * @param {string} data.motivo - Motivo de cancelación (opcional)
   * @returns {Promise} Response de confirmación
   */
  cancelar(id, data = {}) {
    return axios.put(`/laboratorios/${id}/cancelar`, data)
  },

  // ==========================================
  // HISTORIAL Y COMPARACIÓN
  // ==========================================

  /**
   * Obtener historial de laboratorios de un paciente
   * @param {number} pacienteId - ID del paciente
   * @param {Object} params - Parámetros opcionales
   * @param {boolean} params.completados - Solo estudios completados
   * @returns {Promise} Response con lista de laboratorios
   */
  getByPaciente(pacienteId, params = {}) {
    return axios.get(`/laboratorios/paciente/${pacienteId}`, { params })
  },

  /**
   * Obtener histórico de un parámetro específico (para gráficas)
   * @param {number} pacienteId - ID del paciente
   * @param {number} tipoLaboratorioId - ID del tipo de laboratorio
   * @param {string} parametro - Nombre del parámetro (ej: "hemoglobina")
   * @param {Object} params - Parámetros opcionales
   * @param {number} params.limite - Cantidad de resultados (default 10)
   * @returns {Promise} Response con [{fecha, valor}, ...]
   */
  getHistoricoParametro(pacienteId, tipoLaboratorioId, parametro, params = {}) {
    return axios.get(
      `/laboratorios/historico/${pacienteId}/${tipoLaboratorioId}/${parametro}`,
      { params }
    )
  },

  /**
   * Comparar últimos 3 resultados del mismo tipo
   * @param {number} pacienteId - ID del paciente
   * @param {number} tipoLaboratorioId - ID del tipo de laboratorio
   * @returns {Promise} Response con comparación y tendencias
   */
  comparar(pacienteId, tipoLaboratorioId) {
    return axios.get(`/laboratorios/comparar/${pacienteId}/${tipoLaboratorioId}`)
  },

  // ==========================================
  // TIPOS DE LABORATORIO Y CATÁLOGOS
  // ==========================================

  /**
   * Obtener lista de tipos de laboratorio
   * @param {Object} params - Parámetros opcionales
   * @param {string} params.categoria - Filtrar por categoría
   * @returns {Promise} Response con tipos (incluye agrupación por_categoria)
   */
  getTipos(params = {}) {
    return axios.get('/laboratorios/tipos', { params })
  },

  /**
   * Obtener un tipo de laboratorio con sus valores de referencia
   * @param {number} id - ID del tipo
   * @returns {Promise} Response con tipo + valores_referencia[]
   */
  getTipoById(id) {
    return axios.get(`/laboratorios/tipos/${id}`)
  },

  /**
   * Obtener valores de referencia para un tipo de laboratorio
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.tipo_laboratorio_id - ID del tipo (requerido)
   * @param {string} params.parametro - Nombre del parámetro (opcional)
   * @param {number} params.edad - Edad del paciente (opcional)
   * @param {string} params.sexo - Sexo (M/F) (opcional)
   * @returns {Promise} Response con valores de referencia
   */
  getValoresReferencia(params) {
    return axios.get('/laboratorios/valores-referencia', { params })
  },

  /**
   * Obtener lista de categorías disponibles
   * @returns {Promise} Response con array de categorías
   */
  getCategorias() {
    return axios.get('/laboratorios/categorias')
  }
}
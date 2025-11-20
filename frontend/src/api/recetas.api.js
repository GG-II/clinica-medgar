import axios from './axios'

export const recetasAPI = {
  // ==========================================
  // CRUD BÁSICO DE RECETAS
  // ==========================================

  /**
   * Obtener lista de recetas con filtros
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.paciente_id - Filtrar por paciente
   * @param {number} params.medico_id - Filtrar por médico
   * @param {boolean} params.activas - Solo recetas activas
   * @returns {Promise} Response con { data, total }
   */
  getAll(params = {}) {
    return axios.get('/recetas', { params })
  },

  /**
   * Obtener una receta por ID
   * @param {number} id - ID de la receta
   * @returns {Promise} Response con datos completos de la receta
   */
  getById(id) {
    return axios.get(`/recetas/${id}`)
  },

  /**
   * Crear una nueva receta médica
   * @param {Object} data - Datos de la receta
   * @param {number} data.paciente_id - ID del paciente
   * @param {number} data.medico_id - ID del médico
   * @param {number} data.consulta_id - ID de la consulta (opcional)
   * @param {string} data.diagnostico - Diagnóstico (opcional)
   * @param {string} data.indicaciones_generales - Indicaciones generales (opcional)
   * @param {Array} data.medicamentos - Array de medicamentos
   * @returns {Promise} Response con la receta creada (puede incluir warnings de alergias)
   */
  create(data) {
    return axios.post('/recetas', data)
  },

  /**
   * Descargar receta en formato PDF
   * @param {number} id - ID de la receta
   * @returns {Promise} Response con archivo PDF (blob)
   */
  downloadPDF(id) {
    return axios.get(`/recetas/${id}/pdf`, {
      responseType: 'blob' // IMPORTANTE: Para manejar archivos binarios
    })
  },

  /**
   * Desactivar una receta (ya no se puede dispensar)
   * @param {number} id - ID de la receta
   * @returns {Promise} Response de confirmación
   */
  desactivar(id) {
    return axios.put(`/recetas/${id}/desactivar`)
  },

  /**
   * Obtener historial de recetas de un paciente
   * @param {number} pacienteId - ID del paciente
   * @param {Object} params - Parámetros opcionales
   * @param {boolean} params.activas - Solo recetas activas
   * @returns {Promise} Response con historial de recetas
   */
  getByPaciente(pacienteId, params = {}) {
    return axios.get(`/recetas/paciente/${pacienteId}`, { params })
  },

  // ==========================================
  // GESTIÓN DE MEDICAMENTOS
  // ==========================================

  /**
   * Buscar medicamentos (búsqueda predictiva)
   * @param {string} query - Término de búsqueda
   * @param {number} limit - Cantidad máxima de resultados (default: 10)
   * @returns {Promise} Response con lista de medicamentos coincidentes
   */
  searchMedicamentos(query, limit = 10) {
    return axios.get('/recetas/medicamentos', { 
      params: { q: query, limit } 
    })
  },

  /**
   * Obtener información completa de un medicamento
   * @param {number} id - ID del medicamento
   * @returns {Promise} Response con datos completos del medicamento
   */
  getMedicamentoById(id) {
    return axios.get(`/recetas/medicamentos/${id}`)
  },

  /**
   * Agregar un medicamento personalizado al catálogo
   * @param {Object} data - Datos del medicamento
   * @param {string} data.nombre_generico - Nombre genérico (requerido)
   * @param {string} data.nombre_comercial - Nombre comercial (opcional)
   * @param {string} data.presentacion - Presentación (opcional)
   * @param {string} data.concentracion - Concentración (opcional)
   * @param {string} data.via_administracion - Vía de administración (opcional)
   * @param {string} data.interacciones - Interacciones medicamentosas (opcional)
   * @param {string} data.contraindicaciones - Contraindicaciones (opcional)
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con el medicamento creado
   */
  createMedicamento(data) {
    return axios.post('/recetas/medicamentos', data)
  }
}
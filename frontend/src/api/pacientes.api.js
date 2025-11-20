import axios from './axios'

export const pacientesAPI = {
  // ==========================================
  // CRUD BÁSICO DE PACIENTES
  // ==========================================

  /**
   * Obtener lista de pacientes con paginación y filtros
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.page - Número de página (default: 1)
   * @param {number} params.per_page - Items por página (default: 25)
   * @param {string} params.search - Búsqueda por nombre, DPI o teléfono
   * @param {string} params.sexo - Filtro por sexo (M/F)
   * @param {boolean} params.tiene_igss - Filtro por IGSS
   * @returns {Promise} Response con { pacientes, total, page, per_page }
   */
  getAll(params = {}) {
    return axios.get('/pacientes', { params })
  },

  /**
   * Obtener un paciente por ID
   * @param {number} id - ID del paciente
   * @returns {Promise} Response con datos completos del paciente
   */
  getById(id) {
    return axios.get(`/pacientes/${id}`)
  },

  /**
   * Crear un nuevo paciente
   * @param {Object} data - Datos del paciente
   * @returns {Promise} Response con el paciente creado
   */
  create(data) {
    return axios.post('/pacientes', data)
  },

  /**
   * Actualizar un paciente existente
   * @param {number} id - ID del paciente
   * @param {Object} data - Datos a actualizar
   * @returns {Promise} Response con el paciente actualizado
   */
  update(id, data) {
    return axios.put(`/pacientes/${id}`, data)
  },

  /**
   * Eliminar un paciente (soft delete)
   * @param {number} id - ID del paciente
   * @returns {Promise} Response de confirmación
   */
  delete(id) {
    return axios.delete(`/pacientes/${id}`)
  },

  // ==========================================
// BÚSQUEDA Y FILTROS
// ==========================================

/**
 * Obtener lista de pacientes con paginación y filtros
 * @param {Object} params - Parámetros de búsqueda
 * @param {number} params.page - Número de página (default: 1)
 * @param {number} params.per_page - Items por página (default: 20)
 * @param {string} params.busqueda - Búsqueda por nombre, DPI o teléfono
 * @param {string} params.ordenar_por - Campo para ordenar
 * @returns {Promise} Response con { pacientes, total, page, per_page }
 */
getAll(params = {}) {
  // Mapear nombres del frontend al backend
  const backendParams = {
    page: params.page || 1,
    per_page: params.per_page || params.perPage || 25,
    busqueda: params.search || params.busqueda || '',
    ordenar_por: params.ordenar_por || 'nombre_completo'
  }
  
  return axios.get('/pacientes', { params: backendParams })
},

/**
 * Búsqueda rápida de pacientes (para autocomplete)
 * @param {string} query - Término de búsqueda
 * @returns {Promise} Response con lista de pacientes coincidentes
 */
search(query) {
  return axios.get('/pacientes/buscar', { 
    params: { termino: query }  // ✅ CORREGIDO: usa "termino"
  })
},

  /**
   * Obtener estadísticas de pacientes
   * @returns {Promise} Response con estadísticas generales
   */
  getStats() {
    return axios.get('/pacientes/estadisticas')
  },

  // ==========================================
  // GESTIÓN DE ARCHIVOS
  // ==========================================

  /**
   * Subir archivo (foto, documento, etc.) para un paciente
   * @param {number} pacienteId - ID del paciente
   * @param {FormData} formData - Archivo a subir
   * @returns {Promise} Response con info del archivo subido
   */
  uploadFile(pacienteId, formData) {
    return axios.post(`/uploads/paciente/${pacienteId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * Obtener lista de archivos de un paciente
   * @param {number} pacienteId - ID del paciente
   * @returns {Promise} Response con lista de archivos
   */
  getFiles(pacienteId) {
    return axios.get(`/uploads/paciente/${pacienteId}`)
  },

  /**
   * Eliminar un archivo
   * @param {number} fileId - ID del archivo
   * @returns {Promise} Response de confirmación
   */
  deleteFile(fileId) {
    return axios.delete(`/uploads/${fileId}`)
  },

  /**
   * Descargar un archivo
   * @param {number} fileId - ID del archivo
   * @returns {Promise} Response con el archivo
   */
  downloadFile(fileId) {
    return axios.get(`/uploads/download/${fileId}`, {
      responseType: 'blob'
    })
  },

  // ==========================================
  // HISTORIA CLÍNICA
  // ==========================================

  /**
   * Obtener historia clínica completa de un paciente
   * @param {number} pacienteId - ID del paciente
   * @returns {Promise} Response con historia clínica completa
   */
  getHistoriaClinica(pacienteId) {
    return axios.get(`/historia-clinica/paciente/${pacienteId}`)
  },

  /**
   * Actualizar historia clínica de un paciente
   * @param {number} pacienteId - ID del paciente
   * @param {Object} data - Datos de historia clínica a actualizar
   * @returns {Promise} Response con historia actualizada
   */
  updateHistoriaClinica(pacienteId, data) {
    return axios.put(`/historia-clinica/paciente/${pacienteId}`, data)
  },

  // ==========================================
  // SIGNOS VITALES
  // ==========================================

  /**
   * Registrar signos vitales (crea consulta automáticamente)
   * @param {Object} data - Datos de signos vitales
   * @returns {Promise} Response con signos vitales registrados
   */
  addSignosVitales(data) {
    return axios.post('/historia-clinica/signos-vitales', data)
  },

  // ==========================================
  // ANTECEDENTES
  // ==========================================

  /**
   * Registrar un antecedente
   * @param {Object} data - Datos del antecedente
   * @returns {Promise} Response con antecedente registrado
   */
  addAntecedente(data) {
    return axios.post('/historia-clinica/antecedentes', data)
  },

  /**
   * Eliminar un antecedente
   * @param {number} id - ID del antecedente
   * @returns {Promise} Response de confirmación
   */
  deleteAntecedente(id) {
    return axios.delete(`/historia-clinica/antecedentes/${id}`)
  },

  // ==========================================
  // VACUNAS
  // ==========================================

  /**
   * Obtener catálogo de vacunas disponibles
   * @returns {Promise} Response con lista de vacunas
   */
  getVacunas() {
    return axios.get('/historia-clinica/vacunas')
  },

  /**
   * Registrar aplicación de vacuna
   * @param {Object} data - Datos de la aplicación
   * @returns {Promise} Response con vacuna aplicada
   */
  aplicarVacuna(data) {
    return axios.post('/historia-clinica/vacunas/aplicar', data)
  }
}
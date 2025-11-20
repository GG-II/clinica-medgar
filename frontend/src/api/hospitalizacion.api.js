import axios from './axios'

export const hospitalizacionAPI = {
  // ==========================================
  // CAMAS
  // ==========================================

  /**
   * Obtener lista de camas
   * @param {Object} params - Parámetros opcionales
   * @param {string} params.estado - Filtrar por estado (disponible|ocupada|limpieza|mantenimiento)
   * @returns {Promise} Response con camas
   */
  getCamas(params = {}) {
    return axios.get('/hospitalizacion/camas', { params })
  },

  /**
   * Actualizar estado de una cama
   * @param {number} id - ID de la cama
   * @param {Object} data - Datos a actualizar
   * @param {string} data.estado - Nuevo estado
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con cama actualizada
   */
  updateCama(id, data) {
    return axios.put(`/hospitalizacion/camas/${id}`, data)
  },

  // ==========================================
  // HOSPITALIZACIONES
  // ==========================================

  /**
   * Obtener lista de hospitalizaciones con filtros
   * @param {Object} params - Parámetros de búsqueda
   * @param {string} params.estado - Estado (activo|egresado|transferido)
   * @param {number} params.paciente_id - ID del paciente
   * @param {string} params.fecha_inicio - Fecha inicio
   * @param {string} params.fecha_fin - Fecha fin
   * @returns {Promise} Response con hospitalizaciones
   */
  getHospitalizaciones(params = {}) {
    return axios.get('/hospitalizacion/', { params })
  },

  /**
   * Obtener una hospitalización específica con toda su información
   * @param {number} id - ID de la hospitalización
   * @returns {Promise} Response con datos completos (notas, órdenes, registros)
   */
  getHospitalizacionById(id) {
    return axios.get(`/hospitalizacion/${id}`)
  },

  /**
   * Ingresar paciente a hospitalización
   * @param {Object} data - Datos del ingreso
   * @param {number} data.paciente_id - ID del paciente
   * @param {number} data.cama_id - ID de la cama
   * @param {string} data.motivo_ingreso - Motivo de ingreso
   * @param {string} data.diagnostico_ingreso - Diagnóstico de ingreso
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con hospitalización creada
   */
  ingresarPaciente(data) {
    return axios.post('/hospitalizacion/', data)
  },

  /**
   * Egresar paciente de hospitalización
   * @param {number} id - ID de la hospitalización
   * @param {Object} data - Datos del egreso
   * @param {string} data.diagnostico_egreso - Diagnóstico de egreso
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con hospitalización actualizada
   */
  egresarPaciente(id, data) {
    return axios.post(`/hospitalizacion/${id}/egreso`, data)
  },

  // ==========================================
  // NOTAS MÉDICAS
  // ==========================================

  /**
   * Agregar nota médica a hospitalización
   * @param {number} id - ID de la hospitalización
   * @param {Object} data - Datos de la nota
   * @param {string} data.tipo_nota - Tipo (ingreso|evolucion|procedimiento|operatoria|egreso)
   * @param {string} data.contenido - Contenido de la nota
   * @param {Object} data.datos_adicionales - Datos adicionales en JSON (opcional)
   * @returns {Promise} Response con nota creada
   */
  agregarNotaMedica(id, data) {
    return axios.post(`/hospitalizacion/${id}/notas`, data)
  },

  // ==========================================
  // ÓRDENES MÉDICAS
  // ==========================================

  /**
   * Agregar orden médica a hospitalización
   * @param {number} id - ID de la hospitalización
   * @param {Object} data - Datos de la orden
   * @param {string} data.tipo_orden - Tipo (medicamento|dieta|signos_vitales|laboratorio|imagen|interconsulta|cuidados|otro)
   * @param {string} data.descripcion - Descripción de la orden
   * @param {string} data.indicaciones - Indicaciones (opcional)
   * @returns {Promise} Response con orden creada
   */
  agregarOrdenMedica(id, data) {
    return axios.post(`/hospitalizacion/${id}/ordenes`, data)
  },

  /**
   * Suspender una orden médica
   * @param {number} ordenId - ID de la orden
   * @param {Object} data - Datos de suspensión
   * @param {string} data.motivo - Motivo de suspensión (opcional)
   * @returns {Promise} Response con orden actualizada
   */
  suspenderOrden(ordenId, data = {}) {
    return axios.put(`/hospitalizacion/ordenes/${ordenId}/suspender`, data)
  },

  // ==========================================
  // REGISTRO ENFERMERÍA
  // ==========================================

  /**
   * Agregar registro de enfermería
   * @param {number} id - ID de la hospitalización
   * @param {Object} data - Datos del registro
   * @param {string} data.tipo_registro - Tipo (signos_vitales|medicamento|curacion|nota|otro)
   * @param {string} data.descripcion - Descripción
   * @param {Object} data.datos_json - Datos estructurados en JSON (opcional)
   * @returns {Promise} Response con registro creado
   */
  agregarRegistroEnfermeria(id, data) {
    return axios.post(`/hospitalizacion/${id}/enfermeria`, data)
  }
}
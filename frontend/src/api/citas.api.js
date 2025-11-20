import axios from './axios'

export const citasAPI = {
  // ==========================================
  // CRUD BÁSICO DE CITAS
  // ==========================================

  /**
   * Obtener lista de citas con paginación y filtros
   * @param {Object} params - Parámetros de búsqueda
   * @param {string} params.fecha_inicio - Fecha inicio (YYYY-MM-DD)
   * @param {string} params.fecha_fin - Fecha fin (YYYY-MM-DD)
   * @param {number} params.medico_id - Filtrar por médico
   * @param {number} params.paciente_id - Filtrar por paciente
   * @param {string} params.estado - Filtro por estado (programada, confirmada, etc.)
   * @returns {Promise} Response con { citas, total }
   */
  getAll(params = {}) {
    return axios.get('/citas', { params })
  },

  /**
   * Obtener citas del día actual
   * @param {number} medicoId - ID del médico (opcional)
   * @returns {Promise} Response con lista de citas de hoy
   */
  getHoy(medicoId = null) {
    const params = medicoId ? { medico_id: medicoId } : {}
    return axios.get('/citas/hoy', { params })
  },

  /**
   * Obtener una cita por ID
   * @param {number} id - ID de la cita
   * @returns {Promise} Response con datos completos de la cita
   */
  getById(id) {
    return axios.get(`/citas/${id}`)
  },

  /**
   * Crear una nueva cita (valida disponibilidad automáticamente)
   * @param {Object} data - Datos de la cita
   * @param {number} data.paciente_id - ID del paciente
   * @param {number} data.medico_id - ID del médico
   * @param {number} data.tipo_cita_id - ID del tipo de cita
   * @param {string} data.fecha_hora - Fecha y hora (YYYY-MM-DD HH:MM)
   * @param {number} data.duracion_minutos - Duración en minutos (opcional, default 20)
   * @param {string} data.motivo - Motivo de la cita (opcional)
   * @param {string} data.notas - Notas adicionales (opcional)
   * @param {boolean} data.es_emergencia - Es cita de emergencia (opcional, default false)
   * @returns {Promise} Response con la cita creada
   */
  create(data) {
    return axios.post('/citas', data)
  },

  /**
   * Actualizar una cita existente
   * @param {number} id - ID de la cita
   * @param {Object} data - Datos a actualizar
   * @returns {Promise} Response con la cita actualizada
   */
  update(id, data) {
    return axios.put(`/citas/${id}`, data)
  },

  /**
   * Cancelar una cita
   * @param {number} id - ID de la cita
   * @param {string} motivo - Motivo de cancelación (opcional)
   * @returns {Promise} Response de confirmación
   */
  delete(id, motivo = null) {
    const data = motivo ? { motivo } : {}
    return axios.delete(`/citas/${id}`, { data })
  },

  // ==========================================
  // DISPONIBILIDAD Y HORARIOS
  // ==========================================

  /**
   * Verificar si un médico está disponible en una hora específica
   * @param {number} medicoId - ID del médico
   * @param {string} fecha - Fecha (YYYY-MM-DD)
   * @param {string} hora - Hora (HH:MM)
   * @param {number} duracionMinutos - Duración en minutos (opcional, default 20)
   * @returns {Promise} Response con {disponible: boolean, mensaje: string}
   */
  verificarDisponibilidad(medicoId, fecha, hora, duracionMinutos = 20) {
    return axios.get('/citas/disponibilidad', {
      params: {
        medico_id: medicoId,
        fecha: fecha,
        hora: hora,
        duracion_minutos: duracionMinutos
      }
    })
  },

  /**
   * Obtener todos los horarios disponibles de un médico en una fecha
   * @param {number} medicoId - ID del médico
   * @param {string} fecha - Fecha (YYYY-MM-DD)
   * @param {number} duracionMinutos - Duración en minutos (opcional, default 20)
   * @returns {Promise} Response con {horarios_disponibles: [], total: number}
   */
  getHorariosDisponibles(medicoId, fecha, duracionMinutos = 20) {
    return axios.get('/citas/disponibilidad', {
      params: {
        medico_id: medicoId,
        fecha: fecha,
        duracion_minutos: duracionMinutos
        // NO enviar 'hora' para obtener todos los horarios del día
      }
    })
  },

  // ==========================================
  // CATÁLOGOS
  // ==========================================

  /**
   * Obtener lista de tipos de cita disponibles
   * @returns {Promise} Response con tipos de cita
   */
  getTipos() {
    return axios.get('/citas/tipos')
  },

  // ==========================================
  // ESTADÍSTICAS (admin/médico)
  // ==========================================

  /**
   * Obtener estadísticas de citas
   * @param {Object} params - Parámetros opcionales
   * @param {string} params.fecha_inicio - Fecha inicio (YYYY-MM-DD)
   * @param {string} params.fecha_fin - Fecha fin (YYYY-MM-DD)
   * @param {number} params.medico_id - Filtrar por médico
   * @returns {Promise} Response con estadísticas
   */
  getEstadisticas(params = {}) {
    return axios.get('/citas/estadisticas', { params })
  }
}
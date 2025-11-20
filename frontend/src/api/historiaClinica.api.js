import axios from './axios'

export const historiaClinicaAPI = {
  // ==========================================
  // HISTORIA CLÍNICA GENERAL
  // ==========================================

  /**
   * Obtener historia clínica completa de un paciente
   * Incluye: datos básicos, signos vitales, antecedentes y vacunas
   * @param {number} pacienteId - ID del paciente
   * @returns {Promise} Response con historia clínica completa
   */
  getHistoriaCompleta(pacienteId) {
    return axios.get(`/historia-clinica/paciente/${pacienteId}`)
  },

  /**
   * Actualizar datos generales de historia clínica
   * @param {number} pacienteId - ID del paciente
   * @param {Object} data - Datos a actualizar (tipo_sangre)
   * @returns {Promise} Response con historia actualizada
   */
  updateHistoria(pacienteId, data) {
    return axios.put(`/historia-clinica/paciente/${pacienteId}`, data)
  },

  // ==========================================
  // SIGNOS VITALES
  // ==========================================

  /**
   * Registrar signos vitales de un paciente
   * Crea automáticamente una consulta si no se proporciona consulta_id
   * @param {Object} data - Datos de signos vitales
   * @param {number} data.paciente_id - ID del paciente (requerido)
   * @param {string} data.motivo_consulta - Motivo (opcional, para crear consulta automática)
   * @param {number} data.presion_sistolica - Presión sistólica en mmHg
   * @param {number} data.presion_diastolica - Presión diastólica en mmHg
   * @param {number} data.frecuencia_cardiaca - FC en latidos/min
   * @param {number} data.temperatura - Temperatura en °C
   * @param {number} data.saturacion_oxigeno - Saturación O2 en %
   * @param {number} data.frecuencia_respiratoria - FR en resp/min
   * @param {number} data.peso - Peso en kg
   * @param {number} data.talla - Talla en cm
   * @param {number} data.perimetro_cefalico - Perímetro cefálico en cm (pediatría)
   * @param {number} data.frecuencia_cardiaca_fetal - FCF en latidos/min (embarazo)
   * @param {string} data.observaciones - Observaciones adicionales
   * @returns {Promise} Response con signos vitales registrados (incluye IMC calculado)
   */
  registrarSignosVitales(data) {
    return axios.post('/historia-clinica/signos-vitales', data)
  },

  // ==========================================
  // ANTECEDENTES
  // ==========================================

  /**
   * Registrar un antecedente del paciente
   * @param {Object} data - Datos del antecedente
   * @param {number} data.paciente_id - ID del paciente (requerido)
   * @param {string} data.tipo - Tipo de antecedente (requerido)
   *   Valores: 'medicos', 'quirurgicos', 'traumaticos', 'alergicos', 'ginecologicos', 'obstetricos'
   * @param {string} data.descripcion - Descripción del antecedente (requerido)
   * @param {string} data.fecha_evento - Fecha del evento (opcional, formato: YYYY-MM-DD)
   * @param {string} data.relevancia - Relevancia (opcional: 'alta', 'media', 'baja')
   * @returns {Promise} Response con antecedente registrado
   */
  registrarAntecedente(data) {
    return axios.post('/historia-clinica/antecedentes', data)
  },

  /**
   * Eliminar (desactivar) un antecedente
   * @param {number} antecedenteId - ID del antecedente
   * @returns {Promise} Response de confirmación
   */
  eliminarAntecedente(antecedenteId) {
    return axios.delete(`/historia-clinica/antecedentes/${antecedenteId}`)
  },

  // ==========================================
  // VACUNAS
  // ==========================================

  /**
   * Obtener catálogo de vacunas disponibles
   * @returns {Promise} Response con lista de vacunas activas
   */
  getCatalogoVacunas() {
    return axios.get('/historia-clinica/vacunas')
  },

  /**
   * Registrar aplicación de vacuna a un paciente
   * @param {Object} data - Datos de la aplicación
   * @param {number} data.paciente_id - ID del paciente (requerido)
   * @param {number} data.vacuna_id - ID de la vacuna (requerido)
   * @param {number} data.numero_dosis - Número de dosis (requerido)
   * @param {string} data.fecha_aplicacion - Fecha de aplicación (requerido, formato: YYYY-MM-DD)
   * @param {string} data.lote - Lote de la vacuna (opcional)
   * @param {string} data.aplicada_por - Nombre de quien aplicó (opcional)
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con vacuna aplicada
   */
  aplicarVacuna(data) {
    return axios.post('/historia-clinica/vacunas/aplicar', data)
  }
}
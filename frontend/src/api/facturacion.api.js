import axios from './axios'

export const facturacionAPI = {
  // ==========================================
  // CAJA
  // ==========================================

  /**
   * Abrir caja
   * @param {Object} data - Datos de apertura
   * @param {number} data.monto_inicial - Monto inicial en efectivo
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con caja abierta
   */
  abrirCaja(data) {
    return axios.post('/caja/apertura', data)
  },

  /**
   * Cerrar caja
   * @param {Object} data - Datos de cierre
   * @param {number} data.efectivo_contado - Efectivo físico contado
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con caja cerrada y diferencias
   */
  cerrarCaja(data) {
    return axios.post('/caja/cierre', data)
  },

  /**
   * Obtener estado actual de la caja
   * @returns {Promise} Response con caja actual o null
   */
  getEstadoCaja() {
    return axios.get('/caja/estado')
  },

  /**
   * Obtener movimientos de caja
   * @param {Object} params - Parámetros de filtro
   * @param {number} params.caja_id - ID de la caja
   * @param {string} params.tipo - Tipo de movimiento (ingreso|egreso)
   * @param {string} params.fecha_inicio - Fecha inicio
   * @param {string} params.fecha_fin - Fecha fin
   * @returns {Promise} Response con movimientos
   */
  getMovimientos(params = {}) {
    return axios.get('/caja/movimientos', { params })
  },

  /**
   * Registrar ingreso
   * @param {Object} data - Datos del ingreso
   * @param {string} data.categoria - Categoría del ingreso
   * @param {string} data.concepto - Concepto del ingreso
   * @param {number} data.monto - Monto
   * @param {string} data.forma_pago - Forma de pago
   * @param {number} data.paciente_id - ID del paciente (opcional)
   * @param {number} data.medico_id - ID del médico (opcional)
   * @returns {Promise} Response con movimiento registrado
   */
  registrarIngreso(data) {
    return axios.post('/caja/ingresos', data)
  },

  /**
   * Registrar egreso
   * @param {Object} data - Datos del egreso
   * @param {string} data.categoria - Categoría del egreso
   * @param {string} data.concepto - Concepto del egreso
   * @param {number} data.monto - Monto
   * @param {string} data.forma_pago - Forma de pago
   * @returns {Promise} Response con movimiento registrado
   */
  registrarEgreso(data) {
    return axios.post('/caja/egresos', data)
  },

  /**
   * Descargar reporte de arqueo de caja (PDF)
   * @param {number} id - ID de la caja
   * @returns {Promise} Response con PDF
   */
  descargarReporte(id) {
    return axios.get(`/caja/${id}/reporte`, {
      responseType: 'blob'
    })
  },

  // ==========================================
  // FACTURAS
  // ==========================================

  /**
   * Obtener lista de facturas con filtros
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.paciente_id - ID del paciente
   * @param {string} params.estado - Estado de la factura
   * @param {string} params.fecha_inicio - Fecha inicio
   * @param {string} params.fecha_fin - Fecha fin
   * @param {boolean} params.certificada_fel - Solo certificadas FEL
   * @returns {Promise} Response con facturas
   */
  getFacturas(params = {}) {
    return axios.get('/facturas', { params })
  },

  /**
   * Obtener una factura por ID
   * @param {number} id - ID de la factura
   * @returns {Promise} Response con datos completos de la factura
   */
  getFacturaById(id) {
    return axios.get(`/facturas/${id}`)
  },

  /**
   * Crear una nueva factura
   * @param {Object} data - Datos de la factura
   * @param {number} data.paciente_id - ID del paciente
   * @param {number} data.convenio_id - ID del convenio (opcional)
   * @param {string} data.nit_cliente - NIT del cliente
   * @param {string} data.nombre_cliente - Nombre del cliente
   * @param {string} data.direccion_cliente - Dirección del cliente
   * @param {Array} data.detalles - Array de items
   * @param {string} data.forma_pago - Forma de pago
   * @param {number} data.descuento - Descuento (opcional)
   * @returns {Promise} Response con la factura creada
   */
  createFactura(data) {
    return axios.post('/facturas', data)
  },

  /**
   * Anular una factura
   * @param {number} id - ID de la factura
   * @param {Object} data - Datos de anulación
   * @param {string} data.motivo - Motivo de anulación
   * @returns {Promise} Response de confirmación
   */
  anularFactura(id, data) {
    return axios.post(`/facturas/${id}/anular`, data)
  },

  /**
   * Certificar factura con FEL
   * @param {number} id - ID de la factura
   * @returns {Promise} Response con UUID y XML de FEL
   */
  certificarFEL(id) {
    return axios.post(`/facturas/${id}/certificar-fel`)
  },

  // ==========================================
  // CONVENIOS
  // ==========================================

  /**
   * Obtener lista de convenios
   * @param {Object} params - Parámetros opcionales
   * @param {boolean} params.solo_activos - Solo convenios activos
   * @returns {Promise} Response con convenios
   */
  getConvenios(params = {}) {
    return axios.get('/convenios', { params })
  },

  /**
   * Crear un nuevo convenio
   * @param {Object} data - Datos del convenio
   * @param {string} data.nombre - Nombre del convenio
   * @param {string} data.tipo - Tipo (igss|seguro_privado|empresa)
   * @param {number} data.porcentaje_cobertura - Porcentaje de cobertura
   * @param {number} data.dias_credito - Días de crédito
   * @returns {Promise} Response con el convenio creado
   */
  createConvenio(data) {
    return axios.post('/convenios', data)
  },

  // ==========================================
  // CUENTAS POR COBRAR
  // ==========================================

  /**
   * Obtener lista de cuentas por cobrar
   * @param {Object} params - Parámetros de filtro
   * @param {string} params.estado - Estado (pendiente|parcial|pagada|vencida)
   * @param {number} params.paciente_id - ID del paciente
   * @param {number} params.convenio_id - ID del convenio
   * @returns {Promise} Response con cuentas
   */
  getCuentasPorCobrar(params = {}) {
    return axios.get('/cuentas-por-cobrar', { params })
  },

  /**
   * Registrar pago a una cuenta por cobrar
   * @param {number} id - ID de la cuenta
   * @param {Object} data - Datos del pago
   * @param {number} data.monto_pago - Monto del pago
   * @param {string} data.forma_pago - Forma de pago
   * @param {string} data.numero_recibo - Número de recibo (opcional)
   * @param {string} data.observaciones - Observaciones (opcional)
   * @returns {Promise} Response con cuenta actualizada
   */
  registrarPago(id, data) {
    return axios.post(`/cuentas-por-cobrar/${id}/pagar`, data)
  }
}
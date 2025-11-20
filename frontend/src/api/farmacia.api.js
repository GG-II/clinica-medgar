import axios from './axios'

export const farmaciaAPI = {
  // ==========================================
  // PRODUCTOS
  // ==========================================

  /**
   * Obtener lista de productos con filtros
   * @param {Object} params - Parámetros de búsqueda
   * @param {string} params.q - Búsqueda por nombre o código
   * @param {string} params.tipo_producto - Tipo de producto
   * @param {boolean} params.solo_con_stock - Solo con stock disponible
   * @param {number} params.page - Número de página
   * @param {number} params.per_page - Items por página
   * @returns {Promise} Response con { productos, total, pages }
   */
  getProductos(params = {}) {
    return axios.get('/farmacia/productos', { params })
  },

  /**
   * Obtener un producto por ID
   * @param {number} id - ID del producto
   * @returns {Promise} Response con datos completos del producto
   */
  getProductoById(id) {
    return axios.get(`/farmacia/productos/${id}`)
  },

  /**
   * Crear un nuevo producto
   * @param {Object} data - Datos del producto
   * @returns {Promise} Response con el producto creado
   */
  createProducto(data) {
    return axios.post('/farmacia/productos', data)
  },

  /**
   * Actualizar un producto existente
   * @param {number} id - ID del producto
   * @param {Object} data - Datos a actualizar
   * @returns {Promise} Response con el producto actualizado
   */
  updateProducto(id, data) {
    return axios.put(`/farmacia/productos/${id}`, data)
  },

  /**
   * Obtener kardex (historial de movimientos) de un producto
   * @param {number} id - ID del producto
   * @param {Object} params - Parámetros opcionales
   * @param {string} params.fecha_inicio - Fecha inicio (YYYY-MM-DD)
   * @param {string} params.fecha_fin - Fecha fin (YYYY-MM-DD)
   * @returns {Promise} Response con producto y kardex
   */
  getKardex(id, params = {}) {
    return axios.get(`/farmacia/productos/${id}/kardex`, { params })
  },

  // ==========================================
  // ALERTAS Y REORDEN
  // ==========================================

  /**
   * Obtener todas las alertas de inventario
   * @returns {Promise} Response con alertas agrupadas
   */
  getAlertas() {
    return axios.get('/farmacia/alertas')
  },

  /**
   * Obtener productos que necesitan reorden
   * @returns {Promise} Response con productos bajo stock
   */
  getProductosReorden() {
    return axios.get('/farmacia/productos/reorden')
  },

  /**
   * Ajustar inventario de un producto
   * @param {Object} data - Datos del ajuste
   * @param {number} data.producto_id - ID del producto
   * @param {number} data.stock_nuevo - Nuevo stock total
   * @param {string} data.motivo - Motivo del ajuste
   * @returns {Promise} Response con resultado del ajuste
   */
  ajustarInventario(data) {
    return axios.post('/farmacia/inventario/ajustar', data)
  },

  // ==========================================
  // INVENTARIO
  // ==========================================

  /**
   * Obtener valor total del inventario
   * @returns {Promise} Response con valor total
   */
  getInventarioValorizado() {
    return axios.get('/farmacia/inventario/valorizado')
  },

  /**
   * Dispensar un producto
   * @param {Object} data - Datos de la dispensación
   * @param {number} data.producto_id - ID del producto
   * @param {number} data.cantidad - Cantidad a dispensar
   * @param {number} data.receta_id - ID de receta (opcional)
   * @returns {Promise} Response con resultado
   */
  dispensarProducto(data) {
    return axios.post('/farmacia/dispensacion', data)
  },

  // ==========================================
  // PROVEEDORES
  // ==========================================

  /**
   * Obtener lista de proveedores
   * @param {Object} params - Parámetros opcionales
   * @param {boolean} params.solo_activos - Solo proveedores activos
   * @returns {Promise} Response con proveedores
   */
  getProveedores(params = {}) {
    return axios.get('/farmacia/proveedores', { params })
  },

  /**
   * Crear un nuevo proveedor
   * @param {Object} data - Datos del proveedor
   * @returns {Promise} Response con el proveedor creado
   */
  createProveedor(data) {
    return axios.post('/farmacia/proveedores', data)
  },

  // ==========================================
  // COMPRAS
  // ==========================================

  /**
   * Obtener lista de compras
   * @param {Object} params - Parámetros de filtro
   * @param {number} params.proveedor_id - ID del proveedor
   * @param {string} params.estado - Estado de la compra
   * @param {string} params.fecha_inicio - Fecha inicio
   * @param {string} params.fecha_fin - Fecha fin
   * @returns {Promise} Response con compras
   */
  getCompras(params = {}) {
    return axios.get('/farmacia/compras', { params })
  },

  /**
   * Crear una nueva orden de compra
   * @param {Object} data - Datos de la compra
   * @param {number} data.proveedor_id - ID del proveedor
   * @param {Array} data.detalles - Array de productos
   * @returns {Promise} Response con la compra creada
   */
  createCompra(data) {
    return axios.post('/farmacia/compras', data)
  },

  /**
   * Marcar compra como recibida (actualiza inventario)
   * @param {number} id - ID de la compra
   * @returns {Promise} Response con compra actualizada
   */
  recibirCompra(id) {
    return axios.post(`/farmacia/compras/${id}/recibir`)
  }
}
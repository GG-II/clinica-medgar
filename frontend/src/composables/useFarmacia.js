import { ref, computed } from 'vue'
import { useFarmaciaStore } from '@/stores/farmacia'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de farmacia
 * Proporciona métodos y estado reactivo para componentes
 */
export function useFarmacia() {
  const store = useFarmaciaStore()
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
  
  const productos = computed(() => store.productos)
  const productoActual = computed(() => store.productoActual)
  const loading = computed(() => store.loading)
  const error = computed(() => store.error)
  const pagination = computed(() => store.pagination)
  const kardex = computed(() => store.kardex)
  const alertas = computed(() => store.alertas)
  const productosReorden = computed(() => store.productosReorden)
  const inventarioValorizado = computed(() => store.inventarioValorizado)
  const proveedores = computed(() => store.proveedores)
  const compras = computed(() => store.compras)
  const compraActual = computed(() => store.compraActual)
  const filters = computed(() => store.filters)
  const hasProductos = computed(() => store.hasProductos)
  const totalAlertas = computed(() => store.totalAlertas)
  const alertasCriticas = computed(() => store.alertasCriticas)

  // ==========================================
  // MÉTODOS BÁSICOS - PRODUCTOS
  // ==========================================

  /**
   * Cargar lista de productos
   */
  async function loadProductos(params = {}) {
    try {
      await store.fetchProductos(params)
    } catch (err) {
      console.error('Error al cargar productos:', err)
    }
  }

  /**
   * Cargar un producto específico
   */
  async function loadProducto(id) {
    try {
      await store.fetchProductoById(id)
    } catch (err) {
      console.error('Error al cargar producto:', err)
    }
  }

  /**
   * Crear nuevo producto
   */
  async function crearProducto(data) {
    try {
      const result = await store.createProducto(data)
      
      if (result.success) {
        return result
      }
    } catch (err) {
      console.error('Error al crear producto:', err)
      throw err
    }
  }

  /**
   * Actualizar producto existente
   */
  async function actualizarProducto(id, data) {
    try {
      const result = await store.updateProducto(id, data)
      return result
    } catch (err) {
      console.error('Error al actualizar producto:', err)
      throw err
    }
  }

  /**
   * Cargar kardex de un producto
   */
  async function loadKardex(id, params = {}) {
    try {
      await store.fetchKardex(id, params)
    } catch (err) {
      console.error('Error al cargar kardex:', err)
    }
  }

  // ==========================================
  // BÚSQUEDA CON DEBOUNCE
  // ==========================================

  /**
   * Buscar productos con debounce (espera 300ms después de dejar de escribir)
   */
  function buscarProductos(query) {
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
        const result = await store.fetchProductos({ q: query })
        searchResults.value = result.productos || []
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
  // ALERTAS Y REORDEN
  // ==========================================

  /**
   * Cargar alertas de inventario
   */
  async function loadAlertas() {
    try {
      await store.fetchAlertas()
    } catch (err) {
      console.error('Error al cargar alertas:', err)
    }
  }

  /**
   * Cargar productos que necesitan reorden
   */
  async function loadProductosReorden() {
    try {
      await store.fetchProductosReorden()
    } catch (err) {
      console.error('Error al cargar productos a reorden:', err)
    }
  }

  /**
   * Ajustar inventario de un producto
   */
  async function ajustarInventario(productoId, stockNuevo, motivo) {
    try {
      const result = await store.ajustarInventario({
        producto_id: productoId,
        stock_nuevo: stockNuevo,
        motivo
      })
      return result
    } catch (err) {
      console.error('Error al ajustar inventario:', err)
      throw err
    }
  }

  // ==========================================
  // INVENTARIO
  // ==========================================

  /**
   * Cargar inventario valorizado
   */
  async function loadInventarioValorizado() {
    try {
      await store.fetchInventarioValorizado()
    } catch (err) {
      console.error('Error al cargar inventario valorizado:', err)
    }
  }

  /**
   * Dispensar producto
   */
  async function dispensarProducto(productoId, cantidad, recetaId = null) {
    try {
      const result = await store.dispensarProducto({
        producto_id: productoId,
        cantidad,
        receta_id: recetaId
      })
      return result
    } catch (err) {
      console.error('Error al dispensar producto:', err)
      throw err
    }
  }

  // ==========================================
  // PROVEEDORES
  // ==========================================

  /**
   * Cargar proveedores
   */
  async function loadProveedores(params = {}) {
    try {
      await store.fetchProveedores(params)
    } catch (err) {
      console.error('Error al cargar proveedores:', err)
    }
  }

  /**
   * Crear nuevo proveedor
   */
  async function crearProveedor(data) {
    try {
      const result = await store.createProveedor(data)
      return result
    } catch (err) {
      console.error('Error al crear proveedor:', err)
      throw err
    }
  }

  // ==========================================
  // COMPRAS
  // ==========================================

  /**
   * Cargar órdenes de compra
   */
  async function loadCompras(params = {}) {
    try {
      await store.fetchCompras(params)
    } catch (err) {
      console.error('Error al cargar compras:', err)
    }
  }

  /**
   * Crear nueva orden de compra
   */
  async function crearCompra(data) {
    try {
      const result = await store.createCompra(data)
      return result
    } catch (err) {
      console.error('Error al crear compra:', err)
      throw err
    }
  }

  /**
   * Recibir compra con confirmación
   */
  async function recibirCompra(id, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm(
        '¿Está seguro de marcar esta compra como recibida? Esto actualizará el inventario.'
      )
      if (!confirmado) return false
    }
    
    try {
      const result = await store.recibirCompra(id)
      return result
    } catch (err) {
      console.error('Error al recibir compra:', err)
      throw err
    }
  }

  // ==========================================
  // FILTROS Y PAGINACIÓN
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
  // UTILIDADES
  // ==========================================

  /**
   * Obtener nombre del tipo de producto
   */
  function obtenerNombreTipo(tipo) {
    const tipos = {
      'medicamento': 'Medicamento',
      'insumo_medico': 'Insumo Médico',
      'material_curacion': 'Material de Curación',
      'solucion_iv': 'Solución IV',
      'equipo': 'Equipo'
    }
    return tipos[tipo] || tipo
  }

  /**
   * Obtener badge del tipo de producto
   */
  function obtenerBadgeTipo(tipo) {
    const badges = {
      'medicamento': { text: 'Medicamento', variant: 'primary' },
      'insumo_medico': { text: 'Insumo Médico', variant: 'info' },
      'material_curacion': { text: 'Material Curación', variant: 'warning' },
      'solucion_iv': { text: 'Solución IV', variant: 'success' },
      'equipo': { text: 'Equipo', variant: 'secondary' }
    }
    return badges[tipo] || { text: tipo, variant: 'secondary' }
  }

  /**
   * Obtener badge del estado de compra
   */
  function obtenerBadgeEstadoCompra(estado) {
    const badges = {
      'pendiente': { text: 'Pendiente', variant: 'warning' },
      'recibida': { text: 'Recibida', variant: 'success' },
      'parcial': { text: 'Parcial', variant: 'info' },
      'cancelada': { text: 'Cancelada', variant: 'danger' }
    }
    return badges[estado] || { text: estado, variant: 'secondary' }
  }

  /**
   * Verificar si producto tiene stock bajo
   */
  function tieneStockBajo(producto) {
    return producto.stock_actual <= producto.stock_minimo
  }

  /**
   * Verificar si producto está vencido
   */
  function estaVencido(producto) {
    if (!producto.fecha_vencimiento) return false
    
    const hoy = new Date()
    const vencimiento = new Date(producto.fecha_vencimiento)
    return vencimiento < hoy
  }

  /**
   * Calcular días hasta vencimiento
   */
  function diasHastaVencimiento(producto) {
    if (!producto.fecha_vencimiento) return null
    
    const hoy = new Date()
    const vencimiento = new Date(producto.fecha_vencimiento)
    const diferencia = vencimiento - hoy
    const dias = Math.ceil(diferencia / (1000 * 60 * 60 * 24))
    
    return dias
  }

  /**
   * Obtener color según días hasta vencimiento
   */
  function obtenerColorVencimiento(producto) {
    const dias = diasHastaVencimiento(producto)
    
    if (dias === null) return 'text-gray-600'
    if (dias < 0) return 'text-red-600'
    if (dias <= 30) return 'text-orange-600'
    if (dias <= 60) return 'text-yellow-600'
    
    return 'text-green-600'
  }

  /**
   * Formatear precio
   */
  function formatearPrecio(precio) {
    if (!precio) return 'Q 0.00'
    
    return `Q ${parseFloat(precio).toFixed(2)}`
  }

  /**
   * Calcular margen de utilidad
   */
  function calcularMargen(producto) {
    if (!producto.precio_compra || producto.precio_compra === 0) {
      return null
    }
    
    const margen = ((producto.precio_venta - producto.precio_compra) / producto.precio_compra) * 100
    return Math.round(margen * 100) / 100
  }

  /**
   * Obtener severidad de alerta de stock
   */
  function obtenerSeveridadStock(producto) {
    if (producto.stock_actual === 0) return 'critica'
    if (producto.stock_actual <= producto.stock_minimo) return 'alta'
    return 'normal'
  }

  /**
   * Formatear fecha
   */
  function formatearFecha(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    return date.toLocaleDateString('es-GT', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  /**
   * Formatear fecha corta
   */
  function formatearFechaCorta(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    return date.toLocaleDateString('es-GT', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  }

  /**
   * Obtener texto del tipo de movimiento
   */
  function obtenerTextoMovimiento(tipo) {
    const tipos = {
      'entrada': '➕ Entrada',
      'salida': '➖ Salida',
      'ajuste': '🔧 Ajuste',
      'devolucion': '↩️ Devolución'
    }
    return tipos[tipo] || tipo
  }

  /**
   * Obtener color del tipo de movimiento
   */
  function obtenerColorMovimiento(tipo) {
    const colores = {
      'entrada': 'text-green-600',
      'salida': 'text-red-600',
      'ajuste': 'text-blue-600',
      'devolucion': 'text-orange-600'
    }
    return colores[tipo] || 'text-gray-600'
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================

  return {
    // Estado
    productos,
    productoActual,
    loading,
    error,
    pagination,
    kardex,
    alertas,
    productosReorden,
    inventarioValorizado,
    proveedores,
    compras,
    compraActual,
    filters,
    hasProductos,
    totalAlertas,
    alertasCriticas,
    
    // Búsqueda
    searchQuery,
    searchResults,
    searchLoading,
    buscarProductos,
    limpiarBusqueda,
    
    // Productos
    loadProductos,
    loadProducto,
    crearProducto,
    actualizarProducto,
    loadKardex,
    
    // Alertas
    loadAlertas,
    loadProductosReorden,
    ajustarInventario,
    
    // Inventario
    loadInventarioValorizado,
    dispensarProducto,
    
    // Proveedores
    loadProveedores,
    crearProveedor,
    
    // Compras
    loadCompras,
    crearCompra,
    recibirCompra,
    
    // Filtros y paginación
    aplicarFiltros,
    limpiarFiltros,
    irAPagina,
    cambiarItemsPorPagina,
    paginaAnterior,
    paginaSiguiente,
    
    // Utilidades
    obtenerNombreTipo,
    obtenerBadgeTipo,
    obtenerBadgeEstadoCompra,
    tieneStockBajo,
    estaVencido,
    diasHastaVencimiento,
    obtenerColorVencimiento,
    formatearPrecio,
    calcularMargen,
    obtenerSeveridadStock,
    formatearFecha,
    formatearFechaCorta,
    obtenerTextoMovimiento,
    obtenerColorMovimiento
  }
}
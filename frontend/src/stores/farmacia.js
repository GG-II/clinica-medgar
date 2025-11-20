import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { farmaciaAPI } from '@/api/farmacia.api'

export const useFarmaciaStore = defineStore('farmacia', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  const productos = ref([])
  const productoActual = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Paginación
  const pagination = ref({
    page: 1,
    perPage: 20,
    total: 0,
    totalPages: 0
  })
  
  // Kardex
  const kardex = ref([])
  
  // Alertas
  const alertas = ref({
    stock_minimo: [],
    vencidos: [],
    por_vencer_30: [],
    por_vencer_60: []
  })
  
  // Productos a reorden
  const productosReorden = ref([])
  
  // Inventario valorizado
  const inventarioValorizado = ref(null)
  
  // Proveedores
  const proveedores = ref([])
  
  // Compras
  const compras = ref([])
  const compraActual = ref(null)
  
  // Filtros activos
  const filters = ref({
    q: '',
    tipo_producto: null,
    solo_con_stock: false,
    proveedor_id: null,
    estado: null
  })

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Obtener producto por ID desde la lista en memoria
   */
  const getProductoById = computed(() => {
    return (id) => {
      return productos.value.find(p => p.id === parseInt(id))
    }
  })
  
  /**
   * Obtener solo productos activos
   */
  const getProductosActivos = computed(() => {
    return productos.value.filter(p => p.activo)
  })
  
  /**
   * Obtener productos con stock bajo
   */
  const getProductosStockBajo = computed(() => {
    return productos.value.filter(p => p.stock_actual <= p.stock_minimo)
  })
  
  /**
   * Total de productos
   */
  const totalProductos = computed(() => pagination.value.total)
  
  /**
   * Verificar si hay productos cargados
   */
  const hasProductos = computed(() => productos.value.length > 0)
  
  /**
   * Total de alertas
   */
  const totalAlertas = computed(() => {
    return (alertas.value.stock_minimo?.length || 0) +
           (alertas.value.vencidos?.length || 0) +
           (alertas.value.por_vencer_30?.length || 0) +
           (alertas.value.por_vencer_60?.length || 0)
  })
  
  /**
   * Alertas críticas (vencidos + stock cero)
   */
  const alertasCriticas = computed(() => {
    const vencidos = alertas.value.vencidos || []
    const stockCero = (alertas.value.stock_minimo || []).filter(
      a => a.producto.stock_actual === 0
    )
    return [...vencidos, ...stockCero]
  })
  
  /**
   * Obtener proveedor por ID
   */
  const getProveedorById = computed(() => {
    return (id) => {
      return proveedores.value.find(p => p.id === parseInt(id))
    }
  })
  
  /**
   * Obtener compra por ID
   */
  const getCompraById = computed(() => {
    return (id) => {
      return compras.value.find(c => c.id === parseInt(id))
    }
  })

  // ==========================================
  // ACTIONS - PRODUCTOS
  // ==========================================

  /**
   * Obtener lista de productos con filtros
   */
  async function fetchProductos(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      // Combinar filtros activos con parámetros adicionales
      const queryParams = {
        ...filters.value,
        page: pagination.value.page,
        per_page: pagination.value.perPage,
        ...params
      }
      
      const response = await farmaciaAPI.getProductos(queryParams)
      
      if (response.data.success) {
        productos.value = response.data.productos
        
        // Actualizar paginación si viene en la respuesta
        if (response.data.total !== undefined) {
          pagination.value = {
            page: response.data.current_page || pagination.value.page,
            perPage: pagination.value.perPage,
            total: response.data.total,
            totalPages: response.data.pages || Math.ceil(response.data.total / pagination.value.perPage)
          }
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar productos'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener un producto específico por ID
   */
  async function fetchProductoById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.getProductoById(id)
      
      if (response.data.success) {
        productoActual.value = response.data.producto
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar producto'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear un nuevo producto
   */
  async function createProducto(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.createProducto(data)
      
      if (response.data.success) {
        // Agregar el nuevo producto a la lista local
        productos.value.unshift(response.data.producto)
        pagination.value.total += 1
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear producto'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar un producto existente
   */
  async function updateProducto(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.updateProducto(id, data)
      
      if (response.data.success) {
        // Actualizar en la lista local
        const index = productos.value.findIndex(p => p.id === parseInt(id))
        if (index !== -1) {
          productos.value[index] = response.data.producto
        }
        
        // Actualizar producto actual si es el mismo
        if (productoActual.value?.id === parseInt(id)) {
          productoActual.value = response.data.producto
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar producto'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener kardex de un producto
   */
  async function fetchKardex(id, params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.getKardex(id, params)
      
      if (response.data.success) {
        kardex.value = response.data.kardex
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar kardex'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - ALERTAS Y REORDEN
  // ==========================================

  /**
   * Obtener alertas de inventario
   */
  async function fetchAlertas() {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.getAlertas()
      
      if (response.data.success) {
        alertas.value = response.data.alertas
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar alertas'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener productos que necesitan reorden
   */
  async function fetchProductosReorden() {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.getProductosReorden()
      
      if (response.data.success) {
        productosReorden.value = response.data.productos
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar productos a reorden'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Ajustar inventario de un producto
   */
  async function ajustarInventario(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.ajustarInventario(data)
      
      if (response.data.success) {
        // Actualizar producto en la lista si existe
        const producto = response.data.resultado?.producto
        if (producto) {
          const index = productos.value.findIndex(p => p.id === producto.id)
          if (index !== -1) {
            productos.value[index] = producto
          }
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al ajustar inventario'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - INVENTARIO
  // ==========================================

  /**
   * Obtener inventario valorizado
   */
  async function fetchInventarioValorizado() {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.getInventarioValorizado()
      
      if (response.data.success) {
        inventarioValorizado.value = response.data.inventario
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar inventario valorizado'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Dispensar producto
   */
  async function dispensarProducto(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.dispensarProducto(data)
      
      if (response.data.success) {
        // Actualizar producto en la lista si existe
        const producto = response.data.resultado?.producto
        if (producto) {
          const index = productos.value.findIndex(p => p.id === producto.id)
          if (index !== -1) {
            productos.value[index] = producto
          }
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al dispensar producto'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - PROVEEDORES
  // ==========================================

  /**
   * Obtener lista de proveedores
   */
  async function fetchProveedores(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.getProveedores(params)
      
      if (response.data.success) {
        proveedores.value = response.data.proveedores
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar proveedores'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear un nuevo proveedor
   */
  async function createProveedor(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.createProveedor(data)
      
      if (response.data.success) {
        // Agregar el nuevo proveedor a la lista local
        proveedores.value.unshift(response.data.proveedor)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear proveedor'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - COMPRAS
  // ==========================================

  /**
   * Obtener lista de compras
   */
  async function fetchCompras(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.getCompras(params)
      
      if (response.data.success) {
        compras.value = response.data.compras
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar compras'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear una nueva orden de compra
   */
  async function createCompra(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.createCompra(data)
      
      if (response.data.success) {
        // Agregar la nueva compra a la lista local
        compras.value.unshift(response.data.compra)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear compra'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Recibir una compra (actualiza inventario)
   */
  async function recibirCompra(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await farmaciaAPI.recibirCompra(id)
      
      if (response.data.success) {
        // Actualizar compra en la lista local
        const index = compras.value.findIndex(c => c.id === parseInt(id))
        if (index !== -1) {
          compras.value[index] = response.data.compra
        }
        
        // Actualizar compra actual si es la misma
        if (compraActual.value?.id === parseInt(id)) {
          compraActual.value = response.data.compra
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al recibir compra'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // ACTIONS - FILTROS Y UTILIDADES
  // ==========================================

  /**
   * Aplicar filtros y recargar lista
   */
  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1 // Resetear a primera página
    await fetchProductos()
  }

  /**
   * Limpiar todos los filtros
   */
  async function clearFilters() {
    filters.value = {
      q: '',
      tipo_producto: null,
      solo_con_stock: false,
      proveedor_id: null,
      estado: null
    }
    pagination.value.page = 1
    await fetchProductos()
  }

  /**
   * Cambiar página
   */
  async function setPage(page) {
    pagination.value.page = page
    await fetchProductos()
  }

  /**
   * Cambiar items por página
   */
  async function setPerPage(perPage) {
    pagination.value.perPage = perPage
    pagination.value.page = 1
    await fetchProductos()
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    productos.value = []
    productoActual.value = null
    loading.value = false
    error.value = null
    pagination.value = {
      page: 1,
      perPage: 20,
      total: 0,
      totalPages: 0
    }
    kardex.value = []
    alertas.value = {
      stock_minimo: [],
      vencidos: [],
      por_vencer_30: [],
      por_vencer_60: []
    }
    productosReorden.value = []
    inventarioValorizado.value = null
    proveedores.value = []
    compras.value = []
    compraActual.value = null
    filters.value = {
      q: '',
      tipo_producto: null,
      solo_con_stock: false,
      proveedor_id: null,
      estado: null
    }
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State
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
    
    // Getters
    getProductoById,
    getProductosActivos,
    getProductosStockBajo,
    totalProductos,
    hasProductos,
    totalAlertas,
    alertasCriticas,
    getProveedorById,
    getCompraById,
    
    // Actions - Productos
    fetchProductos,
    fetchProductoById,
    createProducto,
    updateProducto,
    fetchKardex,
    
    // Actions - Alertas
    fetchAlertas,
    fetchProductosReorden,
    ajustarInventario,
    
    // Actions - Inventario
    fetchInventarioValorizado,
    dispensarProducto,
    
    // Actions - Proveedores
    fetchProveedores,
    createProveedor,
    
    // Actions - Compras
    fetchCompras,
    createCompra,
    recibirCompra,
    
    // Actions - Filtros
    setFilters,
    clearFilters,
    setPage,
    setPerPage,
    resetStore
  }
})
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { facturacionAPI } from '@/api/facturacion.api'

export const useFacturacionStore = defineStore('facturacion', () => {
  // ==========================================
  // STATE (Estado Reactivo)
  // ==========================================
  
  // Caja
  const cajaActual = ref(null)
  const movimientos = ref([])
  const loadingCaja = ref(false)
  
  // Facturas
  const facturas = ref([])
  const facturaActual = ref(null)
  const loadingFacturas = ref(false)
  
  // Convenios
  const convenios = ref([])
  const loadingConvenios = ref(false)
  
  // Cuentas por Cobrar
  const cuentasPorCobrar = ref([])
  const cuentaActual = ref(null)
  const loadingCuentas = ref(false)
  
  // Errores
  const error = ref(null)
  
  // Filtros
  const filters = ref({
    estado: null,
    fecha_inicio: null,
    fecha_fin: null,
    paciente_id: null,
    convenio_id: null
  })

  // ==========================================
  // GETTERS (Propiedades Computadas)
  // ==========================================
  
  /**
   * Verificar si hay una caja abierta
   */
  const hayCajaAbierta = computed(() => {
    return cajaActual.value?.estado === 'abierta'
  })
  
  /**
   * Obtener total de ingresos de la caja actual
   */
  const totalIngresos = computed(() => {
    if (!cajaActual.value) return 0
    return parseFloat(cajaActual.value.total_ingresos || 0)
  })
  
  /**
   * Obtener total de egresos de la caja actual
   */
  const totalEgresos = computed(() => {
    if (!cajaActual.value) return 0
    return parseFloat(cajaActual.value.total_egresos || 0)
  })
  
  /**
   * Calcular monto esperado en caja
   */
  const montoEsperado = computed(() => {
    if (!cajaActual.value) return 0
    const inicial = parseFloat(cajaActual.value.monto_inicial || 0)
    return inicial + totalIngresos.value - totalEgresos.value
  })
  
  /**
   * Obtener diferencia de caja
   */
  const diferenciaCaja = computed(() => {
    if (!cajaActual.value || !cajaActual.value.diferencia) return 0
    return parseFloat(cajaActual.value.diferencia)
  })
  
  /**
   * Obtener facturas por estado
   */
  const getFacturasByEstado = computed(() => {
    return (estado) => {
      return facturas.value.filter(f => f.estado === estado)
    }
  })
  
  /**
   * Obtener facturas pendientes
   */
  const facturasPendientes = computed(() => {
    return facturas.value.filter(f => f.estado === 'pendiente')
  })
  
  /**
   * Obtener facturas certificadas FEL
   */
  const facturasCertificadas = computed(() => {
    return facturas.value.filter(f => f.certificada_fel)
  })
  
  /**
   * Total de facturas
   */
  const totalFacturas = computed(() => facturas.value.length)
  
  /**
   * Obtener cuentas vencidas
   */
  const cuentasVencidas = computed(() => {
    return cuentasPorCobrar.value.filter(c => c.estado === 'vencida')
  })
  
  /**
   * Obtener cuentas pendientes
   */
  const cuentasPendientes = computed(() => {
    return cuentasPorCobrar.value.filter(c => 
      c.estado === 'pendiente' || c.estado === 'parcial'
    )
  })
  
  /**
   * Total por cobrar
   */
  const totalPorCobrar = computed(() => {
    return cuentasPorCobrar.value.reduce((sum, c) => {
      return sum + parseFloat(c.saldo_pendiente || 0)
    }, 0)
  })
  
  /**
   * Obtener convenio por ID
   */
  const getConvenioById = computed(() => {
    return (id) => {
      return convenios.value.find(c => c.id === parseInt(id))
    }
  })

// ==========================================
  // ACTIONS - CAJA
  // ==========================================

  /**
   * Obtener estado actual de la caja
   */
  async function fetchEstadoCaja() {
    loadingCaja.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.getEstadoCaja()
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "caja" no "data"
        cajaActual.value = response.data.caja
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al obtener estado de caja'
      throw err
    } finally {
      loadingCaja.value = false
    }
  }

  /**
   * Abrir caja
   */
  async function abrirCaja(montoInicial, observaciones = null) {
    loadingCaja.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.abrirCaja({
        monto_inicial: montoInicial,
        observaciones
      })
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "caja" no "data"
        cajaActual.value = response.data.caja
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al abrir caja'
      throw err
    } finally {
      loadingCaja.value = false
    }
  }

  /**
   * Cerrar caja
   */
  async function cerrarCaja(efectivoContado, observaciones = null) {
    loadingCaja.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.cerrarCaja({
        efectivo_contado: efectivoContado,
        observaciones
      })
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "caja" no "data"
        cajaActual.value = response.data.caja
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cerrar caja'
      throw err
    } finally {
      loadingCaja.value = false
    }
  }

  /**
   * Obtener movimientos de caja
   */
  async function fetchMovimientos(params = {}) {
    loadingCaja.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.getMovimientos(params)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "movimientos" no "data"
        movimientos.value = response.data.movimientos || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar movimientos'
      throw err
    } finally {
      loadingCaja.value = false
    }
  }

  /**
   * Registrar ingreso
   */
  async function registrarIngreso(data) {
    loadingCaja.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.registrarIngreso(data)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "movimiento" no "data"
        const movimiento = response.data.movimiento
        movimientos.value.unshift(movimiento)
        
        // Actualizar totales de caja actual
        if (cajaActual.value) {
          cajaActual.value.total_ingresos = 
            (parseFloat(cajaActual.value.total_ingresos) || 0) + parseFloat(data.monto)
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrar ingreso'
      throw err
    } finally {
      loadingCaja.value = false
    }
  }

  /**
   * Registrar egreso
   */
  async function registrarEgreso(data) {
    loadingCaja.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.registrarEgreso(data)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "movimiento" no "data"
        const movimiento = response.data.movimiento
        movimientos.value.unshift(movimiento)
        
        // Actualizar totales de caja actual
        if (cajaActual.value) {
          cajaActual.value.total_egresos = 
            (parseFloat(cajaActual.value.total_egresos) || 0) + parseFloat(data.monto)
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrar egreso'
      throw err
    } finally {
      loadingCaja.value = false
    }
  }

  /**
   * Descargar reporte de arqueo
   */
  async function descargarReporte(cajaId) {
    try {
      const response = await facturacionAPI.descargarReporte(cajaId)
      
      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `arqueo_caja_${cajaId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      
      return true
    } catch (err) {
      error.value = 'Error al descargar reporte'
      throw err
    }
  }

  // ==========================================
  // ACTIONS - FACTURAS
  // ==========================================

  /**
   * Obtener lista de facturas
   */
  async function fetchFacturas(params = {}) {
    loadingFacturas.value = true
    error.value = null
    
    try {
      const queryParams = {
        ...filters.value,
        ...params
      }
      
      const response = await facturacionAPI.getFacturas(queryParams)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "facturas" no "data"
        facturas.value = response.data.facturas || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar facturas'
      throw err
    } finally {
      loadingFacturas.value = false
    }
  }

  /**
   * Obtener una factura por ID
   */
  async function fetchFacturaById(id) {
    loadingFacturas.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.getFacturaById(id)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "factura" no "data"
        facturaActual.value = response.data.factura
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar factura'
      throw err
    } finally {
      loadingFacturas.value = false
    }
  }

  /**
   * Crear una nueva factura
   */
  async function createFactura(data) {
    loadingFacturas.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.createFactura(data)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "factura" no "data"
        facturas.value.unshift(response.data.factura)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear factura'
      throw err
    } finally {
      loadingFacturas.value = false
    }
  }

  /**
   * Anular una factura
   */
  async function anularFactura(id, motivo) {
    loadingFacturas.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.anularFactura(id, { motivo })
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "factura" no "data"
        const factura = response.data.factura
        const index = facturas.value.findIndex(f => f.id === parseInt(id))
        if (index !== -1) {
          facturas.value[index] = factura
        }
        
        if (facturaActual.value?.id === parseInt(id)) {
          facturaActual.value = factura
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al anular factura'
      throw err
    } finally {
      loadingFacturas.value = false
    }
  }

  /**
   * Certificar factura con FEL
   */
  async function certificarFEL(id) {
    loadingFacturas.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.certificarFEL(id)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "factura" no "data"
        const factura = response.data.factura
        const index = facturas.value.findIndex(f => f.id === parseInt(id))
        if (index !== -1) {
          facturas.value[index] = factura
        }
        
        if (facturaActual.value?.id === parseInt(id)) {
          facturaActual.value = factura
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al certificar FEL'
      throw err
    } finally {
      loadingFacturas.value = false
    }
  }

  // ==========================================
  // ACTIONS - CONVENIOS
  // ==========================================

  /**
   * Obtener lista de convenios
   */
  async function fetchConvenios(params = {}) {
    loadingConvenios.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.getConvenios(params)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "convenios" no "data"
        convenios.value = response.data.convenios || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar convenios'
      throw err
    } finally {
      loadingConvenios.value = false
    }
  }

  /**
   * Crear un nuevo convenio
   */
  async function createConvenio(data) {
    loadingConvenios.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.createConvenio(data)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "convenio" no "data"
        convenios.value.unshift(response.data.convenio)
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear convenio'
      throw err
    } finally {
      loadingConvenios.value = false
    }
  }

  // ==========================================
  // ACTIONS - CUENTAS POR COBRAR
  // ==========================================

  /**
   * Obtener lista de cuentas por cobrar
   */
  async function fetchCuentasPorCobrar(params = {}) {
    loadingCuentas.value = true
    error.value = null
    
    try {
      const queryParams = {
        ...filters.value,
        ...params
      }
      
      const response = await facturacionAPI.getCuentasPorCobrar(queryParams)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "cuentas" no "data"
        cuentasPorCobrar.value = response.data.cuentas || []
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar cuentas por cobrar'
      throw err
    } finally {
      loadingCuentas.value = false
    }
  }

  /**
   * Registrar pago a una cuenta por cobrar
   */
  async function registrarPagoCuenta(id, data) {
    loadingCuentas.value = true
    error.value = null
    
    try {
      const response = await facturacionAPI.registrarPago(id, data)
      
      if (response.data.success) {
        // ✅ CORRECCIÓN: El backend devuelve "cuenta" no "data"
        const cuenta = response.data.cuenta
        const index = cuentasPorCobrar.value.findIndex(c => c.id === parseInt(id))
        if (index !== -1) {
          cuentasPorCobrar.value[index] = cuenta
        }
        
        if (cuentaActual.value?.id === parseInt(id)) {
          cuentaActual.value = cuenta
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrar pago'
      throw err
    } finally {
      loadingCuentas.value = false
    }
  }

  // ==========================================
  // ACTIONS - FILTROS Y UTILIDADES
  // ==========================================

  /**
   * Aplicar filtros
   */
  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
  }

  /**
   * Limpiar filtros
   */
  function clearFilters() {
    filters.value = {
      estado: null,
      fecha_inicio: null,
      fecha_fin: null,
      paciente_id: null,
      convenio_id: null
    }
  }

  /**
   * Limpiar estado del store
   */
  function resetStore() {
    cajaActual.value = null
    movimientos.value = []
    facturas.value = []
    facturaActual.value = null
    convenios.value = []
    cuentasPorCobrar.value = []
    cuentaActual.value = null
    error.value = null
    clearFilters()
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================
  
  return {
    // State - Caja
    cajaActual,
    movimientos,
    loadingCaja,
    
    // State - Facturas
    facturas,
    facturaActual,
    loadingFacturas,
    
    // State - Convenios
    convenios,
    loadingConvenios,
    
    // State - Cuentas
    cuentasPorCobrar,
    cuentaActual,
    loadingCuentas,
    
    // State - General
    error,
    filters,
    
    // Getters - Caja
    hayCajaAbierta,
    totalIngresos,
    totalEgresos,
    montoEsperado,
    diferenciaCaja,
    
    // Getters - Facturas
    getFacturasByEstado,
    facturasPendientes,
    facturasCertificadas,
    totalFacturas,
    
    // Getters - Cuentas
    cuentasVencidas,
    cuentasPendientes,
    totalPorCobrar,
    
    // Getters - Convenios
    getConvenioById,
    
    // Actions - Caja
    fetchEstadoCaja,
    abrirCaja,
    cerrarCaja,
    fetchMovimientos,
    registrarIngreso,
    registrarEgreso,
    descargarReporte,
    
    // Actions - Facturas
    fetchFacturas,
    fetchFacturaById,
    createFactura,
    anularFactura,
    certificarFEL,
    
    // Actions - Convenios
    fetchConvenios,
    createConvenio,
    
    // Actions - Cuentas
    fetchCuentasPorCobrar,
    registrarPagoCuenta,
    
    // Actions - Utilidades
    setFilters,
    clearFilters,
    resetStore
  }
})
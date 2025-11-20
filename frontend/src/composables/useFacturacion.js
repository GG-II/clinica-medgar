import { ref, computed } from 'vue'
import { useFacturacionStore } from '@/stores/facturacion'
import { useRouter } from 'vue-router'

/**
 * Composable para manejar la lógica de facturación y caja
 * Proporciona métodos y estado reactivo para componentes
 */
export function useFacturacion() {
  const store = useFacturacionStore()
  const router = useRouter()

  // ==========================================
  // COMPUTED PROPERTIES (desde el store)
  // ==========================================
  
  // Caja
  const cajaActual = computed(() => store.cajaActual)
  const movimientos = computed(() => store.movimientos)
  const loadingCaja = computed(() => store.loadingCaja)
  const hayCajaAbierta = computed(() => store.hayCajaAbierta)
  const totalIngresos = computed(() => store.totalIngresos)
  const totalEgresos = computed(() => store.totalEgresos)
  const montoEsperado = computed(() => store.montoEsperado)
  const diferenciaCaja = computed(() => store.diferenciaCaja)
  
  // Facturas
  const facturas = computed(() => store.facturas)
  const facturaActual = computed(() => store.facturaActual)
  const loadingFacturas = computed(() => store.loadingFacturas)
  const facturasPendientes = computed(() => store.facturasPendientes)
  const facturasCertificadas = computed(() => store.facturasCertificadas)
  const totalFacturas = computed(() => store.totalFacturas)
  
  // Convenios
  const convenios = computed(() => store.convenios)
  const loadingConvenios = computed(() => store.loadingConvenios)
  
  // Cuentas por Cobrar
  const cuentasPorCobrar = computed(() => store.cuentasPorCobrar)
  const cuentaActual = computed(() => store.cuentaActual)
  const loadingCuentas = computed(() => store.loadingCuentas)
  const cuentasVencidas = computed(() => store.cuentasVencidas)
  const cuentasPendientes = computed(() => store.cuentasPendientes)
  const totalPorCobrar = computed(() => store.totalPorCobrar)
  
  // General
  const error = computed(() => store.error)
  const filters = computed(() => store.filters)

  // ==========================================
  // MÉTODOS - CAJA
  // ==========================================

  /**
   * Cargar estado de la caja
   */
  async function loadEstadoCaja() {
    try {
      await store.fetchEstadoCaja()
    } catch (err) {
      console.error('Error al cargar estado de caja:', err)
    }
  }

  /**
   * Abrir caja con confirmación
   */
  async function abrirCaja(montoInicial, observaciones = null) {
    try {
      const result = await store.abrirCaja(montoInicial, observaciones)
      return result
    } catch (err) {
      console.error('Error al abrir caja:', err)
      throw err
    }
  }

  /**
   * Cerrar caja con confirmación
   */
  async function cerrarCaja(efectivoContado, observaciones = null, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm(
        '¿Está seguro de cerrar la caja? Esta acción no se puede deshacer.'
      )
      if (!confirmado) return false
    }
    
    try {
      const result = await store.cerrarCaja(efectivoContado, observaciones)
      return result
    } catch (err) {
      console.error('Error al cerrar caja:', err)
      throw err
    }
  }

  /**
   * Cargar movimientos de caja
   */
  async function loadMovimientos(params = {}) {
    try {
      await store.fetchMovimientos(params)
    } catch (err) {
      console.error('Error al cargar movimientos:', err)
    }
  }

  /**
   * Registrar ingreso
   */
  async function registrarIngreso(data) {
    try {
      const result = await store.registrarIngreso(data)
      return result
    } catch (err) {
      console.error('Error al registrar ingreso:', err)
      throw err
    }
  }

  /**
   * Registrar egreso
   */
  async function registrarEgreso(data) {
    try {
      const result = await store.registrarEgreso(data)
      return result
    } catch (err) {
      console.error('Error al registrar egreso:', err)
      throw err
    }
  }

  /**
   * Descargar reporte de arqueo
   */
  async function descargarReporte(cajaId) {
    try {
      await store.descargarReporte(cajaId)
    } catch (err) {
      console.error('Error al descargar reporte:', err)
      throw err
    }
  }

  // ==========================================
  // MÉTODOS - FACTURAS
  // ==========================================

  /**
   * Cargar facturas
   */
  async function loadFacturas(params = {}) {
    try {
      await store.fetchFacturas(params)
    } catch (err) {
      console.error('Error al cargar facturas:', err)
    }
  }

  /**
   * Cargar una factura específica
   */
  async function loadFactura(id) {
    try {
      await store.fetchFacturaById(id)
    } catch (err) {
      console.error('Error al cargar factura:', err)
    }
  }

  /**
   * Crear nueva factura
   */
  async function crearFactura(data) {
    try {
      const result = await store.createFactura(data)
      
      if (result.success) {
        // Redirigir al detalle de la factura creada (opcional)
        // router.push(`/facturas/${result.data.id}`)
        return result
      }
    } catch (err) {
      console.error('Error al crear factura:', err)
      throw err
    }
  }

  /**
   * Anular factura con confirmación
   */
  async function anularFactura(id, motivo, confirmar = true) {
    if (confirmar) {
      const confirmado = window.confirm(
        '¿Está seguro de anular esta factura? Esta acción no se puede deshacer.'
      )
      if (!confirmado) return false
    }
    
    try {
      const result = await store.anularFactura(id, motivo)
      return result
    } catch (err) {
      console.error('Error al anular factura:', err)
      throw err
    }
  }

  /**
   * Certificar factura con FEL
   */
  async function certificarFEL(id) {
    try {
      const result = await store.certificarFEL(id)
      return result
    } catch (err) {
      console.error('Error al certificar FEL:', err)
      throw err
    }
  }

  // ==========================================
  // MÉTODOS - CONVENIOS
  // ==========================================

  /**
   * Cargar convenios
   */
  async function loadConvenios(params = {}) {
    try {
      await store.fetchConvenios(params)
    } catch (err) {
      console.error('Error al cargar convenios:', err)
    }
  }

  /**
   * Crear nuevo convenio
   */
  async function crearConvenio(data) {
    try {
      const result = await store.createConvenio(data)
      return result
    } catch (err) {
      console.error('Error al crear convenio:', err)
      throw err
    }
  }

  // ==========================================
  // MÉTODOS - CUENTAS POR COBRAR
  // ==========================================

  /**
   * Cargar cuentas por cobrar
   */
  async function loadCuentasPorCobrar(params = {}) {
    try {
      await store.fetchCuentasPorCobrar(params)
    } catch (err) {
      console.error('Error al cargar cuentas por cobrar:', err)
    }
  }

  /**
   * Registrar pago a cuenta
   */
  async function registrarPago(cuentaId, data) {
    try {
      const result = await store.registrarPagoCuenta(cuentaId, data)
      return result
    } catch (err) {
      console.error('Error al registrar pago:', err)
      throw err
    }
  }

  // ==========================================
  // FILTROS
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
  function limpiarFiltros() {
    store.clearFilters()
  }

  // ==========================================
  // UTILIDADES - CAJA
  // ==========================================

  /**
   * Formatear monto en quetzales
   */
  function formatearMonto(monto) {
    if (!monto && monto !== 0) return 'Q 0.00'
    return `Q ${parseFloat(monto).toFixed(2)}`
  }

  /**
   * Obtener badge del tipo de movimiento
   */
  function obtenerBadgeMovimiento(tipo) {
    const badges = {
      'ingreso': { text: 'Ingreso', variant: 'success' },
      'egreso': { text: 'Egreso', variant: 'danger' }
    }
    return badges[tipo] || { text: tipo, variant: 'secondary' }
  }

  /**
   * Obtener color del tipo de movimiento
   */
  function obtenerColorMovimiento(tipo) {
    const colores = {
      'ingreso': 'text-green-600',
      'egreso': 'text-red-600'
    }
    return colores[tipo] || 'text-gray-600'
  }

  /**
   * Verificar si hay diferencia en caja
   */
  function hayDiferencia() {
    return diferenciaCaja.value !== 0
  }

  /**
   * Obtener severidad de diferencia
   */
  function obtenerSeveridadDiferencia() {
    const diff = Math.abs(diferenciaCaja.value)
    if (diff === 0) return 'normal'
    if (diff <= 10) return 'leve'
    if (diff <= 50) return 'media'
    return 'alta'
  }

  // ==========================================
  // UTILIDADES - FACTURAS
  // ==========================================

  /**
   * Obtener badge del estado de factura
   */
  function obtenerBadgeEstadoFactura(estado) {
    const badges = {
      'pendiente': { text: 'Pendiente', variant: 'warning' },
      'pagada': { text: 'Pagada', variant: 'success' },
      'anulada': { text: 'Anulada', variant: 'danger' },
      'credito': { text: 'Crédito', variant: 'info' }
    }
    return badges[estado] || { text: estado, variant: 'secondary' }
  }

  /**
   * Obtener badge de forma de pago
   */
  function obtenerBadgeFormaPago(formaPago) {
    const badges = {
      'efectivo': { text: 'Efectivo', variant: 'success' },
      'transferencia': { text: 'Transferencia', variant: 'info' },
      'tarjeta': { text: 'Tarjeta', variant: 'primary' },
      'cheque': { text: 'Cheque', variant: 'warning' },
      'credito': { text: 'Crédito', variant: 'secondary' }
    }
    return badges[formaPago] || { text: formaPago, variant: 'secondary' }
  }

  /**
   * Verificar si factura está certificada FEL
   */
  function estaCertificadaFEL(factura) {
    return factura.certificada_fel === true
  }

  /**
   * Generar número de factura display
   */
  function formatearNumeroFactura(factura) {
    if (!factura.numero_factura) return 'Sin número'
    return factura.numero_factura
  }

  // ==========================================
  // UTILIDADES - CONVENIOS
  // ==========================================

  /**
   * Obtener badge del tipo de convenio
   */
  function obtenerBadgeTipoConvenio(tipo) {
    const badges = {
      'igss': { text: 'IGSS', variant: 'primary' },
      'seguro_privado': { text: 'Seguro Privado', variant: 'info' },
      'empresa': { text: 'Empresa', variant: 'success' }
    }
    return badges[tipo] || { text: tipo, variant: 'secondary' }
  }

  /**
   * Calcular monto con cobertura de convenio
   */
  function calcularMontoConCobertura(monto, porcentajeCobertura) {
    if (!porcentajeCobertura) return monto
    
    const cobertura = (monto * porcentajeCobertura) / 100
    const montoPaciente = monto - cobertura
    
    return {
      total: monto,
      cobertura,
      paciente: montoPaciente
    }
  }

  // ==========================================
  // UTILIDADES - CUENTAS POR COBRAR
  // ==========================================

  /**
   * Obtener badge del estado de cuenta
   */
  function obtenerBadgeEstadoCuenta(estado) {
    const badges = {
      'pendiente': { text: 'Pendiente', variant: 'warning' },
      'parcial': { text: 'Parcial', variant: 'info' },
      'pagada': { text: 'Pagada', variant: 'success' },
      'vencida': { text: 'Vencida', variant: 'danger' }
    }
    return badges[estado] || { text: estado, variant: 'secondary' }
  }

  /**
   * Verificar si cuenta está vencida
   */
  function estaVencida(cuenta) {
    if (!cuenta.fecha_vencimiento) return false
    
    const hoy = new Date()
    const vencimiento = new Date(cuenta.fecha_vencimiento)
    
    return vencimiento < hoy && cuenta.saldo_pendiente > 0
  }

  /**
   * Calcular días hasta vencimiento
   */
  function diasHastaVencimiento(cuenta) {
    if (!cuenta.fecha_vencimiento) return null
    
    const hoy = new Date()
    const vencimiento = new Date(cuenta.fecha_vencimiento)
    const diferencia = vencimiento - hoy
    const dias = Math.ceil(diferencia / (1000 * 60 * 60 * 24))
    
    return dias
  }

  /**
   * Obtener color según días hasta vencimiento
   */
  function obtenerColorVencimiento(cuenta) {
    const dias = diasHastaVencimiento(cuenta)
    
    if (dias === null) return 'text-gray-600'
    if (dias < 0) return 'text-red-600'
    if (dias <= 7) return 'text-orange-600'
    if (dias <= 15) return 'text-yellow-600'
    
    return 'text-green-600'
  }

  /**
   * Calcular porcentaje pagado
   */
  function calcularPorcentajePagado(cuenta) {
    if (!cuenta.monto_total || cuenta.monto_total === 0) return 0
    
    const porcentaje = (cuenta.monto_pagado / cuenta.monto_total) * 100
    return Math.round(porcentaje)
  }

  // ==========================================
  // UTILIDADES - FECHAS
  // ==========================================

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
   * Formatear fecha y hora
   */
  function formatearFechaHora(fecha) {
    if (!fecha) return ''
    
    const date = new Date(fecha)
    return date.toLocaleString('es-GT', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  // ==========================================
  // RETURN (Exportar todo)
  // ==========================================

  return {
    // Estado - Caja
    cajaActual,
    movimientos,
    loadingCaja,
    hayCajaAbierta,
    totalIngresos,
    totalEgresos,
    montoEsperado,
    diferenciaCaja,
    
    // Estado - Facturas
    facturas,
    facturaActual,
    loadingFacturas,
    facturasPendientes,
    facturasCertificadas,
    totalFacturas,
    
    // Estado - Convenios
    convenios,
    loadingConvenios,
    
    // Estado - Cuentas
    cuentasPorCobrar,
    cuentaActual,
    loadingCuentas,
    cuentasVencidas,
    cuentasPendientes,
    totalPorCobrar,
    
    // Estado - General
    error,
    filters,
    
    // Métodos - Caja
    loadEstadoCaja,
    abrirCaja,
    cerrarCaja,
    loadMovimientos,
    registrarIngreso,
    registrarEgreso,
    descargarReporte,
    
    // Métodos - Facturas
    loadFacturas,
    loadFactura,
    crearFactura,
    anularFactura,
    certificarFEL,
    
    // Métodos - Convenios
    loadConvenios,
    crearConvenio,
    
    // Métodos - Cuentas
    loadCuentasPorCobrar,
    registrarPago,
    
    // Filtros
    aplicarFiltros,
    limpiarFiltros,
    
    // Utilidades - Caja
    formatearMonto,
    obtenerBadgeMovimiento,
    obtenerColorMovimiento,
    hayDiferencia,
    obtenerSeveridadDiferencia,
    
    // Utilidades - Facturas
    obtenerBadgeEstadoFactura,
    obtenerBadgeFormaPago,
    estaCertificadaFEL,
    formatearNumeroFactura,
    
    // Utilidades - Convenios
    obtenerBadgeTipoConvenio,
    calcularMontoConCobertura,
    
    // Utilidades - Cuentas
    obtenerBadgeEstadoCuenta,
    estaVencida,
    diasHastaVencimiento,
    obtenerColorVencimiento,
    calcularPorcentajePagado,
    
    // Utilidades - Fechas
    formatearFecha,
    formatearFechaCorta,
    formatearFechaHora
  }
}
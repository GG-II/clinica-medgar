<template>
  <MainLayout>
    <div class="dashboard-header">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600 mt-2">Bienvenido, {{ authStore.userName }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando dashboard...</p>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- KPIs Cards -->
      <div class="kpi-grid">
        <!-- KPI 1: Citas Hoy -->
        <div class="kpi-card">
          <div class="kpi-icon bg-purple-100 text-purple-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Citas Hoy</p>
            <p class="kpi-value">{{ totalCitasHoy }}</p>
            <p class="kpi-change text-gray-600">
              {{ citasPendientes }} pendientes
            </p>
          </div>
        </div>

        <!-- KPI 2: Ingresos Hoy -->
        <div class="kpi-card">
          <div class="kpi-icon bg-green-100 text-green-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Ingresos Hoy</p>
            <p class="kpi-value">{{ formatearMonto(totalIngresos) }}</p>
            <p class="kpi-change text-green-600">
              {{ hayCajaAbierta ? 'Caja abierta' : 'Caja cerrada' }}
            </p>
          </div>
        </div>

        <!-- KPI 3: Alertas Críticas -->
        <div class="kpi-card">
          <div class="kpi-icon bg-orange-100 text-orange-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Alertas Críticas</p>
            <p class="kpi-value">{{ alertasCriticas.length }}</p>
            <p class="kpi-change text-orange-600">
              {{ totalAlertas }} total
            </p>
          </div>
        </div>
      </div>

      <!-- Próximas Citas -->
      <div class="card mt-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Próximas Citas</h2>
          <button 
            @click="$router.push('/agenda')" 
            class="text-sm text-purple-600 hover:text-purple-700"
          >
            Ver todas →
          </button>
        </div>
        
        <div v-if="loadingCitas" class="text-center py-4">
          <p class="text-gray-600">Cargando citas...</p>
        </div>
        
        <div v-else-if="proximasCitas.length === 0" class="text-center py-8 text-gray-500">
          <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <p class="font-medium">No hay citas próximas</p>
        </div>
        
        <div v-else class="appointments-list">
          <div 
            v-for="cita in proximasCitas" 
            :key="cita.id"
            class="appointment-item"
            @click="$router.push(`/citas/${cita.id}`)"
          >
            <div class="appointment-time">
              <span class="time">{{ formatearHora(cita.fecha_hora) }}</span>
              <span class="date">{{ formatearFechaRelativa(cita.fecha_hora) }}</span>
            </div>
            <div class="appointment-info">
              <p class="patient-name">{{ cita.paciente?.nombre_completo || 'Sin paciente' }}</p>
              <p class="appointment-type">{{ cita.tipo_cita?.nombre || 'Consulta general' }}</p>
            </div>
            <span :class="getBadgeClass(cita.estado)">
              {{ obtenerNombreEstado(cita.estado) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Alertas de Farmacia (si hay) -->
      <div v-if="alertasCriticas.length > 0" class="card mt-6">
        <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
          <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          Alertas Críticas de Farmacia
        </h2>
        <div class="space-y-2">
          <div 
            v-for="alerta in alertasCriticas.slice(0, 5)" 
            :key="alerta.producto_id"
            class="alert-item"
          >
            <div class="flex items-center gap-3">
              <span class="text-2xl">
                {{ alerta.tipo === 'stock_bajo' ? '📦' : '⚠️' }}
              </span>
              <div class="flex-1">
                <p class="font-medium text-gray-900">{{ alerta.producto_nombre }}</p>
                <p class="text-sm text-gray-600">{{ alerta.mensaje }}</p>
              </div>
              <span class="badge badge-danger">{{ alerta.tipo_display }}</span>
            </div>
          </div>
          <button 
            @click="$router.push('/farmacia/alertas')" 
            class="w-full text-center text-sm text-purple-600 hover:text-purple-700 pt-2"
          >
            Ver todas las alertas ({{ totalAlertas }})
          </button>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MainLayout from '@/components/layout/MainLayout.vue'

// Composables - SOLO importar composables (REGLA DE ORO)
import { useCitas } from '@/composables/useCitas'
import { useFacturacion } from '@/composables/useFacturacion'
import { useFarmacia } from '@/composables/useFarmacia'

// Auth Store (este sí se puede usar directamente porque es global)
const authStore = useAuthStore()
const router = useRouter()

// ==========================================
// EXTRAER LO NECESARIO DE LOS COMPOSABLES
// ==========================================

// CITAS - Extraer solo lo necesario
const {
  citas,
  loading: loadingCitas,
  loadCitasHoy,
  getProximasCitas,
  formatearHora,
  formatearFecha,
  obtenerNombreEstado,
  contarPorEstado
} = useCitas()

// FACTURACIÓN - Extraer solo lo necesario
const {
  hayCajaAbierta,
  totalIngresos,
  totalEgresos,
  loadEstadoCaja,
  formatearMonto
} = useFacturacion()

// FARMACIA - Extraer solo lo necesario
const {
  alertas,
  alertasCriticas,
  totalAlertas,
  loadAlertas
} = useFarmacia()

// ==========================================
// ESTADO LOCAL (SOLO para control de UI)
// ==========================================

const isLoading = ref(true)

// ==========================================
// COMPUTED PROPERTIES
// ==========================================

// Total de citas hoy
const totalCitasHoy = computed(() => {
  return citas.value.length
})

// Citas pendientes
const citasPendientes = computed(() => {
  return contarPorEstado('programada') + contarPorEstado('confirmada')
})

// Próximas 5 citas
const proximasCitas = computed(() => {
  return getProximasCitas(5)
})

// ==========================================
// FUNCIONES LOCALES
// ==========================================

/**
 * Obtener clase CSS para el badge según el estado
 */
function getBadgeClass(estado) {
  const classes = {
    'programada': 'badge badge-info',
    'confirmada': 'badge badge-success',
    'en_curso': 'badge badge-warning',
    'completada': 'badge badge-secondary',
    'cancelada': 'badge badge-danger',
    'no_asistio': 'badge badge-warning'
  }
  return classes[estado] || 'badge badge-secondary'
}

/**
 * Formatear fecha de forma relativa (Hoy, Mañana, DD/MM)
 */
function formatearFechaRelativa(fechaHora) {
  if (!fechaHora) return ''
  
  const fecha = new Date(fechaHora)
  const hoy = new Date()
  hoy.setHours(0, 0, 0, 0)
  
  const fechaCita = new Date(fecha)
  fechaCita.setHours(0, 0, 0, 0)
  
  const diff = Math.floor((fechaCita - hoy) / (1000 * 60 * 60 * 24))
  
  if (diff === 0) return 'Hoy'
  if (diff === 1) return 'Mañana'
  if (diff === -1) return 'Ayer'
  
  return formatearFecha(fechaHora)
}

/**
 * Cargar todos los datos del dashboard
 */
async function cargarDashboard() {
  isLoading.value = true
  
  try {
    // Cargar datos en paralelo (más rápido)
    await Promise.all([
      loadCitasHoy(),        // Citas del día
      loadEstadoCaja(),      // Estado de caja
      loadAlertas()          // Alertas de farmacia
    ])
  } catch (error) {
    console.error('Error al cargar dashboard:', error)
  } finally {
    isLoading.value = false
  }
}

// ==========================================
// LIFECYCLE - Cargar datos al montar
// ==========================================

onMounted(() => {
  cargarDashboard()
})
</script>

<style scoped>
.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.kpi-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-content {
  flex: 1;
}

.kpi-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.kpi-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
}

.kpi-change {
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
  white-space: nowrap;
}

.badge-primary {
  background-color: #ede9fe;
  color: #7c3aed;
}

.badge-success {
  background-color: #d1fae5;
  color: #065f46;
}

.badge-info {
  background-color: #dbeafe;
  color: #1e40af;
}

.badge-warning {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-secondary {
  background-color: #f3f4f6;
  color: #4b5563;
}

.badge-danger {
  background-color: #fee2e2;
  color: #991b1b;
}

.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.appointment-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  transition: all 0.2s;
  cursor: pointer;
}

.appointment-item:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
  transform: translateX(4px);
}

.appointment-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem;
  background-color: #ede9fe;
  border-radius: 0.5rem;
  min-width: 80px;
}

.time {
  font-size: 1rem;
  font-weight: 700;
  color: #7c3aed;
}

.date {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.appointment-info {
  flex: 1;
}

.patient-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
}

.appointment-type {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.125rem;
}

.alert-item {
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #fed7aa;
  background-color: #fffbeb;
  transition: background-color 0.2s;
}

.alert-item:hover {
  background-color: #fef3c7;
}

@media (max-width: 640px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .appointment-item {
    flex-wrap: wrap;
  }
}
</style>
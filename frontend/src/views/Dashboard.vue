<template>
  <MainLayout>
    <div class="dashboard-header">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600 mt-2">Bienvenido, {{ authStore.userName }}</p>
    </div>

    <div class="dashboard-content">
      <!-- KPIs Cards -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-icon bg-blue-100 text-blue-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Pacientes Hoy</p>
            <p class="kpi-value">12</p>
            <p class="kpi-change text-green-600">+8% vs ayer</p>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon bg-green-100 text-green-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Ingresos Hoy</p>
            <p class="kpi-value">Q3,450</p>
            <p class="kpi-change text-green-600">+15% vs ayer</p>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon bg-purple-100 text-purple-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Citas Hoy</p>
            <p class="kpi-value">18</p>
            <p class="kpi-change text-gray-600">3 pendientes</p>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon bg-red-100 text-red-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Camas Ocupadas</p>
            <p class="kpi-value">5/8</p>
            <p class="kpi-change text-gray-600">62.5% ocupación</p>
          </div>
        </div>
      </div>

      <!-- Información del Usuario -->
      <div class="card mt-6">
        <h2 class="text-xl font-semibold mb-4">Información de la Sesión</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Usuario:</span>
            <span class="info-value">{{ authStore.user?.username }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Rol:</span>
            <span class="badge badge-primary">{{ roleLabel }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Email:</span>
            <span class="info-value">{{ authStore.user?.email }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Último acceso:</span>
            <span class="info-value">{{ formatDate(authStore.user?.ultimo_acceso) || 'Ahora' }}</span>
          </div>
        </div>
      </div>

      <!-- Próximas Citas -->
      <div class="card mt-6">
        <h2 class="text-xl font-semibold mb-4">Próximas Citas</h2>
        <div class="appointments-list">
          <div class="appointment-item">
            <div class="appointment-time">
              <span class="time">10:00 AM</span>
              <span class="date">Hoy</span>
            </div>
            <div class="appointment-info">
              <p class="patient-name">María González</p>
              <p class="appointment-type">Primera Consulta</p>
            </div>
            <span class="badge badge-primary">Confirmada</span>
          </div>

          <div class="appointment-item">
            <div class="appointment-time">
              <span class="time">11:30 AM</span>
              <span class="date">Hoy</span>
            </div>
            <div class="appointment-info">
              <p class="patient-name">Juan Pérez</p>
              <p class="appointment-type">Reconsulta</p>
            </div>
            <span class="badge badge-warning">Pendiente</span>
          </div>

          <div class="appointment-item">
            <div class="appointment-time">
              <span class="time">02:00 PM</span>
              <span class="date">Hoy</span>
            </div>
            <div class="appointment-info">
              <p class="patient-name">Ana Martínez</p>
              <p class="appointment-type">Control Embarazo</p>
            </div>
            <span class="badge badge-primary">Confirmada</span>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import MainLayout from '@/components/layout/MainLayout.vue'
import { ROLES } from '@/utils/constants'
import { formatDate } from '@/utils/formatters'

const authStore = useAuthStore()

const roleLabel = computed(() => {
  const roles = {
    [ROLES.MEDICO]: 'Médico',
    [ROLES.ENFERMERA]: 'Enfermera',
    [ROLES.RECEPCIONISTA]: 'Recepcionista',
    [ROLES.ADMINISTRADOR]: 'Administrador'
  }
  return roles[authStore.userRole] || 'Usuario'
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.info-value {
  font-size: 0.875rem;
  color: #111827;
  font-weight: 500;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
}

.badge-primary {
  background-color: #ede9fe;
  color: #7c3aed;
}

.badge-warning {
  background-color: #fef3c7;
  color: #92400e;
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
  transition: background-color 0.2s;
}

.appointment-item:hover {
  background-color: #f9fafb;
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

@media (max-width: 640px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .appointment-item {
    flex-wrap: wrap;
  }
}
</style>
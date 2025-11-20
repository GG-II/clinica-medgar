<template>
  <transition name="slide-fade">
    <aside v-if="uiStore.sidebarOpen" class="sidebar">
      <!-- Header del Sidebar -->
      <div class="sidebar-header">
        <img 
          src="@/assets/images/icon-medgar.png" 
          alt="Icon" 
          class="sidebar-icon"
        />
        <div>
          <h2 class="sidebar-title">MEDGAR</h2>
          <p class="sidebar-subtitle">Sistema Clínico</p>
        </div>
      </div>

      <!-- Navegación -->
      <nav class="sidebar-nav">
        <div v-for="item in menuItems" :key="item.name" class="nav-section">
          <p v-if="item.section" class="nav-section-title">{{ item.section }}</p>
          
          <router-link
            v-else
            :to="item.path"
            class="nav-item"
            active-class="nav-item-active"
          >
            <component :is="item.icon" class="nav-icon" />
            <span>{{ item.label }}</span>
            <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
          </router-link>
        </div>
      </nav>

      <!-- Footer del Sidebar -->
      <div class="sidebar-footer">
        <p class="text-xs text-gray-500">v1.0.0</p>
        <p class="text-xs text-gray-400">© 2025 MEDGAR</p>
      </div>
    </aside>
  </transition>
</template>

<script setup>
import { computed, h } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { ROLES } from '@/utils/constants'

const authStore = useAuthStore()
const uiStore = useUIStore()

// Iconos SVG como componentes
const DashboardIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
])

const PatientsIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' })
])

const CalendarIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' })
])

const ClipboardIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' })
])

const BeakerIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z' })
])

const HospitalIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' })
])

const ShoppingIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z' })
])

const CashIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z' })
])

const ChartIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])

const CogIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
])

// Menú dinámico según rol
const menuItems = computed(() => {
  const allMenuItems = [
    { name: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: DashboardIcon, roles: ['all'] },
    
    { section: 'Gestión Médica', roles: ['all'] },
    { name: 'pacientes', label: 'Pacientes', path: '/pacientes', icon: PatientsIcon, roles: ['all'] },
    { name: 'agenda', label: 'Agenda', path: '/agenda', icon: CalendarIcon, roles: ['all'] },
    { name: 'recetas', label: 'Recetas', path: '/recetas', icon: ClipboardIcon, roles: [ROLES.MEDICO] },
    { name: 'laboratorios', label: 'Laboratorios', path: '/laboratorios', icon: BeakerIcon, roles: [ROLES.MEDICO, ROLES.ENFERMERA] },
    
    { section: 'Hospitalización', roles: [ROLES.MEDICO, ROLES.ENFERMERA, ROLES.ADMINISTRADOR] },
    { name: 'hospitalizacion', label: 'Hospitalización', path: '/hospitalizacion', icon: HospitalIcon, roles: [ROLES.MEDICO, ROLES.ENFERMERA] },
    
    { section: 'Administración', roles: [ROLES.ADMINISTRADOR, ROLES.RECEPCIONISTA] },
    { name: 'farmacia', label: 'Farmacia', path: '/farmacia', icon: ShoppingIcon, roles: [ROLES.ADMINISTRADOR, ROLES.RECEPCIONISTA] },
    { name: 'caja', label: 'Caja', path: '/caja', icon: CashIcon, roles: [ROLES.ADMINISTRADOR, ROLES.RECEPCIONISTA] },
    { name: 'reportes', label: 'Reportes', path: '/reportes', icon: ChartIcon, roles: [ROLES.ADMINISTRADOR] },
    
    { section: 'Sistema', roles: [ROLES.ADMINISTRADOR] },
    { name: 'configuracion', label: 'Configuración', path: '/configuracion', icon: CogIcon, roles: [ROLES.ADMINISTRADOR] },
  ]

  // Filtrar según el rol del usuario
  const userRole = authStore.userRole
  return allMenuItems.filter(item => {
    if (item.section) return item.roles.includes('all') || item.roles.includes(userRole)
    return item.roles.includes('all') || item.roles.includes(userRole)
  })
})
</script>

<style scoped>
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e5e7eb;
  height: calc(100vh - 65px);
  position: fixed;
  left: 0;
  top: 65px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  z-index: 40;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  min-height: 80px;
}

.sidebar-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.5rem;
  flex-shrink: 0;
}

.sidebar-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.25;
}

.sidebar-subtitle {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1.25;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 0.5rem;
}

.nav-section-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.75rem 1.5rem 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
}

.nav-item:hover {
  background-color: #f9fafb;
  color: #111827;
}

.nav-item-active {
  background-color: #ede9fe;
  color: #8b5cf6;
  font-weight: 600;
}

.nav-item-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #8b5cf6;
}

.nav-icon {
  flex-shrink: 0;
}

.nav-badge {
  margin-left: auto;
  background-color: #ef4444;
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  min-width: 20px;
  text-align: center;
}

.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  transform: translateX(-100%);
}

.slide-fade-leave-to {
  transform: translateX(-100%);
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    max-width: 280px;
  }
}
</style>
<template>
  <nav class="navbar">
    <div class="navbar-content">
      <!-- Left: Logo y Toggle Sidebar -->
      <div class="navbar-left">
        <button 
          @click="uiStore.toggleSidebar" 
          class="sidebar-toggle"
          aria-label="Toggle menu"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>

        <img 
          src="@/assets/images/logo-medgar.png" 
          alt="Clínica MEDGAR" 
          class="navbar-logo"
        />
      </div>

      <!-- Right: Usuario y acciones -->
      <div class="navbar-right">
        <!-- Notificaciones -->
        <button class="navbar-icon-btn" title="Notificaciones">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
          <span class="notification-badge">3</span>
        </button>

        <!-- Usuario dropdown -->
        <div class="user-menu" @click="toggleUserMenu">
          <Avatar 
            :name="authStore.userName" 
            :src="authStore.user?.foto_url"
            size="md"
          />
          <div class="user-info">
            <p class="user-name">{{ authStore.userName }}</p>
            <p class="user-role">{{ roleLabel }}</p>
          </div>
          <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </div>

        <!-- Dropdown menu -->
        <transition name="fade-down">
          <div v-if="showUserMenu" class="dropdown-menu">
            <router-link to="/perfil" class="dropdown-item">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Mi Perfil
            </router-link>
            
            <router-link to="/configuracion" class="dropdown-item">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              Configuración
            </router-link>
            
            <div class="dropdown-divider"></div>
            
            <button @click="handleLogout" class="dropdown-item text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </transition>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import Avatar from '@/components/common/Avatar.vue'
import { MESSAGES, ROLES } from '@/utils/constants'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const showUserMenu = ref(false)

const roleLabel = computed(() => {
  const roles = {
    [ROLES.MEDICO]: 'Médico',
    [ROLES.ENFERMERA]: 'Enfermera',
    [ROLES.RECEPCIONISTA]: 'Recepcionista',
    [ROLES.ADMINISTRADOR]: 'Administrador'
  }
  return roles[authStore.userRole] || 'Usuario'
})

function toggleUserMenu() {
  showUserMenu.value = !showUserMenu.value
}

function handleLogout() {
  authStore.logout()
  uiStore.showAlert('success', MESSAGES.LOGOUT_SUCCESS)
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  max-width: 100%;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sidebar-toggle {
  padding: 0.5rem;
  border-radius: 0.5rem;
  color: #6b7280;
  transition: all 0.2s;
}

.sidebar-toggle:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.navbar-logo {
  height: 40px;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.navbar-icon-btn {
  position: relative;
  padding: 0.5rem;
  border-radius: 0.5rem;
  color: #6b7280;
  transition: all 0.2s;
}

.navbar-icon-btn:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.notification-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background-color: #ef4444;
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.125rem 0.375rem;
  border-radius: 9999px;
  min-width: 18px;
  text-align: center;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-menu:hover {
  background-color: #f3f4f6;
}

.user-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
  line-height: 1.25;
}

.user-role {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1.25;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  min-width: 200px;
  overflow: hidden;
  z-index: 60;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #374151;
  font-size: 0.875rem;
  transition: background-color 0.2s;
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
}

.dropdown-divider {
  height: 1px;
  background-color: #e5e7eb;
  margin: 0.25rem 0;
}

.fade-down-enter-active,
.fade-down-leave-active {
  transition: all 0.2s ease;
}

.fade-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 640px) {
  .navbar-logo {
    height: 32px;
  }
  
  .user-info {
    display: none;
  }
}
</style>
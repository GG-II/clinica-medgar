<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600 mt-2">Bienvenido, {{ authStore.userName }}</p>
    </div>

    <div class="dashboard-content">
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">¡Sistema Funcionando! 🎉</h2>
        <p class="text-gray-600 mb-4">
          Has iniciado sesión correctamente. Este es el Dashboard principal.
        </p>
        
        <div class="bg-primary-50 p-4 rounded-lg">
          <p class="text-sm text-primary-900">
            <strong>Usuario:</strong> {{ authStore.user?.username }}<br>
            <strong>Rol:</strong> {{ authStore.userRole }}<br>
            <strong>Email:</strong> {{ authStore.user?.email }}
          </p>
        </div>

        <Button 
          variant="danger" 
          class="mt-4"
          @click="handleLogout"
        >
          Cerrar Sesión
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import Button from '@/components/common/Button.vue'
import { MESSAGES } from '@/utils/constants'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

function handleLogout() {
  authStore.logout()
  uiStore.showAlert('success', MESSAGES.LOGOUT_SUCCESS)
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-content {
  display: grid;
  gap: 1.5rem;
}

.card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>
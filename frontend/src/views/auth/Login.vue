<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Logo -->
      <div class="login-header">
        <img 
          src="@/assets/images/logo-medgar.png" 
          alt="Clínica MEDGAR" 
          class="login-logo"
        />
        <h1 class="login-title">Sistema de Gestión Clínica</h1>
        <p class="login-subtitle">Ingresa tus credenciales para continuar</p>
      </div>

      <!-- Formulario -->
      <form @submit.prevent="handleLogin" class="login-form">
        <Input
          v-model="credentials.username"
          label="Usuario o Email"
          type="text"
          placeholder="Ingresa tu usuario"
          required
          :error="errors.username"
        />

        <Input
          v-model="credentials.password"
          label="Contraseña"
          type="password"
          placeholder="Ingresa tu contraseña"
          required
          :error="errors.password"
        />

        <Button
          type="submit"
          variant="primary"
          :loading="isLoading"
          full-width
        >
          Iniciar Sesión
        </Button>
      </form>

      <!-- Footer -->
      <div class="login-footer">
        <p class="text-sm text-gray-600">
          ¿Olvidaste tu contraseña? 
          <a href="#" class="text-primary-600 hover:underline">Recuperar</a>
        </p>
      </div>
    </div>

    <!-- Info adicional -->
    <div class="login-info">
      <p class="text-sm text-gray-500">
        Clínica Médica Dra. Estephanny García
      </p>
      <p class="text-xs text-gray-400 mt-1">
        v1.0.0 - Sistema desarrollado con Vue 3
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { authAPI } from '@/api/auth.api'
import Input from '@/components/common/Input.vue'
import Button from '@/components/common/Button.vue'
import { MESSAGES } from '@/utils/constants'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const credentials = reactive({
  username: '',
  password: ''
})

const errors = reactive({
  username: '',
  password: ''
})

const isLoading = ref(false)

async function handleLogin() {
  // Limpiar errores
  errors.username = ''
  errors.password = ''

  // Validaciones básicas
  if (!credentials.username) {
    errors.username = 'El usuario es requerido'
    return
  }

  if (!credentials.password) {
    errors.password = 'La contraseña es requerida'
    return
  }

  try {
    isLoading.value = true

    // Llamar al backend
    const response = await authAPI.login(credentials)

    if (response.data.success) {
      // Guardar datos de autenticación
      authStore.setAuth(response.data)

      // Mostrar mensaje de éxito
      uiStore.showAlert('success', MESSAGES.LOGIN_SUCCESS)

      // Redirigir al dashboard
      router.push('/dashboard')
    }
  } catch (error) {
    console.error('Error al iniciar sesión:', error)
    
    const errorMessage = error.response?.data?.message || MESSAGES.LOGIN_ERROR
    uiStore.showAlert('error', errorMessage)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  animation: fadeIn 0.5s ease-in-out;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-logo {
  height: 60px;
  margin: 0 auto 1rem;
}

.login-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
}

.login-form {
  margin-bottom: 1.5rem;
}

.login-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.login-info {
  margin-top: 2rem;
  text-align: center;
  color: white;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .login-card {
    padding: 1.5rem;
  }
  
  .login-logo {
    height: 50px;
  }
}
</style>
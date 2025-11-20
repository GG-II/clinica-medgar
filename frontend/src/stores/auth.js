import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.rol || null)
  const userName = computed(() => user.value?.nombre_completo || '')

  // Actions
  function setAuth(authData) {
    user.value = authData.usuario
    token.value = authData.access_token
    refreshToken.value = authData.refresh_token
    
    localStorage.setItem('token', authData.access_token)
    localStorage.setItem('refreshToken', authData.refresh_token)
  }

  function logout() {
    user.value = null
    token.value = null
    refreshToken.value = null
    
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }

  return {
    user,
    token,
    refreshToken,
    isAuthenticated,
    userRole,
    userName,
    setAuth,
    logout
  }
})
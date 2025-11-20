import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  // State
  const sidebarOpen = ref(true)
  const loading = ref(false)
  const alert = ref({
    show: false,
    type: 'info', // 'success', 'error', 'warning', 'info'
    message: ''
  })

  // Actions
  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  function showLoading() {
    loading.value = true
  }

  function hideLoading() {
    loading.value = false
  }

  function showAlert(type, message) {
    alert.value = {
      show: true,
      type,
      message
    }
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {
      hideAlert()
    }, 5000)
  }

  function hideAlert() {
    alert.value.show = false
  }

  return {
    sidebarOpen,
    loading,
    alert,
    toggleSidebar,
    showLoading,
    hideLoading,
    showAlert,
    hideAlert
  }
})
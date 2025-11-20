<template>
  <teleport to="body">
    <div class="toast-container" :class="`toast-position-${position}`">
      <transition-group name="toast-slide">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="toastClasses(toast.type)"
          @click="removeToast(toast.id)"
        >
          <!-- Icono -->
          <div class="toast-icon">
            <svg v-if="toast.type === 'success'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="toast.type === 'error'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="toast.type === 'warning'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
          </div>

          <!-- Contenido -->
          <div class="toast-content">
            <p v-if="toast.title" class="toast-title">{{ toast.title }}</p>
            <p class="toast-message">{{ toast.message }}</p>
          </div>

          <!-- Botón cerrar -->
          <button @click.stop="removeToast(toast.id)" class="toast-close">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>

          <!-- Barra de progreso -->
          <div v-if="toast.duration" class="toast-progress">
            <div 
              class="toast-progress-bar" 
              :style="{ animationDuration: `${toast.duration}ms` }"
            ></div>
          </div>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  position: {
    type: String,
    default: 'top-right',
    validator: (value) => ['top-right', 'top-left', 'bottom-right', 'bottom-left', 'top-center', 'bottom-center'].includes(value)
  }
})

const toasts = ref([])
let toastId = 0

const addToast = ({ type = 'info', title = '', message = '', duration = 5000 }) => {
  const id = toastId++
  const toast = { id, type, title, message, duration }
  
  toasts.value.push(toast)

  if (duration > 0) {
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  return id
}

const removeToast = (id) => {
  const index = toasts.value.findIndex(toast => toast.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

const clearAll = () => {
  toasts.value = []
}

const toastClasses = (type) => {
  const base = 'toast'
  const types = {
    success: 'toast-success',
    error: 'toast-error',
    warning: 'toast-warning',
    info: 'toast-info'
  }
  return `${base} ${types[type]}`
}

// Exponer métodos
defineExpose({
  addToast,
  removeToast,
  clearAll,
  success: (message, options = {}) => addToast({ type: 'success', message, ...options }),
  error: (message, options = {}) => addToast({ type: 'error', message, ...options }),
  warning: (message, options = {}) => addToast({ type: 'warning', message, ...options }),
  info: (message, options = {}) => addToast({ type: 'info', message, ...options })
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
  max-width: 400px;
}

/* Posiciones */
.toast-position-top-right {
  top: 1rem;
  right: 1rem;
}

.toast-position-top-left {
  top: 1rem;
  left: 1rem;
}

.toast-position-bottom-right {
  bottom: 1rem;
  right: 1rem;
}

.toast-position-bottom-left {
  bottom: 1rem;
  left: 1rem;
}

.toast-position-top-center {
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
}

.toast-position-bottom-center {
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
}

/* Toast */
.toast {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  pointer-events: auto;
  cursor: pointer;
  transition: transform 0.2s;
  overflow: hidden;
  min-width: 300px;
}

.toast:hover {
  transform: scale(1.02);
}

.toast-icon {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.toast-message {
  font-size: 0.875rem;
  line-height: 1.5;
}

.toast-close {
  flex-shrink: 0;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-close:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* Barra de progreso */
.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background-color: rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.toast-progress-bar {
  height: 100%;
  background-color: currentColor;
  animation: toast-progress linear forwards;
}

@keyframes toast-progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

/* Tipos */
.toast-success {
  background-color: #d1fae5;
  color: #065f46;
}

.toast-error {
  background-color: #fee2e2;
  color: #991b1b;
}

.toast-warning {
  background-color: #fef3c7;
  color: #92400e;
}

.toast-info {
  background-color: #dbeafe;
  color: #1e40af;
}

/* Animaciones */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.3s ease;
}

.toast-slide-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

/* Responsive */
@media (max-width: 640px) {
  .toast-container {
    left: 1rem;
    right: 1rem;
    max-width: calc(100% - 2rem);
  }

  .toast-position-top-center,
  .toast-position-bottom-center {
    left: 1rem;
    right: 1rem;
    transform: none;
  }

  .toast {
    min-width: auto;
    width: 100%;
  }
}
</style>
<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <!-- Botón trigger -->
    <button
      @click="toggleDropdown"
      :disabled="disabled"
      :class="triggerClasses"
      type="button"
    >
      <slot name="trigger">
        <span>{{ label }}</span>
        <svg 
          class="dropdown-arrow" 
          :class="{ 'dropdown-arrow-open': isOpen }"
          fill="currentColor" 
          viewBox="0 0 20 20"
        >
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </slot>
    </button>

    <!-- Menú dropdown -->
    <transition name="dropdown-fade">
      <div 
        v-if="isOpen"
        :class="menuClasses"
      >
        <slot></slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: 'Opciones'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  position: {
    type: String,
    default: 'bottom-left',
    validator: (value) => ['bottom-left', 'bottom-right', 'top-left', 'top-right'].includes(value)
  },
  width: {
    type: String,
    default: 'auto'
  }
})

const emit = defineEmits(['open', 'close', 'toggle'])

const isOpen = ref(false)
const dropdownRef = ref(null)

const triggerClasses = computed(() => {
  const base = 'dropdown-trigger'
  const disabled = props.disabled ? 'dropdown-trigger-disabled' : ''
  return `${base} ${disabled}`
})

const menuClasses = computed(() => {
  const base = 'dropdown-menu'
  const position = `dropdown-menu-${props.position}`
  const width = props.width !== 'auto' ? '' : 'dropdown-menu-auto'
  return `${base} ${position} ${width}`
})

const toggleDropdown = () => {
  if (props.disabled) return
  
  isOpen.value = !isOpen.value
  emit('toggle', isOpen.value)
  
  if (isOpen.value) {
    emit('open')
  } else {
    emit('close')
  }
}

const closeDropdown = () => {
  if (isOpen.value) {
    isOpen.value = false
    emit('close')
  }
}

// Cerrar al hacer click fuera
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

// Cerrar con tecla ESC
const handleKeydown = (event) => {
  if (event.key === 'Escape' && isOpen.value) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})

// Exponer método para cerrar desde fuera
defineExpose({ close: closeDropdown })
</script>

<style scoped>
.dropdown-wrapper {
  position: relative;
  display: inline-block;
}

/* Trigger button */
.dropdown-trigger {
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background-color: white;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
  outline: none;
}

.dropdown-trigger:hover:not(.dropdown-trigger-disabled) {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.dropdown-trigger:focus {
  border-color: #8b5cf6;
  ring: 2px;
  ring-color: rgba(139, 92, 246, 0.2);
}

.dropdown-trigger-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dropdown-arrow {
  width: 1.25rem;
  height: 1.25rem;
  color: #6b7280;
  transition: transform 0.2s;
}

.dropdown-arrow-open {
  transform: rotate(180deg);
}

/* Menu */
.dropdown-menu {
  position: absolute;
  z-index: 50;
  margin-top: 0.5rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  padding: 0.5rem 0;
  min-width: 10rem;
}

.dropdown-menu-auto {
  width: max-content;
}

/* Posiciones */
.dropdown-menu-bottom-left {
  top: 100%;
  left: 0;
}

.dropdown-menu-bottom-right {
  top: 100%;
  right: 0;
}

.dropdown-menu-top-left {
  bottom: 100%;
  left: 0;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.dropdown-menu-top-right {
  bottom: 100%;
  right: 0;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

/* Animaciones */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.2s ease;
}

.dropdown-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Items del dropdown (para uso en slots) */
:deep(.dropdown-item) {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  color: #374151;
  text-align: left;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

:deep(.dropdown-item:hover) {
  background-color: #f3f4f6;
}

:deep(.dropdown-item-danger) {
  color: #ef4444;
}

:deep(.dropdown-item-danger:hover) {
  background-color: #fee2e2;
}

:deep(.dropdown-divider) {
  height: 1px;
  margin: 0.5rem 0;
  background-color: #e5e7eb;
}
</style>
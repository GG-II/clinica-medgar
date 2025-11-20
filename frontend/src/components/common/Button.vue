<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="loading-spinner-btn"></span>
    <slot v-else></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'ghost'].includes(value)
  },
  type: {
    type: String,
    default: 'button'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  fullWidth: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])

const buttonClasses = computed(() => {
  const base = 'btn-base'
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    danger: 'btn-danger',
    ghost: 'btn-ghost'
  }
  const width = props.fullWidth ? 'w-full' : ''
  const disabled = props.disabled ? 'btn-disabled' : ''
  
  return `${base} ${variants[props.variant]} ${width} ${disabled}`
})
</script>

<style scoped>
.btn-base {
  padding: 0.625rem 1.25rem;
  font-weight: 600;
  font-size: 0.875rem;
  border-radius: 0.5rem;
  transition: all 0.2s;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
  outline: none;
}

.btn-base:focus {
  outline: 2px solid #8b5cf6;
  outline-offset: 2px;
}

.btn-primary {
  background-color: #8b5cf6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #7c3aed;
}

.btn-secondary {
  background-color: #e5e7eb;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #d1d5db;
}

.btn-danger {
  background-color: #ef4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #dc2626;
}

.btn-ghost {
  background-color: transparent;
  color: #6b7280;
}

.btn-ghost:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-spinner-btn {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
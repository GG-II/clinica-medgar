<template>
  <span :class="badgeClasses">
    <slot></slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  rounded: {
    type: Boolean,
    default: false
  }
})

const badgeClasses = computed(() => {
  const base = 'badge-base'
  
  const variants = {
    default: 'badge-default',
    primary: 'badge-primary',
    success: 'badge-success',
    warning: 'badge-warning',
    danger: 'badge-danger',
    info: 'badge-info'
  }
  
  const sizes = {
    sm: 'badge-sm',
    md: 'badge-md',
    lg: 'badge-lg'
  }
  
  const shape = props.rounded ? 'badge-rounded' : 'badge-square'
  
  return `${base} ${variants[props.variant]} ${sizes[props.size]} ${shape}`
})
</script>

<style scoped>
.badge-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.2s;
  white-space: nowrap;
}

/* Tamaños */
.badge-sm {
  padding: 0.125rem 0.5rem;
  font-size: 0.75rem;
}

.badge-md {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}

.badge-lg {
  padding: 0.375rem 1rem;
  font-size: 1rem;
}

/* Formas */
.badge-square {
  border-radius: 0.375rem;
}

.badge-rounded {
  border-radius: 9999px;
}

/* Variantes de color */
.badge-default {
  background-color: #e5e7eb;
  color: #374151;
}

.badge-primary {
  background-color: #ede9fe;
  color: #7c3aed;
}

.badge-success {
  background-color: #d1fae5;
  color: #065f46;
}

.badge-warning {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-danger {
  background-color: #fee2e2;
  color: #991b1b;
}

.badge-info {
  background-color: #dbeafe;
  color: #1e40af;
}
</style>
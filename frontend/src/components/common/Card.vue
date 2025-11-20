<template>
  <div :class="cardClasses">
    <!-- Header -->
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
      </slot>
    </div>

    <!-- Body -->
    <div class="card-body" :class="{ 'card-body-padded': padded }">
      <slot></slot>
    </div>

    <!-- Footer -->
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  padded: {
    type: Boolean,
    default: true
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'bordered', 'elevated'].includes(value)
  }
})

defineEmits(['click'])

const cardClasses = computed(() => {
  const base = 'card-base'
  
  const variants = {
    default: 'card-default',
    bordered: 'card-bordered',
    elevated: 'card-elevated'
  }
  
  const interactive = []
  if (props.hoverable) interactive.push('card-hoverable')
  if (props.clickable) interactive.push('card-clickable')
  
  return `${base} ${variants[props.variant]} ${interactive.join(' ')}`
})
</script>

<style scoped>
.card-base {
  background-color: white;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: all 0.2s;
}

/* Variantes */
.card-default {
  border: 1px solid #e5e7eb;
}

.card-bordered {
  border: 2px solid #d1d5db;
}

.card-elevated {
  border: none;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Estados interactivos */
.card-hoverable:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.card-clickable {
  cursor: pointer;
}

.card-clickable:hover {
  border-color: #8b5cf6;
}

.card-clickable:active {
  transform: scale(0.98);
}

/* Header */
.card-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e5e7eb;
  background-color: #fafafa;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

/* Body */
.card-body {
  background-color: white;
}

.card-body-padded {
  padding: 1.25rem;
}

/* Footer */
.card-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid #e5e7eb;
  background-color: #fafafa;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}
</style>
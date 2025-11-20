<template>
  <div class="datepicker-wrapper">
    <label v-if="label" :for="id" class="datepicker-label">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <div class="datepicker-container">
      <input
        :id="id"
        type="date"
        :value="modelValue"
        :min="min"
        :max="max"
        :disabled="disabled"
        :required="required"
        :class="datepickerClasses"
        @input="$emit('update:modelValue', $event.target.value)"
        @change="handleChange"
        @blur="$emit('blur')"
      />
      
      <!-- Icono de calendario -->
      <svg class="datepicker-icon" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
      </svg>
    </div>

    <p v-if="error" class="datepicker-error">{{ error }}</p>
    <p v-else-if="hint" class="datepicker-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: {
    type: String,
    default: () => `datepicker-${Math.random().toString(36).substr(2, 9)}`
  },
  label: {
    type: String,
    default: ''
  },
  modelValue: {
    type: String,
    default: ''
  },
  min: {
    type: String,
    default: ''
  },
  max: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'blur'])

const datepickerClasses = computed(() => {
  const base = 'datepicker-field'
  const hasError = props.error ? 'datepicker-error-border' : ''
  const isDisabled = props.disabled ? 'datepicker-disabled' : ''
  
  return `${base} ${hasError} ${isDisabled}`
})

const handleChange = (event) => {
  emit('change', event.target.value)
}
</script>

<style scoped>
.datepicker-wrapper {
  margin-bottom: 1rem;
}

.datepicker-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.datepicker-container {
  position: relative;
  display: flex;
  align-items: center;
}

.datepicker-field {
  width: 100%;
  padding: 0.625rem 2.5rem 0.625rem 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
  outline: none;
  background-color: white;
  color: #374151;
}

.datepicker-field:focus {
  border-color: #8b5cf6;
  ring: 2px;
  ring-color: rgba(139, 92, 246, 0.2);
}

.datepicker-field::-webkit-calendar-picker-indicator {
  opacity: 0;
  position: absolute;
  right: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.datepicker-error-border {
  border-color: #ef4444;
}

.datepicker-error-border:focus {
  border-color: #ef4444;
  ring-color: rgba(239, 68, 68, 0.2);
}

.datepicker-disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  opacity: 0.6;
}

.datepicker-icon {
  position: absolute;
  right: 0.75rem;
  width: 1.25rem;
  height: 1.25rem;
  color: #6b7280;
  pointer-events: none;
}

.datepicker-error {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #ef4444;
}

.datepicker-hint {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
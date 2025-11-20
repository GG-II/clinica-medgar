<template>
  <div class="input-wrapper">
    <label v-if="label" :for="id" class="input-label">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <div class="input-container">
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="inputClasses"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur')"
      />
      
      <slot name="icon"></slot>
    </div>
    
    <p v-if="error" class="input-error">{{ error }}</p>
    <p v-else-if="hint" class="input-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  placeholder: {
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

defineEmits(['update:modelValue', 'blur'])

const inputClasses = computed(() => {
  const base = 'input-field'
  const hasError = props.error ? 'input-error-border' : ''
  const isDisabled = props.disabled ? 'input-disabled' : ''
  
  return `${base} ${hasError} ${isDisabled}`
})
</script>

<style scoped>
.input-wrapper {
  margin-bottom: 1rem;
}

.input-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input-field {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
  outline: none;
}

.input-field:focus {
  border-color: #8b5cf6;
  ring: 2px;
  ring-color: rgba(139, 92, 246, 0.2);
}

.input-error-border {
  border-color: #ef4444;
}

.input-error-border:focus {
  border-color: #ef4444;
  ring-color: rgba(239, 68, 68, 0.2);
}

.input-disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  opacity: 0.6;
}

.input-error {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #ef4444;
}

.input-hint {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
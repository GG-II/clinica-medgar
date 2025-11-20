<template>
  <div class="textarea-wrapper">
    <label v-if="label" :for="id" class="textarea-label">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <div class="textarea-container">
      <textarea
        :id="id"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :rows="rows"
        :maxlength="maxLength"
        :class="textareaClasses"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur')"
      ></textarea>
    </div>

    <!-- Contador de caracteres -->
    <div v-if="showCount && maxLength" class="textarea-count">
      {{ characterCount }} / {{ maxLength }}
    </div>

    <p v-if="error" class="textarea-error">{{ error }}</p>
    <p v-else-if="hint" class="textarea-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: {
    type: String,
    default: () => `textarea-${Math.random().toString(36).substr(2, 9)}`
  },
  label: {
    type: String,
    default: ''
  },
  modelValue: {
    type: String,
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
  },
  rows: {
    type: Number,
    default: 4
  },
  maxLength: {
    type: Number,
    default: null
  },
  showCount: {
    type: Boolean,
    default: true
  },
  resize: {
    type: String,
    default: 'vertical',
    validator: (value) => ['none', 'both', 'horizontal', 'vertical'].includes(value)
  }
})

defineEmits(['update:modelValue', 'blur'])

const textareaClasses = computed(() => {
  const base = 'textarea-field'
  const hasError = props.error ? 'textarea-error-border' : ''
  const isDisabled = props.disabled ? 'textarea-disabled' : ''
  const resizeClass = `resize-${props.resize}`
  
  return `${base} ${hasError} ${isDisabled} ${resizeClass}`
})

const characterCount = computed(() => {
  return props.modelValue ? props.modelValue.length : 0
})
</script>

<style scoped>
.textarea-wrapper {
  margin-bottom: 1rem;
}

.textarea-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.textarea-container {
  position: relative;
}

.textarea-field {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-family: inherit;
  line-height: 1.5;
  transition: all 0.2s;
  outline: none;
  background-color: white;
}

.textarea-field:focus {
  border-color: #8b5cf6;
  ring: 2px;
  ring-color: rgba(139, 92, 246, 0.2);
}

.textarea-error-border {
  border-color: #ef4444;
}

.textarea-error-border:focus {
  border-color: #ef4444;
  ring-color: rgba(239, 68, 68, 0.2);
}

.textarea-disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Resize options */
.resize-none {
  resize: none;
}

.resize-both {
  resize: both;
}

.resize-horizontal {
  resize: horizontal;
}

.resize-vertical {
  resize: vertical;
}

/* Contador de caracteres */
.textarea-count {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #6b7280;
  text-align: right;
}

.textarea-error {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #ef4444;
}

.textarea-hint {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
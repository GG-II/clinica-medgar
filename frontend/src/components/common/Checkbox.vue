<template>
  <div class="checkbox-wrapper">
    <label :for="id" class="checkbox-label">
      <input
        :id="id"
        type="checkbox"
        :checked="modelValue"
        :value="value"
        :disabled="disabled"
        :required="required"
        @change="handleChange"
        class="checkbox-input"
      />
      
      <span class="checkbox-box" :class="{ 'checkbox-checked': modelValue, 'checkbox-disabled': disabled }">
        <svg v-if="modelValue" class="checkbox-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
        </svg>
      </span>

      <span v-if="label" class="checkbox-text">
        {{ label }}
        <span v-if="required" class="text-red-500">*</span>
      </span>
    </label>

    <p v-if="error" class="checkbox-error">{{ error }}</p>
    <p v-else-if="hint" class="checkbox-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  id: {
    type: String,
    default: () => `checkbox-${Math.random().toString(36).substr(2, 9)}`
  },
  label: {
    type: String,
    default: ''
  },
  modelValue: {
    type: Boolean,
    default: false
  },
  value: {
    type: [String, Number, Boolean],
    default: true
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

const emit = defineEmits(['update:modelValue', 'change'])

const handleChange = (event) => {
  const checked = event.target.checked
  emit('update:modelValue', checked)
  emit('change', checked)
}
</script>

<style scoped>
.checkbox-wrapper {
  margin-bottom: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  user-select: none;
  position: relative;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-box {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid #d1d5db;
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  transition: all 0.2s;
  flex-shrink: 0;
}

.checkbox-input:focus + .checkbox-box {
  border-color: #8b5cf6;
  ring: 2px;
  ring-color: rgba(139, 92, 246, 0.2);
}

.checkbox-checked {
  background-color: #8b5cf6;
  border-color: #8b5cf6;
}

.checkbox-disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  opacity: 0.6;
}

.checkbox-label:has(.checkbox-disabled) {
  cursor: not-allowed;
}

.checkbox-icon {
  width: 1rem;
  height: 1rem;
  color: white;
}

.checkbox-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.5;
}

.checkbox-error {
  margin-top: 0.375rem;
  margin-left: 2rem;
  font-size: 0.75rem;
  color: #ef4444;
}

.checkbox-hint {
  margin-top: 0.375rem;
  margin-left: 2rem;
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
<template>
  <div class="radio-wrapper">
    <label :for="id" class="radio-label">
      <input
        :id="id"
        type="radio"
        :name="name"
        :value="value"
        :checked="modelValue === value"
        :disabled="disabled"
        :required="required"
        @change="handleChange"
        class="radio-input"
      />
      
      <span class="radio-circle" :class="{ 'radio-checked': modelValue === value, 'radio-disabled': disabled }">
        <span v-if="modelValue === value" class="radio-dot"></span>
      </span>

      <span v-if="label" class="radio-text">
        {{ label }}
        <span v-if="required" class="text-red-500">*</span>
      </span>
    </label>

    <p v-if="error" class="radio-error">{{ error }}</p>
    <p v-else-if="hint" class="radio-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  id: {
    type: String,
    default: () => `radio-${Math.random().toString(36).substr(2, 9)}`
  },
  name: {
    type: String,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  modelValue: {
    type: [String, Number, Boolean],
    default: null
  },
  value: {
    type: [String, Number, Boolean],
    required: true
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

const handleChange = () => {
  emit('update:modelValue', props.value)
  emit('change', props.value)
}
</script>

<style scoped>
.radio-wrapper {
  margin-bottom: 0.75rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  user-select: none;
  position: relative;
}

.radio-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-circle {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid #d1d5db;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  transition: all 0.2s;
  flex-shrink: 0;
}

.radio-input:focus + .radio-circle {
  border-color: #8b5cf6;
  ring: 2px;
  ring-color: rgba(139, 92, 246, 0.2);
}

.radio-checked {
  border-color: #8b5cf6;
}

.radio-disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  opacity: 0.6;
}

.radio-label:has(.radio-disabled) {
  cursor: not-allowed;
}

.radio-dot {
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background-color: #8b5cf6;
}

.radio-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.5;
}

.radio-error {
  margin-top: 0.375rem;
  margin-left: 2rem;
  font-size: 0.75rem;
  color: #ef4444;
}

.radio-hint {
  margin-top: 0.375rem;
  margin-left: 2rem;
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
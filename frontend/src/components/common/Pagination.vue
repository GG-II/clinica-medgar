<template>
  <div v-if="totalPages > 1" class="pagination-wrapper">
    <!-- Info de resultados -->
    <div class="pagination-info">
      <p class="text-sm text-gray-600">
        Mostrando <span class="font-semibold">{{ startItem }}</span> a 
        <span class="font-semibold">{{ endItem }}</span> de 
        <span class="font-semibold">{{ total }}</span> resultados
      </p>
    </div>

    <!-- Botones de paginación -->
    <div class="pagination-controls">
      <!-- Botón primera página -->
      <button 
        @click="goToPage(1)"
        :disabled="currentPage === 1"
        class="pagination-btn"
        :class="{ 'pagination-btn-disabled': currentPage === 1 }"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
        </svg>
      </button>

      <!-- Botón anterior -->
      <button 
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="pagination-btn"
        :class="{ 'pagination-btn-disabled': currentPage === 1 }"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
        </svg>
      </button>

      <!-- Números de página -->
      <button
        v-for="page in visiblePages"
        :key="page"
        @click="page !== '...' ? goToPage(page) : null"
        class="pagination-number"
        :class="{
          'pagination-number-active': page === currentPage,
          'pagination-ellipsis': page === '...'
        }"
        :disabled="page === '...'"
      >
        {{ page }}
      </button>

      <!-- Botón siguiente -->
      <button 
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="pagination-btn"
        :class="{ 'pagination-btn-disabled': currentPage === totalPages }"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
        </svg>
      </button>

      <!-- Botón última página -->
      <button 
        @click="goToPage(totalPages)"
        :disabled="currentPage === totalPages"
        class="pagination-btn"
        :class="{ 'pagination-btn-disabled': currentPage === totalPages }"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10.293 15.707a1 1 0 010-1.414L14.586 10l-4.293-4.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
          <path fill-rule="evenodd" d="M4.293 15.707a1 1 0 010-1.414L8.586 10 4.293 5.707a1 1 0 011.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
        </svg>
      </button>
    </div>

    <!-- Selector de items por página -->
    <div v-if="showPerPage" class="pagination-per-page">
      <label class="text-sm text-gray-600">Por página:</label>
      <select 
        :value="perPage"
        @change="handlePerPageChange"
        class="per-page-select"
      >
        <option v-for="option in perPageOptions" :key="option" :value="option">
          {{ option }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    default: 1
  },
  perPage: {
    type: Number,
    default: 10
  },
  total: {
    type: Number,
    required: true
  },
  maxVisiblePages: {
    type: Number,
    default: 5
  },
  showPerPage: {
    type: Boolean,
    default: true
  },
  perPageOptions: {
    type: Array,
    default: () => [10, 25, 50, 100]
  }
})

const emit = defineEmits(['update:currentPage', 'update:perPage', 'page-change'])

const totalPages = computed(() => {
  return Math.ceil(props.total / props.perPage)
})

const startItem = computed(() => {
  return (props.currentPage - 1) * props.perPage + 1
})

const endItem = computed(() => {
  const end = props.currentPage * props.perPage
  return end > props.total ? props.total : end
})

const visiblePages = computed(() => {
  const pages = []
  const half = Math.floor(props.maxVisiblePages / 2)
  let start = props.currentPage - half
  let end = props.currentPage + half

  if (start < 1) {
    start = 1
    end = Math.min(props.maxVisiblePages, totalPages.value)
  }

  if (end > totalPages.value) {
    end = totalPages.value
    start = Math.max(1, totalPages.value - props.maxVisiblePages + 1)
  }

  // Agregar primera página y ellipsis si es necesario
  if (start > 1) {
    pages.push(1)
    if (start > 2) pages.push('...')
  }

  // Agregar páginas visibles
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  // Agregar ellipsis y última página si es necesario
  if (end < totalPages.value) {
    if (end < totalPages.value - 1) pages.push('...')
    pages.push(totalPages.value)
  }

  return pages
})

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value && page !== props.currentPage) {
    emit('update:currentPage', page)
    emit('page-change', page)
  }
}

const handlePerPageChange = (event) => {
  const newPerPage = parseInt(event.target.value)
  emit('update:perPage', newPerPage)
  emit('update:currentPage', 1) // Reset a primera página
  emit('page-change', 1)
}
</script>

<style scoped>
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  background-color: white;
  border-top: 1px solid #e5e7eb;
  gap: 1rem;
  flex-wrap: wrap;
}

.pagination-info {
  flex-shrink: 0;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pagination-btn {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  color: #6b7280;
  transition: all 0.2s;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-btn-disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-number {
  min-width: 2.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}

.pagination-number:hover:not(:disabled) {
  background-color: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-number-active {
  background-color: #8b5cf6;
  color: white;
  border-color: #8b5cf6;
}

.pagination-number-active:hover {
  background-color: #7c3aed;
  border-color: #7c3aed;
}

.pagination-ellipsis {
  cursor: default;
  border: none;
  background-color: transparent;
}

.pagination-ellipsis:hover {
  background-color: transparent;
  border: none;
}

.pagination-per-page {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.per-page-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background-color: white;
  cursor: pointer;
  outline: none;
  transition: all 0.2s;
}

.per-page-select:focus {
  border-color: #8b5cf6;
  ring: 2px;
  ring-color: rgba(139, 92, 246, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
  .pagination-wrapper {
    flex-direction: column;
    gap: 1rem;
  }

  .pagination-info {
    order: 3;
    text-align: center;
  }

  .pagination-controls {
    order: 1;
  }

  .pagination-per-page {
    order: 2;
  }
}
</style>
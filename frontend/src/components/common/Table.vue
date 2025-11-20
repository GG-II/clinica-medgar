<template>
  <div class="table-wrapper">
    <!-- Loading State -->
    <div v-if="loading" class="table-loading">
      <div class="loading-spinner"></div>
      <p class="text-gray-600 mt-2">Cargando datos...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!data || data.length === 0" class="table-empty">
      <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
      </svg>
      <p class="text-gray-600 font-medium">{{ emptyMessage }}</p>
    </div>

    <!-- Table -->
    <div v-else class="table-container">
      <table class="data-table">
        <thead class="table-header">
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              :class="[
                'table-header-cell',
                column.sortable ? 'sortable' : '',
                column.align ? `text-${column.align}` : 'text-left'
              ]"
              @click="column.sortable ? handleSort(column.key) : null"
            >
              <div class="header-content">
                <span>{{ column.label }}</span>
                <svg 
                  v-if="column.sortable" 
                  class="sort-icon"
                  :class="{ 'sort-active': sortKey === column.key }"
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path 
                    v-if="sortKey === column.key && sortOrder === 'asc'"
                    fill-rule="evenodd" 
                    d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" 
                    clip-rule="evenodd"
                  />
                  <path 
                    v-else-if="sortKey === column.key && sortOrder === 'desc'"
                    fill-rule="evenodd" 
                    d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" 
                    clip-rule="evenodd"
                  />
                  <path 
                    v-else
                    d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 6.414l-3.293 3.293a1 1 0 01-1.414 0zm0 4a1 1 0 011.414 0L10 17l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  />
                </svg>
              </div>
            </th>
            <th v-if="hasActions" class="table-header-cell text-center">
              Acciones
            </th>
          </tr>
        </thead>

        <tbody class="table-body">
          <tr 
            v-for="(row, index) in sortedData" 
            :key="index"
            :class="[
              'table-row',
              rowClickable ? 'row-clickable' : ''
            ]"
            @click="handleRowClick(row)"
          >
            <td 
              v-for="column in columns" 
              :key="column.key"
              :class="[
                'table-cell',
                column.align ? `text-${column.align}` : 'text-left'
              ]"
            >
              <!-- Slot personalizado por columna -->
              <slot 
                :name="`cell-${column.key}`" 
                :row="row" 
                :value="getNestedValue(row, column.key)"
              >
                {{ formatValue(row, column) }}
              </slot>
            </td>

            <!-- Columna de acciones -->
            <td v-if="hasActions" class="table-cell text-center">
              <slot name="actions" :row="row">
                <div class="action-buttons">
                  <button 
                    v-if="showView"
                    @click.stop="$emit('view', row)"
                    class="action-btn action-btn-view"
                    title="Ver detalle"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                      <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <button 
                    v-if="showEdit"
                    @click.stop="$emit('edit', row)"
                    class="action-btn action-btn-edit"
                    title="Editar"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                    </svg>
                  </button>
                  <button 
                    v-if="showDelete"
                    @click.stop="$emit('delete', row)"
                    class="action-btn action-btn-delete"
                    title="Eliminar"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true,
    // Format: [{ key: 'nombre', label: 'Nombre', sortable: true, align: 'left' }]
  },
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  emptyMessage: {
    type: String,
    default: 'No hay datos para mostrar'
  },
  rowClickable: {
    type: Boolean,
    default: false
  },
  showView: {
    type: Boolean,
    default: true
  },
  showEdit: {
    type: Boolean,
    default: true
  },
  showDelete: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['row-click', 'view', 'edit', 'delete', 'sort'])

const sortKey = ref('')
const sortOrder = ref('asc') // 'asc' o 'desc'

const hasActions = computed(() => {
  return props.showView || props.showEdit || props.showDelete
})

const sortedData = computed(() => {
  if (!sortKey.value) return props.data

  return [...props.data].sort((a, b) => {
    const aVal = getNestedValue(a, sortKey.value)
    const bVal = getNestedValue(b, sortKey.value)

    let comparison = 0
    if (aVal > bVal) comparison = 1
    if (aVal < bVal) comparison = -1

    return sortOrder.value === 'asc' ? comparison : -comparison
  })
})

const handleSort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  emit('sort', { key: sortKey.value, order: sortOrder.value })
}

const handleRowClick = (row) => {
  if (props.rowClickable) {
    emit('row-click', row)
  }
}

const getNestedValue = (obj, path) => {
  return path.split('.').reduce((current, key) => current?.[key], obj)
}

const formatValue = (row, column) => {
  const value = getNestedValue(row, column.key)
  
  if (value === null || value === undefined) return '-'
  if (column.format) return column.format(value, row)
  
  return value
}
</script>

<style scoped>
.table-wrapper {
  width: 100%;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

/* Loading State */
.table-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #8b5cf6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Empty State */
.table-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

/* Table Container */
.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

/* Header */
.table-header {
  background-color: #fafafa;
  border-bottom: 2px solid #e5e7eb;
}

.table-header-cell {
  padding: 0.875rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.table-header-cell.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.table-header-cell.sortable:hover {
  background-color: #f3f4f6;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-icon {
  width: 16px;
  height: 16px;
  color: #d1d5db;
  transition: color 0.2s;
}

.sort-icon.sort-active {
  color: #8b5cf6;
}

/* Body */
.table-body {
  background-color: white;
}

.table-row {
  border-bottom: 1px solid #e5e7eb;
  transition: background-color 0.2s;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background-color: #f9fafb;
}

.table-row.row-clickable {
  cursor: pointer;
}

.table-row.row-clickable:hover {
  background-color: #f3f4f6;
}

.table-cell {
  padding: 1rem;
  font-size: 0.875rem;
  color: #1f2937;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn-view {
  color: #3b82f6;
  background-color: transparent;
}

.action-btn-view:hover {
  background-color: #dbeafe;
}

.action-btn-edit {
  color: #8b5cf6;
  background-color: transparent;
}

.action-btn-edit:hover {
  background-color: #ede9fe;
}

.action-btn-delete {
  color: #ef4444;
  background-color: transparent;
}

.action-btn-delete:hover {
  background-color: #fee2e2;
}

/* Responsive */
@media (max-width: 768px) {
  .table-header-cell,
  .table-cell {
    padding: 0.75rem 0.5rem;
    font-size: 0.813rem;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>
<template>
  <MainLayout>
    <!-- Header -->
    <div class="mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Pacientes</h1>
          <p class="text-gray-600 mt-1">Gestión de pacientes del sistema</p>
        </div>
        <Button @click="irANuevo">
          Nuevo Paciente
        </Button>
      </div>
    </div>

    <!-- Search -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        type="text"
        placeholder="Buscar paciente..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
      />
      <p class="mt-2 text-sm text-gray-600">
        Total: <strong>{{ totalPacientes }}</strong> pacientes
      </p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <div class="loading-spinner-large mx-auto"></div>
      <p class="mt-4 text-gray-600">Cargando pacientes...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!hasPacientes" class="bg-white rounded-lg shadow p-12 text-center">
      <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
      </svg>
      <h3 class="text-lg font-semibold text-gray-900 mb-2">No hay pacientes registrados</h3>
      <p class="text-gray-600 mb-4">Comienza agregando tu primer paciente</p>
      <Button @click="irANuevo">
        Crear Primer Paciente
      </Button>
    </div>

    <!-- Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Paciente
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Edad
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Sexo
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Teléfono
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr 
            v-for="paciente in pacientes" 
            :key="paciente.id"
            class="hover:bg-gray-50 cursor-pointer"
            @click="verDetalle(paciente)"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-semibold">
                  {{ getIniciales(paciente.nombre_completo) }}
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">
                    {{ paciente.nombre_completo }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ formatearDPI(paciente.dpi) }}
                  </div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ calcularEdad(paciente.fecha_nacimiento) }} años
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getBadgeClassSexo(paciente.sexo)">
                {{ obtenerBadgeSexo(paciente.sexo).text }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <a 
                v-if="paciente.telefono"
                :href="`tel:${paciente.telefono}`"
                class="text-purple-600 hover:text-purple-700"
                @click.stop
              >
                {{ formatearTelefono(paciente.telefono) }}
              </a>
              <span v-else class="text-gray-400">Sin teléfono</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button 
                @click.stop="verDetalle(paciente)"
                class="text-purple-600 hover:text-purple-900 mr-3"
              >
                Ver
              </button>
              <button 
                @click.stop="confirmarEliminar(paciente)"
                class="text-red-600 hover:text-red-900"
              >
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination simple -->
      <div class="bg-gray-50 px-6 py-4 border-t border-gray-200">
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-700">
            Mostrando {{ pacientes.length }} de {{ totalPacientes }} pacientes
          </div>
          <div class="flex gap-2">
            <button
              @click="irAPagina(pagination.page - 1)"
              :disabled="pagination.page === 1"
              class="px-3 py-1 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <span class="px-3 py-1">
              Página {{ pagination.page }} de {{ pagination.totalPages }}
            </span>
            <button
              @click="irAPagina(pagination.page + 1)"
              :disabled="pagination.page === pagination.totalPages"
              class="px-3 py-1 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Eliminar -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div class="text-center">
          <svg class="w-16 h-16 mx-auto mb-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">¿Eliminar paciente?</h3>
          <p class="text-gray-600 mb-4">
            Se eliminará a <strong>{{ pacienteAEliminar?.nombre_completo }}</strong>
          </p>
          <p class="text-sm text-gray-500">Esta acción no se puede deshacer</p>
        </div>
        <div class="flex gap-3 justify-end mt-6">
          <Button variant="secondary" @click="showDeleteModal = false">
            Cancelar
          </Button>
          <Button variant="danger" :loading="loading" @click="eliminarPaciente">
            Eliminar
          </Button>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePacientes } from '@/composables/usePacientes'
import MainLayout from '@/components/layout/MainLayout.vue'
import Button from '@/components/common/Button.vue'

const router = useRouter()

// Composable
const {
  pacientes,
  loading,
  pagination,
  hasPacientes,
  totalPacientes,
  loadPacientes,
  irAPagina,
  eliminarPaciente: eliminarPacienteStore,
  calcularEdad,
  formatearTelefono,
  formatearDPI,
  obtenerBadgeSexo
} = usePacientes()

// Estado local
const searchQuery = ref('')
const showDeleteModal = ref(false)
const pacienteAEliminar = ref(null)

// Funciones
function getIniciales(nombreCompleto) {
  if (!nombreCompleto) return '??'
  const palabras = nombreCompleto.trim().split(' ')
  if (palabras.length === 1) return palabras[0].substring(0, 2).toUpperCase()
  return (palabras[0][0] + palabras[palabras.length - 1][0]).toUpperCase()
}

function getBadgeClassSexo(sexo) {
  const base = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
  return sexo === 'M' ? `${base} bg-blue-100 text-blue-800` : `${base} bg-pink-100 text-pink-800`
}

function handleSearch() {
  // TODO: Implementar búsqueda
  console.log('Buscando:', searchQuery.value)
}

function verDetalle(paciente) {
  router.push(`/pacientes/${paciente.id}`)
}

function irANuevo() {
  router.push('/pacientes/nuevo')
}

function confirmarEliminar(paciente) {
  pacienteAEliminar.value = paciente
  showDeleteModal.value = true
}

async function eliminarPaciente() {
  try {
    await eliminarPacienteStore(pacienteAEliminar.value.id, false)
    showDeleteModal.value = false
    pacienteAEliminar.value = null
    await loadPacientes()
  } catch (err) {
    console.error('Error:', err)
  }
}

// Lifecycle
onMounted(() => {
  loadPacientes()
})
</script>

<style scoped>
.loading-spinner-large {
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
</style>
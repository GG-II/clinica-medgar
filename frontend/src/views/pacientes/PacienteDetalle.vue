<template>
  <MainLayout>
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="loading-spinner-large"></div>
      <p class="ml-4 text-gray-600">Cargando paciente...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <p class="text-red-800">{{ error }}</p>
      <Button variant="secondary" @click="volver" class="mt-4">
        Volver a la lista
      </Button>
    </div>

    <!-- Paciente Detail -->
    <div v-else-if="pacienteActual">
      <!-- Header con acciones -->
      <div class="flex justify-between items-start mb-6">
        <div class="flex items-center gap-4">
          <button 
            @click="volver"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <div>
            <h1 class="text-3xl font-bold text-gray-900">{{ pacienteActual.nombre_completo }}</h1>
            <p class="text-gray-600 mt-1">Paciente #{{ pacienteActual.id }}</p>
          </div>
        </div>

        <div class="flex gap-3">
          <Button variant="secondary" @click="editarPaciente">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            Editar
          </Button>
          <Button @click="verHistoria">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            Historia Clínica
          </Button>
          <Button variant="danger" @click="showDeleteModal = true">
            Eliminar
          </Button>
        </div>
      </div>

      <!-- Grid de Información -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Columna Izquierda: Info Personal -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Información Personal -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Información Personal
            </h2>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">DPI</label>
                <p class="text-gray-900">{{ formatearDPI(pacienteActual.dpi) }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Fecha de Nacimiento</label>
                <p class="text-gray-900">{{ formatearFecha(pacienteActual.fecha_nacimiento) }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Edad</label>
                <p class="text-gray-900">{{ calcularEdad(pacienteActual.fecha_nacimiento) }} años</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Sexo</label>
                <p>
                  <span :class="getBadgeClassSexo(pacienteActual.sexo)">
                    {{ obtenerBadgeSexo(pacienteActual.sexo).text }}
                  </span>
                </p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Estado Civil</label>
                <p class="text-gray-900">{{ pacienteActual.estado_civil || 'No especificado' }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Ocupación</label>
                <p class="text-gray-900">{{ pacienteActual.ocupacion || 'No especificado' }}</p>
              </div>
            </div>
          </div>

          <!-- Contacto -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
              Información de Contacto
            </h2>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">Teléfono</label>
                <p class="text-gray-900">
                  <a 
                    v-if="pacienteActual.telefono"
                    :href="`tel:${pacienteActual.telefono}`"
                    class="text-purple-600 hover:underline"
                  >
                    {{ formatearTelefono(pacienteActual.telefono) }}
                  </a>
                  <span v-else class="text-gray-400">Sin teléfono</span>
                </p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Email</label>
                <p class="text-gray-900">
                  <a 
                    v-if="pacienteActual.email"
                    :href="`mailto:${pacienteActual.email}`"
                    class="text-purple-600 hover:underline"
                  >
                    {{ pacienteActual.email }}
                  </a>
                  <span v-else class="text-gray-400">Sin email</span>
                </p>
              </div>
              <div class="col-span-2">
                <label class="text-sm font-medium text-gray-500">Dirección</label>
                <p class="text-gray-900">{{ pacienteActual.direccion || 'No especificado' }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Municipio</label>
                <p class="text-gray-900">{{ pacienteActual.municipio || 'No especificado' }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Departamento</label>
                <p class="text-gray-900">{{ pacienteActual.departamento || 'No especificado' }}</p>
              </div>
            </div>
          </div>

          <!-- Información Médica -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              Información Médica
            </h2>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">Tipo de Sangre</label>
                <p class="text-gray-900">{{ pacienteActual.tipo_sangre || 'No especificado' }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">IGSS</label>
                <p>
                  <span :class="getBadgeClassIGSS(pacienteActual.tiene_igss)">
                    {{ pacienteActual.tiene_igss ? 'Sí' : 'No' }}
                  </span>
                </p>
              </div>
              <div v-if="pacienteActual.tiene_igss" class="col-span-2">
                <label class="text-sm font-medium text-gray-500">Número IGSS</label>
                <p class="text-gray-900">{{ pacienteActual.numero_igss || 'No especificado' }}</p>
              </div>
              <div class="col-span-2">
                <label class="text-sm font-medium text-gray-500">Alergias</label>
                <p class="text-gray-900">{{ pacienteActual.alergias || 'Ninguna registrada' }}</p>
              </div>
              <div class="col-span-2">
                <label class="text-sm font-medium text-gray-500">Condiciones Médicas</label>
                <p class="text-gray-900">{{ pacienteActual.condiciones_medicas || 'Ninguna registrada' }}</p>
              </div>
            </div>
          </div>

          <!-- Contacto de Emergencia -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              Contacto de Emergencia
            </h2>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">Nombre</label>
                <p class="text-gray-900">{{ pacienteActual.contacto_emergencia_nombre || 'No especificado' }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Parentesco</label>
                <p class="text-gray-900">{{ pacienteActual.contacto_emergencia_parentesco || 'No especificado' }}</p>
              </div>
              <div class="col-span-2">
                <label class="text-sm font-medium text-gray-500">Teléfono</label>
                <p class="text-gray-900">
                  <a 
                    v-if="pacienteActual.contacto_emergencia_telefono"
                    :href="`tel:${pacienteActual.contacto_emergencia_telefono}`"
                    class="text-purple-600 hover:underline"
                  >
                    {{ formatearTelefono(pacienteActual.contacto_emergencia_telefono) }}
                  </a>
                  <span v-else class="text-gray-400">Sin teléfono</span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Columna Derecha: Avatar y Stats -->
        <div class="space-y-6">
          <!-- Avatar -->
          <div class="bg-white rounded-lg shadow p-6 text-center">
            <div class="w-32 h-32 mx-auto bg-purple-100 rounded-full flex items-center justify-center text-purple-600 text-4xl font-bold mb-4">
              {{ getIniciales(pacienteActual.nombre_completo) }}
            </div>
            <h3 class="text-lg font-semibold text-gray-900">{{ pacienteActual.nombre_completo }}</h3>
            <p class="text-sm text-gray-600 mt-1">{{ calcularEdad(pacienteActual.fecha_nacimiento) }} años</p>
          </div>

          <!-- Quick Stats -->
          <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Estadísticas</h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                <span class="text-sm font-medium text-gray-600">Consultas Totales</span>
                <span class="text-lg font-bold text-purple-600">0</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span class="text-sm font-medium text-gray-600">Última Consulta</span>
                <span class="text-sm font-semibold text-blue-600">Sin consultas</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                <span class="text-sm font-medium text-gray-600">Estado</span>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Activo
                </span>
              </div>
            </div>
          </div>

          <!-- Fechas -->
          <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Información del Sistema</h3>
            <div class="space-y-3 text-sm">
              <div>
                <label class="font-medium text-gray-500">Registrado</label>
                <p class="text-gray-900">{{ formatearFechaHora(pacienteActual.created_at) }}</p>
              </div>
              <div>
                <label class="font-medium text-gray-500">Última Actualización</label>
                <p class="text-gray-900">{{ formatearFechaHora(pacienteActual.updated_at) }}</p>
              </div>
            </div>
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
            Se eliminará a <strong>{{ pacienteActual?.nombre_completo }}</strong>
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
import { useRouter, useRoute } from 'vue-router'
import { usePacientes } from '@/composables/usePacientes'
import MainLayout from '@/components/layout/MainLayout.vue'
import Button from '@/components/common/Button.vue'

const router = useRouter()
const route = useRoute()

// Composable
const {
  pacienteActual,
  loading,
  error,
  loadPaciente,
  eliminarPaciente: eliminarPacienteStore,
  calcularEdad,
  formatearTelefono,
  formatearDPI,
  obtenerBadgeSexo
} = usePacientes()

// Estado local
const showDeleteModal = ref(false)

// Funciones de formateo locales
function formatearFecha(fecha) {
  if (!fecha) return 'No especificado'
  const date = new Date(fecha)
  const opciones = { year: 'numeric', month: 'long', day: 'numeric' }
  return date.toLocaleDateString('es-GT', opciones)
}

function formatearFechaHora(fecha) {
  if (!fecha) return 'No especificado'
  const date = new Date(fecha)
  const opciones = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return date.toLocaleDateString('es-GT', opciones)
}

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

function getBadgeClassIGSS(tieneIGSS) {
  const base = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
  return tieneIGSS ? `${base} bg-green-100 text-green-800` : `${base} bg-gray-100 text-gray-800`
}

function volver() {
  router.push('/pacientes')
}

function editarPaciente() {
  router.push(`/pacientes/${route.params.id}/editar`)
}

function verHistoria() {
  router.push(`/pacientes/${route.params.id}/historia`)
}

async function eliminarPaciente() {
  try {
    await eliminarPacienteStore(route.params.id, true)
    showDeleteModal.value = false
    router.push('/pacientes')
  } catch (err) {
    console.error('Error:', err)
  }
}

// Lifecycle
onMounted(() => {
  loadPaciente(route.params.id)
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
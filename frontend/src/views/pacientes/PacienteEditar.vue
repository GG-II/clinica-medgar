<template>
  <MainLayout>
    <div class="max-w-4xl mx-auto">
      <!-- Loading State -->
      <div v-if="loading && !pacienteActual" class="flex justify-center py-12">
        <div class="loading-spinner-large"></div>
        <p class="ml-4 text-gray-600">Cargando paciente...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-800">{{ error }}</p>
        <Button variant="secondary" @click="volver" class="mt-4">
          Volver
        </Button>
      </div>

      <!-- Formulario -->
      <div v-else-if="pacienteActual">
        <!-- Header -->
        <div class="flex items-center gap-4 mb-6">
          <button 
            @click="volver"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Editar Paciente</h1>
            <p class="text-gray-600 mt-1">{{ pacienteActual.nombre_completo }}</p>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Información Personal -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Información Personal
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Nombre Completo -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Nombre Completo <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.nombre_completo"
                  type="text"
                  required
                  class="input-field"
                  :class="{ 'border-red-500': errors.nombre_completo }"
                  placeholder="Ej: Juan Carlos Pérez García"
                />
                <p v-if="errors.nombre_completo" class="text-red-500 text-sm mt-1">
                  {{ errors.nombre_completo }}
                </p>
              </div>

              <!-- DPI -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  DPI
                </label>
                <input
                  v-model="form.dpi"
                  type="text"
                  maxlength="13"
                  class="input-field"
                  :class="{ 'border-red-500': errors.dpi }"
                  placeholder="1234567890101"
                  @input="validarDPI"
                />
                <p v-if="errors.dpi" class="text-red-500 text-sm mt-1">
                  {{ errors.dpi }}
                </p>
                <p class="text-gray-500 text-xs mt-1">13 dígitos</p>
              </div>

              <!-- Fecha de Nacimiento -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Fecha de Nacimiento <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.fecha_nacimiento"
                  type="date"
                  required
                  class="input-field"
                  :max="fechaMaxima"
                />
                <p v-if="form.fecha_nacimiento" class="text-gray-500 text-xs mt-1">
                  {{ calcularEdadDesdeForm() }} años
                </p>
              </div>

              <!-- Sexo -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Sexo <span class="text-red-500">*</span>
                </label>
                <select v-model="form.sexo" required class="input-field">
                  <option value="M">Masculino</option>
                  <option value="F">Femenino</option>
                </select>
              </div>

              <!-- Estado Civil -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Estado Civil
                </label>
                <select v-model="form.estado_civil" class="input-field">
                  <option value="">Seleccionar...</option>
                  <option value="Soltero/a">Soltero/a</option>
                  <option value="Casado/a">Casado/a</option>
                  <option value="Unido/a">Unido/a</option>
                  <option value="Divorciado/a">Divorciado/a</option>
                  <option value="Viudo/a">Viudo/a</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Información de Contacto -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
              Información de Contacto
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Teléfono -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Teléfono
                </label>
                <input
                  v-model="form.telefono"
                  type="tel"
                  maxlength="8"
                  class="input-field"
                  placeholder="12345678"
                  @input="validarTelefono"
                />
                <p v-if="errors.telefono" class="text-red-500 text-sm mt-1">
                  {{ errors.telefono }}
                </p>
              </div>

              <!-- Email -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  v-model="form.email"
                  type="email"
                  class="input-field"
                  placeholder="ejemplo@correo.com"
                />
              </div>

              <!-- Dirección -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Dirección
                </label>
                <textarea
                  v-model="form.direccion"
                  rows="2"
                  class="input-field"
                  placeholder="Calle, zona, colonia o aldea"
                ></textarea>
              </div>

              <!-- Municipio -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Municipio
                </label>
                <input
                  v-model="form.municipio"
                  type="text"
                  class="input-field"
                  placeholder="Ej: Huehuetenango"
                />
              </div>

              <!-- Departamento -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Departamento
                </label>
                <select v-model="form.departamento" class="input-field">
                  <option value="">Seleccionar...</option>
                  <option value="Alta Verapaz">Alta Verapaz</option>
                  <option value="Baja Verapaz">Baja Verapaz</option>
                  <option value="Chimaltenango">Chimaltenango</option>
                  <option value="Chiquimula">Chiquimula</option>
                  <option value="El Progreso">El Progreso</option>
                  <option value="Escuintla">Escuintla</option>
                  <option value="Guatemala">Guatemala</option>
                  <option value="Huehuetenango">Huehuetenango</option>
                  <option value="Izabal">Izabal</option>
                  <option value="Jalapa">Jalapa</option>
                  <option value="Jutiapa">Jutiapa</option>
                  <option value="Petén">Petén</option>
                  <option value="Quetzaltenango">Quetzaltenango</option>
                  <option value="Quiché">Quiché</option>
                  <option value="Retalhuleu">Retalhuleu</option>
                  <option value="Sacatepéquez">Sacatepéquez</option>
                  <option value="San Marcos">San Marcos</option>
                  <option value="Santa Rosa">Santa Rosa</option>
                  <option value="Sololá">Sololá</option>
                  <option value="Suchitepéquez">Suchitepéquez</option>
                  <option value="Totonicapán">Totonicapán</option>
                  <option value="Zacapa">Zacapa</option>
                </select>
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

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- IGSS -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  ¿Tiene IGSS?
                </label>
                <div class="flex items-center gap-4 mt-2">
                  <label class="flex items-center">
                    <input
                      v-model="form.tiene_igss"
                      type="radio"
                      :value="true"
                      class="mr-2"
                    />
                    Sí
                  </label>
                  <label class="flex items-center">
                    <input
                      v-model="form.tiene_igss"
                      type="radio"
                      :value="false"
                      class="mr-2"
                    />
                    No
                  </label>
                </div>
              </div>

              <!-- Número IGSS -->
              <div v-if="form.tiene_igss">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Número IGSS
                </label>
                <input
                  v-model="form.numero_igss"
                  type="text"
                  class="input-field"
                  placeholder="123456789"
                />
              </div>

              <!-- Observaciones -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Observaciones
                </label>
                <textarea
                  v-model="form.observaciones"
                  rows="3"
                  class="input-field"
                  placeholder="Notas adicionales, condiciones médicas, alergias, etc."
                ></textarea>
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

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Nombre -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Nombre Completo
                </label>
                <input
                  v-model="form.contacto_emergencia_nombre"
                  type="text"
                  class="input-field"
                  placeholder="Nombre del contacto"
                />
              </div>

              <!-- Relación -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Parentesco
                </label>
                <input
                  v-model="form.contacto_emergencia_relacion"
                  type="text"
                  class="input-field"
                  placeholder="Ej: Hijo/a, Esposo/a, Hermano/a"
                />
              </div>

              <!-- Teléfono -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Teléfono
                </label>
                <input
                  v-model="form.contacto_emergencia_telefono"
                  type="tel"
                  maxlength="8"
                  class="input-field"
                  placeholder="12345678"
                />
              </div>
            </div>
          </div>

          <!-- Mensaje de Error General -->
          <div v-if="errorGeneral" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-800">{{ errorGeneral }}</p>
          </div>

          <!-- Botones de Acción -->
          <div class="flex gap-3 justify-end">
            <Button 
              type="button"
              variant="secondary" 
              @click="volver"
              :disabled="loading"
            >
              Cancelar
            </Button>
            <Button 
              type="submit"
              :loading="loading"
            >
              Guardar Cambios
            </Button>
          </div>
        </form>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
  actualizarPaciente
} = usePacientes()

// Estado del formulario
const form = ref({
  nombre_completo: '',
  dpi: '',
  fecha_nacimiento: '',
  sexo: 'M',
  estado_civil: '',
  telefono: '',
  email: '',
  direccion: '',
  municipio: '',
  departamento: '',
  tiene_igss: false,
  numero_igss: '',
  observaciones: '',
  contacto_emergencia_nombre: '',
  contacto_emergencia_relacion: '',
  contacto_emergencia_telefono: ''
})

const errors = ref({})
const errorGeneral = ref('')

// Computed
const fechaMaxima = computed(() => {
  const hoy = new Date()
  return hoy.toISOString().split('T')[0]
})

// Funciones de validación
function validarDPI() {
  if (form.value.dpi && form.value.dpi.length !== 13) {
    errors.value.dpi = 'El DPI debe tener 13 dígitos'
  } else {
    delete errors.value.dpi
  }
}

function validarTelefono() {
  if (form.value.telefono && form.value.telefono.length !== 8) {
    errors.value.telefono = 'El teléfono debe tener 8 dígitos'
  } else {
    delete errors.value.telefono
  }
}

function calcularEdadDesdeForm() {
  if (!form.value.fecha_nacimiento) return 0
  
  const hoy = new Date()
  const nacimiento = new Date(form.value.fecha_nacimiento)
  let edad = hoy.getFullYear() - nacimiento.getFullYear()
  const mes = hoy.getMonth() - nacimiento.getMonth()
  
  if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
    edad--
  }
  
  return edad
}

function cargarDatosPaciente() {
  if (!pacienteActual.value) return
  
  // Cargar datos en el formulario
  form.value = {
    nombre_completo: pacienteActual.value.nombre_completo || '',
    dpi: pacienteActual.value.dpi || '',
    fecha_nacimiento: pacienteActual.value.fecha_nacimiento || '',
    sexo: pacienteActual.value.sexo || 'M',
    estado_civil: pacienteActual.value.estado_civil || '',
    telefono: pacienteActual.value.telefono || '',
    email: pacienteActual.value.email || '',
    direccion: pacienteActual.value.direccion || '',
    municipio: pacienteActual.value.municipio || '',
    departamento: pacienteActual.value.departamento || '',
    tiene_igss: pacienteActual.value.tiene_igss || false,
    numero_igss: pacienteActual.value.numero_igss || '',
    observaciones: pacienteActual.value.observaciones || '',
    contacto_emergencia_nombre: pacienteActual.value.contacto_emergencia_nombre || '',
    contacto_emergencia_relacion: pacienteActual.value.contacto_emergencia_relacion || '',
    contacto_emergencia_telefono: pacienteActual.value.contacto_emergencia_telefono || ''
  }
}

function validarFormulario() {
  errors.value = {}
  errorGeneral.value = ''
  
  if (!form.value.nombre_completo || form.value.nombre_completo.trim().length < 3) {
    errors.value.nombre_completo = 'El nombre debe tener al menos 3 caracteres'
  }
  
  if (form.value.dpi && form.value.dpi.length !== 13) {
    errors.value.dpi = 'El DPI debe tener 13 dígitos'
  }
  
  if (form.value.telefono && form.value.telefono.length !== 8) {
    errors.value.telefono = 'El teléfono debe tener 8 dígitos'
  }
  
  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validarFormulario()) {
    errorGeneral.value = 'Por favor corrige los errores en el formulario'
    return
  }
  
  try {
    await actualizarPaciente(route.params.id, form.value)
    // El composable redirige automáticamente al detalle
  } catch (error) {
    errorGeneral.value = error.message || 'Error al actualizar el paciente'
  }
}

function volver() {
  router.push(`/pacientes/${route.params.id}`)
}

// Lifecycle
onMounted(async () => {
  await loadPaciente(route.params.id)
  cargarDatosPaciente()
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

.input-field {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
  outline: none;
}

.input-field:focus {
  border-color: #8b5cf6;
  ring: 2px;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.input-field:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  opacity: 0.6;
}

textarea.input-field {
  resize: vertical;
  font-family: inherit;
}

select.input-field {
  cursor: pointer;
}
</style>
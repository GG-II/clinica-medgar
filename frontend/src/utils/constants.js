// Roles de usuario
export const ROLES = {
  MEDICO: 'medico',
  ENFERMERA: 'enfermera',
  RECEPCIONISTA: 'recepcionista',
  ADMINISTRADOR: 'administrador'
}

// Estados de citas
export const ESTADOS_CITA = {
  PROGRAMADA: 'programada',
  CONFIRMADA: 'confirmada',
  EN_CURSO: 'en_curso',
  COMPLETADA: 'completada',
  CANCELADA: 'cancelada',
  NO_ASISTIO: 'no_asistio'
}

// Tipos de antecedentes
export const TIPOS_ANTECEDENTES = {
  MEDICOS: 'medicos',
  QUIRURGICOS: 'quirurgicos',
  TRAUMATICOS: 'traumaticos',
  ALERGICOS: 'alergicos',
  GINECOLOGICOS: 'ginecologicos',
  OBSTETRICOS: 'obstetricos'
}

// Mensajes de la aplicación
export const MESSAGES = {
  LOGIN_SUCCESS: 'Inicio de sesión exitoso',
  LOGIN_ERROR: 'Usuario o contraseña incorrectos',
  LOGOUT_SUCCESS: 'Sesión cerrada correctamente',
  SAVE_SUCCESS: 'Guardado correctamente',
  DELETE_SUCCESS: 'Eliminado correctamente',
  ERROR_GENERAL: 'Ocurrió un error. Por favor intenta de nuevo.'
}

// Colores por tipo de cita
export const COLORES_CITA = {
  'primera_consulta': '#3B82F6',
  'reconsulta': '#10B981',
  'procedimiento': '#F59E0B',
  'control_embarazo': '#EC4899',
  'control_nino_sano': '#8B5CF6',
  'emergencia': '#EF4444'
}
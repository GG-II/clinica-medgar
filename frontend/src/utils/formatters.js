// Validar email
export function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Validar teléfono guatemalteco (8 dígitos)
export function isValidPhone(phone) {
  const re = /^\d{8}$/
  return re.test(phone.replace(/\s/g, ''))
}

// Validar DPI guatemalteco (13 dígitos)
export function isValidDPI(dpi) {
  const cleaned = dpi.replace(/\s/g, '')
  return /^\d{13}$/.test(cleaned)
}

// Validar fecha (formato YYYY-MM-DD)
export function isValidDate(date) {
  if (!date) return false
  const re = /^\d{4}-\d{2}-\d{2}$/
  return re.test(date)
}

// Validar contraseña fuerte
export function isStrongPassword(password) {
  // Mínimo 8 caracteres, una mayúscula, una minúscula, un número
  const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
  return re.test(password)
}

// Validar campo requerido
export function isRequired(value) {
  if (typeof value === 'string') {
    return value.trim().length > 0
  }
  return value !== null && value !== undefined
}
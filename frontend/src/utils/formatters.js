// Formatear fecha a DD/MM/YYYY
export function formatDate(date) {
  if (!date) return ''
  const d = new Date(date)
  const day = String(d.getDate()).padStart(2, '0')
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const year = d.getFullYear()
  return `${day}/${month}/${year}`
}

// Formatear fecha y hora
export function formatDateTime(datetime) {
  if (!datetime) return ''
  const d = new Date(datetime)
  const date = formatDate(d)
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  return `${date} ${hours}:${minutes}`
}

// Formatear teléfono guatemalteco (1234-5678)
export function formatPhone(phone) {
  if (!phone) return ''
  const cleaned = phone.replace(/\D/g, '')
  if (cleaned.length !== 8) return phone
  return `${cleaned.slice(0, 4)}-${cleaned.slice(4)}`
}

// Formatear DPI (1234 56789 0101)
export function formatDPI(dpi) {
  if (!dpi) return ''
  const cleaned = dpi.replace(/\D/g, '')
  if (cleaned.length !== 13) return dpi
  return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 9)} ${cleaned.slice(9)}`
}

// Formatear moneda (Q1,234.56)
export function formatCurrency(amount) {
  if (amount === null || amount === undefined) return 'Q0.00'
  return `Q${Number(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`
}

// Calcular edad desde fecha de nacimiento
export function calculateAge(birthDate) {
  if (!birthDate) return 0
  const today = new Date()
  const birth = new Date(birthDate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  return age
}

// Obtener iniciales de nombre
export function getInitials(name) {
  if (!name) return ''
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
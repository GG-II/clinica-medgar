import axios from './axios'

export const pacientesAPI = {
  // Listar pacientes con paginación
  getAll(params = {}) {
    return axios.get('/pacientes', { params })
  },

  // Obtener un paciente
  getById(id) {
    return axios.get(`/pacientes/${id}`)
  },

  // Buscar pacientes
  search(query) {
    return axios.get('/pacientes/buscar', { params: { q: query } })
  },

  // Crear paciente
  create(data) {
    return axios.post('/pacientes', data)
  },

  // Actualizar paciente
  update(id, data) {
    return axios.put(`/pacientes/${id}`, data)
  },

  // Eliminar paciente
  delete(id) {
    return axios.delete(`/pacientes/${id}`)
  },

  // Obtener estadísticas
  getStats() {
    return axios.get('/pacientes/estadisticas')
  }
}
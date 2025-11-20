import axios from './axios'

export const authAPI = {
  // Login
  login(credentials) {
    return axios.post('/auth/login', credentials)
  },

  // Logout
  logout() {
    return axios.post('/auth/logout')
  },

  // Obtener usuario actual
  getCurrentUser() {
    return axios.get('/auth/me')
  },

  // Refresh token
  refreshToken(refreshToken) {
    return axios.post('/auth/refresh', { refresh_token: refreshToken })
  },

  // Cambiar contraseña
  changePassword(data) {
    return axios.put('/auth/change-password', data)
  }
}
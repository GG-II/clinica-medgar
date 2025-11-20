import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  // ✅ SOLO ESTA RUTA POR AHORA
  {
    path: '/pacientes',
    name: 'Pacientes',
    component: () => import('@/views/pacientes/PacientesList.vue'),
    meta: { requiresAuth: true }
  },
  
  // 🔴 COMENTADAS TEMPORALMENTE (descoméntalas cuando creemos los archivos)
   {
     path: '/pacientes/nuevo',
     name: 'PacienteNuevo',
     component: () => import('@/views/pacientes/PacienteNuevo.vue'),
     meta: { requiresAuth: true }
   },
   {
     path: '/pacientes/:id',
     name: 'PacienteDetalle',
     component: () => import('@/views/pacientes/PacienteDetalle.vue'),
     meta: { requiresAuth: true }
   },
 {
     path: '/pacientes/:id/editar',
     name: 'PacienteEditar',
     component: () => import('@/views/pacientes/PacienteEditar.vue'),
     meta: { requiresAuth: true }
   },
  // {
  //   path: '/pacientes/:id/historia',
  //   name: 'HistoriaClinica',
  //   component: () => import('@/views/historia/HistoriaClinica.vue'),
  //   meta: { requiresAuth: true }
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación - protege rutas que requieren autenticación
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth
  const isAuthenticated = authStore.isAuthenticated

  if (requiresAuth && !isAuthenticated) {
    // Si la ruta requiere auth y no está autenticado, redirigir a login
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    // Si ya está autenticado y va a login, redirigir a dashboard
    next('/dashboard')
  } else {
    // Permitir navegación
    next()
  }
})

export default router
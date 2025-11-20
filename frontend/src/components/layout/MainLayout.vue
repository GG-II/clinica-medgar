<template>
  <div class="main-layout">
    <!-- Navbar -->
    <Navbar />

    <div class="layout-body">
      <!-- Sidebar -->
      <Sidebar />

      <!-- Contenido principal -->
      <main :class="mainClasses">
        <div class="content-wrapper">
          <slot />
        </div>

        <!-- Footer -->
        <Footer />
      </main>
    </div>

    <!-- Overlay para cerrar sidebar en móvil -->
    <transition name="fade">
      <div
        v-if="uiStore.sidebarOpen && isMobile"
        class="sidebar-overlay"
        @click="uiStore.toggleSidebar"
      ></div>
    </transition>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useUIStore } from '@/stores/ui'
import Navbar from './Navbar.vue'
import Sidebar from './Sidebar.vue'
import Footer from './Footer.vue'

const uiStore = useUIStore()
const isMobile = ref(false)

const mainClasses = computed(() => {
  return {
    'main-content': true,
    'main-content-expanded': !uiStore.sidebarOpen
  }
})

function checkMobile() {
  isMobile.value = window.innerWidth < 768
  
  // Auto-cerrar sidebar en móvil
  if (isMobile.value && uiStore.sidebarOpen) {
    uiStore.toggleSidebar()
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f9fafb;
}

.layout-body {
  display: flex;
  flex: 1;
  position: relative;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  margin-top: 65px;
  min-height: calc(100vh - 65px);
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease;
}

.main-content-expanded {
  margin-left: 0;
}

.content-wrapper {
  flex: 1;
  padding: 2rem;
}

.sidebar-overlay {
  position: fixed;
  top: 65px;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 35;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }

  .content-wrapper {
    padding: 1rem;
  }
}
</style>
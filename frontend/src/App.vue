<template>
  <div id="app" class="min-h-screen">
    <!-- Componente de Loading global -->
    <Loading :show="uiStore.loading" />
    
    <!-- Componente de Alert global -->
    <Alert
      :show="uiStore.alert.show"
      :type="uiStore.alert.type"
      :message="uiStore.alert.message"
      @close="uiStore.hideAlert"
    />
    
    <!-- Vista actual -->
    <router-view />
  </div>
</template>

<script setup>
import { useUIStore } from '@/stores/ui'
import Loading from '@/components/common/Loading.vue'
import Alert from '@/components/common/Alert.vue'

const uiStore = useUIStore()
</script>
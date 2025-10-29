<template>
  <div id="app">
    <!-- 路由视图 -->
    <router-view />
    
    <!-- 全局加载状态 -->
    <div v-if="globalLoading" class="global-loading">
      <div class="loading-spinner"></div>
    </div>
    
    <!-- 全局消息提示 -->
    <div v-if="globalMessage.show" class="global-message" :class="globalMessage.type">
      {{ globalMessage.content }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useGlobalStore } from '@/stores/global'

const globalStore = useGlobalStore()

// 响应式数据
const globalLoading = ref(false)
const globalMessage = ref({
  show: false,
  type: 'info',
  content: ''
})

// 监听全局状态变化
onMounted(() => {
  // 监听加载状态
  globalStore.$subscribe((mutation, state) => {
    globalLoading.value = state.loading
  })
  
  // 监听消息状态
  globalStore.$subscribe((mutation, state) => {
    if (state.message.show) {
      globalMessage.value = { ...state.message }
      // 3秒后自动隐藏
      setTimeout(() => {
        globalMessage.value.show = false
        globalStore.hideMessage()
      }, 3000)
    }
  })
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: var(--background-secondary);
}

.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-index-modal);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--background-primary);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.global-message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-medium);
  color: white;
  z-index: var(--z-index-tooltip);
  max-width: 300px;
  box-shadow: var(--shadow-medium);
}

.global-message.info {
  background-color: var(--info-color);
}

.global-message.success {
  background-color: var(--success-color);
}

.global-message.warning {
  background-color: var(--warning-color);
}

.global-message.error {
  background-color: var(--error-color);
}
</style>
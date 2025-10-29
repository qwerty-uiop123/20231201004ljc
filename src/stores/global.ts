import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGlobalStore = defineStore('global', () => {
  // 全局加载状态
  const loading = ref(false)
  
  // 全局消息
  const message = ref({
    show: false,
    type: 'info' as 'info' | 'success' | 'warning' | 'error',
    content: ''
  })
  
  // 主题模式
  const theme = ref<'light' | 'dark'>('light')
  
  // 网络状态
  const online = ref(navigator.onLine)
  
  // 设置加载状态
  const setLoading = (status: boolean) => {
    loading.value = status
  }
  
  // 显示消息
  const showMessage = (content: string, type: 'info' | 'success' | 'warning' | 'error' = 'info') => {
    message.value = {
      show: true,
      type,
      content
    }
  }
  
  // 隐藏消息
  const hideMessage = () => {
    message.value.show = false
  }
  
  // 切换主题
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    document.documentElement.setAttribute('data-theme', theme.value)
  }
  
  // 监听网络状态
  if (typeof window !== 'undefined') {
    window.addEventListener('online', () => {
      online.value = true
      showMessage('网络已连接', 'success')
    })
    
    window.addEventListener('offline', () => {
      online.value = false
      showMessage('网络连接已断开', 'warning')
    })
  }
  
  return {
    loading,
    message,
    theme,
    online,
    setLoading,
    showMessage,
    hideMessage,
    toggleTheme
  }
})
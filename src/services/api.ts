import axios from 'axios'
import { useGlobalStore } from '@/stores/global'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const globalStore = useGlobalStore()
    globalStore.setLoading(true)
    
    // 添加token到请求头
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    const globalStore = useGlobalStore()
    globalStore.setLoading(false)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    const globalStore = useGlobalStore()
    globalStore.setLoading(false)
    return response.data
  },
  (error) => {
    const globalStore = useGlobalStore()
    globalStore.setLoading(false)
    
    if (error.response) {
      const status = error.response.status
      const message = error.response.data?.detail || error.response.data?.message || '请求失败'
      
      switch (status) {
        case 401:
          globalStore.showMessage('登录已过期，请重新登录', 'error')
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          globalStore.showMessage('权限不足', 'error')
          break
        case 404:
          globalStore.showMessage('请求的资源不存在', 'error')
          break
        case 500:
          globalStore.showMessage('服务器内部错误', 'error')
          break
        default:
          globalStore.showMessage(message, 'error')
      }
    } else if (error.request) {
      globalStore.showMessage('网络连接失败，请检查网络', 'error')
    } else {
      globalStore.showMessage('请求配置错误', 'error')
    }
    
    return Promise.reject(error)
  }
)

export default api
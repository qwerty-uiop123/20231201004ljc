import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo, LoginForm, RegisterForm } from '@/types/user'
import { authApi, userApi } from '@/services/auth'
import { useGlobalStore } from '@/stores/global'

export const useUserStore = defineStore('user', () => {
  const globalStore = useGlobalStore()
  
  // 用户信息
  const userInfo = ref<UserInfo | null>(null)
  
  // 登录状态
  const isLoggedIn = computed(() => !!userInfo.value)
  
  // 用户设置
  const userSettings = ref({
    theme: 'light' as 'light' | 'dark',
    notification: true,
    privacy: 'public' as 'public' | 'private',
    language: 'zh-CN'
  })
  
  // 登录方法
  const login = async (form: LoginForm) => {
    try {
      globalStore.setLoading(true)
      
      // 调用真实登录API
      const response = await authApi.login(form)
      
      if (response.access) {
        // 保存token
        localStorage.setItem('token', response.access)
        localStorage.setItem('refresh_token', response.refresh)
        
        // 获取用户信息
        const userResponse = await authApi.getUserInfo()
        userInfo.value = userResponse
        
        globalStore.showMessage('登录成功', 'success')
        return { success: true }
      } else {
        return { success: false, message: '登录失败' }
      }
    } catch (error: any) {
      const message = error.response?.data?.detail || '登录失败，请重试'
      return { success: false, message }
    } finally {
      globalStore.setLoading(false)
    }
  }
  
  // 注册方法
  const register = async (form: RegisterForm) => {
    try {
      globalStore.setLoading(true)
      
      // 调用真实注册API
      const response = await authApi.register(form)
      
      globalStore.showMessage('注册成功，请登录', 'success')
      return { success: true }
    } catch (error: any) {
      const message = error.response?.data?.detail || '注册失败，请重试'
      return { success: false, message }
    } finally {
      globalStore.setLoading(false)
    }
  }
  
  // 退出登录
  const logout = async () => {
    try {
      await authApi.logout()
    } catch (error) {
      // 即使API调用失败也继续执行本地清理
    } finally {
      userInfo.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
    }
  }
  
  // 更新用户信息
  const updateUserInfo = async (info: Partial<UserInfo>) => {
    if (userInfo.value) {
      try {
        const response = await userApi.updateUserInfo(userInfo.value.id, info)
        userInfo.value = { ...userInfo.value, ...response }
        globalStore.showMessage('用户信息更新成功', 'success')
      } catch (error: any) {
        const message = error.response?.data?.detail || '更新失败'
        globalStore.showMessage(message, 'error')
        throw error
      }
    }
  }
  
  // 检查登录状态
  const checkLoginStatus = async () => {
    const token = localStorage.getItem('token')
    if (token && !userInfo.value) {
      try {
        const response = await authApi.getUserInfo()
        userInfo.value = response
      } catch (error) {
        // token无效，清除本地存储
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
      }
    }
  }
  

  
  return {
    userInfo,
    isLoggedIn,
    userSettings,
    login,
    register,
    logout,
    updateUserInfo,
    checkLoginStatus
  }
})
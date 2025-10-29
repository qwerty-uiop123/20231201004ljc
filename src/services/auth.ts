import api from './api'
import type { UserInfo, LoginForm, RegisterForm } from '@/types/user'

// 用户认证相关API
export const authApi = {
  // 用户注册
  async register(form: RegisterForm) {
    const response = await api.post('/auth/register/', form)
    return response
  },
  
  // 用户登录
  async login(form: LoginForm) {
    const response = await api.post('/auth/login/', form)
    return response
  },
  
  // 刷新token
  async refreshToken(refreshToken: string) {
    const response = await api.post('/auth/refresh/', { refresh: refreshToken })
    return response
  },
  
  // 获取用户信息
  async getUserInfo() {
    const response = await api.get('/auth/user/')
    return response
  },
  
  // 修改密码
  async changePassword(oldPassword: string, newPassword: string) {
    const response = await api.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword
    })
    return response
  },
  
  // 退出登录
  async logout() {
    const response = await api.post('/auth/logout/')
    return response
  }
}

// 用户管理相关API
export const userApi = {
  // 更新用户信息
  async updateUserInfo(userId: number, userInfo: Partial<UserInfo>) {
    const response = await api.put(`/users/${userId}/`, userInfo)
    return response
  },
  
  // 获取用户详情
  async getUserDetail(userId: number) {
    const response = await api.get(`/users/${userId}/`)
    return response
  },
  
  // 上传头像
  async uploadAvatar(userId: number, avatarFile: File) {
    const formData = new FormData()
    formData.append('avatar', avatarFile)
    
    const response = await api.put(`/users/${userId}/avatar/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response
  }
}
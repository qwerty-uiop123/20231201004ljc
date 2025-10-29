import api from './api'

// 消息相关API
export const messageApi = {
  // 获取对话列表
  async getConversations(params?: {
    page?: number
    page_size?: number
  }) {
    const response = await api.get('/chat/conversations/', { params })
    return response
  },
  
  // 获取对话详情
  async getConversation(conversationId: number) {
    const response = await api.get(`/chat/conversations/${conversationId}/`)
    return response
  },
  
  // 创建对话
  async createConversation(participantId: number) {
    const response = await api.post('/chat/conversations/', {
      participants: [participantId]
    })
    return response
  },
  
  // 获取消息列表
  async getMessages(conversationId: number, params?: {
    page?: number
    page_size?: number
  }) {
    const response = await api.get(`/chat/conversations/${conversationId}/messages/`, { params })
    return response
  },
  
  // 发送消息
  async sendMessage(conversationId: number, data: {
    content: string
    message_type?: 'text' | 'image' | 'file'
    file?: File
  }) {
    const formData = new FormData()
    formData.append('content', data.content)
    formData.append('message_type', data.message_type || 'text')
    
    if (data.file) {
      formData.append('file', data.file)
    }
    
    const response = await api.post(`/chat/conversations/${conversationId}/messages/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response
  },
  
  // 删除消息
  async deleteMessage(messageId: number) {
    const response = await api.delete(`/chat/messages/${messageId}/`)
    return response
  },
  
  // 标记消息为已读
  async markAsRead(messageId: number) {
    const response = await api.post(`/chat/messages/${messageId}/read/`)
    return response
  },
  
  // 获取系统通知
  async getNotifications(params?: {
    page?: number
    page_size?: number
    unread_only?: boolean
  }) {
    const response = await api.get('/chat/notifications/', { params })
    return response
  },
  
  // 标记通知为已读
  async markNotificationAsRead(notificationId: number) {
    const response = await api.post(`/chat/notifications/${notificationId}/read/`)
    return response
  },
  
  // 标记所有通知为已读
  async markAllNotificationsAsRead() {
    const response = await api.post('/chat/notifications/mark-all-read/')
    return response
  },
  
  // 发送私信
  async sendDirectMessage(data: {
    recipient_id: number
    content: string
    message_type?: 'text' | 'image' | 'file'
    file?: File
  }) {
    const formData = new FormData()
    formData.append('recipient_id', data.recipient_id.toString())
    formData.append('content', data.content)
    formData.append('message_type', data.message_type || 'text')
    
    if (data.file) {
      formData.append('file', data.file)
    }
    
    const response = await api.post('/chat/send/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response
  }
}

// 搜索相关API
export const searchApi = {
  // 搜索贴吧
  async searchTiebas(query: string, params?: {
    page?: number
    page_size?: number
  }) {
    const response = await api.get('/tiebas/search/', {
      params: { q: query, ...params }
    })
    return response
  },
  
  // 搜索帖子
  async searchPosts(query: string, params?: {
    page?: number
    page_size?: number
    tieba?: number
  }) {
    const response = await api.get('/posts/search/', {
      params: { q: query, ...params }
    })
    return response
  },
  
  // 搜索用户
  async searchUsers(query: string, params?: {
    page?: number
    page_size?: number
  }) {
    const response = await api.get('/users/search/', {
      params: { q: query, ...params }
    })
    return response
  }
}
import api from './api'

// 贴吧相关API
export const tiebaApi = {
  // 获取贴吧列表
  async getTiebas(params?: {
    page?: number
    page_size?: number
    category?: string
    search?: string
    sort?: string
  }) {
    const response = await api.get('/tiebas/', { params })
    return response
  },
  
  // 获取贴吧详情
  async getTiebaDetail(tiebaId: number) {
    const response = await api.get(`/tiebas/${tiebaId}/`)
    return response
  },
  
  // 创建贴吧
  async createTieba(data: {
    name: string
    description: string
    category: string
    avatar?: File
  }) {
    const formData = new FormData()
    formData.append('name', data.name)
    formData.append('description', data.description)
    formData.append('category', data.category)
    if (data.avatar) {
      formData.append('avatar', data.avatar)
    }
    
    const response = await api.post('/tiebas/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response
  },
  
  // 加入贴吧
  async joinTieba(tiebaId: number) {
    const response = await api.post(`/tiebas/${tiebaId}/join/`)
    return response
  },
  
  // 退出贴吧
  async leaveTieba(tiebaId: number) {
    const response = await api.post(`/tiebas/${tiebaId}/leave/`)
    return response
  },
  
  // 关注贴吧
  async followTieba(tiebaId: number) {
    const response = await api.post(`/tiebas/${tiebaId}/follow/`)
    return response
  },
  
  // 取消关注贴吧
  async unfollowTieba(tiebaId: number) {
    const response = await api.post(`/tiebas/${tiebaId}/unfollow/`)
    return response
  },
  
  // 获取贴吧成员
  async getTiebaMembers(tiebaId: number, params?: {
    page?: number
    page_size?: number
  }) {
    const response = await api.get(`/tiebas/${tiebaId}/members/`, { params })
    return response
  }
}

// 帖子相关API
export const postApi = {
  // 获取帖子列表
  async getPosts(params?: {
    page?: number
    page_size?: number
    tieba?: number
    author?: number
    search?: string
    sort?: string
  }) {
    const response = await api.get('/posts/', { params })
    return response
  },
  
  // 获取帖子详情
  async getPostDetail(postId: number) {
    const response = await api.get(`/posts/${postId}/`)
    return response
  },
  
  // 创建帖子
  async createPost(data: {
    title: string
    content: string
    tieba: number
    images?: File[]
  }) {
    const formData = new FormData()
    formData.append('title', data.title)
    formData.append('content', data.content)
    formData.append('tieba', data.tieba.toString())
    
    if (data.images) {
      data.images.forEach((image, index) => {
        formData.append(`images`, image)
      })
    }
    
    const response = await api.post('/posts/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response
  },
  
  // 更新帖子
  async updatePost(postId: number, data: {
    title?: string
    content?: string
  }) {
    const response = await api.put(`/posts/${postId}/`, data)
    return response
  },
  
  // 删除帖子
  async deletePost(postId: number) {
    const response = await api.delete(`/posts/${postId}/`)
    return response
  },
  
  // 点赞帖子
  async likePost(postId: number) {
    const response = await api.post(`/posts/${postId}/like/`)
    return response
  },
  
  // 取消点赞帖子
  async unlikePost(postId: number) {
    const response = await api.post(`/posts/${postId}/unlike/`)
    return response
  },
  
  // 收藏帖子
  async favoritePost(postId: number) {
    const response = await api.post(`/posts/${postId}/favorite/`)
    return response
  },
  
  // 取消收藏帖子
  async unfavoritePost(postId: number) {
    const response = await api.post(`/posts/${postId}/unfavorite/`)
    return response
  },
  
  // 获取帖子回复
  async getPostReplies(postId: number, params?: {
    page?: number
    page_size?: number
  }) {
    const response = await api.get(`/posts/${postId}/replies/`, { params })
    return response
  },
  
  // 回复帖子
  async replyPost(postId: number, data: {
    content: string
    parent?: number
  }) {
    const response = await api.post(`/posts/${postId}/replies/`, data)
    return response
  }
}
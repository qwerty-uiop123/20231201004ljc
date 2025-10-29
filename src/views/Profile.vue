<template>
  <div class="profile-page">
    <!-- 用户信息头部 -->
    <div class="profile-header">
      <div class="user-info">
        <div class="avatar-section">
          <img :src="userInfo?.avatar || '/default-avatar.png'" :alt="userInfo?.nickname" class="user-avatar" />
          <button class="edit-avatar-btn" @click="handleEditAvatar">
            <span class="edit-icon">📷</span>
          </button>
        </div>
        
        <div class="user-details">
          <h1 class="username">{{ userInfo?.nickname }}</h1>
          <p class="user-id">ID: {{ userInfo?.id }}</p>
          <p class="user-bio">{{ userInfo?.bio || '这个人很懒，什么都没有写' }}</p>
          
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-number">{{ userStats?.postCount || 0 }}</span>
              <span class="stat-label">帖子</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ userStats?.replyCount || 0 }}</span>
              <span class="stat-label">回复</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ userStats?.followerCount || 0 }}</span>
              <span class="stat-label">粉丝</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ userStats?.followingCount || 0 }}</span>
              <span class="stat-label">关注</span>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <button class="edit-profile-btn" @click="handleEditProfile">
            <span class="btn-icon">✏️</span>
            编辑资料
          </button>
          <button class="settings-btn" @click="handleSettings">
            <span class="btn-icon">⚙️</span>
            设置
          </button>
        </div>
      </div>
    </div>

    <!-- 导航标签页 -->
    <div class="profile-tabs">
      <div class="tabs-container">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.label }}</span>
        </button>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="profile-content">
      <!-- 我的帖子 -->
      <div v-if="activeTab === 'posts'" class="tab-content">
        <div class="content-header">
          <h2>我的帖子</h2>
          <div class="filter-options">
            <button
              v-for="filter in postFilters"
              :key="filter.value"
              :class="['filter-btn', { active: postFilter === filter.value }]"
              @click="postFilter = filter.value"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        
        <div class="posts-list">
          <div
            v-for="post in filteredPosts"
            :key="post.id"
            class="post-item"
            @click="handleViewPost(post)"
          >
            <div class="post-header">
              <span class="tieba-name">{{ post.tiebaName }}</span>
              <span class="post-time">{{ formatTime(post.createTime) }}</span>
            </div>
            
            <h3 class="post-title">{{ post.title }}</h3>
            
            <div class="post-content">
              <p>{{ post.content }}</p>
            </div>
            
            <div class="post-stats">
              <span class="stat">
                <span class="stat-icon">👁️</span>
                {{ post.viewCount }}
              </span>
              <span class="stat">
                <span class="stat-icon">💬</span>
                {{ post.replyCount }}
              </span>
              <span class="stat">
                <span class="stat-icon">👍</span>
                {{ post.likeCount }}
              </span>
            </div>
            
            <div class="post-actions">
              <button class="action-btn" @click.stop="handleEditPost(post)">
                <span class="action-icon">✏️</span>
                编辑
              </button>
              <button class="action-btn delete" @click.stop="handleDeletePost(post)">
                <span class="action-icon">🗑️</span>
                删除
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && filteredPosts.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <p class="empty-text">暂无帖子</p>
          <p class="empty-subtext">去发表你的第一个帖子吧！</p>
          <button class="create-post-btn" @click="handleCreatePost">
            发表帖子
          </button>
        </div>
      </div>

      <!-- 我的回复 -->
      <div v-if="activeTab === 'replies'" class="tab-content">
        <div class="content-header">
          <h2>我的回复</h2>
        </div>
        
        <div class="replies-list">
          <div
            v-for="reply in userReplies"
            :key="reply.id"
            class="reply-item"
            @click="handleViewReplyPost(reply)"
          >
            <div class="reply-header">
              <span class="post-title">{{ reply.postTitle }}</span>
              <span class="reply-time">{{ formatTime(reply.createTime) }}</span>
            </div>
            
            <div class="reply-content">
              <p>{{ reply.content }}</p>
            </div>
            
            <div class="reply-stats">
              <span class="stat">
                <span class="stat-icon">👍</span>
                {{ reply.likeCount }}
              </span>
            </div>
            
            <div class="reply-actions">
              <button class="action-btn" @click.stop="handleEditReply(reply)">
                <span class="action-icon">✏️</span>
                编辑
              </button>
              <button class="action-btn delete" @click.stop="handleDeleteReply(reply)">
                <span class="action-icon">🗑️</span>
                删除
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && userReplies.length === 0" class="empty-state">
          <div class="empty-icon">💬</div>
          <p class="empty-text">暂无回复</p>
          <p class="empty-subtext">去参与讨论吧！</p>
        </div>
      </div>

      <!-- 我的收藏 -->
      <div v-if="activeTab === 'collections'" class="tab-content">
        <div class="content-header">
          <h2>我的收藏</h2>
        </div>
        
        <div class="collections-list">
          <div
            v-for="collection in userCollections"
            :key="collection.id"
            class="collection-item"
            @click="handleViewCollection(collection)"
          >
            <div class="collection-type">
              <span class="type-badge">{{ collection.type === 'post' ? '帖子' : '贴吧' }}</span>
            </div>
            
            <h3 class="collection-title">{{ collection.title }}</h3>
            
            <div class="collection-meta">
              <span class="meta-item">{{ collection.source }}</span>
              <span class="meta-item">{{ formatTime(collection.createTime) }}</span>
            </div>
            
            <div class="collection-actions">
              <button class="action-btn" @click.stop="handleRemoveCollection(collection)">
                <span class="action-icon">🗑️</span>
                取消收藏
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && userCollections.length === 0" class="empty-state">
          <div class="empty-icon">⭐</div>
          <p class="empty-text">暂无收藏</p>
          <p class="empty-subtext">收藏你感兴趣的内容吧！</p>
        </div>
      </div>

      <!-- 我的贴吧 -->
      <div v-if="activeTab === 'tiebas'" class="tab-content">
        <div class="content-header">
          <h2>我的贴吧</h2>
        </div>
        
        <div class="tiebas-list">
          <div
            v-for="tieba in userTiebas"
            :key="tieba.id"
            class="tieba-item"
            @click="handleViewTieba(tieba)"
          >
            <div class="tieba-avatar">
              <img :src="tieba.avatar || '/default-tieba.png'" :alt="tieba.name" />
            </div>
            
            <div class="tieba-info">
              <h3 class="tieba-name">{{ tieba.name }}</h3>
              <p class="tieba-desc">{{ tieba.description }}</p>
              
              <div class="tieba-stats">
                <span class="stat">
                  <span class="stat-icon">👥</span>
                  {{ tieba.memberCount }} 成员
                </span>
                <span class="stat">
                  <span class="stat-icon">📝</span>
                  {{ tieba.postCount }} 帖子
                </span>
              </div>
            </div>
            
            <div class="tieba-actions">
              <button class="action-btn" @click.stop="handleQuitTieba(tieba)">
                <span class="action-icon">🚪</span>
                退出
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && userTiebas.length === 0" class="empty-state">
          <div class="empty-icon">🏷️</div>
          <p class="empty-text">暂无贴吧</p>
          <p class="empty-subtext">去发现并加入感兴趣的贴吧吧！</p>
          <button class="discover-tiebas-btn" @click="handleDiscoverTiebas">
            发现贴吧
          </button>
        </div>
      </div>

      <!-- 消息中心 -->
      <div v-if="activeTab === 'messages'" class="tab-content">
        <div class="content-header">
          <h2>消息中心</h2>
          <div class="message-filters">
            <button
              v-for="filter in messageFilters"
              :key="filter.value"
              :class="['filter-btn', { active: messageFilter === filter.value }]"
              @click="messageFilter = filter.value"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        
        <div class="messages-list">
          <div
            v-for="message in filteredMessages"
            :key="message.id"
            class="message-item"
            :class="{ unread: !message.isRead }"
            @click="handleViewMessage(message)"
          >
            <div class="message-avatar">
              <img :src="message.sender.avatar || '/default-avatar.png'" :alt="message.sender.nickname" />
            </div>
            
            <div class="message-content">
              <div class="message-header">
                <span class="sender-name">{{ message.sender.nickname }}</span>
                <span class="message-time">{{ formatTime(message.createTime) }}</span>
              </div>
              
              <div class="message-body">
                <p class="message-preview">{{ message.content }}</p>
              </div>
            </div>
            
            <div class="message-status">
              <span v-if="!message.isRead" class="unread-badge"></span>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && filteredMessages.length === 0" class="empty-state">
          <div class="empty-icon">📨</div>
          <p class="empty-text">暂无消息</p>
          <p class="empty-subtext">还没有收到任何消息</p>
        </div>
      </div>
    </div>

    <!-- 编辑资料模态框 -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>编辑资料</h3>
          <button class="close-btn" @click="showEditModal = false">×</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="handleSaveProfile">
            <div class="form-group">
              <label>昵称</label>
              <input v-model="editForm.nickname" type="text" required />
            </div>
            
            <div class="form-group">
              <label>个人简介</label>
              <textarea v-model="editForm.bio" rows="3" placeholder="介绍一下自己..."></textarea>
            </div>
            
            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="showEditModal = false">取消</button>
              <button type="submit" class="save-btn">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGlobalStore } from '@/stores/global'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const globalStore = useGlobalStore()
const userStore = useUserStore()

// 响应式数据
const activeTab = ref('posts')
const loading = ref(false)
const showEditModal = ref(false)
const postFilter = ref('all')
const messageFilter = ref('all')

// 表单数据
const editForm = ref({
  nickname: '',
  bio: ''
})

// 标签页配置
const tabs = [
  { id: 'posts', label: '我的帖子', icon: '📝' },
  { id: 'replies', label: '我的回复', icon: '💬' },
  { id: 'collections', label: '我的收藏', icon: '⭐' },
  { id: 'tiebas', label: '我的贴吧', icon: '🏷️' },
  { id: 'messages', label: '消息中心', icon: '📨' }
]

// 过滤选项
const postFilters = [
  { value: 'all', label: '全部' },
  { value: 'published', label: '已发布' },
  { value: 'draft', label: '草稿' }
]

const messageFilters = [
  { value: 'all', label: '全部' },
  { value: 'unread', label: '未读' },
  { value: 'system', label: '系统' },
  { value: 'private', label: '私信' }
]

// 模拟数据
const userInfo = computed(() => userStore.userInfo)
const userStats = computed(() => userStore.userStats)

const userPosts = ref([
  {
    id: 1,
    title: 'Vue 3.0 新特性详解',
    content: 'Vue 3.0 带来了很多新特性，包括 Composition API、更好的 TypeScript 支持、性能优化等。',
    tiebaName: '编程',
    createTime: '2023-12-01T10:00:00',
    viewCount: 1234,
    replyCount: 56,
    likeCount: 89,
    status: 'published'
  },
  {
    id: 2,
    title: 'React Hooks 最佳实践',
    content: '分享一些 React Hooks 的使用经验和最佳实践。',
    tiebaName: '前端开发',
    createTime: '2023-11-28T15:30:00',
    viewCount: 567,
    replyCount: 23,
    likeCount: 45,
    status: 'published'
  }
])

const userReplies = ref([
  {
    id: 1,
    postTitle: 'TypeScript 类型系统深入理解',
    content: '感谢分享，类型系统确实很重要！',
    createTime: '2023-11-30T14:20:00',
    likeCount: 5
  }
])

const userCollections = ref([
  {
    id: 1,
    type: 'post',
    title: 'JavaScript 异步编程完全指南',
    source: '编程',
    createTime: '2023-11-25T09:15:00'
  }
])

const userTiebas = ref([
  {
    id: 1,
    name: '编程',
    description: '编程技术交流',
    avatar: '',
    memberCount: 12345,
    postCount: 5678
  }
])

const userMessages = ref([
  {
    id: 1,
    type: 'private',
    sender: {
      id: 2,
      nickname: 'React爱好者',
      avatar: ''
    },
    content: '你好，看了你的帖子很有收获！',
    createTime: '2023-12-01T16:45:00',
    isRead: false
  }
])

// 计算属性
const filteredPosts = computed(() => {
  if (postFilter.value === 'all') return userPosts.value
  return userPosts.value.filter(post => post.status === postFilter.value)
})

const filteredMessages = computed(() => {
  if (messageFilter.value === 'all') return userMessages.value
  if (messageFilter.value === 'unread') return userMessages.value.filter(msg => !msg.isRead)
  return userMessages.value.filter(msg => msg.type === messageFilter.value)
})

// 方法
const handleEditProfile = () => {
  if (!userInfo.value) return
  
  editForm.value = {
    nickname: userInfo.value.nickname || '',
    bio: userInfo.value.bio || ''
  }
  showEditModal.value = true
}

const handleSaveProfile = async () => {
  try {
    // 模拟保存API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 更新用户信息
    if (userInfo.value) {
      userInfo.value.nickname = editForm.value.nickname
      userInfo.value.bio = editForm.value.bio
    }
    
    globalStore.showMessage('资料更新成功', 'success')
    showEditModal.value = false
  } catch (error) {
    globalStore.showMessage('更新失败，请重试', 'error')
  }
}

const handleEditAvatar = () => {
  globalStore.showMessage('头像编辑功能开发中', 'info')
}

const handleSettings = () => {
  router.push('/settings')
}

const handleViewPost = (post: any) => {
  router.push(`/post/${post.id}`)
}

const handleEditPost = (post: any) => {
  globalStore.showMessage('帖子编辑功能开发中', 'info')
}

const handleDeletePost = async (post: any) => {
  if (!confirm('确定要删除这个帖子吗？')) return
  
  try {
    // 模拟删除API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    userPosts.value = userPosts.value.filter(p => p.id !== post.id)
    globalStore.showMessage('帖子删除成功', 'success')
  } catch (error) {
    globalStore.showMessage('删除失败，请重试', 'error')
  }
}

const handleCreatePost = () => {
  router.push('/create-post')
}

const handleViewReplyPost = (reply: any) => {
  // 跳转到对应的帖子
  router.push(`/post/1`) // 这里应该是reply.postId
}

const handleEditReply = (reply: any) => {
  globalStore.showMessage('回复编辑功能开发中', 'info')
}

const handleDeleteReply = async (reply: any) => {
  if (!confirm('确定要删除这个回复吗？')) return
  
  try {
    // 模拟删除API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    userReplies.value = userReplies.value.filter(r => r.id !== reply.id)
    globalStore.showMessage('回复删除成功', 'success')
  } catch (error) {
    globalStore.showMessage('删除失败，请重试', 'error')
  }
}

const handleViewCollection = (collection: any) => {
  if (collection.type === 'post') {
    router.push(`/post/1`) // 这里应该是collection.targetId
  } else {
    router.push(`/tieba/1`) // 这里应该是collection.targetId
  }
}

const handleRemoveCollection = async (collection: any) => {
  if (!confirm('确定要取消收藏吗？')) return
  
  try {
    // 模拟取消收藏API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    userCollections.value = userCollections.value.filter(c => c.id !== collection.id)
    globalStore.showMessage('取消收藏成功', 'success')
  } catch (error) {
    globalStore.showMessage('操作失败，请重试', 'error')
  }
}

const handleViewTieba = (tieba: any) => {
  router.push(`/tieba/${tieba.id}`)
}

const handleQuitTieba = async (tieba: any) => {
  if (!confirm(`确定要退出 ${tieba.name} 吧吗？`)) return
  
  try {
    // 模拟退出贴吧API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    userTiebas.value = userTiebas.value.filter(t => t.id !== tieba.id)
    globalStore.showMessage(`已退出 ${tieba.name} 吧`, 'success')
  } catch (error) {
    globalStore.showMessage('操作失败，请重试', 'error')
  }
}

const handleDiscoverTiebas = () => {
  router.push('/')
}

const handleViewMessage = (message: any) => {
  // 标记为已读
  message.isRead = true
  // 跳转到消息详情或对话页面
  router.push('/messages')
}

const formatTime = (timeStr: string) => {
  const time = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - time.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  
  return time.toLocaleDateString()
}

// 生命周期
onMounted(() => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  // 加载用户数据
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
</script>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 24px;
}

.user-info {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 24px;
  align-items: start;
}

.avatar-section {
  position: relative;
}

.user-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid var(--primary-color);
}

.edit-avatar-btn {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: var(--primary-color);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-icon {
  font-size: 16px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.username {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.user-id {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.user-bio {
  font-size: 16px;
  color: var(--text-primary);
  line-height: 1.5;
  margin: 0;
}

.user-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.edit-profile-btn,
.settings-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 14px;
}

.btn-icon {
  font-size: 16px;
}

.profile-tabs {
  background: var(--bg-secondary);
  border-radius: 12px;
  margin-bottom: 24px;
}

.tabs-container {
  display: flex;
  overflow-x: auto;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  white-space: nowrap;
  border-bottom: 2px solid transparent;
}

.tab-btn.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}

.tab-icon {
  font-size: 18px;
}

.tab-label {
  font-size: 14px;
  font-weight: 600;
}

.profile-content {
  min-height: 400px;
}

.tab-content {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.content-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.filter-options,
.message-filters {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 12px;
}

.filter-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.posts-list,
.replies-list,
.collections-list,
.tiebas-list,
.messages-list {
  display: grid;
  gap: 16px;
}

.post-item,
.reply-item,
.collection-item,
.tieba-item,
.message-item {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.post-item:hover,
.reply-item:hover,
.collection-item:hover,
.tieba-item:hover,
.message-item:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.tieba-name {
  font-size: 12px;
  color: var(--primary-color);
  background: rgba(76, 175, 80, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
}

.post-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.post-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.post-content p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 12px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.stat-icon {
  font-size: 12px;
}

.post-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 12px;
}

.action-btn:hover {
  background: var(--bg-tertiary);
}

.action-btn.delete {
  color: #ff6b6b;
  border-color: #ff6b6b;
}

.action-btn.delete:hover {
  background: rgba(255, 107, 107, 0.1);
}

.action-icon {
  font-size: 12px;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.post-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.reply-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.reply-content p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 8px 0;
}

.reply-stats {
  margin-bottom: 8px;
}

.reply-actions {
  display: flex;
  gap: 8px;
}

.collection-type {
  margin-bottom: 8px;
}

.type-badge {
  font-size: 10px;
  color: var(--primary-color);
  background: rgba(76, 175, 80, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
}

.collection-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.collection-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}

.meta-item {
  font-size: 12px;
  color: var(--text-tertiary);
}

.collection-actions {
  display: flex;
  gap: 8px;
}

.tieba-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
}

.tieba-avatar img {
  width: 60px;
  height: 60px;
  border-radius: 8px;
}

.tieba-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tieba-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.tieba-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tieba-stats {
  display: flex;
  gap: 12px;
}

.tieba-actions {
  display: flex;
  gap: 8px;
}

.message-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: start;
}

.message-item.unread {
  background: rgba(76, 175, 80, 0.05);
}

.message-avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sender-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.message-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.message-preview {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.message-status {
  display: flex;
  align-items: center;
}

.unread-badge {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-color);
}

.loading-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  color: var(--text-secondary);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  margin-bottom: 8px;
}

.empty-subtext {
  font-size: 14px;
  margin-bottom: 16px;
}

.create-post-btn,
.discover-tiebas-btn {
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-secondary);
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90%;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--text-tertiary);
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn,
.save-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.cancel-btn {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.save-btn {
  background: var(--primary-color);
  color: white;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .profile-page {
    padding: 16px;
  }
  
  .profile-header {
    padding: 24px;
  }
  
  .user-info {
    grid-template-columns: 1fr;
    gap: 16px;
    text-align: center;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .action-buttons {
    flex-direction: row;
    justify-content: center;
  }
  
  .tabs-container {
    justify-content: flex-start;
  }
  
  .tab-btn {
    padding: 12px 16px;
  }
  
  .tab-content {
    padding: 16px;
  }
  
  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .filter-options,
  .message-filters {
    align-self: stretch;
    justify-content: center;
  }
  
  .tieba-item {
    grid-template-columns: 1fr;
    gap: 12px;
    text-align: center;
  }
  
  .message-item {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .modal-content {
    width: 95%;
    margin: 20px;
  }
}
</style>
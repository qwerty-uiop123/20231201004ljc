<template>
  <div class="messages-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">消息中心</h1>
      <div class="header-actions">
        <button class="action-btn" @click="handleMarkAllRead">
          <span class="action-icon">📨</span>
          标记全部已读
        </button>
        <button class="action-btn" @click="handleClearAll">
          <span class="action-icon">🗑️</span>
          清空消息
        </button>
      </div>
    </div>

    <!-- 消息类型筛选 -->
    <div class="message-filters">
      <div class="filter-tabs">
        <button
          v-for="tab in messageTabs"
          :key="tab.value"
          :class="['filter-tab', { active: activeTab === tab.value }]"
          @click="activeTab = tab.value"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.label }}</span>
          <span v-if="tab.count > 0" class="tab-count">{{ tab.count }}</span>
        </button>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="messages-container">
      <!-- 私信列表 -->
      <div v-if="activeTab === 'private'" class="messages-section">
        <div class="section-header">
          <h2 class="section-title">私信</h2>
          <div class="section-actions">
            <button class="new-message-btn" @click="handleNewMessage">
              <span class="btn-icon">✉️</span>
              新消息
            </button>
          </div>
        </div>
        
        <div class="conversations-list">
          <div
            v-for="conversation in filteredConversations"
            :key="conversation.id"
            class="conversation-item"
            :class="{ unread: conversation.unreadCount > 0 }"
            @click="handleOpenConversation(conversation)"
          >
            <div class="conversation-avatar">
              <img :src="conversation.user.avatar || '/default-avatar.png'" :alt="conversation.user.nickname" />
              <span v-if="conversation.unreadCount > 0" class="unread-badge">{{ conversation.unreadCount }}</span>
            </div>
            
            <div class="conversation-content">
              <div class="conversation-header">
                <span class="user-name">{{ conversation.user.nickname }}</span>
                <span class="last-time">{{ formatTime(conversation.lastMessageTime) }}</span>
              </div>
              
              <div class="conversation-preview">
                <p class="preview-text">{{ conversation.lastMessage }}</p>
              </div>
            </div>
            
            <div class="conversation-actions">
              <button class="action-btn small" @click.stop="handleDeleteConversation(conversation)">
                <span class="action-icon">🗑️</span>
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && filteredConversations.length === 0" class="empty-state">
          <div class="empty-icon">💬</div>
          <p class="empty-text">暂无私信</p>
          <p class="empty-subtext">还没有收到任何私信</p>
          <button class="new-message-btn" @click="handleNewMessage">
            发送新消息
          </button>
        </div>
      </div>

      <!-- 系统消息 -->
      <div v-if="activeTab === 'system'" class="messages-section">
        <div class="section-header">
          <h2 class="section-title">系统消息</h2>
        </div>
        
        <div class="system-messages-list">
          <div
            v-for="message in filteredSystemMessages"
            :key="message.id"
            class="system-message-item"
            :class="{ unread: !message.isRead }"
            @click="handleViewSystemMessage(message)"
          >
            <div class="message-icon">
              <span class="icon">📢</span>
            </div>
            
            <div class="message-content">
              <div class="message-header">
                <span class="message-title">{{ message.title }}</span>
                <span class="message-time">{{ formatTime(message.createTime) }}</span>
              </div>
              
              <div class="message-body">
                <p class="message-text">{{ message.content }}</p>
              </div>
            </div>
            
            <div class="message-status">
              <span v-if="!message.isRead" class="unread-dot"></span>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && filteredSystemMessages.length === 0" class="empty-state">
          <div class="empty-icon">📢</div>
          <p class="empty-text">暂无系统消息</p>
          <p class="empty-subtext">还没有收到系统消息</p>
        </div>
      </div>

      <!-- 通知消息 -->
      <div v-if="activeTab === 'notification'" class="messages-section">
        <div class="section-header">
          <h2 class="section-title">通知</h2>
        </div>
        
        <div class="notifications-list">
          <div
            v-for="notification in filteredNotifications"
            :key="notification.id"
            class="notification-item"
            :class="{ unread: !notification.isRead }"
            @click="handleViewNotification(notification)"
          >
            <div class="notification-icon">
              <span class="icon">{{ getNotificationIcon(notification.type) }}</span>
            </div>
            
            <div class="notification-content">
              <div class="notification-header">
                <span class="notification-title">{{ notification.title }}</span>
                <span class="notification-time">{{ formatTime(notification.createTime) }}</span>
              </div>
              
              <div class="notification-body">
                <p class="notification-text">{{ notification.content }}</p>
              </div>
              
              <div v-if="notification.relatedPost" class="notification-source">
                <span class="source-label">来自：</span>
                <span class="source-text">{{ notification.relatedPost.title }}</span>
              </div>
            </div>
            
            <div class="notification-status">
              <span v-if="!notification.isRead" class="unread-dot"></span>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && filteredNotifications.length === 0" class="empty-state">
          <div class="empty-icon">🔔</div>
          <p class="empty-text">暂无通知</p>
          <p class="empty-subtext">还没有收到任何通知</p>
        </div>
      </div>

      <!-- 对话详情 -->
      <div v-if="activeTab === 'conversation' && activeConversation" class="conversation-section">
        <div class="conversation-header">
          <button class="back-btn" @click="activeTab = 'private'">
            <span class="back-icon">←</span>
            返回
          </button>
          
          <div class="conversation-user">
            <img :src="activeConversation.user.avatar || '/default-avatar.png'" :alt="activeConversation.user.nickname" />
            <span class="user-name">{{ activeConversation.user.nickname }}</span>
          </div>
          
          <div class="conversation-actions">
            <button class="action-btn" @click="handleDeleteConversation(activeConversation)">
              <span class="action-icon">🗑️</span>
              删除对话
            </button>
          </div>
        </div>
        
        <div class="messages-list">
          <div
            v-for="message in conversationMessages"
            :key="message.id"
            class="message-item"
            :class="{ own: message.isOwn, unread: !message.isRead && !message.isOwn }"
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
                <p class="message-text">{{ message.content }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="message-input-section">
          <div class="message-input">
            <textarea
              v-model="newMessage"
              placeholder="输入消息..."
              rows="3"
              class="message-textarea"
            ></textarea>
            
            <div class="input-actions">
              <button class="send-btn" @click="handleSendMessage" :disabled="!canSendMessage">
                <span class="send-icon">📤</span>
                发送
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新消息模态框 -->
    <div v-if="showNewMessageModal" class="modal-overlay" @click="showNewMessageModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>发送新消息</h3>
          <button class="close-btn" @click="showNewMessageModal = false">×</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>收件人</label>
            <input v-model="newMessageRecipient" type="text" placeholder="输入用户名或ID" />
          </div>
          
          <div class="form-group">
            <label>消息内容</label>
            <textarea v-model="newMessageContent" rows="4" placeholder="输入消息内容..."></textarea>
          </div>
          
          <div class="form-actions">
            <button class="cancel-btn" @click="showNewMessageModal = false">取消</button>
            <button class="send-btn" @click="handleSendNewMessage" :disabled="!canSendNewMessage">发送</button>
          </div>
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
import { messageApi } from '@/services/message'

const router = useRouter()
const globalStore = useGlobalStore()
const userStore = useUserStore()

// 响应式数据
const activeTab = ref('private')
const loading = ref(false)
const showNewMessageModal = ref(false)
const activeConversation = ref<any>(null)
const newMessage = ref('')
const newMessageRecipient = ref('')
const newMessageContent = ref('')

// 消息类型标签页
const messageTabs = computed(() => [
  {
    value: 'private',
    label: '私信',
    icon: '💬',
    count: conversations.value.filter(c => c.unreadCount > 0).length
  },
  {
    value: 'system',
    label: '系统消息',
    icon: '📢',
    count: systemMessages.value.filter(m => !m.isRead).length
  },
  {
    value: 'notification',
    label: '通知',
    icon: '🔔',
    count: notifications.value.filter(n => !n.isRead).length
  }
])

// 真实数据
const conversations = ref([])
const systemMessages = ref([])
const notifications = ref([])

const conversationMessages = ref([
  {
    id: 1,
    sender: {
      id: 2,
      nickname: 'React爱好者',
      avatar: ''
    },
    content: '你好，看了你的帖子很有收获！',
    createTime: '2023-12-01T16:45:00',
    isRead: true,
    isOwn: false
  },
  {
    id: 2,
    sender: {
      id: userStore.userInfo?.id,
      nickname: userStore.userInfo?.nickname,
      avatar: userStore.userInfo?.avatar
    },
    content: '谢谢！很高兴对你有帮助。',
    createTime: '2023-12-01T16:50:00',
    isRead: true,
    isOwn: true
  },
  {
    id: 3,
    sender: {
      id: 2,
      nickname: 'React爱好者',
      avatar: ''
    },
    content: '你对React和Vue的比较有什么看法？',
    createTime: '2023-12-01T16:55:00',
    isRead: false,
    isOwn: false
  }
])

// 计算属性
const filteredConversations = computed(() => {
  return conversations.value
})

const filteredSystemMessages = computed(() => {
  return systemMessages.value
})

const filteredNotifications = computed(() => {
  return notifications.value
})

const canSendMessage = computed(() => {
  return newMessage.value.trim() && userStore.isLoggedIn
})

const canSendNewMessage = computed(() => {
  return newMessageRecipient.value.trim() && newMessageContent.value.trim() && userStore.isLoggedIn
})

// 数据加载方法
const loadConversations = async () => {
  try {
    loading.value = true
    const response = await messageApi.getConversations()
    conversations.value = response.data || []
  } catch (error) {
    console.error('加载对话列表失败:', error)
    globalStore.showMessage('加载对话列表失败', 'error')
  } finally {
    loading.value = false
  }
}

const loadSystemMessages = async () => {
  try {
    const response = await messageApi.getNotifications({ unread_only: false })
    systemMessages.value = response.data || []
  } catch (error) {
    console.error('加载系统消息失败:', error)
  }
}

// 方法
const handleMarkAllRead = async () => {
  try {
    await messageApi.markAllNotificationsAsRead()
    
    // 重新加载数据
    await loadConversations()
    await loadSystemMessages()
    
    globalStore.showMessage('已标记全部消息为已读', 'success')
  } catch (error) {
    globalStore.showMessage('操作失败，请重试', 'error')
  }
}

const handleClearAll = async () => {
  if (!confirm('确定要清空所有消息吗？此操作不可撤销。')) return
  
  try {
    // 注意：实际项目中通常不会提供清空所有消息的API
    // 这里只是演示，实际应该逐个删除
    conversations.value = []
    systemMessages.value = []
    notifications.value = []
    
    globalStore.showMessage('消息已清空', 'success')
  } catch (error) {
    globalStore.showMessage('操作失败，请重试', 'error')
  }
}

const handleNewMessage = () => {
  if (!userStore.isLoggedIn) {
    globalStore.showMessage('请先登录', 'warning')
    router.push('/login')
    return
  }
  
  showNewMessageModal.value = true
}

const handleOpenConversation = async (conversation: any) => {
  try {
    // 获取对话详情和消息列表
    const [conversationDetail, messagesResponse] = await Promise.all([
      messageApi.getConversation(conversation.id),
      messageApi.getMessages(conversation.id)
    ])
    
    activeConversation.value = conversationDetail.data
    conversationMessages.value = messagesResponse.data || []
    activeTab.value = 'conversation'
    
    // 标记对话为已读
    await messageApi.markAsRead(conversation.id)
    
    // 更新对话列表中的未读状态
    conversation.unreadCount = 0
  } catch (error) {
    console.error('打开对话失败:', error)
    globalStore.showMessage('打开对话失败', 'error')
  }
}

const handleDeleteConversation = async (conversation: any) => {
  if (!confirm('确定要删除这个对话吗？')) return
  
  try {
    await messageApi.deleteMessage(conversation.id)
    
    conversations.value = conversations.value.filter(conv => conv.id !== conversation.id)
    
    if (activeConversation.value?.id === conversation.id) {
      activeTab.value = 'private'
      activeConversation.value = null
    }
    
    globalStore.showMessage('对话已删除', 'success')
  } catch (error) {
    globalStore.showMessage('删除失败，请重试', 'error')
  }
}

const handleViewSystemMessage = (message: any) => {
  message.isRead = true
  // 可以跳转到系统消息详情页面
  globalStore.showMessage('系统消息详情功能开发中', 'info')
}

const handleViewNotification = (notification: any) => {
  notification.isRead = true
  
  // 跳转到相关帖子
  if (notification.relatedPost) {
    router.push(`/post/${notification.relatedPost.id}`)
  }
}

const handleSendMessage = async () => {
  if (!canSendMessage.value || !activeConversation.value) return
  
  try {
    const response = await messageApi.sendMessage({
      conversation_id: activeConversation.value.id,
      content: newMessage.value
    })
    
    const newMsg = {
      id: response.data.id,
      sender: {
        id: userStore.userInfo?.id,
        nickname: userStore.userInfo?.nickname,
        avatar: userStore.userInfo?.avatar
      },
      content: newMessage.value,
      createTime: new Date().toISOString(),
      isRead: true,
      isOwn: true
    }
    
    conversationMessages.value.push(newMsg)
    
    // 更新对话的最后消息
    activeConversation.value.lastMessage = newMessage.value
    activeConversation.value.lastMessageTime = newMsg.createTime
    
    newMessage.value = ''
    
    // 自动滚动到底部
    setTimeout(() => {
      const messagesList = document.querySelector('.messages-list')
      if (messagesList) {
        messagesList.scrollTop = messagesList.scrollHeight
      }
    }, 100)
  } catch (error) {
    globalStore.showMessage('发送失败，请重试', 'error')
  }
}

const handleSendNewMessage = async () => {
  if (!canSendNewMessage.value) return
  
  try {
    // 发送私信（后端会自动创建对话）
    const response = await messageApi.sendDirectMessage({
      recipient_id: parseInt(newMessageRecipient.value),
      content: newMessageContent.value,
      message_type: 'text'
    })
    
    // 重新加载对话列表
    await loadConversations()
    
    showNewMessageModal.value = false
    newMessageRecipient.value = ''
    newMessageContent.value = ''
    
    globalStore.showMessage('消息发送成功', 'success')
  } catch (error) {
    console.error('发送私信失败:', error)
    globalStore.showMessage('发送失败，请重试', 'error')
  }
}

const getNotificationIcon = (type: string) => {
  const icons: Record<string, string> = {
    like: '👍',
    reply: '💬',
    follow: '👤',
    system: '📢'
  }
  return icons[type] || '🔔'
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
onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  // 加载消息数据
  loading.value = true
  try {
    await Promise.all([
      loadConversations(),
      loadSystemMessages()
    ])
  } catch (error) {
    console.error('加载消息数据失败:', error)
    globalStore.showMessage('加载消息数据失败', 'error')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.messages-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 14px;
}

.action-btn:hover {
  background: var(--bg-tertiary);
}

.action-icon {
  font-size: 16px;
}

.message-filters {
  background: var(--bg-secondary);
  border-radius: 12px;
  margin-bottom: 24px;
}

.filter-tabs {
  display: flex;
  overflow-x: auto;
}

.filter-tab {
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

.filter-tab.active {
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

.tab-count {
  background: var(--primary-color);
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 12px;
  min-width: 20px;
  text-align: center;
}

.messages-container {
  min-height: 600px;
}

.messages-section,
.conversation-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-actions {
  display: flex;
  gap: 12px;
}

.new-message-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.btn-icon {
  font-size: 16px;
}

.conversations-list,
.system-messages-list,
.notifications-list {
  display: grid;
  gap: 12px;
}

.conversation-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  padding: 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.conversation-item:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.conversation-item.unread {
  background: rgba(76, 175, 80, 0.05);
}

.conversation-avatar {
  position: relative;
}

.conversation-avatar img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.unread-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
}

.conversation-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.last-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.preview-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.conversation-actions {
  display: flex;
  align-items: center;
}

.action-btn.small {
  padding: 6px;
  border: none;
  background: transparent;
  color: var(--text-tertiary);
}

.action-btn.small:hover {
  color: var(--text-secondary);
}

.system-message-item,
.notification-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  padding: 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.system-message-item:hover,
.notification-item:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.system-message-item.unread,
.notification-item.unread {
  background: rgba(76, 175, 80, 0.05);
}

.message-icon,
.notification-icon {
  display: flex;
  align-items: center;
}

.icon {
  font-size: 24px;
}

.message-content,
.notification-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-header,
.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-title,
.notification-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.message-time,
.notification-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.message-text,
.notification-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
}

.notification-source {
  font-size: 12px;
  color: var(--text-tertiary);
}

.source-label {
  font-weight: 600;
}

.message-status,
.notification-status {
  display: flex;
  align-items: center;
}

.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-color);
}

.conversation-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 14px;
}

.back-icon {
  font-size: 16px;
}

.conversation-user {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.conversation-user img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.messages-list {
  max-height: 400px;
  overflow-y: auto;padding: 16px;
  margin-bottom: 20px;
}

.message-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.message-item.own {
  grid-template-columns: 1fr auto;
}

.message-item.own .message-content {
  order: -1;
}

.message-avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.message-content {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 12px 16px;
}

.message-item.own .message-content {
  background: var(--primary-color);
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.sender-name {
  font-size: 14px;
  font-weight: 600;
}

.message-item.own .sender-name {
  color: rgba(255, 255, 255, 0.9);
}

.message-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.message-item.own .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.message-text {
  font-size: 14px;
  line-height: 1.4;
  margin: 0;
}

.message-input-section {
  border-top: 1px solid var(--border-color);
  padding-top: 20px;
}

.message-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
  resize: vertical;
  min-height: 80px;
}

.message-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.input-actions {
  display: flex;
  justify-content: flex-end;
}

.send-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.send-btn:disabled {
  background: var(--text-tertiary);
  cursor: not-allowed;
}

.send-icon {
  font-size: 16px;
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
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 0;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
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
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
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
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn {
  padding: 8px 20px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 14px;
}

.cancel-btn:hover {
  background: var(--bg-tertiary);
}

.loading-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  opacity: 0.5;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.empty-subtext {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .messages-page {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .filter-tabs {
    justify-content: space-between;
  }
  
  .filter-tab {
    flex: 1;
    justify-content: center;
    padding: 12px 16px;
  }
  
  .conversation-item {
    grid-template-columns: auto 1fr;
    gap: 12px;
  }
  
  .conversation-actions {
    display: none;
  }
  
  .conversation-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .modal-content {
    width: 95%;
    margin: 20px;
  }
}

@media (max-width: 480px) {
  .messages-page {
    padding: 12px;
  }
  
  .messages-section,
  .conversation-section {
    padding: 16px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .section-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .conversation-avatar img {
    width: 40px;
    height: 40px;
  }
  
  .message-avatar img {
    width: 32px;
    height: 32px;
  }
}
</style>
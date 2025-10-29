import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { MessageInfo, PrivateMessage, Conversation, MessageStats, SendMessageForm } from '@/types/message'
import { messageApi } from '@/services/message'
import { useGlobalStore } from '@/stores/global'

export const useMessageStore = defineStore('message', () => {
  // 消息列表
  const messages = ref<MessageInfo[]>([])
  
  // 私信列表
  const privateMessages = ref<PrivateMessage[]>([])
  
  // 会话列表
  const conversations = ref<Conversation[]>([])
  
  // 当前会话
  const currentConversation = ref<Conversation | null>(null)
  
  // 消息统计
  const messageStats = ref<MessageStats>({
    unreadCount: 0,
    unreadSystem: 0,
    unreadReply: 0,
    unreadLike: 0,
    unreadFollow: 0,
    unreadMention: 0,
    unreadPrivate: 0
  })
  
  // 加载状态
  const loading = ref(false)
  
  // 全局store
  const globalStore = useGlobalStore()
  
  // 计算未读消息总数
  const totalUnread = computed(() => {
    return messages.value.filter(msg => !msg.isRead).length +
           privateMessages.value.filter(msg => !msg.isRead).length
  })
  
  // 获取消息列表
  const getMessages = async (type?: string, page = 1, pageSize = 20) => {
    loading.value = true
    globalStore.setLoading(true)
    try {
      const response = await messageApi.getNotifications({
        page,
        page_size: pageSize,
        unread_only: type === 'unread'
      })
      
      if (response.data) {
        const apiMessages = response.data.results || response.data
        const formattedMessages = apiMessages.map((msg: any) => ({
          id: msg.id,
          type: msg.message_type || 'system',
          title: msg.title || `${msg.message_type}消息`,
          content: msg.content,
          sender: {
            id: msg.sender?.id || 0,
            username: msg.sender?.username || 'system',
            nickname: msg.sender?.nickname || '系统',
            avatar: msg.sender?.avatar || '',
            level: msg.sender?.level || 1
          },
          targetId: msg.target_id,
          targetType: msg.target_type,
          targetTitle: msg.target_title,
          createTime: msg.created_at || msg.create_time,
          isRead: msg.is_read || false,
          link: msg.link || '/'
        }))
        
        if (page === 1) {
          messages.value = formattedMessages
        } else {
          messages.value.push(...formattedMessages)
        }
        updateMessageStats()
        return { 
          success: true, 
          data: formattedMessages, 
          hasMore: response.data.next !== null 
        }
      } else {
        globalStore.showMessage('获取消息失败', 'error')
        return { success: false, message: '获取消息失败' }
      }
    } catch (error: any) {
      console.error('获取消息失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '获取消息失败'
      globalStore.showMessage(errorMessage, 'error')
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
      globalStore.setLoading(false)
    }
  }
  
  // 获取私信列表
  const getPrivateMessages = async (conversationId?: number, page = 1, pageSize = 20) => {
    loading.value = true
    globalStore.setLoading(true)
    try {
      if (!conversationId) {
        globalStore.showMessage('请先选择会话', 'warning')
        return { success: false, message: '请先选择会话' }
      }
      
      const response = await messageApi.getMessages(conversationId, {
        page,
        page_size: pageSize
      })
      
      if (response.data) {
        const apiMessages = response.data.results || response.data
        const formattedMessages = apiMessages.map((msg: any) => ({
          id: msg.id,
          sender: {
            id: msg.sender?.id,
            username: msg.sender?.username,
            nickname: msg.sender?.nickname,
            avatar: msg.sender?.avatar || '',
            level: msg.sender?.level || 1
          },
          receiver: {
            id: msg.receiver?.id,
            username: msg.receiver?.username,
            nickname: msg.receiver?.nickname,
            avatar: msg.receiver?.avatar || '',
            level: msg.receiver?.level || 1
          },
          content: msg.content,
          createTime: msg.created_at || msg.create_time,
          isRead: msg.is_read || false,
          conversationId: msg.conversation_id || conversationId,
          messageType: msg.message_type || 'text'
        }))
        
        if (page === 1) {
          privateMessages.value = formattedMessages
        } else {
          privateMessages.value.push(...formattedMessages)
        }
        updateMessageStats()
        return { 
          success: true, 
          data: formattedMessages, 
          hasMore: response.data.next !== null 
        }
      } else {
        globalStore.showMessage('获取私信失败', 'error')
        return { success: false, message: '获取私信失败' }
      }
    } catch (error: any) {
      console.error('获取私信失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '获取私信失败'
      globalStore.showMessage(errorMessage, 'error')
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
      globalStore.setLoading(false)
    }
  }
  
  // 获取会话列表
  const getConversations = async () => {
    loading.value = true
    globalStore.setLoading(true)
    try {
      const response = await messageApi.getConversations()
      
      if (response.data) {
        const apiConversations = response.data.results || response.data
        const formattedConversations = apiConversations.map((conv: any) => ({
          id: conv.id,
          participants: conv.participants?.map((p: any) => ({
            id: p.id,
            username: p.username,
            nickname: p.nickname,
            avatar: p.avatar || '',
            level: p.level || 1
          })) || [],
          lastMessage: conv.last_message ? {
            id: conv.last_message.id,
            sender: {
              id: conv.last_message.sender?.id,
              username: conv.last_message.sender?.username,
              nickname: conv.last_message.sender?.nickname,
              avatar: conv.last_message.sender?.avatar || '',
              level: conv.last_message.sender?.level || 1
            },
            receiver: {
              id: conv.last_message.receiver?.id,
              username: conv.last_message.receiver?.username,
              nickname: conv.last_message.receiver?.nickname,
              avatar: conv.last_message.receiver?.avatar || '',
              level: conv.last_message.receiver?.level || 1
            },
            content: conv.last_message.content,
            createTime: conv.last_message.created_at || conv.last_message.create_time,
            isRead: conv.last_message.is_read || false,
            conversationId: conv.last_message.conversation_id || conv.id
          } : null,
          unreadCount: conv.unread_count || 0,
          createTime: conv.created_at || conv.create_time,
          updateTime: conv.updated_at || conv.update_time
        }))
        
        conversations.value = formattedConversations
        return { success: true, data: formattedConversations }
      } else {
        globalStore.showMessage('获取会话列表失败', 'error')
        return { success: false, message: '获取会话列表失败' }
      }
    } catch (error: any) {
      console.error('获取会话列表失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '获取会话列表失败'
      globalStore.showMessage(errorMessage, 'error')
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
      globalStore.setLoading(false)
    }
  }
  
  // 发送私信
  const sendPrivateMessage = async (form: SendMessageForm) => {
    try {
      if (!form.conversationId) {
        // 如果没有会话ID，先创建会话
        const createResponse = await messageApi.createConversation(form.receiverId)
        if (createResponse.data) {
          form.conversationId = createResponse.data.id
        } else {
          globalStore.showMessage('创建会话失败', 'error')
          return { success: false, message: '创建会话失败' }
        }
      }
      
      const response = await messageApi.sendMessage(form.conversationId!, {
        content: form.content,
        message_type: 'text'
      })
      
      if (response.data) {
        const newMessage = {
          id: response.data.id,
          sender: {
            id: response.data.sender?.id,
            username: response.data.sender?.username,
            nickname: response.data.sender?.nickname,
            avatar: response.data.sender?.avatar || '',
            level: response.data.sender?.level || 1
          },
          receiver: {
            id: response.data.receiver?.id,
            username: response.data.receiver?.username,
            nickname: response.data.receiver?.nickname,
            avatar: response.data.receiver?.avatar || '',
            level: response.data.receiver?.level || 1
          },
          content: response.data.content,
          createTime: response.data.created_at || response.data.create_time,
          isRead: response.data.is_read || false,
          conversationId: response.data.conversation_id || form.conversationId
        }
        
        privateMessages.value.unshift(newMessage)
        globalStore.showMessage('发送成功', 'success')
        return { success: true, data: newMessage }
      } else {
        globalStore.showMessage('发送私信失败', 'error')
        return { success: false, message: '发送私信失败' }
      }
    } catch (error: any) {
      console.error('发送私信失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '发送私信失败'
      globalStore.showMessage(errorMessage, 'error')
      return { success: false, message: errorMessage }
    }
  }
  
  // 标记消息为已读
  const markAsRead = async (messageIds: number[]) => {
    try {
      const promises = messageIds.map(id => messageApi.markAsRead(id))
      await Promise.all(promises)
      
      // 更新消息状态
      messages.value.forEach(msg => {
        if (messageIds.includes(msg.id)) {
          msg.isRead = true
        }
      })
      privateMessages.value.forEach(msg => {
        if (messageIds.includes(msg.id)) {
          msg.isRead = true
        }
      })
      updateMessageStats()
      globalStore.showMessage('标记已读成功', 'success')
      return { success: true }
    } catch (error: any) {
      console.error('标记已读失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '标记已读失败'
      globalStore.showMessage(errorMessage, 'error')
      return { success: false, message: errorMessage }
    }
  }
  
  // 标记所有消息为已读
  const markAllAsRead = async () => {
    try {
      await messageApi.markAllNotificationsAsRead()
      
      // 更新所有消息状态
      messages.value.forEach(msg => {
        msg.isRead = true
      })
      privateMessages.value.forEach(msg => {
        msg.isRead = true
      })
      updateMessageStats()
      globalStore.showMessage('全部标记已读成功', 'success')
      return { success: true }
    } catch (error: any) {
      console.error('标记所有已读失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '标记所有已读失败'
      globalStore.showMessage(errorMessage, 'error')
      return { success: false, message: errorMessage }
    }
  }
  
  // 删除消息
  const deleteMessage = async (messageId: number) => {
    try {
      await messageApi.deleteMessage(messageId)
      
      // 从消息列表中移除
      messages.value = messages.value.filter(msg => msg.id !== messageId)
      privateMessages.value = privateMessages.value.filter(msg => msg.id !== messageId)
      updateMessageStats()
      globalStore.showMessage('删除消息成功', 'success')
      return { success: true }
    } catch (error: any) {
      console.error('删除消息失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '删除消息失败'
      globalStore.showMessage(errorMessage, 'error')
      return { success: false, message: errorMessage }
    }
  }
  
  // 更新消息统计
  const updateMessageStats = () => {
    const stats = {
      unreadSystem: messages.value.filter(msg => msg.type === 'system' && !msg.isRead).length,
      unreadReply: messages.value.filter(msg => msg.type === 'reply' && !msg.isRead).length,
      unreadLike: messages.value.filter(msg => msg.type === 'like' && !msg.isRead).length,
      unreadFollow: messages.value.filter(msg => msg.type === 'follow' && !msg.isRead).length,
      unreadMention: messages.value.filter(msg => msg.type === 'mention' && !msg.isRead).length,
      unreadPrivate: privateMessages.value.filter(msg => !msg.isRead).length
    }
    
    messageStats.value = {
      ...stats,
      unreadCount: Object.values(stats).reduce((sum, count) => sum + count, 0)
    }
  }
  
  return {
    messages,
    privateMessages,
    conversations,
    currentConversation,
    messageStats,
    totalUnread,
    loading,
    getMessages,
    getPrivateMessages,
    getConversations,
    sendPrivateMessage,
    markAsRead,
    markAllAsRead,
    deleteMessage,
    updateMessageStats
  }
})
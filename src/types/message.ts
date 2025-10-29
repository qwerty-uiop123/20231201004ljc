// 消息相关类型定义

export interface MessageInfo {
  id: number
  type: 'system' | 'reply' | 'like' | 'follow' | 'mention' | 'private'
  title: string
  content: string
  sender?: MessageSender
  targetId?: number
  targetType?: string
  targetTitle?: string
  createTime: string
  isRead: boolean
  link?: string
}

export interface MessageSender {
  id: number
  username: string
  nickname: string
  avatar: string
  level: number
}

export interface PrivateMessage {
  id: number
  sender: MessageSender
  receiver: MessageSender
  content: string
  createTime: string
  isRead: boolean
  conversationId: number
}

export interface Conversation {
  id: number
  participants: MessageSender[]
  lastMessage: PrivateMessage
  unreadCount: number
  createTime: string
  updateTime: string
}

export interface MessageStats {
  unreadCount: number
  unreadSystem: number
  unreadReply: number
  unreadLike: number
  unreadFollow: number
  unreadMention: number
  unreadPrivate: number
}

export interface SendMessageForm {
  receiverId: number
  content: string
  type?: 'text' | 'image' | 'file'
}

export interface MarkAsReadParams {
  messageIds?: number[]
  type?: string
  all?: boolean
}
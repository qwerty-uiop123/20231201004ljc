// 用户相关类型定义

export interface UserInfo {
  id: number
  username: string
  nickname: string
  avatar: string
  level: number
  joinDate: string
  token: string
  email?: string
  phone?: string
  bio?: string
  location?: string
  website?: string
  followers?: number
  following?: number
  posts?: number
  likes?: number
}

export interface LoginForm {
  username: string
  password: string
  remember?: boolean
}

export interface RegisterForm {
  username: string
  password: string
  email: string
  nickname?: string
  agreeTerms?: boolean
}

export interface UserSettings {
  theme: 'light' | 'dark'
  notification: boolean
  privacy: 'public' | 'private'
  language: string
  autoPlayVideo?: boolean
  showNSFW?: boolean
  emailNotification?: boolean
  pushNotification?: boolean
}

export interface UserStats {
  posts: number
  likes: number
  followers: number
  following: number
  tiebas: number
  daysActive: number
  reputation: number
}

export interface UserActivity {
  id: number
  type: 'post' | 'comment' | 'like' | 'follow' | 'join'
  targetId: number
  targetType: string
  targetTitle?: string
  timestamp: string
  tiebaName?: string
}
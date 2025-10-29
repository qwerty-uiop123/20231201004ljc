// 贴吧相关类型定义

export interface TiebaInfo {
  id: number
  name: string
  displayName: string
  avatar: string
  description: string
  memberCount: number
  postCount: number
  todayPostCount: number
  onlineCount: number
  createTime: string
  category: string
  tags: string[]
  isOfficial: boolean
  isHot: boolean
  isJoined: boolean
  moderators: TiebaModerator[]
  rules?: string
  announcement?: string
}

export interface TiebaModerator {
  id: number
  username: string
  nickname: string
  avatar: string
  level: number
  role: 'owner' | 'admin' | 'moderator'
}

export interface PostInfo {
  id: number
  title: string
  content: string
  author: PostAuthor
  tiebaId: number
  tiebaName: string
  createTime: string
  updateTime: string
  viewCount: number
  replyCount: number
  likeCount: number
  isTop: boolean
  isEssence: boolean
  isLiked: boolean
  isCollected: boolean
  images?: string[]
  videos?: string[]
  tags?: string[]
  lastReply?: PostReply
}

export interface PostAuthor {
  id: number
  username: string
  nickname: string
  avatar: string
  level: number
  isOfficial?: boolean
  isModerator?: boolean
}

export interface PostReply {
  id: number
  content: string
  author: PostAuthor
  createTime: string
  likeCount: number
  replyCount: number
}

export interface PostDetail extends PostInfo {
  replies: PostReply[]
  totalReplies: number
  currentPage: number
  totalPages: number
}

export interface CreatePostForm {
  tiebaId: number
  title: string
  content: string
  images?: File[]
  tags?: string[]
  isAnonymous?: boolean
}

export interface CreateReplyForm {
  postId: number
  content: string
  replyTo?: number
  images?: File[]
  isAnonymous?: boolean
}

export interface TiebaCategory {
  id: number
  name: string
  icon: string
  tiebas: TiebaInfo[]
}

export interface SearchTiebaParams {
  keyword: string
  category?: string
  sortBy?: 'member' | 'post' | 'time'
  page?: number
  pageSize?: number
}

export interface SearchPostParams {
  keyword: string
  tiebaId?: number
  authorId?: number
  sortBy?: 'time' | 'hot' | 'reply'
  timeRange?: 'all' | 'day' | 'week' | 'month'
  page?: number
  pageSize?: number
}
<template>
  <div class="post-detail-page">
    <!-- 帖子内容 -->
    <div class="post-content-section">
      <div class="post-header">
        <div class="post-meta">
          <div class="author-info">
            <img :src="postDetail?.author.avatar || '/default-avatar.png'" :alt="postDetail?.author.nickname" />
            <div class="author-details">
              <span class="author-name">{{ postDetail?.author.nickname }}</span>
              <span class="post-time">{{ formatTime(postDetail?.createTime) }}</span>
            </div>
          </div>
          <div class="post-badges">
            <span v-if="postDetail?.isTop" class="badge top">置顶</span>
            <span v-if="postDetail?.isEssence" class="badge essence">精华</span>
          </div>
        </div>
        
        <h1 class="post-title">{{ postDetail?.title }}</h1>
        
        <div class="post-stats">
          <span class="stat-item">
            <strong>{{ postDetail?.viewCount }}</strong> 浏览
          </span>
          <span class="stat-item">
            <strong>{{ postDetail?.replyCount }}</strong> 回复
          </span>
          <span class="stat-item">
            <strong>{{ postDetail?.likeCount }}</strong> 点赞
          </span>
        </div>
      </div>
      
      <div class="post-body">
        <div class="post-text">
          <p>{{ postDetail?.content }}</p>
        </div>
        
        <div v-if="postDetail?.images && postDetail.images.length > 0" class="post-images">
          <div class="images-grid">
            <img
              v-for="(image, index) in postDetail.images"
              :key="index"
              :src="image"
              :alt="`帖子图片 ${index + 1}`"
              class="post-image"
              @click="handleImageClick(image)"
            />
          </div>
        </div>
      </div>
      
      <div class="post-actions">
        <button
          :class="['action-btn', 'like-btn', { liked: postDetail?.isLiked }]"
          @click="handleLikePost"
        >
          <span class="action-icon">👍</span>
          <span class="action-text">点赞</span>
          <span class="action-count">{{ postDetail?.likeCount }}</span>
        </button>
        
        <button
          :class="['action-btn', 'collect-btn', { collected: postDetail?.isCollected }]"
          @click="handleCollectPost"
        >
          <span class="action-icon">⭐</span>
          <span class="action-text">收藏</span>
        </button>
        
        <button class="action-btn share-btn" @click="handleSharePost">
          <span class="action-icon">📤</span>
          <span class="action-text">分享</span>
        </button>
        
        <button class="action-btn reply-btn" @click="scrollToReply">
          <span class="action-icon">💬</span>
          <span class="action-text">回复</span>
        </button>
      </div>
    </div>

    <!-- 回复列表 -->
    <div class="replies-section">
      <div class="section-header">
        <h2 class="section-title">
          回复
          <span class="reply-count">({{ postDetail?.replyCount || 0 }})</span>
        </h2>
        <div class="sort-options">
          <button
            v-for="sort in sortOptions"
            :key="sort.value"
            :class="['sort-btn', { active: currentSort === sort.value }]"
            @click="currentSort = sort.value"
          >
            {{ sort.label }}
          </button>
        </div>
      </div>
      
      <div class="replies-list">
        <div
          v-for="reply in sortedReplies"
          :key="reply.id"
          class="reply-item"
        >
          <div class="reply-header">
            <div class="reply-author">
              <img :src="reply.author.avatar || '/default-avatar.png'" :alt="reply.author.nickname" />
              <div class="author-info">
                <span class="author-name">{{ reply.author.nickname }}</span>
                <span class="reply-time">{{ formatTime(reply.createTime) }}</span>
              </div>
            </div>
            <div class="reply-actions">
              <button class="action-btn small" @click="handleLikeReply(reply)">
                <span class="action-icon">👍</span>
                <span class="action-count">{{ reply.likeCount }}</span>
              </button>
              <button class="action-btn small" @click="handleReplyToReply(reply)">
                <span class="action-icon">↩️</span>
                <span class="action-text">回复</span>
              </button>
            </div>
          </div>
          
          <div class="reply-content">
            <p>{{ reply.content }}</p>
          </div>
          
          <div v-if="reply.replyTo" class="reply-to">
            <span class="reply-to-label">回复 @{{ reply.replyTo.author.nickname }}：</span>
            <span class="reply-to-content">{{ reply.replyTo.content }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="loading" class="loading-section">
        <div class="loading-spinner"></div>
        <span>加载中...</span>
      </div>
      
      <div v-if="!loading && postDetail?.replies?.length === 0" class="empty-state">
        <div class="empty-icon">💬</div>
        <p class="empty-text">暂无回复</p>
        <p class="empty-subtext">成为第一个回复的人吧！</p>
      </div>
      
      <div v-if="hasMoreReplies" class="load-more">
        <button class="load-more-btn" @click="loadMoreReplies" :disabled="loading">
          加载更多回复
        </button>
      </div>
    </div>

    <!-- 回复框 -->
    <div class="reply-form-section">
      <div class="reply-form">
        <div class="form-header">
          <h3>发表回复</h3>
          <div v-if="replyToReply" class="replying-to">
            回复 @{{ replyToReply.author.nickname }}
            <button class="cancel-reply" @click="replyToReply = null">×</button>
          </div>
        </div>
        
        <textarea
          v-model="replyContent"
          placeholder="请输入回复内容..."
          class="reply-textarea"
          rows="4"
        ></textarea>
        
        <div class="form-actions">
          <button class="cancel-btn" @click="resetReplyForm">取消</button>
          <button
            class="submit-btn"
            @click="handleSubmitReply"
            :disabled="!canSubmitReply"
          >
            发表回复
          </button>
        </div>
      </div>
    </div>

    <!-- 图片预览模态框 -->
    <div v-if="previewImage" class="image-preview-modal" @click="previewImage = null">
      <div class="modal-content" @click.stop>
        <img :src="previewImage" :alt="'预览图片'" class="preview-image" />
        <button class="close-btn" @click="previewImage = null">×</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGlobalStore } from '@/stores/global'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const globalStore = useGlobalStore()
const userStore = useUserStore()

// 响应式数据
const postDetail = ref<any>(null)
const loading = ref(false)
const currentSort = ref('time')
const replyContent = ref('')
const replyToReply = ref<any>(null)
const previewImage = ref<string | null>(null)
const currentPage = ref(1)
const hasMoreReplies = ref(true)

// 排序选项
const sortOptions = [
  { value: 'time', label: '最新' },
  { value: 'hot', label: '热门' }
]

// 计算属性
const canSubmitReply = computed(() => {
  return replyContent.value.trim() && userStore.isLoggedIn
})

const sortedReplies = computed(() => {
  if (!postDetail.value?.replies) return []
  
  const replies = [...postDetail.value.replies]
  
  if (currentSort.value === 'time') {
    return replies.sort((a, b) => new Date(b.createTime).getTime() - new Date(a.createTime).getTime())
  } else if (currentSort.value === 'hot') {
    return replies.sort((a, b) => b.likeCount - a.likeCount)
  }
  
  return replies
})

// 方法
const handleLikePost = async () => {
  if (!userStore.isLoggedIn) {
    globalStore.showMessage('请先登录', 'warning')
    router.push('/login')
    return
  }
  
  if (!postDetail.value) return
  
  try {
    // 模拟点赞API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    postDetail.value.isLiked = !postDetail.value.isLiked
    if (postDetail.value.isLiked) {
      postDetail.value.likeCount += 1
      globalStore.showMessage('点赞成功', 'success')
    } else {
      postDetail.value.likeCount -= 1
      globalStore.showMessage('取消点赞', 'info')
    }
  } catch (error) {
    globalStore.showMessage('操作失败，请重试', 'error')
  }
}

const handleCollectPost = async () => {
  if (!userStore.isLoggedIn) {
    globalStore.showMessage('请先登录', 'warning')
    router.push('/login')
    return
  }
  
  if (!postDetail.value) return
  
  try {
    // 模拟收藏API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    postDetail.value.isCollected = !postDetail.value.isCollected
    if (postDetail.value.isCollected) {
      globalStore.showMessage('收藏成功', 'success')
    } else {
      globalStore.showMessage('取消收藏', 'info')
    }
  } catch (error) {
    globalStore.showMessage('操作失败，请重试', 'error')
  }
}

const handleSharePost = () => {
  if (!postDetail.value) return
  
  // 模拟分享功能
  if (navigator.share) {
    navigator.share({
      title: postDetail.value.title,
      text: postDetail.value.content,
      url: window.location.href
    })
  } else {
    // 复制链接到剪贴板
    navigator.clipboard.writeText(window.location.href)
    globalStore.showMessage('链接已复制到剪贴板', 'success')
  }
}

const handleLikeReply = async (reply: any) => {
  if (!userStore.isLoggedIn) {
    globalStore.showMessage('请先登录', 'warning')
    router.push('/login')
    return
  }
  
  try {
    // 模拟点赞回复API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    
    reply.isLiked = !reply.isLiked
    if (reply.isLiked) {
      reply.likeCount += 1
    } else {
      reply.likeCount -= 1
    }
  } catch (error) {
    globalStore.showMessage('操作失败，请重试', 'error')
  }
}

const handleReplyToReply = (reply: any) => {
  replyToReply.value = reply
  scrollToReply()
}

const handleSubmitReply = async () => {
  if (!canSubmitReply.value || !postDetail.value) return
  
  try {
    // 模拟发表回复API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newReply = {
      id: Date.now(),
      content: replyContent.value,
      author: {
        id: userStore.userInfo?.id,
        nickname: userStore.userInfo?.nickname,
        avatar: userStore.userInfo?.avatar
      },
      createTime: new Date().toISOString(),
      likeCount: 0,
      replyCount: 0,
      replyTo: replyToReply.value
    }
    
    if (!postDetail.value.replies) {
      postDetail.value.replies = []
    }
    
    postDetail.value.replies.unshift(newReply)
    postDetail.value.replyCount += 1
    
    globalStore.showMessage('回复成功', 'success')
    resetReplyForm()
  } catch (error) {
    globalStore.showMessage('回复失败，请重试', 'error')
  }
}

const resetReplyForm = () => {
  replyContent.value = ''
  replyToReply.value = null
}

const scrollToReply = () => {
  const replyForm = document.querySelector('.reply-form-section')
  if (replyForm) {
    replyForm.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleImageClick = (image: string) => {
  previewImage.value = image
}

const loadMoreReplies = async () => {
  if (!postDetail.value) return
  
  loading.value = true
  try {
    // 模拟加载更多回复
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newReplies = Array.from({ length: 10 }, (_, i) => ({
      id: (currentPage.value * 10) + i + 1,
      content: `这是第${(currentPage.value * 10) + i + 1}条回复内容...`,
      author: {
        id: 1000 + i,
        nickname: `用户${1000 + i}`,
        avatar: ''
      },
      createTime: new Date(Date.now() - Math.random() * 86400000 * 7).toISOString(),
      likeCount: Math.floor(Math.random() * 50),
      replyCount: Math.floor(Math.random() * 10)
    }))
    
    postDetail.value.replies.push(...newReplies)
    currentPage.value += 1
    hasMoreReplies.value = currentPage.value < 5
  } catch (error) {
    globalStore.showMessage('加载失败，请重试', 'error')
  } finally {
    loading.value = false
  }
}

const formatTime = (timeStr?: string) => {
  if (!timeStr) return ''
  
  const time = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - time.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  
  return time.toLocaleDateString()
}

// 模拟获取帖子详情
const mockPostDetail = {
  id: 1,
  title: 'Vue 3.0 新特性详解',
  content: 'Vue 3.0 带来了很多新特性，包括 Composition API、更好的 TypeScript 支持、性能优化等。Composition API 让我们可以更好地组织代码逻辑，特别是在处理复杂组件时。新的响应式系统基于 Proxy，提供了更好的性能和更强大的功能。',
  author: {
    id: 1,
    nickname: '前端开发者',
    avatar: ''
  },
  tiebaId: 1,
  tiebaName: '编程',
  createTime: '2023-12-01T10:00:00',
  updateTime: '2023-12-01T10:00:00',
  viewCount: 1234,
  replyCount: 56,
  likeCount: 89,
  isTop: true,
  isEssence: true,
  isLiked: false,
  isCollected: false,
  images: [
    'https://via.placeholder.com/400x300',
    'https://via.placeholder.com/400x300'
  ],
  replies: [
    {
      id: 1,
      content: '感谢分享，Composition API 确实让代码组织更加清晰！',
      author: {
        id: 2,
        nickname: 'React爱好者',
        avatar: ''
      },
      createTime: '2023-12-01T10:30:00',
      likeCount: 12,
      replyCount: 3
    },
    {
      id: 2,
      content: 'TypeScript 支持真的很重要，现在开发大型项目都离不开它。',
      author: {
        id: 3,
        nickname: 'TypeScript用户',
        avatar: ''
      },
      createTime: '2023-12-01T11:00:00',
      likeCount: 8,
      replyCount: 1
    }
  ]
}

// 生命周期
onMounted(async () => {
  const postId = parseInt(route.params.id as string)
  if (isNaN(postId)) {
    router.push('/404')
    return
  }
  
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    postDetail.value = mockPostDetail
  } catch (error) {
    globalStore.showMessage('加载帖子失败', 'error')
    router.push('/404')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.post-detail-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.post-content-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.post-header {
  margin-bottom: 24px;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.author-info {
  display: flex;
  align-items: center;
}

.author-info img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 12px;
}

.author-details {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.post-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.post-badges {
  display: flex;
  gap: 8px;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.badge.top {
  background: #ff6b6b;
  color: white;
}

.badge.essence {
  background: #ffd93d;
  color: #333;
}

.post-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--text-primary);
  line-height: 1.3;
}

.post-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-item strong {
  color: var(--text-primary);
  font-weight: 600;
}

.post-body {
  margin-bottom: 24px;
}

.post-text {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.post-images {
  margin-top: 20px;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.post-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.post-image:hover {
  transform: scale(1.02);
}

.post-actions {
  display: flex;
  gap: 16px;
  border-top: 1px solid var(--border-color);
  padding-top: 20px;
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
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--bg-tertiary);
}

.action-btn.liked {
  background: rgba(76, 175, 80, 0.1);
  border-color: #4caf50;
  color: #4caf50;
}

.action-btn.collected {
  background: rgba(255, 193, 7, 0.1);
  border-color: #ffc107;
  color: #ffc107;
}

.action-icon {
  font-size: 16px;
}

.action-text {
  font-size: 14px;
}

.action-count {
  font-size: 12px;
  font-weight: 600;
}

.action-btn.small {
  padding: 4px 8px;
  font-size: 12px;
}

.replies-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
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
}

.reply-count {
  color: var(--text-secondary);
  font-weight: normal;
}

.sort-options {
  display: flex;
  gap: 8px;
}

.sort-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 12px;
}

.sort-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.replies-list {
  display: grid;
  gap: 20px;
}

.reply-item {
  padding: 16px;
  background: var(--bg-primary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.reply-author {
  display: flex;
  align-items: center;
}

.reply-author img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 8px;
}

.reply-actions {
  display: flex;
  gap: 8px;
}

.reply-content {
  margin-bottom: 12px;
}

.reply-content p {
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-primary);
}

.reply-to {
  padding: 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}

.reply-to-label {
  font-weight: 600;
}

.reply-to-content {
  margin-left: 4px;
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
}

.load-more {
  text-align: center;
  margin-top: 20px;
}

.load-more-btn {
  padding: 10px 20px;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.reply-form-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
}

.reply-form {
  max-width: 100%;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.form-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.replying-to {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}

.cancel-reply {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: var(--text-tertiary);
}

.reply-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
  resize: vertical;
  margin-bottom: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn,
.submit-btn {
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

.submit-btn {
  background: var(--primary-color);
  color: white;
}

.submit-btn:disabled {
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  cursor: not-allowed;
}

.image-preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  border-radius: 8px;
}

.close-btn {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .post-detail-page {
    padding: 16px;
  }
  
  .post-content-section,
  .replies-section,
  .reply-form-section {
    padding: 16px;
  }
  
  .post-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .post-actions {
    flex-wrap: wrap;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .sort-options {
    align-self: stretch;
    justify-content: center;
  }
}
</style>
<template>
  <div class="tieba-detail-page">
    <!-- 贴吧头部信息 -->
    <div class="tieba-header">
      <div class="tieba-basic-info">
        <div class="tieba-avatar">
          <img :src="currentTieba?.avatar || '/default-avatar.png'" :alt="currentTieba?.displayName" />
        </div>
        <div class="tieba-details">
          <h1 class="tieba-name">{{ currentTieba?.displayName }}</h1>
          <p class="tieba-description">{{ currentTieba?.description }}</p>
          <div class="tieba-stats">
            <span class="stat-item">
              <strong>{{ currentTieba?.memberCount }}</strong> 成员
            </span>
            <span class="stat-item">
              <strong>{{ currentTieba?.postCount }}</strong> 帖子
            </span>
            <span class="stat-item">
              <strong>{{ currentTieba?.todayPostCount }}</strong> 今日
            </span>
            <span class="stat-item">
              <strong>{{ currentTieba?.onlineCount }}</strong> 在线
            </span>
          </div>
          <div class="tieba-tags">
            <span
              v-for="tag in currentTieba?.tags"
              :key="tag"
              class="tag"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
      
      <div class="tieba-actions">
        <button
          v-if="!currentTieba?.isJoined"
          class="join-btn primary"
          @click="handleJoinTieba"
          :disabled="loading"
        >
          加入贴吧
        </button>
        <button
          v-else
          class="leave-btn secondary"
          @click="handleLeaveTieba"
          :disabled="loading"
        >
          退出贴吧
        </button>
        <button class="share-btn">
          <span class="share-icon">📤</span>
          分享
        </button>
      </div>
    </div>

    <!-- 贴吧导航 -->
    <div class="tieba-nav">
      <div class="nav-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['tab', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.name }}
        </button>
      </div>
    </div>

    <!-- 贴吧内容区域 -->
    <div class="tieba-content">
      <!-- 帖子列表 -->
      <div v-if="activeTab === 'posts'" class="posts-section">
        <div class="posts-header">
          <h2 class="section-title">帖子列表</h2>
          <button class="new-post-btn" @click="handleNewPost">
            <span class="plus-icon">+</span>
            发帖
          </button>
        </div>
        
        <div class="posts-list">
          <div
            v-for="post in postList"
            :key="post.id"
            class="post-card"
            @click="handlePostClick(post)"
          >
            <div class="post-header">
              <div class="author-info">
                <img :src="post.author.avatar || '/default-avatar.png'" :alt="post.author.nickname" />
                <div class="author-details">
                  <span class="author-name">{{ post.author.nickname }}</span>
                  <span class="post-time">{{ formatTime(post.createTime) }}</span>
                </div>
              </div>
              <div class="post-badges">
                <span v-if="post.isTop" class="badge top">置顶</span>
                <span v-if="post.isEssence" class="badge essence">精华</span>
              </div>
            </div>
            
            <div class="post-content">
              <h3 class="post-title">{{ post.title }}</h3>
              <p class="post-excerpt">{{ post.content }}</p>
            </div>
            
            <div class="post-stats">
              <span class="view-count">{{ post.viewCount }} 浏览</span>
              <span class="reply-count">{{ post.replyCount }} 回复</span>
              <span class="like-count">{{ post.likeCount }} 点赞</span>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        
        <div v-if="!loading && postList.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <p class="empty-text">暂无帖子</p>
          <button class="empty-action" @click="handleNewPost">创建第一个帖子</button>
        </div>
        
        <div v-if="hasMore" class="load-more">
          <button class="load-more-btn" @click="loadMorePosts" :disabled="loading">
            加载更多
          </button>
        </div>
      </div>

      <!-- 贴吧介绍 -->
      <div v-if="activeTab === 'about'" class="about-section">
        <div class="about-card">
          <h3 class="card-title">贴吧介绍</h3>
          <div class="about-content">
            <p>{{ currentTieba?.description }}</p>
            
            <div v-if="currentTieba?.rules" class="rules-section">
              <h4>吧规</h4>
              <p>{{ currentTieba?.rules }}</p>
            </div>
            
            <div v-if="currentTieba?.announcement" class="announcement-section">
              <h4>公告</h4>
              <p>{{ currentTieba?.announcement }}</p>
            </div>
            
            <div class="create-info">
              <p>创建时间：{{ formatDate(currentTieba?.createTime) }}</p>
              <p>分类：{{ currentTieba?.category }}</p>
            </div>
          </div>
        </div>
        
        <div class="moderators-card">
          <h3 class="card-title">吧务团队</h3>
          <div class="moderators-list">
            <div
              v-for="moderator in currentTieba?.moderators"
              :key="moderator.id"
              class="moderator-item"
            >
              <img :src="moderator.avatar || '/default-avatar.png'" :alt="moderator.nickname" />
              <div class="moderator-info">
                <span class="moderator-name">{{ moderator.nickname }}</span>
                <span class="moderator-role">{{ getRoleText(moderator.role) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 成员列表 -->
      <div v-if="activeTab === 'members'" class="members-section">
        <h2 class="section-title">贴吧成员</h2>
        <div class="members-grid">
          <div
            v-for="member in mockMembers"
            :key="member.id"
            class="member-card"
          >
            <img :src="member.avatar || '/default-avatar.png'" :alt="member.nickname" />
            <div class="member-info">
              <span class="member-name">{{ member.nickname }}</span>
              <span class="member-level">Lv.{{ member.level }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 发帖模态框 -->
    <div v-if="showPostModal" class="modal-overlay">
      <div class="post-modal">
        <div class="modal-header">
          <h3>发布新帖子</h3>
          <button class="close-btn" @click="showPostModal = false">×</button>
        </div>
        <div class="modal-content">
          <input
            v-model="newPostTitle"
            type="text"
            placeholder="请输入帖子标题"
            class="post-title-input"
          />
          <textarea
            v-model="newPostContent"
            placeholder="请输入帖子内容..."
            class="post-content-input"
            rows="6"
          ></textarea>
        </div>
        <div class="modal-actions">
          <button class="cancel-btn" @click="showPostModal = false">取消</button>
          <button class="submit-btn" @click="handleSubmitPost" :disabled="!canSubmitPost">
            发布
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTiebaStore } from '@/stores/tieba'
import { useGlobalStore } from '@/stores/global'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const tiebaStore = useTiebaStore()
const globalStore = useGlobalStore()
const userStore = useUserStore()

// 响应式数据
const activeTab = ref('posts')
const loading = ref(false)
const currentPage = ref(1)
const hasMore = ref(true)
const showPostModal = ref(false)
const newPostTitle = ref('')
const newPostContent = ref('')

// 标签页配置
const tabs = [
  { id: 'posts', name: '帖子' },
  { id: 'about', name: '介绍' },
  { id: 'members', name: '成员' }
]

// 计算属性
const currentTieba = computed(() => tiebaStore.currentTieba)
const postList = computed(() => tiebaStore.postList)
const canSubmitPost = computed(() => {
  return newPostTitle.value.trim() && newPostContent.value.trim() && userStore.isLoggedIn
})

// 模拟成员数据
const mockMembers = ref([
  { id: 1, nickname: '用户1', avatar: '', level: 15 },
  { id: 2, nickname: '用户2', avatar: '', level: 12 },
  { id: 3, nickname: '用户3', avatar: '', level: 10 },
  { id: 4, nickname: '用户4', avatar: '', level: 8 },
  { id: 5, nickname: '用户5', avatar: '', level: 6 }
])

// 方法
const handleJoinTieba = async () => {
  if (!currentTieba.value) return
  
  try {
    const result = await tiebaStore.joinTieba(currentTieba.value.id)
    if (result.success) {
      globalStore.showMessage('加入贴吧成功', 'success')
    } else {
      globalStore.showMessage(result.message || '加入失败', 'error')
    }
  } catch (error) {
    globalStore.showMessage('网络错误，请重试', 'error')
  }
}

const handleLeaveTieba = async () => {
  if (!currentTieba.value) return
  
  try {
    const result = await tiebaStore.leaveTieba(currentTieba.value.id)
    if (result.success) {
      globalStore.showMessage('退出贴吧成功', 'success')
    } else {
      globalStore.showMessage(result.message || '退出失败', 'error')
    }
  } catch (error) {
    globalStore.showMessage('网络错误，请重试', 'error')
  }
}

const handlePostClick = (post: any) => {
  router.push(`/post/${post.id}`)
}

const handleNewPost = () => {
  if (!userStore.isLoggedIn) {
    globalStore.showMessage('请先登录', 'warning')
    router.push('/login')
    return
  }
  
  showPostModal.value = true
  newPostTitle.value = ''
  newPostContent.value = ''
}

const handleSubmitPost = async () => {
  if (!canSubmitPost.value || !currentTieba.value) return
  
  try {
    // 模拟发帖API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    globalStore.showMessage('帖子发布成功', 'success')
    showPostModal.value = false
    
    // 刷新帖子列表
    await loadPosts(1)
  } catch (error) {
    globalStore.showMessage('发布失败，请重试', 'error')
  }
}

const loadPosts = async (page: number) => {
  if (!currentTieba.value) return
  
  loading.value = true
  try {
    const result = await tiebaStore.getPostList(currentTieba.value.id, page, 20)
    if (result.success) {
      hasMore.value = result.hasMore || false
      currentPage.value = page
    } else {
      globalStore.showMessage(result.message || '加载失败', 'error')
    }
  } catch (error) {
    globalStore.showMessage('网络错误，请重试', 'error')
  } finally {
    loading.value = false
  }
}

const loadMorePosts = async () => {
  await loadPosts(currentPage.value + 1)
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

const formatDate = (dateStr?: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString()
}

const getRoleText = (role: string) => {
  const roleMap: Record<string, string> = {
    'owner': '吧主',
    'admin': '管理员',
    'moderator': '小吧主'
  }
  return roleMap[role] || role
}

// 生命周期
onMounted(async () => {
  const tiebaId = parseInt(route.params.id as string)
  if (isNaN(tiebaId)) {
    router.push('/404')
    return
  }
  
  // 获取贴吧详情
  await tiebaStore.getTiebaDetail(tiebaId)
  
  // 获取帖子列表
  await loadPosts(1)
})
</script>

<style scoped>
.tieba-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.tieba-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 24px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

.tieba-basic-info {
  display: flex;
  align-items: flex-start;
  flex: 1;
}

.tieba-avatar {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  margin-right: 20px;
}

.tieba-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tieba-details {
  flex: 1;
}

.tieba-name {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.tieba-description {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.5;
}

.tieba-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.stat-item {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-item strong {
  color: var(--text-primary);
  font-weight: 600;
}

.tieba-tags {
  display: flex;
  gap: 8px;
}

.tag {
  padding: 4px 12px;
  background: rgba(var(--primary-rgb), 0.1);
  color: var(--primary-color);
  border-radius: 16px;
  font-size: 12px;
}

.tieba-actions {
  display: flex;
  gap: 12px;
}

.join-btn,
.leave-btn,
.share-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}

.join-btn.primary {
  background: var(--primary-color);
  color: white;
}

.leave-btn.secondary {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.share-btn {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.tieba-nav {
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border-color);
}

.nav-tabs {
  display: flex;
  gap: 0;
}

.tab {
  padding: 12px 24px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.tab.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}

.tab:hover {
  color: var(--primary-color);
}

.tieba-content {
  min-height: 400px;
}

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
}

.new-post-btn {
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.posts-list {
  display: grid;
  gap: 16px;
}

.post-card {
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.post-header {
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
  width: 40px;
  height: 40px;
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

.post-content {
  margin-bottom: 16px;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.post-excerpt {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-stats {
  font-size: 12px;
  color: var(--text-tertiary);
}

.post-stats span {
  margin-right: 16px;
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
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  margin-bottom: 20px;
}

.empty-action {
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.load-more {
  text-align: center;
  margin-top: 30px;
}

.load-more-btn {
  padding: 12px 24px;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.about-section {
  display: grid;
  gap: 20px;
}

.about-card,
.moderators-card {
  padding: 24px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.about-content h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 16px 0 8px 0;
  color: var(--text-primary);
}

.about-content p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.moderators-list {
  display: grid;
  gap: 16px;
}

.moderator-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.moderator-item img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.moderator-info {
  display: flex;
  flex-direction: column;
}

.moderator-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.moderator-role {
  font-size: 12px;
  color: var(--text-tertiary);
}

.members-section {
  padding: 24px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.member-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.member-card img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.member-info {
  display: flex;
  flex-direction: column;
}

.member-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.member-level {
  font-size: 12px;
  color: var(--text-tertiary);
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

.post-modal {
  background: var(--bg-primary);
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow: auto;
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
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--text-secondary);
}

.modal-content {
  padding: 24px;
}

.post-title-input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 16px;
  margin-bottom: 16px;
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.post-content-input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid var(--border-color);
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .tieba-detail-page {
    padding: 16px;
  }
  
  .tieba-header {
    flex-direction: column;
    gap: 20px;
  }
  
  .tieba-basic-info {
    flex-direction: column;
    text-align: center;
  }
  
  .tieba-avatar {
    margin-right: 0;
    margin-bottom: 16px;
  }
  
  .tieba-stats {
    justify-content: center;
  }
  
  .tieba-actions {
    justify-content: center;
  }
  
  .nav-tabs {
    overflow-x: auto;
  }
  
  .members-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>
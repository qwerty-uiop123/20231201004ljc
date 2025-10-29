<template>
  <div class="home-page">
    <!-- 搜索栏 -->
    <div class="search-section">
      <div class="search-container">
        <div class="search-input-wrapper">
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索贴吧、帖子、用户..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <button class="search-btn" @click="handleSearch">
            <span class="search-icon">🔍</span>
          </button>
        </div>
        <div class="search-history" v-if="searchHistory.length > 0">
          <span class="history-label">搜索历史：</span>
          <span
            v-for="item in searchHistory"
            :key="item"
            class="history-item"
            @click="searchKeyword = item; handleSearch()"
          >
            {{ item }}
          </span>
          <span class="clear-history" @click="clearSearchHistory">清除</span>
        </div>
      </div>
    </div>

    <!-- 轮播图 -->
    <div class="banner-section">
      <div class="banner-container">
        <div class="banner-slide active">
          <img src="@/assets/banner1.jpg" alt="热门贴吧推荐" />
          <div class="banner-content">
            <h3>热门贴吧推荐</h3>
            <p>发现更多有趣的社区</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类导航 -->
    <div class="category-section">
      <div class="category-container">
        <h2 class="section-title">贴吧分类</h2>
        <div class="category-grid">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-item"
            @click="handleCategoryClick(category)"
          >
            <div class="category-icon">{{ category.icon }}</div>
            <span class="category-name">{{ category.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门贴吧 -->
    <div class="hot-tieba-section">
      <div class="section-header">
        <h2 class="section-title">热门贴吧</h2>
        <span class="more-link" @click="handleViewMoreTiebas">查看更多</span>
      </div>
      <div class="tieba-grid">
        <div
          v-for="tieba in hotTiebas"
          :key="tieba.id"
          class="tieba-card"
          @click="handleTiebaClick(tieba)"
        >
          <div class="tieba-avatar">
            <img :src="tieba.avatar || '/default-avatar.png'" :alt="tieba.displayName" />
          </div>
          <div class="tieba-info">
            <h3 class="tieba-name">{{ tieba.displayName }}</h3>
            <p class="tieba-desc">{{ tieba.description }}</p>
            <div class="tieba-stats">
              <span class="member-count">{{ tieba.memberCount }} 成员</span>
              <span class="post-count">{{ tieba.postCount }} 帖子</span>
            </div>
          </div>
          <div class="tieba-actions">
            <button
              v-if="!tieba.isJoined"
              class="join-btn"
              @click.stop="handleJoinTieba(tieba)"
            >
              加入
            </button>
            <button v-else class="joined-btn" disabled>已加入</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐帖子 -->
    <div class="recommended-posts-section">
      <div class="section-header">
        <h2 class="section-title">推荐帖子</h2>
        <span class="more-link" @click="handleViewMorePosts">查看更多</span>
      </div>
      <div class="posts-list">
        <div
          v-for="post in recommendedPosts"
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
            <div class="post-tieba">{{ post.tiebaName }}</div>
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
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-section">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTiebaStore } from '@/stores/tieba'
import { useGlobalStore } from '@/stores/global'

const router = useRouter()
const tiebaStore = useTiebaStore()
const globalStore = useGlobalStore()

// 响应式数据
const searchKeyword = ref('')
const loading = ref(false)

// 计算属性
const searchHistory = ref(['编程', '游戏', '电影', '音乐'])
const categories = ref([
  { id: 1, name: '游戏', icon: '🎮' },
  { id: 2, name: '影视', icon: '🎬' },
  { id: 3, name: '音乐', icon: '🎵' },
  { id: 4, name: '体育', icon: '⚽' },
  { id: 5, name: '科技', icon: '💻' },
  { id: 6, name: '生活', icon: '🏠' },
  { id: 7, name: '学习', icon: '📚' },
  { id: 8, name: '动漫', icon: '🎨' }
])

const hotTiebas = ref([
  {
    id: 1,
    name: 'programming',
    displayName: '编程',
    avatar: '',
    description: '编程技术交流社区',
    memberCount: 12345,
    postCount: 56789,
    isJoined: false
  },
  {
    id: 2,
    name: 'game',
    displayName: '游戏',
    avatar: '',
    description: '游戏讨论社区',
    memberCount: 9876,
    postCount: 43210,
    isJoined: true
  }
])

const recommendedPosts = ref([
  {
    id: 1,
    title: 'Vue 3.0 新特性详解',
    content: 'Vue 3.0 带来了很多新特性，包括 Composition API、更好的 TypeScript 支持等...',
    author: {
      id: 1,
      nickname: '前端开发者',
      avatar: ''
    },
    tiebaName: '编程',
    createTime: '2023-12-01T10:00:00',
    viewCount: 1234,
    replyCount: 56,
    likeCount: 89
  },
  {
    id: 2,
    title: 'React 18 新功能体验',
    content: 'React 18 的并发特性让应用更加流畅，自动批处理等特性值得尝试...',
    author: {
      id: 2,
      nickname: 'React爱好者',
      avatar: ''
    },
    tiebaName: '前端开发',
    createTime: '2023-12-01T09:30:00',
    viewCount: 987,
    replyCount: 34,
    likeCount: 67
  }
])

// 方法
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    // 添加到搜索历史
    if (!searchHistory.value.includes(searchKeyword.value)) {
      searchHistory.value.unshift(searchKeyword.value)
      if (searchHistory.value.length > 10) {
        searchHistory.value.pop()
      }
    }
    
    // 跳转到搜索结果页
    router.push({
      path: '/search',
      query: { q: searchKeyword.value }
    })
  }
}

const clearSearchHistory = () => {
  searchHistory.value = []
}

const handleCategoryClick = (category: any) => {
  router.push({
    path: '/category',
    query: { id: category.id, name: category.name }
  })
}

const handleTiebaClick = (tieba: any) => {
  router.push(`/tieba/${tieba.id}`)
}

const handleJoinTieba = async (tieba: any) => {
  try {
    const result = await tiebaStore.joinTieba(tieba.id)
    if (result.success) {
      globalStore.showMessage('加入贴吧成功', 'success')
      tieba.isJoined = true
    } else {
      globalStore.showMessage(result.message || '加入失败', 'error')
    }
  } catch (error) {
    globalStore.showMessage('网络错误，请重试', 'error')
  }
}

const handlePostClick = (post: any) => {
  router.push(`/post/${post.id}`)
}

const handleViewMoreTiebas = () => {
  router.push('/tiebas')
}

const handleViewMorePosts = () => {
  router.push('/posts')
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
  loading.value = true
  try {
    // 获取热门贴吧
    await tiebaStore.getHotTiebas()
    hotTiebas.value = tiebaStore.hotTiebas
    
    // 获取推荐贴吧
    await tiebaStore.getRecommendedTiebas()
  } catch (error) {
    globalStore.showMessage('数据加载失败', 'error')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-section {
  margin-bottom: 30px;
}

.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  background: var(--bg-secondary);
  border-radius: 24px;
  padding: 8px 16px;
  border: 1px solid var(--border-color);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 16px;
  color: var(--text-primary);
}

.search-btn {
  background: var(--primary-color);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-history {
  margin-top: 10px;
  font-size: 14px;
  color: var(--text-secondary);
}

.history-item {
  margin-right: 10px;
  cursor: pointer;
}

.history-item:hover {
  color: var(--primary-color);
}

.clear-history {
  color: var(--error-color);
  cursor: pointer;
  margin-left: 10px;
}

.banner-section {
  margin-bottom: 30px;
}

.banner-container {
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg-secondary);
}

.banner-slide img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.category-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.category-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.category-name {
  font-size: 14px;
  color: var(--text-primary);
}

.hot-tieba-section,
.recommended-posts-section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.more-link {
  color: var(--primary-color);
  cursor: pointer;
  font-size: 14px;
}

.tieba-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.tieba-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tieba-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tieba-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 16px;
}

.tieba-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tieba-info {
  flex: 1;
}

.tieba-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.tieba-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.tieba-stats {
  font-size: 12px;
  color: var(--text-tertiary);
}

.tieba-stats span {
  margin-right: 12px;
}

.tieba-actions {
  margin-left: 16px;
}

.join-btn,
.joined-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.join-btn {
  background: var(--primary-color);
  color: white;
}

.joined-btn {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.posts-list {
  display: grid;
  gap: 16px;
}

.post-card {
  padding: 16px;
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
  margin-bottom: 12px;
}

.author-info {
  display: flex;
  align-items: center;
}

.author-info img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 8px;
}

.author-details {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.post-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.post-tieba {
  font-size: 12px;
  color: var(--primary-color);
  background: rgba(var(--primary-rgb), 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

.post-content {
  margin-bottom: 12px;
}

.post-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.post-excerpt {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-stats {
  font-size: 12px;
  color: var(--text-tertiary);
}

.post-stats span {
  margin-right: 12px;
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .home-page {
    padding: 16px;
  }
  
  .category-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .tieba-grid {
    grid-template-columns: 1fr;
  }
}
</style>
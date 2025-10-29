<template>
  <div class="search-page">
    <!-- 搜索头部 -->
    <div class="search-header">
      <div class="search-input-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索贴吧、帖子、用户..."
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <button class="search-btn" @click="handleSearch">
          <span class="search-icon">🔍</span>
        </button>
      </div>
      
      <!-- 搜索类型筛选 -->
      <div class="search-tabs">
        <button
          v-for="tab in searchTabs"
          :key="tab.value"
          :class="['tab-btn', { active: activeTab === tab.value }]"
          @click="activeTab = tab.value"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- 搜索结果 -->
    <div class="search-results">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>搜索中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!hasResults" class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>暂无搜索结果</h3>
        <p>尝试使用不同的关键词搜索</p>
      </div>

      <!-- 搜索结果列表 -->
      <div v-else class="results-container">
        <!-- 贴吧搜索结果 -->
        <div v-if="activeTab === 'tieba' && tiebaResults.length" class="result-section">
          <h3 class="section-title">贴吧</h3>
          <div class="tieba-results">
            <div
              v-for="tieba in tiebaResults"
              :key="tieba.id"
              class="tieba-item"
              @click="goToTieba(tieba.id)"
            >
              <div class="tieba-avatar">
                <img :src="tieba.avatar" :alt="tieba.name" />
              </div>
              <div class="tieba-info">
                <h4 class="tieba-name">{{ tieba.name }}</h4>
                <p class="tieba-desc">{{ tieba.description }}</p>
                <div class="tieba-stats">
                  <span class="member-count">{{ tieba.memberCount }} 成员</span>
                  <span class="post-count">{{ tieba.postCount }} 帖子</span>
                </div>
              </div>
              <button
                :class="['join-btn', { joined: tieba.isJoined }]"
                @click.stop="toggleJoinTieba(tieba)"
              >
                {{ tieba.isJoined ? '已加入' : '加入' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 帖子搜索结果 -->
        <div v-if="activeTab === 'post' && postResults.length" class="result-section">
          <h3 class="section-title">帖子</h3>
          <div class="post-results">
            <div
              v-for="post in postResults"
              :key="post.id"
              class="post-item"
              @click="goToPost(post.id)"
            >
              <div class="post-header">
                <div class="post-author">
                  <img :src="post.author.avatar" :alt="post.author.name" />
                  <span class="author-name">{{ post.author.name }}</span>
                </div>
                <span class="post-time">{{ formatTime(post.createTime) }}</span>
              </div>
              <h4 class="post-title">{{ post.title }}</h4>
              <p class="post-content">{{ post.content }}</p>
              <div class="post-stats">
                <span class="reply-count">{{ post.replyCount }} 回复</span>
                <span class="like-count">{{ post.likeCount }} 点赞</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 用户搜索结果 -->
        <div v-if="activeTab === 'user' && userResults.length" class="result-section">
          <h3 class="section-title">用户</h3>
          <div class="user-results">
            <div
              v-for="user in userResults"
              :key="user.id"
              class="user-item"
              @click="goToUserProfile(user.id)"
            >
              <div class="user-avatar">
                <img :src="user.avatar" :alt="user.name" />
              </div>
              <div class="user-info">
                <h4 class="user-name">{{ user.name }}</h4>
                <p class="user-bio">{{ user.bio }}</p>
                <div class="user-stats">
                  <span class="follower-count">{{ user.followerCount }} 粉丝</span>
                  <span class="post-count">{{ user.postCount }} 帖子</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTiebaStore } from '@/stores/tieba'

const route = useRoute()
const router = useRouter()
const tiebaStore = useTiebaStore()

// 搜索状态
const searchQuery = ref('')
const activeTab = ref('tieba') // tieba, post, user
const loading = ref(false)

// 搜索结果
const tiebaResults = ref([])
const postResults = ref([])
const userResults = ref([])

// 搜索类型标签
const searchTabs = [
  { label: '贴吧', value: 'tieba' },
  { label: '帖子', value: 'post' },
  { label: '用户', value: 'user' }
]

// 是否有搜索结果
const hasResults = computed(() => {
  return tiebaResults.value.length > 0 || postResults.value.length > 0 || userResults.value.length > 0
})

// 处理搜索
const handleSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  loading.value = true
  
  try {
    // 模拟搜索API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟搜索结果
    if (activeTab.value === 'tieba') {
      tiebaResults.value = [
        {
          id: '1',
          name: 'Vue.js',
          description: 'Vue.js 官方贴吧，讨论Vue相关技术',
          avatar: '/api/placeholder/60/60',
          memberCount: 12345,
          postCount: 5678,
          isJoined: false
        },
        {
          id: '2',
          name: 'React',
          description: 'React技术讨论社区',
          avatar: '/api/placeholder/60/60',
          memberCount: 9876,
          postCount: 4321,
          isJoined: true
        }
      ]
    } else if (activeTab.value === 'post') {
      postResults.value = [
        {
          id: '1',
          title: 'Vue 3.0新特性详解',
          content: 'Vue 3.0带来了很多新特性，包括Composition API、更好的TypeScript支持等...',
          author: {
            name: 'Vue爱好者',
            avatar: '/api/placeholder/40/40'
          },
          createTime: new Date('2024-01-15'),
          replyCount: 156,
          likeCount: 289
        }
      ]
    } else if (activeTab.value === 'user') {
      userResults.value = [
        {
          id: '1',
          name: 'Vue开发者',
          bio: '专注于Vue.js技术分享',
          avatar: '/api/placeholder/60/60',
          followerCount: 1234,
          postCount: 56
        }
      ]
    }
  } catch (error) {
    console.error('搜索失败:', error)
  } finally {
    loading.value = false
  }
}

// 跳转到贴吧
const goToTieba = (tiebaId: string) => {
  router.push(`/tieba/${tiebaId}`)
}

// 跳转到帖子
const goToPost = (postId: string) => {
  router.push(`/post/${postId}`)
}

// 跳转到用户资料
const goToUserProfile = (userId: string) => {
  router.push(`/profile/${userId}`)
}

// 加入/退出贴吧
const toggleJoinTieba = (tieba: any) => {
  tieba.isJoined = !tieba.isJoined
  // 这里可以调用store的加入/退出贴吧方法
}

// 格式化时间
const formatTime = (time: Date) => {
  return time.toLocaleDateString('zh-CN')
}

onMounted(() => {
  // 从路由参数获取搜索关键词
  if (route.query.q) {
    searchQuery.value = route.query.q as string
    handleSearch()
  }
})
</script>

<style scoped lang="scss">
.search-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  margin-bottom: 30px;
}

.search-input-container {
  display: flex;
  margin-bottom: 20px;
  
  .search-input {
    flex: 1;
    padding: 12px 16px;
    border: 2px solid var(--border-color);
    border-right: none;
    border-radius: 8px 0 0 8px;
    font-size: 16px;
    
    &:focus {
      outline: none;
      border-color: var(--primary-color);
    }
  }
  
  .search-btn {
    padding: 12px 20px;
    background: var(--primary-color);
    border: none;
    border-radius: 0 8px 8px 0;
    cursor: pointer;
    
    &:hover {
      background: var(--primary-hover);
    }
    
    .search-icon {
      font-size: 18px;
    }
  }
}

.search-tabs {
  display: flex;
  gap: 20px;
  
  .tab-btn {
    padding: 8px 16px;
    border: none;
    background: transparent;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    
    &.active {
      background: var(--primary-color);
      color: white;
    }
    
    &:hover {
      background: var(--bg-hover);
    }
  }
}

.search-results {
  min-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  
  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--border-color);
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  
  p {
    color: var(--text-secondary);
  }
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  
  .empty-icon {
    font-size: 64px;
    margin-bottom: 20px;
    opacity: 0.5;
  }
  
  h3 {
    margin-bottom: 8px;
    color: var(--text-primary);
  }
  
  p {
    color: var(--text-secondary);
  }
}

.result-section {
  margin-bottom: 40px;
  
  .section-title {
    margin-bottom: 20px;
    font-size: 20px;
    color: var(--text-primary);
  }
}

.tieba-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    border-color: var(--primary-color);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .tieba-avatar {
    width: 60px;
    height: 60px;
    border-radius: 8px;
    overflow: hidden;
    margin-right: 16px;
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
  
  .tieba-info {
    flex: 1;
    
    .tieba-name {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 4px;
    }
    
    .tieba-desc {
      color: var(--text-secondary);
      margin-bottom: 8px;
      font-size: 14px;
    }
    
    .tieba-stats {
      display: flex;
      gap: 16px;
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }
  
  .join-btn {
    padding: 8px 16px;
    border: 1px solid var(--primary-color);
    background: transparent;
    color: var(--primary-color);
    border-radius: 6px;
    cursor: pointer;
    
    &.joined {
      background: var(--primary-color);
      color: white;
    }
    
    &:hover {
      opacity: 0.8;
    }
  }
}

.post-item {
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    border-color: var(--primary-color);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    .post-author {
      display: flex;
      align-items: center;
      
      img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        margin-right: 8px;
      }
      
      .author-name {
        font-weight: 500;
      }
    }
    
    .post-time {
      color: var(--text-tertiary);
      font-size: 12px;
    }
  }
  
  .post-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
  }
  
  .post-content {
    color: var(--text-secondary);
    margin-bottom: 12px;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .post-stats {
    display: flex;
    gap: 16px;
    font-size: 12px;
    color: var(--text-tertiary);
  }
}

.user-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    border-color: var(--primary-color);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .user-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 16px;
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
  
  .user-info {
    flex: 1;
    
    .user-name {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 4px;
    }
    
    .user-bio {
      color: var(--text-secondary);
      margin-bottom: 8px;
      font-size: 14px;
    }
    
    .user-stats {
      display: flex;
      gap: 16px;
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .search-page {
    padding: 16px;
  }
  
  .search-tabs {
    gap: 12px;
    
    .tab-btn {
      padding: 6px 12px;
      font-size: 12px;
    }
  }
  
  .tieba-item {
    flex-direction: column;
    align-items: flex-start;
    
    .tieba-avatar {
      margin-right: 0;
      margin-bottom: 12px;
    }
    
    .join-btn {
      align-self: flex-end;
      margin-top: 12px;
    }
  }
}
</style>
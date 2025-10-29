<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <!-- 错误代码 -->
      <div class="error-code">
        <span class="code-number">4</span>
        <span class="code-zero">0</span>
        <span class="code-number">4</span>
      </div>
      
      <!-- 错误信息 -->
      <div class="error-info">
        <h1 class="error-title">页面不存在</h1>
        <p class="error-description">
          抱歉，您访问的页面可能已被删除或暂时不可用
        </p>
        
        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button class="primary-btn" @click="goHome">
            返回首页
          </button>
          <button class="secondary-btn" @click="goBack">
            返回上页
          </button>
        </div>
        
        <!-- 搜索建议 -->
        <div class="search-suggestion">
          <p class="suggestion-title">或者尝试搜索：</p>
          <div class="suggestion-tags">
            <span 
              v-for="tag in suggestionTags" 
              :key="tag"
              class="suggestion-tag"
              @click="searchTag(tag)"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- 装饰元素 -->
      <div class="decoration">
        <div class="decoration-item"></div>
        <div class="decoration-item"></div>
        <div class="decoration-item"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 搜索建议标签
const suggestionTags = ref([
  'Vue.js', 'React', 'JavaScript', 'TypeScript',
  '前端开发', '后端开发', '移动开发', '人工智能'
])

// 返回首页
const goHome = () => {
  router.push('/')
}

// 返回上页
const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    goHome()
  }
}

// 搜索标签
const searchTag = (tag: string) => {
  router.push(`/search?q=${encodeURIComponent(tag)}`)
}
</script>

<style scoped lang="scss">
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  padding: 20px;
}

.not-found-container {
  text-align: center;
  max-width: 600px;
  position: relative;
}

.error-code {
  margin-bottom: 40px;
  
  .code-number,
  .code-zero {
    display: inline-block;
    font-size: 120px;
    font-weight: 900;
    line-height: 1;
    margin: 0 10px;
  }
  
  .code-number {
    color: var(--primary-color);
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .code-zero {
    color: var(--text-secondary);
    position: relative;
    
    &::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 80px;
      height: 80px;
      border: 8px solid var(--border-color);
      border-radius: 50%;
      opacity: 0.3;
    }
  }
}

.error-info {
  margin-bottom: 60px;
  
  .error-title {
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 16px;
  }
  
  .error-description {
    font-size: 18px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 40px;
  }
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 40px;
  
  .primary-btn,
  .secondary-btn {
    padding: 12px 32px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
  
  .primary-btn {
    background: var(--primary-color);
    color: white;
    
    &:hover {
      background: var(--primary-hover);
    }
  }
  
  .secondary-btn {
    background: transparent;
    color: var(--text-primary);
    border: 2px solid var(--border-color);
    
    &:hover {
      border-color: var(--primary-color);
      color: var(--primary-color);
    }
  }
}

.search-suggestion {
  .suggestion-title {
    font-size: 14px;
    color: var(--text-tertiary);
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  .suggestion-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
  }
  
  .suggestion-tag {
    padding: 6px 12px;
    background: var(--bg-hover);
    color: var(--text-secondary);
    border-radius: 20px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      background: var(--primary-color);
      color: white;
      transform: translateY(-1px);
    }
  }
}

.decoration {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  pointer-events: none;
  z-index: -1;
  
  .decoration-item {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
    
    &:nth-child(1) {
      width: 200px;
      height: 200px;
      top: 0;
      left: 0;
      background: var(--primary-color);
      animation: float 6s ease-in-out infinite;
    }
    
    &:nth-child(2) {
      width: 150px;
      height: 150px;
      bottom: 0;
      right: 0;
      background: var(--accent-color);
      animation: float 8s ease-in-out infinite reverse;
    }
    
    &:nth-child(3) {
      width: 100px;
      height: 100px;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: var(--warning-color);
      animation: float 10s ease-in-out infinite;
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@media (max-width: 768px) {
  .error-code {
    .code-number,
    .code-zero {
      font-size: 80px;
      margin: 0 5px;
    }
    
    .code-zero::before {
      width: 60px;
      height: 60px;
      border-width: 6px;
    }
  }
  
  .error-info {
    .error-title {
      font-size: 24px;
    }
    
    .error-description {
      font-size: 16px;
    }
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
    
    .primary-btn,
    .secondary-btn {
      width: 200px;
    }
  }
  
  .decoration {
    width: 200px;
    height: 200px;
    
    .decoration-item {
      &:nth-child(1) {
        width: 120px;
        height: 120px;
      }
      
      &:nth-child(2) {
        width: 80px;
        height: 80px;
      }
      
      &:nth-child(3) {
        width: 60px;
        height: 60px;
      }
    }
  }
}

@media (max-width: 480px) {
  .error-code {
    .code-number,
    .code-zero {
      font-size: 60px;
    }
    
    .code-zero::before {
      width: 40px;
      height: 40px;
      border-width: 4px;
    }
  }
  
  .suggestion-tags {
    gap: 6px;
    
    .suggestion-tag {
      font-size: 12px;
      padding: 4px 8px;
    }
  }
}
</style>
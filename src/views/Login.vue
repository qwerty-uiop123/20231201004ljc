<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧品牌区域 -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="brand-logo">
            <span class="logo-icon">💬</span>
            <h1 class="logo-text">贴吧App</h1>
          </div>
          
          <div class="brand-description">
            <h2>欢迎回来</h2>
            <p>加入贴吧社区，与志同道合的朋友一起交流分享</p>
          </div>
          
          <div class="brand-features">
            <div class="feature-item">
              <span class="feature-icon">🔥</span>
              <span class="feature-text">热门贴吧讨论</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">👥</span>
              <span class="feature-text">千万用户社区</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">💡</span>
              <span class="feature-text">实时消息互动</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="form-section">
        <div class="form-content">
          <div class="form-header">
            <h2 class="form-title">登录账号</h2>
            <p class="form-subtitle">请输入您的账号信息</p>
          </div>

          <!-- 登录表单 -->
          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label for="username" class="form-label">用户名或邮箱</label>
              <div class="input-wrapper">
                <span class="input-icon">👤</span>
                <input
                  id="username"
                  v-model="loginForm.username"
                  type="text"
                  placeholder="请输入用户名或邮箱"
                  class="form-input"
                  :class="{ error: errors.username }"
                  @blur="validateField('username')"
                />
              </div>
              <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
            </div>

            <div class="form-group">
              <label for="password" class="form-label">密码</label>
              <div class="input-wrapper">
                <span class="input-icon">🔒</span>
                <input
                  id="password"
                  v-model="loginForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="请输入密码"
                  class="form-input"
                  :class="{ error: errors.password }"
                  @blur="validateField('password')"
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                >
                  <span class="toggle-icon">{{ showPassword ? '🙈' : '👁️' }}</span>
                </button>
              </div>
              <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
            </div>

            <div class="form-options">
              <label class="remember-me">
                <input
                  v-model="loginForm.rememberMe"
                  type="checkbox"
                  class="checkbox"
                />
                <span class="checkbox-label">记住我</span>
              </label>
              
              <button type="button" class="forgot-password" @click="handleForgotPassword">
                忘记密码？
              </button>
            </div>

            <button
              type="submit"
              class="login-button"
              :disabled="loading || !isFormValid"
              :class="{ loading: loading }"
            >
              <span v-if="loading" class="loading-spinner"></span>
              <span v-else>登录</span>
            </button>

            <div class="divider">
              <span class="divider-text">或</span>
            </div>

            <div class="social-login">
              <button type="button" class="social-button wechat" @click="handleSocialLogin('wechat')">
                <span class="social-icon">💬</span>
                <span class="social-text">微信登录</span>
              </button>
              
              <button type="button" class="social-button qq" @click="handleSocialLogin('qq')">
                <span class="social-icon">🐧</span>
                <span class="social-text">QQ登录</span>
              </button>
            </div>
          </form>

          <div class="form-footer">
            <p class="register-text">
              还没有账号？
              <button type="button" class="register-link" @click="handleRegister">立即注册</button>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 忘记密码模态框 -->
    <div v-if="showForgotPasswordModal" class="modal-overlay" @click="showForgotPasswordModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>忘记密码</h3>
          <button class="close-btn" @click="showForgotPasswordModal = false">×</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>邮箱地址</label>
            <input v-model="forgotPasswordEmail" type="email" placeholder="请输入注册时使用的邮箱" />
          </div>
          
          <div class="form-actions">
            <button class="cancel-btn" @click="showForgotPasswordModal = false">取消</button>
            <button class="submit-btn" @click="handleSubmitForgotPassword" :disabled="!forgotPasswordEmail">
              发送重置链接
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGlobalStore } from '@/stores/global'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const globalStore = useGlobalStore()
const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const showPassword = ref(false)
const showForgotPasswordModal = ref(false)
const forgotPasswordEmail = ref('')

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  rememberMe: false
})

// 表单验证错误
const errors = reactive({
  username: '',
  password: ''
})

// 计算属性
const isFormValid = computed(() => {
  return loginForm.username.trim() && 
         loginForm.password.trim() && 
         !errors.username && 
         !errors.password
})

// 表单验证方法
const validateField = (field: string) => {
  const value = loginForm[field as keyof typeof loginForm]
  
  switch (field) {
    case 'username':
      if (!value.trim()) {
        errors.username = '请输入用户名或邮箱'
      } else if (value.trim().length < 3) {
        errors.username = '用户名至少3个字符'
      } else {
        errors.username = ''
      }
      break
      
    case 'password':
      if (!value.trim()) {
        errors.password = '请输入密码'
      } else if (value.trim().length < 6) {
        errors.password = '密码至少6个字符'
      } else {
        errors.password = ''
      }
      break
  }
}

// 登录处理
const handleLogin = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  
  try {
    // 调用用户store的登录方法
    const success = await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (success) {
      globalStore.showMessage('登录成功！', 'success')
      
      // 跳转到首页或之前访问的页面
      const redirectPath = router.currentRoute.value.query.redirect as string || '/'
      router.push(redirectPath)
    } else {
      globalStore.showMessage('用户名或密码错误', 'error')
    }
  } catch (error) {
    globalStore.showMessage('登录失败，请重试', 'error')
  } finally {
    loading.value = false
  }
}

// 忘记密码处理
const handleForgotPassword = () => {
  showForgotPasswordModal.value = true
}

const handleSubmitForgotPassword = async () => {
  if (!forgotPasswordEmail.value.trim()) return
  
  try {
    // 模拟发送重置密码邮件
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    globalStore.showMessage('重置链接已发送到您的邮箱', 'success')
    showForgotPasswordModal.value = false
    forgotPasswordEmail.value = ''
  } catch (error) {
    globalStore.showMessage('发送失败，请重试', 'error')
  }
}

// 社交登录处理
const handleSocialLogin = (platform: string) => {
  globalStore.showMessage(`${platform}登录功能开发中`, 'info')
}

// 注册处理
const handleRegister = () => {
  router.push('/register')
}

// 生命周期
onMounted(() => {
  // 如果用户已登录，直接跳转到首页
  if (userStore.isLoggedIn) {
    router.push('/')
  }
  
  // 检查是否有记住的登录信息
  const rememberedUsername = localStorage.getItem('rememberedUsername')
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    loginForm.rememberMe = true
  }
})

// 监听记住我状态变化
watch(() => loginForm.rememberMe, (newValue) => {
  if (newValue) {
    localStorage.setItem('rememberedUsername', loginForm.username)
  } else {
    localStorage.removeItem('rememberedUsername')
  }
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: var(--bg-primary);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.brand-section {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  color: white;
  padding: 60px 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-content {
  max-width: 400px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 40px;
}

.logo-icon {
  font-size: 48px;
}

.logo-text {
  font-size: 32px;
  font-weight: 700;
  margin: 0;
}

.brand-description h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 16px;
}

.brand-description p {
  font-size: 16px;
  line-height: 1.6;
  opacity: 0.9;
  margin-bottom: 40px;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.feature-icon {
  font-size: 20px;
}

.feature-text {
  font-size: 16px;
  font-weight: 500;
}

.form-section {
  padding: 60px 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-content {
  max-width: 400px;
  width: 100%;
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.form-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  font-size: 18px;
  z-index: 1;
}

.form-input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-input.error {
  border-color: var(--error-color);
}

.password-toggle {
  position: absolute;
  right: 16px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-size: 18px;
}

.error-message {
  font-size: 12px;
  color: var(--error-color);
  margin-top: 4px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox {
  width: 16px;
  height: 16px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-primary);
  cursor: pointer;
}

.checkbox-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.forgot-password {
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
}

.login-button {
  width: 100%;
  padding: 16px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.login-button:disabled {
  background: var(--text-tertiary);
  cursor: not-allowed;
}

.login-button.loading {
  color: transparent;
}

.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

.divider {
  position: relative;
  text-align: center;
  margin: 20px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--border-color);
}

.divider-text {
  background: var(--bg-primary);
  padding: 0 16px;
  color: var(--text-tertiary);
  font-size: 14px;
}

.social-login {
  display: flex;
  gap: 12px;
}

.social-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-button:hover {
  border-color: var(--primary-color);
}

.social-button.wechat:hover {
  border-color: #07C160;
}

.social-button.qq:hover {
  border-color: #12B7F5;
}

.social-icon {
  font-size: 18px;
}

.form-footer {
  text-align: center;
  margin-top: 32px;
}

.register-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.register-link {
  background: none;
  border: none;
  color: var(--primary-color);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

/* 模态框样式 */
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
  max-width: 400px;
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

.modal-body .form-group {
  margin-bottom: 20px;
}

.modal-body label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-body input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
}

.modal-body input:focus {
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

.submit-btn {
  padding: 8px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.submit-btn:disabled {
  background: var(--text-tertiary);
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  
  .brand-section {
    display: none;
  }
  
  .form-section {
    padding: 40px 24px;
  }
  
  .social-login {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .login-page {
    padding: 16px;
  }
  
  .form-section {
    padding: 32px 20px;
  }
  
  .form-title {
    font-size: 24px;
  }
  
  .form-subtitle {
    font-size: 14px;
  }
}
</style>
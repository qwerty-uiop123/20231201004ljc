<template>
  <div class="register-page">
    <div class="register-container">
      <!-- 左侧品牌区域 -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="brand-logo">
            <span class="logo-icon">💬</span>
            <h1 class="logo-text">贴吧App</h1>
          </div>
          
          <div class="brand-description">
            <h2>加入我们</h2>
            <p>创建账号，开始您的贴吧社区之旅</p>
          </div>
          
          <div class="brand-features">
            <div class="feature-item">
              <span class="feature-icon">🚀</span>
              <span class="feature-text">快速注册</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">🔒</span>
              <span class="feature-text">安全可靠</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">🎯</span>
              <span class="feature-text">个性化推荐</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧注册表单 -->
      <div class="form-section">
        <div class="form-content">
          <div class="form-header">
            <h2 class="form-title">创建账号</h2>
            <p class="form-subtitle">请填写注册信息</p>
          </div>

          <!-- 注册表单 -->
          <form @submit.prevent="handleRegister" class="register-form">
            <div class="form-row">
              <div class="form-group">
                <label for="username" class="form-label">用户名</label>
                <div class="input-wrapper">
                  <span class="input-icon">👤</span>
                  <input
                    id="username"
                    v-model="registerForm.username"
                    type="text"
                    placeholder="请输入用户名"
                    class="form-input"
                    :class="{ error: errors.username }"
                    @blur="validateField('username')"
                    @input="checkUsernameAvailability"
                  />
                </div>
                <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
                <span v-if="usernameAvailable !== null" class="availability-message" :class="{ available: usernameAvailable, taken: !usernameAvailable }">
                  {{ usernameAvailable ? '用户名可用' : '用户名已被使用' }}
                </span>
              </div>

              <div class="form-group">
                <label for="nickname" class="form-label">昵称</label>
                <div class="input-wrapper">
                  <span class="input-icon">😊</span>
                  <input
                    id="nickname"
                    v-model="registerForm.nickname"
                    type="text"
                    placeholder="请输入昵称"
                    class="form-input"
                    :class="{ error: errors.nickname }"
                    @blur="validateField('nickname')"
                  />
                </div>
                <span v-if="errors.nickname" class="error-message">{{ errors.nickname }}</span>
              </div>
            </div>

            <div class="form-group">
              <label for="email" class="form-label">邮箱地址</label>
              <div class="input-wrapper">
                <span class="input-icon">📧</span>
                <input
                  id="email"
                  v-model="registerForm.email"
                  type="email"
                  placeholder="请输入邮箱地址"
                  class="form-input"
                  :class="{ error: errors.email }"
                  @blur="validateField('email')"
                />
              </div>
              <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="password" class="form-label">密码</label>
                <div class="input-wrapper">
                  <span class="input-icon">🔒</span>
                  <input
                    id="password"
                    v-model="registerForm.password"
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
                <div class="password-strength">
                  <div class="strength-bar" :class="passwordStrength">
                    <div class="strength-fill"></div>
                  </div>
                  <span class="strength-text">{{ getPasswordStrengthText() }}</span>
                </div>
              </div>

              <div class="form-group">
                <label for="confirmPassword" class="form-label">确认密码</label>
                <div class="input-wrapper">
                  <span class="input-icon">🔒</span>
                  <input
                    id="confirmPassword"
                    v-model="registerForm.confirmPassword"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    placeholder="请再次输入密码"
                    class="form-input"
                    :class="{ error: errors.confirmPassword }"
                    @blur="validateField('confirmPassword')"
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    <span class="toggle-icon">{{ showConfirmPassword ? '🙈' : '👁️' }}</span>
                  </button>
                </div>
                <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
              </div>
            </div>

            <div class="form-group">
              <label class="agreement-label">
                <input
                  v-model="registerForm.agreedToTerms"
                  type="checkbox"
                  class="agreement-checkbox"
                  :class="{ error: errors.agreedToTerms }"
                />
                <span class="agreement-text">
                  我已阅读并同意
                  <button type="button" class="agreement-link" @click="handleViewTerms">《用户协议》</button>
                  和
                  <button type="button" class="agreement-link" @click="handleViewPrivacy">《隐私政策》</button>
                </span>
              </label>
              <span v-if="errors.agreedToTerms" class="error-message">{{ errors.agreedToTerms }}</span>
            </div>

            <button
              type="submit"
              class="register-button"
              :disabled="loading || !isFormValid"
              :class="{ loading: loading }"
            >
              <span v-if="loading" class="loading-spinner"></span>
              <span v-else>注册账号</span>
            </button>

            <div class="divider">
              <span class="divider-text">或</span>
            </div>

            <div class="social-register">
              <button type="button" class="social-button wechat" @click="handleSocialRegister('wechat')">
                <span class="social-icon">💬</span>
                <span class="social-text">微信注册</span>
              </button>
              
              <button type="button" class="social-button qq" @click="handleSocialRegister('qq')">
                <span class="social-icon">🐧</span>
                <span class="social-text">QQ注册</span>
              </button>
            </div>
          </form>

          <div class="form-footer">
            <p class="login-text">
              已有账号？
              <button type="button" class="login-link" @click="handleLogin">立即登录</button>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户协议模态框 -->
    <div v-if="showTermsModal" class="modal-overlay" @click="showTermsModal = false">
      <div class="modal-content large" @click.stop>
        <div class="modal-header">
          <h3>用户协议</h3>
          <button class="close-btn" @click="showTermsModal = false">×</button>
        </div>
        
        <div class="modal-body">
          <div class="terms-content">
            <h4>欢迎使用贴吧App</h4>
            <p>请仔细阅读以下用户协议...</p>
            <!-- 协议内容 -->
          </div>
          
          <div class="modal-actions">
            <button class="agree-btn" @click="handleAgreeTerms">同意并继续</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 隐私政策模态框 -->
    <div v-if="showPrivacyModal" class="modal-overlay" @click="showPrivacyModal = false">
      <div class="modal-content large" @click.stop>
        <div class="modal-header">
          <h3>隐私政策</h3>
          <button class="close-btn" @click="showPrivacyModal = false">×</button>
        </div>
        
        <div class="modal-body">
          <div class="privacy-content">
            <h4>隐私保护政策</h4>
            <p>我们重视您的隐私...</p>
            <!-- 隐私政策内容 -->
          </div>
          
          <div class="modal-actions">
            <button class="agree-btn" @click="handleAgreePrivacy">同意并继续</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGlobalStore } from '@/stores/global'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const globalStore = useGlobalStore()
const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const showTermsModal = ref(false)
const showPrivacyModal = ref(false)
const usernameAvailable = ref<boolean | null>(null)

// 注册表单数据
const registerForm = reactive({
  username: '',
  nickname: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreedToTerms: false
})

// 表单验证错误
const errors = reactive({
  username: '',
  nickname: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreedToTerms: ''
})

// 计算属性
const isFormValid = computed(() => {
  return registerForm.username.trim() && 
         registerForm.nickname.trim() && 
         registerForm.email.trim() && 
         registerForm.password.trim() && 
         registerForm.confirmPassword.trim() && 
         registerForm.agreedToTerms &&
         !errors.username && 
         !errors.nickname && 
         !errors.email && 
         !errors.password && 
         !errors.confirmPassword &&
         usernameAvailable.value !== false
})

// 密码强度计算
const passwordStrength = computed(() => {
  const password = registerForm.password
  if (!password) return 'weak'
  
  let strength = 0
  
  // 长度检查
  if (password.length >= 8) strength += 1
  if (password.length >= 12) strength += 1
  
  // 字符类型检查
  if (/[a-z]/.test(password)) strength += 1
  if (/[A-Z]/.test(password)) strength += 1
  if (/[0-9]/.test(password)) strength += 1
  if (/[^a-zA-Z0-9]/.test(password)) strength += 1
  
  if (strength <= 2) return 'weak'
  if (strength <= 4) return 'medium'
  return 'strong'
})

// 表单验证方法
const validateField = (field: string) => {
  const value = registerForm[field as keyof typeof registerForm]
  
  switch (field) {
    case 'username':
      if (!value.trim()) {
        errors.username = '请输入用户名'
      } else if (value.trim().length < 3) {
        errors.username = '用户名至少3个字符'
      } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
        errors.username = '用户名只能包含字母、数字和下划线'
      } else {
        errors.username = ''
      }
      break
      
    case 'nickname':
      if (!value.trim()) {
        errors.nickname = '请输入昵称'
      } else if (value.trim().length < 2) {
        errors.nickname = '昵称至少2个字符'
      } else if (value.trim().length > 20) {
        errors.nickname = '昵称不能超过20个字符'
      } else {
        errors.nickname = ''
      }
      break
      
    case 'email':
      if (!value.trim()) {
        errors.email = '请输入邮箱地址'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        errors.email = '请输入有效的邮箱地址'
      } else {
        errors.email = ''
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
      
    case 'confirmPassword':
      if (!value.trim()) {
        errors.confirmPassword = '请确认密码'
      } else if (value !== registerForm.password) {
        errors.confirmPassword = '两次输入的密码不一致'
      } else {
        errors.confirmPassword = ''
      }
      break
      
    case 'agreedToTerms':
      if (!value) {
        errors.agreedToTerms = '请同意用户协议和隐私政策'
      } else {
        errors.agreedToTerms = ''
      }
      break
  }
}

// 检查用户名可用性
const checkUsernameAvailability = async () => {
  if (!registerForm.username.trim() || errors.username) {
    usernameAvailable.value = null
    return
  }
  
  // 防抖处理
  clearTimeout((window as any).usernameCheckTimeout)
  ;(window as any).usernameCheckTimeout = setTimeout(async () => {
    try {
      // 模拟检查用户名可用性
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // 模拟一些已存在的用户名
      const takenUsernames = ['admin', 'user', 'test', 'demo']
      usernameAvailable.value = !takenUsernames.includes(registerForm.username.toLowerCase())
    } catch (error) {
      usernameAvailable.value = null
    }
  }, 300)
}

// 获取密码强度文本
const getPasswordStrengthText = () => {
  switch (passwordStrength.value) {
    case 'weak': return '弱'
    case 'medium': return '中'
    case 'strong': return '强'
    default: return ''
  }
}

// 注册处理
const handleRegister = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  
  try {
    // 调用用户store的注册方法
    const success = await userStore.register({
      username: registerForm.username,
      nickname: registerForm.nickname,
      email: registerForm.email,
      password: registerForm.password
    })
    
    if (success) {
      globalStore.showMessage('注册成功！', 'success')
      
      // 自动登录
      const loginSuccess = await userStore.login({
        username: registerForm.username,
        password: registerForm.password
      })
      
      if (loginSuccess) {
        router.push('/')
      }
    } else {
      globalStore.showMessage('注册失败，请重试', 'error')
    }
  } catch (error) {
    globalStore.showMessage('注册失败，请重试', 'error')
  } finally {
    loading.value = false
  }
}

// 查看协议和隐私政策
const handleViewTerms = () => {
  showTermsModal.value = true
}

const handleViewPrivacy = () => {
  showPrivacyModal.value = true
}

const handleAgreeTerms = () => {
  registerForm.agreedToTerms = true
  showTermsModal.value = false
  validateField('agreedToTerms')
}

const handleAgreePrivacy = () => {
  registerForm.agreedToTerms = true
  showPrivacyModal.value = false
  validateField('agreedToTerms')
}

// 社交注册处理
const handleSocialRegister = (platform: string) => {
  globalStore.showMessage(`${platform}注册功能开发中`, 'info')
}

// 登录处理
const handleLogin = () => {
  router.push('/login')
}

// 监听用户名变化
watch(() => registerForm.username, () => {
  usernameAvailable.value = null
  validateField('username')
})

// 监听密码变化
watch(() => registerForm.password, () => {
  validateField('password')
  validateField('confirmPassword')
})

// 监听确认密码变化
watch(() => registerForm.confirmPassword, () => {
  validateField('confirmPassword')
})

// 生命周期
onMounted(() => {
  // 如果用户已登录，直接跳转到首页
  if (userStore.isLoggedIn) {
    router.push('/')
  }
})
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
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

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
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

.availability-message {
  font-size: 12px;
  margin-top: 4px;
}

.availability-message.available {
  color: var(--success-color);
}

.availability-message.taken {
  color: var(--error-color);
}

.password-strength {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: var(--border-color);
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
}

.strength-bar.weak .strength-fill {
  width: 33%;
  background: var(--error-color);
}

.strength-bar.medium .strength-fill {
  width: 66%;
  background: var(--warning-color);
}

.strength-bar.strong .strength-fill {
  width: 100%;
  background: var(--success-color);
}

.strength-text {
  font-size: 12px;
  color: var(--text-tertiary);
  min-width: 20px;
}

.agreement-label {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  cursor: pointer;
  margin-top: 8px;
}

.agreement-checkbox {
  width: 16px;
  height: 16px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-primary);
  cursor: pointer;
  margin-top: 2px;
}

.agreement-checkbox.error {
  border-color: var(--error-color);
}

.agreement-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.agreement-link {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  text-decoration: underline;
  font-size: 14px;
}

.register-button {
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
  margin-top: 8px;
}

.register-button:disabled {
  background: var(--text-tertiary);
  cursor: not-allowed;
}

.register-button.loading {
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

.social-register {
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

.login-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.login-link {
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
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content.large {
  max-width: 600px;
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

.terms-content,
.privacy-content {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.terms-content h4,
.privacy-content h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

.terms-content p,
.privacy-content p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.modal-actions {
  display: flex;
  justify-content: center;
}

.agree-btn {
  padding: 12px 32px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-container {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  
  .brand-section {
    display: none;
  }
  
  .form-section {
    padding: 40px 24px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .social-register {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .register-page {
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
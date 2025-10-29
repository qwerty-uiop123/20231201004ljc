import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/main.scss'
// 创建Vue应用
const app = createApp(App)

// 使用状态管理
const pinia = createPinia()
app.use(pinia)

// 使用路由
app.use(router)

// 配置Veaury
app.config.globalProperties.applyReactInVue = applyReactInVue

// 挂载应用
app.mount('#app')
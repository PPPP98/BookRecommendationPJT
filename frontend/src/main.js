import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// axios 기본 설정
axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)

// 라우터 추가
app.use(router)

// 전역 컴포넌트, 플러그인 등록
// app.component('component-name', Component)

// 앱 마운트
app.mount('#app')

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// axios 기본 설정
axios.defaults.baseURL = 'http://localhost:8000'

const pinia = createPinia()
const app = createApp(App)

// 라우터 추가
app.use(pinia)
app.use(router)

// 전역 에러 핸들링
app.config.errorHandler = (err, instance, info) => {
  console.error('전역 에러:', err)
  console.error('컴포넌트 인스턴스:', instance)
  console.error('추가 정보:', info)
  alert('예기치 않은 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
}

// 전역 컴포넌트, 플러그인 등록
// app.component('component-name', Component)

// 앱 마운트
app.mount('#app')

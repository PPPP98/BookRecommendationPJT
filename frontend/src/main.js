import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 글로벌 CSS 또는 스타일 파일 추가 가능

const app = createApp(App)

// 라우터 추가
app.use(router)

// 전역 컴포넌트, 플러그인 등록
// app.component('component-name', Component)

// 앱 마운트
app.mount('#app')

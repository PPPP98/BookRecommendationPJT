<template>
  <div 
    :class="containerClasses"
    @wheel.passive="handleWheel"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @keydown.down="nextPage"
    @keydown.up="prevPage"
    @scroll-to-first="handleScrollToFirst"
    tabindex="0"
    ref="container"
    :data-page="currentPage"
  >
    <div class="pages-wrapper">
      <FirstPage 
        :data-active="currentPage === 0"
        :data-prev="currentPage > 0"
        :data-next="currentPage < 0"
      />
      <SecondPage 
        :data-active="currentPage === 1"
        :data-prev="currentPage > 1"
        :data-next="currentPage < 1"
        :goToFirstPage="() => goToPage(0)"
      />
      <ThirdPage 
        :data-active="currentPage === 2"
        :data-prev="currentPage > 2"
        :data-next="currentPage < 2"
      />
      <FourthPage 
        :data-active="currentPage === 3"
        :data-prev="currentPage > 3"
        :data-next="currentPage < 3"
      />
    </div>
    
    <div class="page-indicators">
      <div 
        v-for="index in totalPages" 
        :key="index"
        class="indicator"
        :class="{ active: currentPage === index - 1 }"
        @click="goToPage(index - 1)"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import FirstPage from './pages/FirstPage.vue'
import SecondPage from './pages/SecondPage.vue'
import ThirdPage from './pages/ThirdPage.vue'
import FourthPage from './pages/FourthPage.vue'
import { useAuthStore } from '../stores/auth'

// Pinia 스토어에서 로그인 상태 가져오기
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

// 페이지 상태 관리
const currentPage = ref(0)
const isAnimating = ref(false)
const totalPages = 4
const container = ref(null)
const touchStartY = ref(0)
const moveDirection = ref('') // 'up' 또는 'down'

// 페이지 컨테이너 클래스 계산
const containerClasses = computed(() => ({
  'main-container': true
}))

// 페이지 이동 함수
const nextPage = () => {
  if (isAnimating.value || currentPage.value >= totalPages - 1) return
  
  isAnimating.value = true
  moveDirection.value = 'up'
  setTimeout(() => { 
    isAnimating.value = false
    moveDirection.value = ''
  }, 500)
  currentPage.value++
}

const prevPage = () => {
  // 로그인 상태에서는 첫 번째 페이지로 이동하지 못하도록 함
  if (isAnimating.value || currentPage.value <= 0 || (isAuthenticated.value && currentPage.value <= 1)) return
  
  isAnimating.value = true
  moveDirection.value = 'down'
  setTimeout(() => { 
    isAnimating.value = false
    moveDirection.value = ''
  }, 500)
  currentPage.value--
}

const goToPage = (page) => {
  if (isAnimating.value || page === currentPage.value) return
  if (isAuthenticated.value && page === 0) return // 로그인 상태에서는 첫 페이지로 가지 못함
  
  isAnimating.value = true
  setTimeout(() => { isAnimating.value = false }, 500)
  currentPage.value = page
}

// 휠 이벤트 처리
const handleWheel = (e) => {
  if (isAnimating.value) return

  if (e.deltaY > 0 && currentPage.value < totalPages - 1) {
    // 아래로 스크롤
    nextPage()
  } else if (e.deltaY < 0 && currentPage.value > 0 && !(isAuthenticated.value && currentPage.value <= 1)) {
    // 위로 스크롤 (로그인 상태에서는 첫 페이지로 가지 못함)
    prevPage()
  }
}

// 터치 이벤트 처리
const handleTouchStart = (e) => {
  touchStartY.value = e.touches[0].clientY
}

const handleTouchMove = (e) => {
  if (isAnimating.value) return
  
  const touchEndY = e.touches[0].clientY
  const diff = touchStartY.value - touchEndY
  
  // 위로 스와이프 (아래로 이동)
  if (diff > 50 && currentPage.value < totalPages - 1) {
    nextPage()
    touchStartY.value = touchEndY
  }
  // 아래로 스와이프 (위로 이동)
  else if (diff < -50 && currentPage.value > 0 && !(isAuthenticated.value && currentPage.value <= 1)) {
    // 로그인 상태에서는 첫 페이지로 가지 못함
    prevPage()
    touchStartY.value = touchEndY
  }
}

// FirstPage로 스크롤하는 이벤트 핸들러
const handleScrollToFirst = (event) => {
  if (event.detail.targetPage === 0) {
    goToPage(0)
  }
}

import { watch } from 'vue'

// 로그인 상태 감시
watch(isAuthenticated, (newValue) => {
  if (newValue && currentPage.value === 0) {
    nextPage()
  }
}, { immediate: true })

onMounted(() => {
  // 앱 초기화 시 인증 상태 복원
  authStore.initializeAuth()
  
  // 키보드 포커스를 컨테이너에 설정
  if (container.value) {
    container.value.focus()
  }
})

</script>

<style scoped>
/* Navbar sticky 옵션 */
:global(.navbar) {
  position: fixed;
  top: 0;
  z-index: 100;
  background: #fff;
  width: 100vw;
  border-bottom: 1px solid #ececec;
  height: var(--navbar-height);
}

.main-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.pages-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: visible;
  padding-top: var(--navbar-height); /* navbar 높이만큼 패딩 추가 */
}

.pages-wrapper > * {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  pointer-events: none;
  will-change: transform, opacity;
  transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
  transform: translateY(100%);
}

/* 첫 번째 페이지는 항상 보임 */
.pages-wrapper > *:first-child {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
  z-index: 1;
}

/* 현재 페이지 표시 */
.pages-wrapper > *[data-active="true"] {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
  z-index: 2;
}

/* 이전 페이지 */
.pages-wrapper > *[data-prev="true"] {
  opacity: 0;
  transform: translateY(-100%);
  z-index: 1;
}

/* 다음 페이지 */
.pages-wrapper > *[data-next="true"] {
  opacity: 0;
  transform: translateY(100%);
  z-index: 1;
}

.page-indicators {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 15px;
  z-index: 100;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  backdrop-filter: blur(5px);
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background-color: white;
  transform: scale(1.2);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .main-container {
    touch-action: none; /* 모바일에서 기본 스크롤 방지 */
  }
  
  .page-indicators {
    right: 10px;
  }
  
  .indicator {
    width: 8px;
    height: 8px;
  }
}
</style>

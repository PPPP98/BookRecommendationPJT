<template>
  <div class="main-page">
    <!-- 왼쪽 이미지 배경 -->
    <ImageGrid />
    
    <!-- 오른쪽 로그인 컨테이너 -->
    <div class="login-section" v-if="!isLoggedIn">
      <LoginModal />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import ImageGrid from '../components/common/ImageGrid.vue';
import LoginModal from '../components/user/LoginModal.vue';

// 로그인 상태 체크 (실제로는 스토어나 API 호출로 구현)
const isLoggedIn = ref(false);

// 실제 구현에서는 Pinia 스토어에서 로그인 상태를 가져옴
// import { useAuthStore } from '../stores/auth'
// const authStore = useAuthStore()
// const isLoggedIn = computed(() => authStore.isLoggedIn)

// import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
// import { Swiper, SwiperSlide } from 'swiper/vue'
// import { Pagination, Navigation } from 'swiper/modules'
// import 'swiper/css'
// import 'swiper/css/pagination'
// import 'swiper/css/navigation'

// const sectionItems = [1, 2, 3, 4, 5]
// const sectionRefs = ref([])
// const sectionRootRef = ref(null)
// const swiperRef = ref(null)

// function setSectionRef(el, idx) {
//   if (el) sectionRefs.value[idx] = el
// }

// let observer = null
// let lastActiveIdx = -1

// onMounted(async () => {
//   await nextTick()
//   observer = new window.IntersectionObserver(
//     (entries) => {
//       let maxRatio = 0
//       let maxIdx = -1
//       entries.forEach((entry) => {
//         const idx = sectionRefs.value.findIndex(el => el === entry.target)
//         if (entry.intersectionRatio > 0.15 && entry.intersectionRatio > maxRatio) {
//           maxRatio = entry.intersectionRatio
//           maxIdx = idx
//         }
//       })
//       if (maxIdx !== -1 && maxIdx !== lastActiveIdx && sectionRefs.value[maxIdx]) {
//         lastActiveIdx = maxIdx
//         sectionRefs.value[maxIdx].scrollIntoView({ behavior: 'smooth' })
//       }
//     },
//     { threshold: [0.15] }
//   )
//   sectionRefs.value.filter(Boolean).forEach(el => observer.observe(el))
// })

// onBeforeUnmount(() => {
//   if (observer) observer.disconnect()
// })

// // Swiper에서 마지막 슬라이드에서 아래로 넘길 때 카드 섹션으로 이동
// function onSlideChange(swiper) {
//   // Swiper의 실제 슬라이드 개수(루프 포함)에서 마지막 "실제" 슬라이드 index 계산
//   // swiper.realIndex는 loop 모드에서도 실제 인덱스를 반환
//   // swiper.slides.length는 루프 슬라이드 포함이므로, slidesPerView=1에서 3개면 3-1=2
//   if (swiper.realIndex === swiper.slides.length - swiper.loopedSlides - 1) {
//     // 마지막 슬라이드에서 아래로 넘기면
//     if (sectionRootRef.value) {
//       sectionRootRef.value.scrollIntoView({ behavior: 'smooth' })
//     }
//   }
// }
</script>

<style scoped>
/* Navbar sticky 옵션 */
:global(.navbar) {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  width: 100vw;
  border-bottom: 1px solid #ececec;
}

.main-page {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  background-color: white;
  justify-content: center;
  align-items: center;
}

.login-section {
  position: absolute;
  top: 50%;
  right: 10%;
  transform: translateY(-50%);
  width: 30%;
  max-width: 450px;
  z-index: 20;
  background-color: transparent; /* 투명 배경으로 변경 */
  border-radius: 10px;
  padding: 0; /* 패딩 제거 */
}

@media (max-width: 1200px) {
  .login-section {
    width: 40%;
  }
}

@media (max-width: 768px) {
  .main-page {
    flex-direction: column;
  }
  
  .login-section {
    width: 90%;
    max-width: 400px;
  }
}
</style>

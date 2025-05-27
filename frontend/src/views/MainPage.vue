<template>
  <div class="main-page">
<<<<<<< HEAD
    <Navbar />
    
    <main class="main-content">
      <div class="hero-section">
        <h1 class="hero-title">AI와 함께하는<br>새로운 도서 탐색</h1>
      </div>

      <div class="banner-section">
        <div class="banner-content">
          <!-- 메인 배너 내용 -->
        </div>
      </div>

      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon square"></div>
          <h3>AI 추천도서</h3>
          <p>개인 맞춤형 도서 추천을 제공합니다</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon circle"></div>
          <h3>베스트셀러 Top10</h3>
          <p>가장 인기있는 도서를 확인하세요</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon triangle"></div>
          <h3>도서 큐레이션</h3>
          <p>관심사별 엄선된 도서 컬렉션</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon square"></div>
          <h3>독서 커뮤니티</h3>
          <p>다른 독자들과 의견을 나누세요</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon circle"></div>
          <h3>근처 도서관</h3>
          <p>가까운 도서관을 찾아보세요</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon triangle"></div>
          <h3>도서 리뷰</h3>
          <p>상세한 도서 리뷰를 확인하세요</p>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import { useBooksStore } from '@/stores/books'
import { onMounted } from 'vue'

export default {
  name: 'MainPage',
  components: {
    Navbar,
    Footer,
  },
  setup() {
    const booksStore = useBooksStore()

    onMounted(async () => {
      try {
        await booksStore.fetchBooks()
        await booksStore.fetchCategories()
        // threadsStore.fetchThreads() 호출 제거됨
      } catch (error) {
        console.error('Error loading data:', error)
      }
    })

    return {
      books: booksStore.books,
      categories: booksStore.categories,
      // threads: threadsStore.threads, // 완전히 제거
    }
  }
}
</script>

<style scoped>
.main-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-section {
  text-align: left;
  padding: 2rem 0;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  line-height: 1.3;
}

.banner-section {
  background-color: #f1f3f5;
  border-radius: 12px;
  height: 300px;
  margin: 2rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.feature-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 1.5rem;
}

.feature-icon.square {
  background-color: #e9ecef;
}

.feature-icon.circle {
  background-color: #e9ecef;
  border-radius: 50%;
}

.feature-icon.triangle {
  background-color: #e9ecef;
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.feature-card p {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .main-content {
    padding: 1.5rem;
  }
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 1.8rem;
  }
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.5rem;
  }
  .feature-card {
    padding: 1rem;
  }
}

/* 애니메이션 효과 */
.hero-title {
  animation: fadeIn 1s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
=======
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
>>>>>>> dc8ae51dd3168e30110089178adc633091541404
  }
}
</style>

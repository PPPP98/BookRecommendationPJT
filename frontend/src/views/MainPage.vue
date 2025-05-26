<template>
  <div class="main-page">
    <Navbar />
    <main class="main-content">
      <div class="hero-section">
        <h1 class="hero-title">AI와 함께하는<br>새로운 도서 탐색</h1>
      </div>
      <!-- Swiper 배너 (전체화면) -->
      <div
        class="banner-section-fullscreen"
        ref="swiperBannerRef"
        @wheel="onBannerWheel"
        @touchstart.passive="onTouchStart"
        @touchmove.passive="onTouchMove"
      >
        <Swiper
          :modules="[Pagination, Autoplay]"
          :pagination="{ clickable: true }"
          :autoplay="{ delay: 3500, disableOnInteraction: false }"
          loop
        >
          <SwiperSlide v-for="(banner, idx) in banners" :key="idx">
            <div class="banner-content-fullscreen">
              <img v-if="banner.img" :src="banner.img" alt="" class="h-40 w-40 md:h-60 md:w-60 mb-8 rounded-2xl object-cover shadow-xl" />
              <div class="text-center">
                <div class="text-3xl md:text-5xl font-extrabold mb-4">{{ banner.title }}</div>
                <div class="text-lg md:text-2xl text-gray-600">{{ banner.desc }}</div>
              </div>
            </div>
          </SwiperSlide>
        </Swiper>
      </div>
      <!-- 카드 섹션 -->
      <div class="features-fullscreen" ref="featuresRef">
        <section
          v-for="(feature, idx) in features"
          :key="idx"
          :id="feature.id"
          ref="featureRefs"
          :class="[
            'feature-card-fullscreen',
            isVisible[idx] ? 'opacity-100' : 'opacity-0',
            'transition-opacity duration-1000'
          ]"
        >
          <div :class="['feature-icon', feature.iconClass]"></div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Navbar from '@/components/common/Navbar.vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination, Autoplay } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'

const banners = [
  {
    title: '신규 회원 AI 추천 큐레이션 오픈!',
    desc: '가입만 해도 나만의 책 추천이 바로 시작됩니다.',
    img: 'https://bookshelf-snowy.vercel.app/_next/static/media/hero-bookshelf.6e7f1c2f.svg'
  },
  {
    title: '베스트셀러 업데이트',
    desc: '실시간 인기 도서를 한눈에!',
    img: 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=200&q=80'
  },
  {
    title: '커뮤니티에서 독서 친구를 만나보세요',
    desc: '책을 좋아하는 사람들과 소통하고 공유하세요.',
    img: 'https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=200&q=80'
  }
]

const features = [
  { id: 'feature-ai', iconClass: 'square', title: 'AI 추천도서', desc: '개인 맞춤형 도서 추천을 제공합니다' },
  { id: 'feature-best', iconClass: 'circle', title: '베스트셀러 Top10', desc: '가장 인기있는 도서를 확인하세요' },
  { id: 'feature-curation', iconClass: 'triangle', title: '도서 큐레이션', desc: '관심사별 엄선된 도서 컬렉션' },
  { id: 'feature-community', iconClass: 'square', title: '독서 커뮤니티', desc: '다른 독자들과 의견을 나누세요' },
  { id: 'feature-library', iconClass: 'circle', title: '근처 도서관', desc: '가까운 도서관을 찾아보세요' },
  { id: 'feature-thread', iconClass: 'triangle', title: '인기 쓰레드', desc: '상세한 도서 리뷰를 확인하세요' },
]

// Intersection Observer
const featureRefs = ref([])
const isVisible = ref(features.map(() => false))
let observer

onMounted(() => {
  observer = new window.IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const idx = featureRefs.value.findIndex((el) => el === entry.target)
        if (idx !== -1) {
          isVisible.value[idx] = entry.isIntersecting
        }
      })
    },
    { threshold: 0.4 }
  )
  featureRefs.value.forEach((el) => el && observer.observe(el))
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
})

// --- 스와이프 배너에서 아래로 스크롤 시 자동 이동 기능 ---
const swiperBannerRef = ref(null)
const featuresRef = ref(null)
let touchStartY = 0

function onBannerWheel(e) {
  if (e.deltaY > 0) {
    e.preventDefault()
    scrollToFeatures()
  }
}
function onTouchStart(e) {
  if (e.touches && e.touches.length === 1) {
    touchStartY = e.touches[0].clientY
  }
}
function onTouchMove(e) {
  if (e.touches && e.touches.length === 1) {
    const moveY = e.touches[0].clientY
    if (touchStartY && moveY - touchStartY < -30) { // 아래로 스와이프
      scrollToFeatures()
      touchStartY = 0 // 한 번만 동작
    }
  }
}
function scrollToFeatures() {
  if (featuresRef.value) {
    featuresRef.value.scrollIntoView({ behavior: 'smooth' })
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
/* Swiper 전체화면 배너 */
.banner-section-fullscreen {
  width: 100vw;
  height: 100vh;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  background: #f1f3f5;
  border-radius: 0;
  margin-bottom: 3rem;
  z-index: 1;
}
.swiper, .swiper-container {
  width: 100vw !important;
  height: 100vh !important;
}
.swiper-slide {
  width: 100vw !important;
  height: 100vh !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.banner-content-fullscreen {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: none;
  padding: 2rem;
  box-sizing: border-box;
}
@media (max-width: 768px) {
  .banner-content-fullscreen {
    padding: 1rem;
  }
}

/* ===== 카드 전체화면(가로세로) ===== */
.features-fullscreen {
  width: 100vw;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  height: 100vh;
  background: #f8f9fa;
}
.feature-card-fullscreen {
  width: 100vw;
  height: 100vh;
  margin: 0;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  scroll-snap-align: start;
  opacity: 0;
  transition: opacity 1s;
  box-shadow: 0 0 32px 0 rgba(0,0,0,0.03);
}
.opacity-100 {
  opacity: 1 !important;
}
.opacity-0 {
  opacity: 0 !important;
}
.feature-card-fullscreen h3 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  color: #23243a;
}
.feature-card-fullscreen p {
  color: #666;
  font-size: 1.2rem;
  line-height: 1.5;
  text-align: center;
  max-width: 400px;
}
.feature-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 2.2rem;
  background-color: #e9ecef;
  display: block;
}
.feature-icon.square {
  border-radius: 16px;
}
.feature-icon.circle {
  border-radius: 50%;
}
.feature-icon.triangle {
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}
@media (max-width: 900px) {
  .feature-card-fullscreen h3 { font-size: 1.4rem; }
  .feature-card-fullscreen p { font-size: 1rem; }
  .feature-icon { width: 56px; height: 56px; }
}
@media (max-width: 600px) {
  .feature-card-fullscreen { padding: 1.5rem; }
  .feature-card-fullscreen h3 { font-size: 1.1rem; }
  .feature-icon { width: 40px; height: 40px; }
}
</style>

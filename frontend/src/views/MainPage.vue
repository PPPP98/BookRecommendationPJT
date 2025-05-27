<template>
  <div>
    <Navbar />
    <!-- Swiper 슬라이더 -->
    <Swiper
      ref="swiperRef"
      :modules="[Pagination, Navigation]"
      :pagination="{ clickable: true }"
      :navigation="true"
      loop
      class="swiper-container"
      @slideChange="onSlideChange"
    >
      <SwiperSlide v-for="n in 3" :key="n" class="swiper-slide">
        슬라이드{{ n }}
      </SwiperSlide>
    </Swiper>

    <!-- 카드 섹션 -->
    <div class="section" ref="sectionRootRef">
      <div
        v-for="(item, idx) in sectionItems"
        :key="idx"
        :ref="el => setSectionRef(el, idx)"
        :class="['section-wrapper', `section-wrapper-${idx+1}`]"
      >
        <div class="image">이미지</div>
        <div class="text">텍스트</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination, Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'
import Navbar from '@/components/common/Navbar.vue'

const sectionItems = [1, 2, 3, 4, 5]
const sectionRefs = ref([])
const sectionRootRef = ref(null)
const swiperRef = ref(null)

function setSectionRef(el, idx) {
  if (el) sectionRefs.value[idx] = el
}

let observer = null
let lastActiveIdx = -1

onMounted(async () => {
  await nextTick()
  observer = new window.IntersectionObserver(
    (entries) => {
      let maxRatio = 0
      let maxIdx = -1
      entries.forEach((entry) => {
        const idx = sectionRefs.value.findIndex(el => el === entry.target)
        if (entry.intersectionRatio > 0.15 && entry.intersectionRatio > maxRatio) {
          maxRatio = entry.intersectionRatio
          maxIdx = idx
        }
      })
      if (maxIdx !== -1 && maxIdx !== lastActiveIdx && sectionRefs.value[maxIdx]) {
        lastActiveIdx = maxIdx
        sectionRefs.value[maxIdx].scrollIntoView({ behavior: 'smooth' })
      }
    },
    { threshold: [0.15] }
  )
  sectionRefs.value.filter(Boolean).forEach(el => observer.observe(el))
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
})

// Swiper에서 마지막 슬라이드에서 아래로 넘길 때 카드 섹션으로 이동
function onSlideChange(swiper) {
  // Swiper의 실제 슬라이드 개수(루프 포함)에서 마지막 "실제" 슬라이드 index 계산
  // swiper.realIndex는 loop 모드에서도 실제 인덱스를 반환
  // swiper.slides.length는 루프 슬라이드 포함이므로, slidesPerView=1에서 3개면 3-1=2
  if (swiper.realIndex === swiper.slides.length - swiper.loopedSlides - 1) {
    // 마지막 슬라이드에서 아래로 넘기면
    if (sectionRootRef.value) {
      sectionRootRef.value.scrollIntoView({ behavior: 'smooth' })
    }
  }
}
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

/* Swiper */
.swiper-container{
  width:100vw;
  height:100vh;
  overflow: hidden;
}
.swiper-slide{
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
}
/* 카드 섹션 */
.section{
  width:100vw;
  height:100vh;
  overflow-y: auto;
}
.section-wrapper{
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  gap:10px;
  background-color: #E1E1E1;
  transition: background 0.3s, box-shadow 0.3s, transform 0.3s;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  border-radius: 24px;
  cursor: pointer;
}
.section-wrapper:hover {
  box-shadow: 0 12px 32px rgba(0,0,0,0.18);
  transform: scale(1.03);
}

.section-wrapper-1 { background-color: #E1E1E1; }
.section-wrapper-2 { background-color: #FDE68A; }
.section-wrapper-3 { background-color: #A7F3D0; }
.section-wrapper-4 { background-color: #BFDBFE; }
.section-wrapper-5 { background-color: #FCA5A5; }

.image {
  background: #fff;
  border-radius: 12px;
  width: 300px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  transition: box-shadow 0.3s;
}
.section-wrapper:hover .image {
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}

.text {
  font-size: 2rem;
  font-weight: 600;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  transition: box-shadow 0.3s;
}
.section-wrapper:hover .text {
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
</style>

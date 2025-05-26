<template>
  <div>
    <Navbar />
    <!-- Swiper 슬라이더 -->
    <Swiper
      :modules="[Pagination, Navigation]"
      :pagination="{ clickable: true }"
      :navigation="true"
      loop
      class="swiper-container"
    >
      <SwiperSlide v-for="n in 3" :key="n" class="swiper-slide">
        슬라이드{{ n }}
      </SwiperSlide>
    </Swiper>

    <!-- 카드 섹션 -->
    <div class="section">
      <div
        v-for="(item, idx) in sectionItems"
        :key="idx"
        :class="['section-wrapper', `section-wrapper-${idx+1}`]"
      >
        <div class="image">이미지</div>
        <div class="text">텍스트</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination, Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'
import Navbar from '@/components/common/Navbar.vue'

const sectionItems = [1, 2, 3, 4, 5]
</script>

<style scoped>
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
.section{
  width:100vw;
  height:100vh;
}
.section-wrapper{
  width: 100%;
  height: 100%;
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

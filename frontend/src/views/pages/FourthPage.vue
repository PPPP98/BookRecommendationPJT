<template>
  <div class="page fourth-page">
    <div class="content">
      <h1>독서 커뮤니티</h1>
      <p>다른 독자들과 함께 이야기를 나누어보세요</p>
      <div class="community-features">
        <router-link 
          v-for="(feature, index) in features" 
          :key="index" 
          :to="feature.path" 
          class="feature-card"
        >
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </router-link>
      </div>
    
      <div class="map-container">
        <img :class="['slide-top', 'map', { active: isFourth }]" src="/map.png" alt="지도">
      </div>
      <img :class="['fade-in-top', 'pin', { active: isFourth }]" src="/pin.png" alt="핀">
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

// 라우터 인스턴스 가져오기
const router = useRouter();

interface Feature {
  title: string;
  description: string;
  path: string; // 라우터 경로 속성 추가
}

// prop 정의
const props = defineProps({
  isFourth: {
    type: Boolean,
    default: false
  }
});

const features: Feature[] = [
  {
    title: '내 서재',
    description: '좋아하는 책을 모아보세요',
    path: '/mypage'
  },
  {
    title: '도서관 찾기',
    description: '대여 가능한 도서를 가까운 도서관에서 찾아보세요',
    path: '/library'
  },
  {
    title: '커뮤니티',
    description: '다른 독자들과 소통하고 의견을 나누세요',
    path: '/community'
  }
];
</script>

<style scoped>
.page {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #f1f3f5;
}

.content {
  padding: 2rem;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
  margin-top: 50px;
}

.community-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit; /* 링크 색상 상속 */
  display: block; /* 블록 요소로 표시 */
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

p {
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.pin {
  position: absolute;
  top: 55%;
  left: center;
  opacity: 0; /* 초기에는 숨김 상태 */
}

.map-container {
  position: relative;
  width: 100%;
  margin-top: 2rem;
  overflow: hidden;
}

.map {
  width: 100%;
  opacity: 0; /* 초기에는 숨김 상태 */
}

/* 애니메이션 정의 */
@keyframes slide-top {
  0% {
    transform: translateY(100px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fade-in-top {
  0% {
    transform: translateY(-30px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 애니메이션 클래스 */
.slide-top.active {
  animation: slide-top 1s ease forwards;
}

.fade-in-top.active {
  animation: fade-in-top 1.2s ease 0.5s forwards;
}

@media (max-width: 768px) {
  .community-features {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .content {
    padding: 1rem;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
}
</style>

<template>
  <div class="page fourth-page">
    <div class="content">
      <h1>독서 커뮤니티</h1>
      <p>다른 독자들과 함께 이야기를 나누어보세요</p>
      <div class="community-features">
        <div v-for="(feature, index) in features" :key="index" class="feature-card">
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Feature {
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    title: '독서 토론',
    description: '다양한 주제로 이야기를 나누세요'
  },
  {
    title: '독후감 공유',
    description: '나만의 독서 경험을 공유하세요'
  },
  {
    title: '독서 모임',
    description: '함께 읽고 토론하는 즐거움'
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
  transition: transform 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-5px);
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

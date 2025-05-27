<template>
  <div class="page third-page">
    <div class="content">
      <h1>도서 카테고리</h1>
      <p class="subtitle">관심있는 도서 카테고리를 선택하세요</p>
      <div class="category-grid">
        <div 
          v-for="category in categories" 
          :key="category.id" 
          class="category-card"
          @click="selectCategory(category)"
        >
          <h3>{{ category.name }}</h3>
          <p>{{ category.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const categories = ref([
  { id: 1, name: '소설', description: '다양한 장르의 소설을 만나보세요', path: '/books/fiction' },
  { id: 2, name: '자기계발', description: '더 나은 삶을 위한 인사이트', path: '/books/self-improvement' },
  { id: 3, name: '과학/기술', description: '세상을 이해하는 새로운 관점', path: '/books/science' },
  { id: 4, name: '예술/디자인', description: '창의적 영감을 주는 작품들', path: '/books/art' }
])

const selectCategory = (category) => {
  router.push(category.path)
}
</script>

<style scoped>
.page {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content {
  padding: 2rem;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.category-card {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.category-card:hover {
  transform: translateY(-5px);
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .content {
    padding: 1rem;
  }
  
  .category-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
}
</style>

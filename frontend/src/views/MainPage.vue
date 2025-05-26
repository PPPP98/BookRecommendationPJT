<template>
  <div class="main-page">
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
  }
}
</style>

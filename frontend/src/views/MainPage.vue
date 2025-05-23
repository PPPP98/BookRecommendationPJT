<!-- 
  MainPage 컴포넌트
  역할: 웹사이트의 메인 랜딩 페이지
  기능:
    - 추천 도서, 베스트셀러, 신작 도서 목록 표시
    - 인기 쓰레드, 팔로우 쓰레드 표시
    - 도서 검색 기능
    - 카테고리 바로가기
  데이터 구조:
    - books: Array - 도서 목록
    - threads: Array - 쓰레드 목록
    - categories: Array - 카테고리 목록
-->
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

export default {
  name: 'MainPage',
  components: {
    Navbar,
    Footer,
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
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
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

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
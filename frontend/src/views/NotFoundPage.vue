<!-- 
  NotFoundPage 컴포넌트
  역할: 존재하지 않는 페이지에 접근했을 때 표시되는 404 페이지
-->
<template>
  <div class="not-found-page">
    <Navbar />
    
    <main class="main-content">
      <div class="error-container">
        <div class="error-code">404</div>
        <h1>페이지를 찾을 수 없습니다</h1>
        <p>요청하신 페이지가 존재하지 않거나, 삭제되었거나, 주소가 변경되었을 수 있습니다.</p>
        <div class="actions">
          <button @click="$router.push('/')" class="home-button">홈으로 이동</button>
          <button @click="$router.back()" class="back-button">이전 페이지로</button>
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
  name: 'NotFoundPage',
  components: {
    Navbar,
    Footer
  }
}
</script>

<style scoped>
.not-found-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.error-container {
  text-align: center;
  max-width: 500px;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: #e9ecef;
  margin-bottom: 1rem;
}

h1 {
  margin-bottom: 1rem;
}

p {
  color: #6c757d;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.home-button, .back-button {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.home-button {
  background: #0066cc;
  color: white;
  border: none;
}

.back-button {
  background: white;
  border: 1px solid #ddd;
}
</style>

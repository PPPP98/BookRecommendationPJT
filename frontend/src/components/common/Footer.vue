<!-- 
  Footer 컴포넌트
  역할: 웹사이트의 하단에 표시되는 공통 푸터
  데이터: 정적 데이터 (회사 정보, 링크 등)
-->
<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>도서 추천 서비스</h3>
        <p>&copy; 2025 Book Recommendation. All rights reserved.</p>
      </div>
      <div class="footer-section">
        <h4>링크</h4>
        <ul>
          <li><a href="/">홈</a></li>
          <li><a href="/about">소개</a></li>
          <li><a href="/contact">문의하기</a></li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  padding: 2rem;
  background-color: #f5f5f5;
  margin-top: 2rem;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section {
  margin: 0 1rem;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section a {
  text-decoration: none;
  color: #333;
}
</style>

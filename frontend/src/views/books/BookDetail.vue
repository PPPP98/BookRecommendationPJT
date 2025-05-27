<template>
  <div class="book-detail-page">
    <main class="main-content" v-if="book">
      <div class="book-header-flex">
        <!-- 왼쪽: 책 정보, 액션, 섹션 (30px 아래로) -->
        <div class="book-info-col lowered">
          <div class="book-title">{{ book.title }}</div>
          <div v-if="book.subTitle" class="book-subtitle">{{ book.subTitle }}</div>
          <div class="book-author">{{ book.author }}</div>
          <br>
          <div class="book-meta-row">
            <span v-if="book.publisher">출판사: {{ book.publisher }}</span>
            <span v-if="book.pub_date"> | 출간일: {{ book.pub_date }}</span>
            <span v-if="book.category_name"> <br><br> 카테고리: {{ book.category_name }}</span>
          </div>
          <div class="book-rating-row" v-if="book.customer_review_rank">
            평점: <span class="stars">{{ generateStars(book.customer_review_rank) }}</span>
            <span class="score">{{ book.customer_review_rank }}/5</span>
          </div>
          <div class="book-actions-row">
            <button
              class="like-btn"
              :class="{ liked: book.is_liked }"
              @click="toggleLike"
              :disabled="likeLoading"
            >
              <span class="heart">{{ book.is_liked ? '❤️' : '🤍' }}</span>
              {{ book.like_count }}
            </button>
            <button class="write-btn" @click="navigateToThreadWrite">
              이 책으로 글쓰기
            </button>
          </div>
          
        </div>
        <!-- 오른쪽: 책 표지 -->
        <div class="book-cover-col">
          <img
            v-if="book.cover"
            :src="book.cover"
            :alt="book.title"
            class="book-cover-img"
            @error="onImgError"
          />
          <div v-else class="book-cover-placeholder"></div>
        </div>
      </div>

      <!-- 상세 설명(10줄 초과 ... + 더보기) -->
      <section class="book-description-section">
        <h3>상세 설명</h3>
        <div
          class="book-description"
          :class="{ collapsed: !descExpanded && isDescLong }"
          ref="descRef"
        >
          {{ book.description || '책에 대한 설명이 없습니다.' }}
        </div>
        <button
          v-if="isDescLong"
          class="desc-toggle-btn"
          @click="descExpanded = !descExpanded"
        >
          {{ descExpanded ? '접기' : '더보기' }}
        </button>
      </section>

      <!-- 저자 소개 -->
      <section class="author-info-section" v-if="book.author_info">
        <h3>저자 소개</h3>
        <div class="author-profile">
          <img
            v-if="book.author_photo"
            :src="book.author_photo"
            :alt="book.author"
            class="author-photo"
            @error="onImgError"
          />
          <p>{{ book.author_info }}</p>
        </div>
      </section>

      <!-- 커뮤니티 글 목록 -->
      <section class="book-threads-section">
        <h3>이 책의 커뮤니티 글<span v-if="book.thread_count"> ({{ book.thread_count }})</span></h3>
        <ul v-if="book.threads && book.threads.length">
          <li v-for="thread in book.threads" :key="thread.id" class="thread-list-item">
            <router-link :to="`/threads/${thread.id}`" class="thread-title-link">{{ thread.title }}</router-link>
          </li>
        </ul>
        <div v-else class="empty-state">아직 작성된 글이 없습니다.</div>
      </section>

      <!-- 유사 도서 -->
      <section class="similar-books-section" v-if="book.similar_books && book.similar_books.length">
        <h3>유사 도서</h3>
        <div class="similar-books-list">
          <div
            class="similar-book-card"
            v-for="sim in book.similar_books"
            :key="sim.id"
            @click="navigateToBook(sim.id)"
          >
            <img :src="sim.cover" :alt="sim.title" class="similar-book-cover" @error="onImgError" />
            <div class="similar-book-title">{{ sim.title }}</div>
            <div class="similar-book-author">{{ sim.author }}</div>
            <div class="similar-book-category">{{ sim.category_name }}</div>
            <div class="similarity-score">유사도: {{ (sim.similarity_score * 100).toFixed(1) }}%</div>
          </div>
        </div>
      </section>
      <footer class="footer-section">
        <div>© 2024 모든 권리 보유</div>
      </footer>
    </main>
    <ErrorPage v-else-if="error" type="error" :message="error" />
    <ErrorPage v-else type="loading" message="도서 정보를 불러오는 중입니다." />
  </div>
</template>

<script>
import axios from 'axios'
import ErrorPage from '@/components/common/ErrorPage.vue'

export default {
  name: 'BookDetail',
  components: { ErrorPage },
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      book: null,
      error: null,
      likeLoading: false,
      descExpanded: false,
      isDescLong: false
    }
  },
  methods: {
    async fetchBook() {
      try {
        const response = await axios.get(`/api/books/${this.id}/`)
        this.book = response.data
        this.error = null
        this.$nextTick(this.checkDescLong)
      } catch (err) {
        if (err.response && err.response.status === 404) {
          this.error = '도서를 찾을 수 없습니다.'
        } else {
          this.error = '도서 정보를 불러오는데 실패했습니다.'
        }
        this.book = null
      }
    },
    async toggleLike() {
      if (!this.book) return
      this.likeLoading = true
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          alert('로그인이 필요합니다.')
          this.$router.push('/auth/login')
          return
        }
        const response = await axios.post(
          `/api/books/${this.book.id}/like/`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.book.is_liked = response.data.liked
        this.book.like_count = response.data.like_count
      } catch (err) {
        alert('좋아요 처리 중 오류가 발생했습니다.')
      } finally {
        this.likeLoading = false
      }
    },
    navigateToThreadWrite() {
      this.$router.push({ name: 'ThreadWrite', params: { bookId: this.book.id } })
    },
    navigateToBook(bookId) {
      // 스크롤을 맨 위로 이동하고 새 도서 데이터 로드
      window.scrollTo({ top: 0, behavior: 'smooth' })
      this.$router.push(`/books/${bookId}/`)
    },
    onImgError(e) {
      e.target.src = 'https://cdn-icons-png.flaticon.com/512/29/29302.png'
    },
    generateStars(rank) {
      const val = Math.round(rank || 0)
      const filled = Math.min(5, Math.max(0, val))
      return '★'.repeat(filled) + '☆'.repeat(5 - filled)
    },
    checkDescLong() {
      // 10줄 초과면 isDescLong = true
      const ref = this.$refs.descRef
      if (!ref) {
        this.isDescLong = false
        return
      }
      // 줄 수 계산: <div>의 scrollHeight / lineHeight
      const style = window.getComputedStyle(ref)
      const lineHeight = parseFloat(style.lineHeight)
      const lines = Math.round(ref.scrollHeight / lineHeight)
      this.isDescLong = lines > 10
    }
  },
  watch: {
    'book.description': function () {
      this.$nextTick(this.checkDescLong)
    },
    '$route.params.id': function(newId) {
      this.fetchBook()
    }
  },
  mounted() {
    this.fetchBook()
  }
}
</script>

<style scoped>
.book-detail-page {
  min-height: 100vh;
  background: #fff;
  color: #222;
  font-family: 'Pretendard', 'Inter', Arial, sans-serif;
}
.main-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2.7rem 1.2rem 0 1.2rem;
}
.book-header-flex {
  display: flex;
  align-items: flex-start;
  gap: 3.5rem;
  margin-bottom: 2.7rem;
}
/* 오른쪽: 표지 */
.book-cover-col {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
}
.book-cover-img {
  width: 500px;
  height: 500px;
  object-fit: cover;
  border-radius: 10px;
  background: #f5f5f5;
  margin-top: 30px;
}
.book-cover-placeholder {
  width: 500px;
  height: 500px;
  background: repeating-linear-gradient(
    45deg, #eee, #eee 10px, #fff 10px, #fff 20px
  );
  border-radius: 10px;
  margin-top: 30px;
}
/* 왼쪽: 정보 (30px 아래로) */
.book-info-col.lowered {
  flex: 1.2;
  min-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  position: relative;
  top: 60px;
}
.book-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.1rem;
  letter-spacing: -0.01em;
}
.book-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 0.3rem;
}
.book-author {
  font-size: 1.1rem;
  color: #aaa;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.book-meta-row {
  font-size: 0.95rem;
  color: #888;
  margin-bottom: 0.5rem;
}
.book-rating-row {
  font-size: 1.01rem;
  color: #1976d2;
  margin-bottom: 0.7rem;
}
.stars {
  color: #f7b500;
  margin-right: 0.5em;
}
.score {
  color: #1976d2;
  font-weight: 700;
}
.book-actions-row {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin: 1.1rem 0 0.7rem 0;
}
.like-btn {
  background: #fff;
  color: #dc3545;
  border: none;
  font-size: 0.99rem;
  font-weight: 700;
  border-radius: 16px;
  padding: 0.45em 1.3em;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  display: flex;
  align-items: center;
  gap: 0.5em;
}
.like-btn.liked {
  background: #ffeaea;
}
.like-btn .heart {
  font-size: 1.1em;
}
.write-btn {
  background: #222;
  color: #fff;
  border: none;
  border-radius: 16px;
  padding: 0.45em 1.3em;
  font-weight: 600;
  font-size: 0.99rem;
  margin-left: 0.6rem;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
}
.write-btn:hover {
  background: #444;
}
.section-list {
  margin: 1.3rem 0 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  gap: 1.1rem;
  color: #888;
  font-size: 1.01rem;
}
.section-list li:before {
  content: '▣';
  margin-right: 0.5em;
  color: #ccc;
}
.book-description-section {
  margin-bottom: 2.2rem;
}
.book-description {
  font-size: 1.01rem;
  color: #333;
  line-height: 1.7;
  max-width: 700px;
  margin-bottom: 0.7rem;
  white-space: pre-line;
  transition: max-height 0.2s;
}
.book-description.collapsed {
  display: -webkit-box;
  -webkit-line-clamp: 10;
  -webkit-box-orient: vertical;
  overflow: hidden;
  max-height: 22em;
}
.desc-toggle-btn {
  background: #f5f5f5;
  color: #1976d2;
  border: none;
  border-radius: 8px;
  padding: 0.35em 1.2em;
  font-size: 0.97rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 0.7rem;
  margin-top: 0.2rem;
}
.desc-toggle-btn:hover {
  background: #e3eaf3;
}
.author-info-section {
  margin-bottom: 2.2rem;
}
.author-profile {
  display: flex;
  align-items: flex-start;
  gap: 1.2rem;
  margin-top: 0.5rem;
}
.author-photo {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  background: #f5f5f5;
}
.book-threads-section {
  margin-bottom: 2.2rem;
}
.thread-list-item {
  background: #f8f9fa;
  padding: 0.8rem 1rem;
  margin-bottom: 0.8rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.thread-list-item:hover {
  background: #f1f3f5;
  box-shadow: 0 2px 5px rgba(0,0,0,0.08);
  transform: translateY(-1px);
}
.thread-title-link {
  color: #1976d2;
  font-weight: 600;
  text-decoration: none;
  display: block;
  font-size: 1.02rem;
}
.thread-title-link:hover {
  text-decoration: none;
  color: #1565c0;
}
.empty-state {
  color: #888;
  font-size: 0.98rem;
  margin-top: 0.7rem;
}
.similar-books-section {
  margin-bottom: 2.2rem;
}
.similar-books-list {
  display: flex;
  gap: 1.3rem;
  flex-wrap: wrap;
}
.similar-book-card {
  width: 170px;
  background: #fafbfc;
  border-radius: 10px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.04);
  padding: 1rem 0.7rem 0.7rem 0.7rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 0.13s;
}
.similar-book-card:hover {
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.13);
}
.similar-book-cover {
  width: 90px;
  height: 120px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 0.7rem;
}
.similar-book-title {
  font-size: 1.01rem;
  font-weight: 700;
  color: #222;
  text-align: center;
  margin-bottom: 0.2rem;
  white-space: normal;
  word-break: break-all;
}
.similar-book-author {
  font-size: 0.93rem;
  color: #888;
  margin-bottom: 0.1rem;
  text-align: center;
}
.similar-book-category {
  font-size: 0.9rem;
  color: #bbb;
  margin-bottom: 0.1rem;
  text-align: center;
}
.similarity-score {
  font-size: 0.9rem;
  color: #1976d2;
  margin-top: 0.2rem;
  text-align: center;
}
.footer-section {
  margin-top: 3.5rem;
  color: #bbb;
  font-size: 0.95rem;
  text-align: left;
  padding-bottom: 1.8rem;
}
@media (max-width: 1100px) {
  .main-content { padding: 1.2rem 0.2rem 0 0.2rem; }
  .book-header-flex { flex-direction: column; gap: 1.5rem; }
  .book-cover-col { justify-content: flex-start; }
  .book-cover-img,
  .book-cover-placeholder { width: 320px; height: 320px; }
}
@media (max-width: 700px) {
  .main-content { padding: 0.5rem 0.1rem 0 0.1rem; }
  .book-cover-img,
  .book-cover-placeholder { width: 180px; height: 180px; }
  .similar-books-list { gap: 0.7rem; }
  .similar-book-card { width: 120px; padding: 0.5rem 0.2rem 0.3rem 0.2rem; }
}
</style>

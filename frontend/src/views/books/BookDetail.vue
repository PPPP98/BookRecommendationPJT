<template>
  <div class="book-detail-page">
    <Navbar />

    <main class="main-content" v-if="book">
      <div class="book-header">
        <img :src="book.cover" :alt="book.title" class="book-cover" />
        <div class="book-meta">
          <h1>{{ book.title }}</h1>
          <h2 v-if="book.subTitle" class="subtitle">{{ book.subTitle }}</h2>
          <div class="book-author">
            <span>저자: {{ book.author }}</span>
            <span v-if="book.publisher" class="publisher">| 출판사: {{ book.publisher }}</span>
            <span v-if="book.pub_date" class="pub-date">| 출간일: {{ book.pub_date }}</span>
          </div>
          <div class="book-category">카테고리: {{ book.category_name }}</div>
          <div class="book-rating" v-if="book.customer_review_rank">
            평점: {{ book.customer_review_rank }} / 5
          </div>
          <div class="book-likes-action">
            <button
              class="like-button"
              :class="{ liked: book.is_liked }"
              @click="toggleLike"
              :disabled="likeLoading"
            >
              <span class="heart">
                {{ book.is_liked ? '❤️' : '🤍' }}
              </span>
              <span class="like-count">{{ book.like_count }}</span>
              <span class="like-label">좋아요</span>
            </button>
          </div>
        </div>
      </div>

      <div class="book-description">
        <h3>상세 설명</h3>
        <p>{{ book.description }}</p>
      </div>

      <div class="author-info" v-if="book.author_info">
        <h3>저자 소개</h3>
        <div class="author-profile">
          <img v-if="book.author_photo" :src="book.author_photo" :alt="book.author" class="author-photo" />
          <p>{{ book.author_info }}</p>
        </div>
      </div>

      <div class="book-actions">
        <button class="thread-write-button" @click="navigateToThreadWrite">
          이 책으로 커뮤니티 글 작성
        </button>
      </div>

      <!-- 작성된 커뮤니티 글 목록 -->
      <div class="book-threads" v-if="book.threads && book.threads.length">
        <h3>이 책의 커뮤니티 글 ({{ book.thread_count }})</h3>
        <ul>
          <li v-for="thread in book.threads" :key="thread.id">
            <router-link :to="`/threads/${thread.id}`">{{ thread.title }}</router-link>
            <span class="thread-author">({{ thread.comment_count }})</span>
            <span class="thread-author">추천수: {{ thread.like_count }}</span>
            <span class="thread-author">작성자: {{ thread.user.nickname }}</span>
          </li>
        </ul>
      </div>
      <div class="book-threads" v-else>
        <h3>이 책의 커뮤니티 글</h3>
        <div class="empty-state">아직 작성된 글이 없습니다.</div>
      </div>

      <!-- 유사 도서 목록 -->
      <div class="similar-books-section" v-if="book.similar_books && book.similar_books.length">
        <h3>유사 도서</h3>
        <div class="similar-books-list">
          <div
            class="similar-book-card"
            v-for="sim in book.similar_books"
            :key="sim.id"
            @click="navigateToBook(sim.id)"
          >
            <img :src="sim.cover" :alt="sim.title" class="similar-book-cover" />
            <div class="similar-book-title">{{ sim.title }}</div>
            <div class="similar-book-author">{{ sim.author }}</div>
            <div class="similar-book-category">{{ sim.category_name }}</div>
            <div class="similarity-score">유사도: {{ (sim.similarity_score * 100).toFixed(1) }}%</div>
          </div>
        </div>
      </div>
    </main>

    <ErrorPage v-else-if="error" type="error" :message="error" />
    <ErrorPage v-else type="loading" message="도서 정보를 불러오는 중입니다." />

    <Footer />
  </div>
</template>

<script>
import axios from 'axios'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import ErrorPage from '@/components/common/ErrorPage.vue'

export default {
  name: 'BookDetail',
  components: {
    Navbar,
    Footer,
    ErrorPage
  },
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
      likeLoading: false
    }
  },
  methods: {
    async fetchBook() {
  try {
    const response = await axios.get(`/api/books/${this.id}/`)
    this.book = response.data
    this.error = null

    // === threads와 thread_count 실제 값 콘솔 출력 ===
    console.log('book.threads:', this.book.threads)
    console.log('book.thread_count:', this.book.thread_count)
    // threads 배열의 각 thread도 출력
    if (Array.isArray(this.book.threads)) {
      this.book.threads.forEach((thread, idx) => {
        console.log(`thread[${idx}]`, thread)
      })
    }
    // ============================================
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
      this.$router.push({ name: 'BookDetail', params: { id: bookId } })
    }
  },
  mounted() {
    this.fetchBook()
  }
}
</script>

<style scoped>
.book-detail-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.main-content {
  flex: 1;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}
.book-header {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  margin-bottom: 2rem;
}
.book-cover {
  width: 160px;
  height: 220px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.book-meta {
  flex: 1;
}
.subtitle {
  font-size: 1.1rem;
  color: #666;
  margin-top: 0.5rem;
}
.book-author, .book-category, .book-rating {
  margin-top: 0.7rem;
  color: #444;
}
.book-likes-action {
  margin-top: 0.7rem;
}
.like-button {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: none;
  border: none;
  color: #dc3545;
  font-size: 1.15rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  padding: 0.2rem 0.7rem;
  border-radius: 20px;
}
.like-button.liked {
  background: #ffeaea;
}
.like-button:disabled {
  color: #aaa;
  background: #f0f0f0;
  cursor: not-allowed;
}
.heart {
  font-size: 1.3rem;
  vertical-align: middle;
}
.like-count {
  min-width: 18px;
  text-align: center;
  font-size: 1.07rem;
  margin-left: 2px;
  margin-right: 2px;
}
.like-label {
  font-size: 1rem;
  color: #666;
  margin-left: 2px;
}
.book-description {
  margin-bottom: 2rem;
}
.author-info {
  margin-bottom: 2rem;
}
.author-profile {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}
.author-photo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}
.book-actions {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}
.thread-write-button {
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
}
.thread-write-button:hover {
  background-color: #0052a3;
}
.book-threads {
  margin-top: 2rem;
}
.book-threads ul {
  list-style: none;
  padding: 0;
}
.book-threads li {
  margin-bottom: 0.5rem;
}
.book-threads a {
  color: #0066cc;
  text-decoration: underline;
}
.empty-state {
  color: #888;
  padding: 1rem 0;
  font-size: 0.97rem;
  text-align: center;
}
.similar-books-section {
  margin-top: 2.5rem;
}
.similar-books-list {
  display: flex;
  gap: 1.2rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}
.similar-book-card {
  background: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 1rem;
  width: 170px;
  cursor: pointer;
  text-align: center;
  transition: box-shadow 0.18s, border 0.18s;
  border: 1.5px solid #eee;
}
.similar-book-card:hover {
  box-shadow: 0 6px 20px rgba(25,118,210,0.12);
  border: 1.5px solid #1976d2;
}
.similar-book-cover {
  width: 80px;
  height: 110px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 0.7rem;
}
.similar-book-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.2rem;
  color: #1976d2;
}
.similar-book-author {
  font-size: 0.95rem;
  color: #444;
  margin-bottom: 0.1rem;
}
.similar-book-category {
  font-size: 0.92rem;
  color: #888;
}
.similarity-score {
  font-size: 0.9rem;
  color: #1976d2;
  margin-top: 0.2rem;
}
</style>

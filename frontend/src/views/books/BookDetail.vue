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

      <div class="book-threads" v-if="book.threads && book.threads.length">
        <h3>이 책의 커뮤니티 글 ({{ book.thread_count }})</h3>
        <ul>
          <li v-for="thread in book.threads" :key="thread.id">
            <router-link :to="`/threads/${thread.id}`">{{ thread.title }}</router-link>
          </li>
        </ul>
      </div>
    </main>

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
      } catch (err) {
        this.error = '도서 정보를 불러오는데 실패했습니다.'
        console.error('도서 상세 정보 불러오기 실패:', err)
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
        console.error('좋아요 처리 실패:', err)
      } finally {
        this.likeLoading = false
      }
    },
    navigateToThreadWrite() {
      this.$router.push({ name: 'ThreadWrite', params: { bookId: this.book.id } })
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
.book-author, .book-category {
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
</style>

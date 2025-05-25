<template>
  <div class="thread-write-page">
    <Navbar />
    <main class="main-content">
      <h1>새 글 작성</h1>
      <form @submit.prevent="submitThread">
        <div class="form-group">
          <label for="title">제목</label>
          <input
            id="title"
            v-model="thread.title"
            type="text"
            required
            placeholder="제목을 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="book">관련 도서</label>
          <select
            id="book"
            v-model="thread.bookId"
            required
          >
            <option value="" disabled>도서를 선택하세요</option>
            <option v-for="book in books" :key="book.id" :value="book.id">
              {{ book.title }} ({{ book.author }})
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="rating">평점</label>
          <div class="rating-selector">
            <div
              v-for="score in 5"
              :key="score"
              class="star"
              :class="{ active: thread.rating >= score }"
              @click="thread.rating = score"
            >⭐</div>
            <span class="rating-value">{{ thread.rating }}/5</span>
          </div>
        </div>
        <div class="form-group">
          <label for="content">내용</label>
          <textarea
            id="content"
            v-model="thread.content"
            rows="10"
            required
            placeholder="내용을 입력하세요"
          ></textarea>
        </div>
        <div class="form-actions">
          <button type="button" @click="$router.back()" class="cancel-btn">취소</button>
          <button type="submit" class="submit-btn" :disabled="!isFormValid || loading">
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            등록
          </button>
        </div>
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </main>
    <Footer />
  </div>
</template>

<script>
import axios from 'axios'
import Footer from '@/components/common/Footer.vue'
import Navbar from '@/components/common/Navbar.vue'

export default {
  name: 'ThreadWrite',
  components: {
    Footer,
    Navbar
  },
  data() {
    return {
      books: [],
      thread: {
        title: '',
        content: '',
        bookId: '',
        rating: 0
      },
      loading: false,
      error: null
    }
  },
  computed: {
    isFormValid() {
      return (
        this.thread.title &&
        this.thread.bookId &&
        this.thread.rating > 0 &&
        this.thread.content
      )
    }
  },
  methods: {
    async fetchBooks() {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          // 토큰이 없으면 로그인 페이지로 이동
          this.$router.push('/auth/login')
          return
        }
        const response = await axios.get('/api/books/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.books = response.data.results
      } catch (err) {
        console.error('도서 목록 가져오기 실패:', err)
        if (err.response && err.response.status === 401) {
          // 401이면 로그인 페이지로 이동
          this.$router.push('/auth/login')
        } else {
          this.error = '도서 목록을 불러오는데 실패했습니다.'
        }
      }
    },
    async submitThread() {
      if (!this.isFormValid) return
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.$router.push('/auth/login')
          this.loading = false
          return
        }
        const response = await axios.post(
          `/api/threads/books/${this.thread.bookId}/create/`,
          {
            title: this.thread.title,
            content: this.thread.content,
            rating: this.thread.rating
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )
        console.log('스레드 생성 성공:', response.data)
        this.$router.push('/community')
      } catch (error) {
        console.error('스레드 생성 실패:', error)
        if (error.response && error.response.status === 401) {
          this.$router.push('/auth/login')
        } else {
          this.error =
            (error.response && (error.response.data.message || error.response.data.error)) ||
            '스레드 생성에 실패했습니다.'
        }
      } finally {
        this.loading = false
      }
    }
  },
  async mounted() {
    await this.fetchBooks()
  }
}
</script>

<style scoped>
.thread-write-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}
h1 {
  margin-bottom: 2rem;
}
.form-group {
  margin-bottom: 1.5rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
input, select, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}
.rating-selector {
  display: flex;
  align-items: center;
}
.star {
  font-size: 1.5rem;
  color: #ccc;
  cursor: pointer;
}
.star.active {
  color: #f0ad4e;
}
.rating-value {
  margin-left: 1rem;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
.cancel-btn {
  padding: 0.75rem 1.5rem;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}
.submit-btn {
  padding: 0.75rem 1.5rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}
.error {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
}
</style>

<template>
  <div class="thread-write-page">
    <main class="main-content">
      <h1>새 글 작성</h1>
      <div class="selected-book" v-if="selectedBook">
        <strong>선택한 도서:</strong>
        <span class="book-title">{{ selectedBook.title }} <small>({{ selectedBook.author }})</small></span>
      </div>
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

export default {
  name: 'ThreadWrite',
  props: {
    bookId: {
      type: [String, Number],
      required: true
    }
  },
  components: {
    Footer,
    Navbar
  },
  data() {
    return {
      selectedBook: null, // 선택한 도서 정보
      thread: {
        title: '',
        content: '',
        bookId: this.bookId,
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
    async fetchBook() {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.$router.push('/auth/login')
          return
        }
        // 선택한 도서 1개만 조회
        const response = await axios.get(`/api/books/${this.bookId}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.selectedBook = response.data
      } catch (err) {
        console.error('도서 정보 가져오기 실패:', err)
        if (err.response && err.response.status === 401) {
          this.$router.push('/auth/login')
        } else {
          this.error = '도서 정보를 불러오는데 실패했습니다.'
        }
      }
    },
    async submitThread() {
      if (!this.isFormValid) return
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('access_token')
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
        if (error.response) {
          this.error =
            error.response.data?.detail || '스레드 생성 중 오류가 발생했습니다.'
        } else {
          this.error = '서버와의 연결에 문제가 발생했습니다.'
        }
      } finally {
        this.loading = false
      }
    }
  },
  async mounted() {
    await this.fetchBook()
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
.selected-book {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}
.book-title {
  color: #0066cc;
  font-weight: bold;
  margin-left: 0.5rem;
}
.form-group {
  margin-bottom: 1.5rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
input, textarea {
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

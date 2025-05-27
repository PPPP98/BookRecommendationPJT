<template>
  <div class="thread-write-page">
    <main class="main-content">
      <h1>새 커뮤니티 글 작성</h1>

      <!-- 선택 도서 정보 -->
      <div class="selected-book" v-if="selectedBook">
  <div class="book-info">
    <img :src="selectedBook.cover" :alt="selectedBook.title" class="book-cover" />
    <div>
      <span class="book-title">{{ selectedBook.title }}</span>
      <span class="book-author">({{ selectedBook.author }})</span>
      <!-- 기존 평점 노출 -->
      
      <!-- 내가 매길 평점 (별점 선택) -->
      <div class="user-rating-selector" @mouseleave="hoverRating = 0">
        <span class="rating-label">내 평점</span>
        <span v-for="score in 5" :key="score"
          class="star"
          :class="{ active: (hoverRating || thread.rating) >= score }"
          @mouseover="hoverRating = score"
          @click="thread.rating = score"
        >&#9733;</span>
        <span class="rating-value">{{ thread.rating }}/5</span>
      </div>
    </div>
  </div>
</div>


      <form class="thread-form" @submit.prevent="submitThread">
        <div class="form-group">
          <label for="title">제목</label>
          <input
            id="title"
            v-model="thread.title"
            type="text"
            required
            maxlength="100"
            placeholder="제목을 입력하세요 (최대 100자)"
          />
        </div>
        
        <div class="form-group">
          <label for="content">내용</label>
          <textarea
            id="content"
            v-model="thread.content"
            rows="8"
            required
            maxlength="2000"
            placeholder="책을 읽고 느낀 점, 감상, 추천 이유 등 자유롭게 작성해 주세요 (최대 2000자)"
          ></textarea>
        </div>
        <div class="form-actions">
          <button type="button" @click="$router.back()" class="cancel-btn">취소</button>
          <button type="submit" class="submit-btn" :disabled="!isFormValid || loading">
            <span v-if="loading" class="spinner"></span>
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
      selectedBook: null,
      thread: {
        title: '',
        content: '',
        bookId: this.bookId,
        rating: 0
      },
      hoverRating: 0,
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
        const response = await axios.get(`/api/books/${this.bookId}/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.selectedBook = response.data
      } catch (err) {
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
            headers: { Authorization: `Bearer ${token}` }
          }
        )
        this.$router.push('/community')
      } catch (error) {
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
  background: #f7f9fb;
}
.main-content {
  flex: 1;
  padding: 2.5rem 1rem 2rem 1rem;
  max-width: 600px;
  margin: 0 auto;
}
h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  letter-spacing: -0.01em;
  color: #222;
}
.selected-book {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  background: #eef3fa;
  border-radius: 10px;
  padding: 1rem 1.2rem;
  margin-bottom: 2rem;
}
.selected-book .label {
  font-weight: 600;
  color: #1976d2;
  font-size: 1rem;
  margin-right: 0.7rem;
}
.selected-book .book-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.selected-book .book-cover {
  width: 45px;
  height: 62px;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(25, 118, 210, 0.07);
}
.selected-book .book-title {
  font-weight: 600;
  font-size: 1.05rem;
  color: #222;
}
.selected-book .book-author {
  font-size: 0.95rem;
  color: #666;
  margin-left: 0.5rem;
}
.thread-form {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.07);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
}
.form-group {
  margin-bottom: 1.6rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #222;
  font-size: 1rem;
}
input, textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #dde2e6;
  border-radius: 6px;
  font-size: 1rem;
  background: #fafbfc;
  transition: border 0.15s;
}
input:focus, textarea:focus {
  border-color: #1976d2;
  outline: none;
}
.rating-selector {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 1.5rem;
  user-select: none;
}
.star {
  color: #e0e0e0;
  cursor: pointer;
  transition: color 0.15s;
}
.star.active {
  color: #f7b500;
  text-shadow: 0 1px 4px #ffecb3;
}
.rating-value {
  margin-left: 1rem;
  font-size: 1rem;
  color: #1976d2;
  font-weight: 600;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
.cancel-btn {
  padding: 0.7rem 1.5rem;
  background: #f8f9fa;
  border: 1px solid #dde2e6;
  border-radius: 6px;
  color: #666;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border 0.15s;
}
.cancel-btn:hover {
  background: #e3eaf3;
  border-color: #b7c3d2;
}
.submit-btn {
  padding: 0.7rem 1.5rem;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.submit-btn:disabled {
  background: #bcd3ee;
  cursor: not-allowed;
}
.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid #fff;
  border-top: 2px solid #1976d2;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 0.5rem;
  vertical-align: middle;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.error {
  color: #dc3545;
  margin-top: 1.2rem;
  text-align: center;
  font-size: 1rem;
  font-weight: 500;
}
@media (max-width: 600px) {
  .main-content {
    padding: 1rem;
  }
  .thread-form {
    padding: 1.2rem 0.5rem 1rem 0.5rem;
  }
  .selected-book {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.7rem 0.7rem;
  }
}
</style>

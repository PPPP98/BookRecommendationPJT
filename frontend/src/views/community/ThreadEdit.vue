<template>
  <div class="thread-edit-page">
    <main class="main-content" v-if="thread">
      <h1>글 수정</h1>
      <div class="selected-book" v-if="thread.book">
        <strong>선택한 도서:</strong>
        <span class="book-title">{{ thread.book.title }} <small>({{ thread.book.author }})</small></span>
      </div>
      <form @submit.prevent="submitEdit">
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
            수정
          </button>
        </div>
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </main>
    <ErrorPage v-else type="loading" message="쓰레드를 불러오는 중입니다." />
    <Footer />
  </div>
</template>

<script>
import axios from 'axios'
import Footer from '@/components/common/Footer.vue'
import ErrorPage from '@/components/common/ErrorPage.vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ThreadEdit',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  components: {
    Footer,
    ErrorPage
  },
  data() {
    return {
      thread: {
        title: '',
        content: '',
        rating: 0,
        book: null,
      },
      loading: false,
      error: null,
      userId: null
    }
  },
  computed: {
    isFormValid() {
      return (
        this.thread.title &&
        this.thread.rating > 0 &&
        this.thread.content
      )
    }
  },
  methods: {
    async fetchThread() {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.$router.push('/auth/login')
          return
        }
        
        const response = await axios.get(`/api/threads/${this.id}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        
        this.thread = {
          ...response.data,
          book: response.data.book || {}
        }

        // 자신의 글이 아니면 뒤로 가기
        const authStore = useAuthStore()
        this.userId = authStore.user?.pk || authStore.user?.id || null
        
        if (String(this.userId) !== String(this.thread.user?.id || this.thread.user?.pk)) {
          alert('자신의 글만 수정할 수 있습니다.')
          this.$router.back()
        }
      } catch (err) {
        console.error('쓰레드 불러오기 실패:', err)
        if (err.response && err.response.status === 401) {
          this.$router.push('/auth/login')
        } else if (err.response && err.response.status === 404) {
          this.$router.push('/not-found')
        } else {
          this.error = '쓰레드 정보를 불러오는데 실패했습니다.'
        }
      }
    },
    async submitEdit() {
      if (!this.isFormValid) return
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.$router.push('/auth/login')
          return
        }
        
        const response = await axios.put(
          `/api/threads/${this.id}/update-delete/`,
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
        
        console.log('스레드 수정 성공:', response.data)
        this.$router.push(`/threads/${this.id}`)
      } catch (error) {
        console.error('스레드 수정 실패:', error)
        if (error.response) {
          if (error.response.status === 401) {
            this.$router.push('/auth/login')
          } else {
            this.error = error.response.data?.detail || '스레드 수정 중 오류가 발생했습니다.'
          }
        } else {
          this.error = '서버와의 연결에 문제가 발생했습니다.'
        }
      } finally {
        this.loading = false
      }
    }
  },
  async created() {
    await this.fetchThread()
  }
}
</script>

<style scoped>
.thread-edit-page {
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

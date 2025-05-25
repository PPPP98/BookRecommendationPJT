<template>
  <div class="thread-detail-page">
    <Navbar />
    <main class="main-content" v-if="thread">
      <div class="thread-header">
        <h1>{{ thread.title }}</h1>
        <div class="author-info">
          <img :src="thread.author.profile_image || '/default-profile.png'" :alt="thread.author.username" class="author-image">
          <span class="author-name">{{ thread.author.nickname || thread.author.username }}</span>
          <span class="created-at">{{ formattedDate }}</span>
        </div>
      </div>

      <div class="book-info">
        <div class="book-label">📚 관련 도서</div>
        <h3>{{ thread.bookTitle }}</h3>
        <div class="rating">
          <span>평점: </span>
          <span class="stars">{{ '⭐'.repeat(Math.floor(thread.rating)) }}</span>
          <span class="rating-number">{{ thread.rating }}/5</span>
        </div>
      </div>

      <div class="thread-content">
        <p>{{ thread.content }}</p>
      </div>

      <div class="thread-actions">
        <button class="like-button" @click="toggleLike" :disabled="likeLoading">
          {{ isLiked ? '❤️' : '🤍' }} {{ thread.likes }}명이 좋아합니다
        </button>
        <!-- 삭제 버튼 -->
        <button v-if="isMine" @click="deleteThread" class="delete-button">삭제</button>
      </div>

      <div class="comments-section">
        <h2>댓글 ({{ thread.comments.length }})</h2>
        <div class="comment-form">
          <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
          <button @click="addComment" :disabled="!newComment.trim() || commentLoading">등록</button>
        </div>
        <div class="comments-list">
          <div v-for="comment in thread.comments" :key="comment.id" class="comment">
            <div class="comment-header">
              <span class="comment-author">{{ comment.user.nickname || comment.user.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
          </div>
        </div>
      </div>
      <div v-if="error" class="error-state">{{ error }}</div>
    </main>
    <ErrorPage v-else type="loading" message="쓰레드를 불러오는 중입니다." />
    <Footer />
  </div>
</template>

<script>
import axios from 'axios'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import ErrorPage from '@/components/common/ErrorPage.vue'
import { useAuthStore } from '@/stores/auth' // Pinia/Vuex 등에서 로그인 사용자 정보 가져오기

export default {
  name: 'ThreadDetail',
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
      thread: null,
      newComment: '',
      isLiked: false,
      likeLoading: false,
      commentLoading: false,
      error: null,
      userId: null // 현재 로그인 사용자 id
    }
  },
  computed: {
    formattedDate() {
      if (!this.thread?.created_at) return ''
      const date = new Date(this.thread.created_at)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    },
    isMine() {
      // 실제 로그인 사용자와 글 작성자 비교
      return this.thread && this.thread.user && this.userId === this.thread.user.id
    }
  },
  methods: {
    async fetchThread() {
      try {
        const response = await axios.get(`/api/threads/${this.id}/`)
        this.thread = {
          ...response.data,
          author: response.data.user,
          likes: response.data.like_count,
          comments: response.data.comments,
          rating: response.data.rating,
          bookTitle: response.data.book_title || '', // 필요시
        }
        this.isLiked = response.data.is_liked
      } catch (err) {
        this.$router.push('/not-found')
      }
    },
    async toggleLike() {
      if (!this.thread) return
      this.likeLoading = true
      try {
        const response = await axios.post(`/api/threads/${this.thread.id}/like/`)
        this.isLiked = response.data.liked
        this.thread.likes = response.data.like_count
      } catch (err) {
        // 에러 처리
      } finally {
        this.likeLoading = false
      }
    },
    async addComment() {
      if (!this.newComment.trim() || !this.thread) return
      this.commentLoading = true
      try {
        const response = await axios.post(
          `/api/threads/${this.thread.id}/comments/create/`,
          { content: this.newComment }
        )
        this.thread.comments.push(response.data)
        this.newComment = ''
      } catch (err) {
        // 에러 처리
      } finally {
        this.commentLoading = false
      }
    },
    async deleteThread() {
      if (!confirm('정말 삭제하시겠습니까?')) return
      try {
        await axios.delete(`/api/threads/${this.thread.id}/update-delete/`)
        this.$router.push('/community')
      } catch (err) {
        this.error = '삭제에 실패했습니다.'
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    }
  },
  async created() {
    // 로그인 사용자 정보 가져오기 (Pinia/Vuex 등에서)
    try {
      const authStore = useAuthStore()
      this.userId = authStore.user?.id || null
    } catch (e) {
      this.userId = null
    }
    await this.fetchThread()
  }
}
</script>

<style scoped>
.thread-detail-page {
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
.thread-header {
  margin-bottom: 2rem;
}
.author-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #666;
  margin-top: 0.5rem;
}
.author-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
.book-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.book-label {
  color: #666;
  margin-bottom: 0.5rem;
}
.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.stars {
  color: #f0ad4e;
}
.thread-content {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}
.thread-actions {
  margin-bottom: 2rem;
}
.like-button {
  background: none;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.delete-button {
  margin-left: 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.comments-section {
  margin-top: 3rem;
}
.comment-form {
  margin-bottom: 2rem;
}
.comment-form textarea {
  width: 100%;
  height: 100px;
  padding: 0.5rem;
  margin-bottom: 1rem;
}
.comment-form button {
  background: #0066cc;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.comment-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.comment {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}
.comment-author {
  font-weight: bold;
}
.comment-date {
  color: #666;
  font-size: 0.9rem;
}
.error-state {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
}
</style>

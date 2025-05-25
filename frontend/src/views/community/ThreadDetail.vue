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
        <div class="book-detail">
          <img
            class="book-cover"
            :src="thread.bookCover || fallbackBookCover"
            :alt="thread.bookTitle"
            @error="onBookImgError"
          />
          <div class="book-meta">
            <h3>{{ thread.bookTitle }}</h3>
            <div class="rating">
              <span>평점: </span>
              <span class="stars">{{ '⭐'.repeat(Math.floor(thread.rating)) }}</span>
              <span class="rating-number">{{ thread.rating }}/5</span>
            </div>
          </div>
        </div>
      </div>

      <div class="thread-content">
        <p>{{ thread.content }}</p>
      </div>

      <div class="thread-actions">
        <button class="like-button" @click="toggleLike" :disabled="likeLoading">
          {{ isLiked ? '❤️' : '🤍' }} {{ thread.likes }}명이 좋아합니다
        </button>
        <button v-if="isMine" @click="startEdit" class="edit-button">수정</button>
        <button v-if="isMine" @click="deleteThread" class="delete-button">삭제</button>
      </div>

      <!-- 수정 폼 -->
      <div v-if="editing" class="edit-form">
        <input v-model="editTitle" placeholder="제목 수정" />
        <textarea v-model="editContent" rows="10" placeholder="내용 수정"></textarea>
        <div class="edit-actions">
          <button @click="submitEdit" class="submit-btn" :disabled="editLoading">저장</button>
          <button @click="cancelEdit" class="cancel-btn">취소</button>
        </div>
        <div v-if="editError" class="error-state">{{ editError }}</div>
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
import { useAuthStore } from '@/stores/auth'

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
      fallbackBookCover: 'https://cdn-icons-png.flaticon.com/512/29/29302.png', // 무료 책 아이콘
      newComment: '',
      isLiked: false,
      likeLoading: false,
      commentLoading: false,
      error: null,
      userId: null,
      // 수정 관련
      editing: false,
      editTitle: '',
      editContent: '',
      editLoading: false,
      editError: null,
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
          bookTitle: response.data.book_title || response.data.book?.title || '',
          bookCover: response.data.book_cover || response.data.book?.cover || '', // cover 필드 우선 사용
        }
        this.isLiked = response.data.is_liked
      } catch (err) {
        this.$router.push('/not-found')
      }
    },
    onBookImgError(e) {
      e.target.src = this.fallbackBookCover
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
        const token = localStorage.getItem('access_token')
        await axios.delete(`/api/threads/${this.thread.id}/update-delete/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.$router.push('/community')
      } catch (err) {
        this.error = '삭제에 실패했습니다.'
      }
    },
    startEdit() {
      this.editing = true
      this.editTitle = this.thread.title
      this.editContent = this.thread.content
      this.editError = null
    },
    cancelEdit() {
      this.editing = false
      this.editTitle = ''
      this.editContent = ''
      this.editError = null
    },
    async submitEdit() {
      if (!this.editTitle.trim() || !this.editContent.trim()) {
        this.editError = '제목과 내용을 모두 입력하세요.'
        return
      }
      this.editLoading = true
      this.editError = null
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.put(
          `/api/threads/${this.thread.id}/update-delete/`,
          {
            title: this.editTitle,
            content: this.editContent,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )
        this.thread.title = response.data.title
        this.thread.content = response.data.content
        this.editing = false
        this.editTitle = ''
        this.editContent = ''
      } catch (err) {
        this.editError = '수정에 실패했습니다.'
      } finally {
        this.editLoading = false
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
    try {
      const authStore = useAuthStore()
      this.userId = authStore.user?.id || authStore.user?.pk || null
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
.book-detail {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.book-cover {
  width: 80px;
  height: 110px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  background: #fff;
}
.book-meta {
  flex: 1;
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
.edit-button {
  margin-left: 1rem;
  background-color: #ffc107;
  color: #333;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.edit-button:hover {
  background-color: #e0a800;
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
.edit-form {
  margin: 2rem 0;
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}
.edit-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.submit-btn {
  background: #0066cc;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.cancel-btn {
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem 1rem;
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

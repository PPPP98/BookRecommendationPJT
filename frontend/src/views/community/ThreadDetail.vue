<!-- 
  ThreadDetail 페이지
  역할: 쓰레드의 상세 정보와 댓글을 표시
  기능:
    - 쓰레드 상세 정보 표시
    - 댓글 목록 표시 및 작성
    - 좋아요 기능
  데이터 구조:
    - thread: {
        id: Number,
        title: String,
        content: String,
        bookTitle: String,
        author: {
          id: Number,
          username: String,
          profile_image: String
        },
        likes: Number,
        comments: Array,
        rating: Number,
        createdAt: String
      }
-->
<template>
  <div class="thread-detail-page">
    <Navbar />
    
    <main class="main-content" v-if="thread">
      <div class="thread-header">
        <h1>{{ thread.title }}</h1>
        <div class="author-info">
          <img :src="thread.author.profile_image" :alt="thread.author.username" class="author-image">
          <span class="author-name">{{ thread.author.username }}</span>
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
        <button class="like-button" @click="toggleLike">
          {{ isLiked ? '❤️' : '🤍' }} {{ thread.likes }}명이 좋아합니다
        </button>
      </div>

      <div class="comments-section">
        <h2>댓글 ({{ thread.comments.length }})</h2>

        <div class="comment-form">
          <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
          <button @click="addComment" :disabled="!newComment.trim()">등록</button>
        </div>

        <div class="comments-list">
          <div v-for="comment in thread.comments" :key="comment.id" class="comment">
            <div class="comment-header">
              <span class="comment-author">{{ comment.user }}</span>
              <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
          </div>
        </div>
      </div>
    </main>

    <ErrorPage v-else type="loading" message="쓰레드를 불러오는 중입니다." />

    <Footer />
  </div>
</template>

<script>
import { threads } from '@/mocks/threads'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import ErrorPage from '@/components/common/ErrorPage.vue'

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
      isLiked: false,
      newComment: ''
    }
  },
  computed: {
    formattedDate() {
      if (!this.thread?.createdAt) return ''
      
      const date = new Date(this.thread.createdAt)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    }
  },
  methods: {
    fetchThread() {
      // API 연동 시 실제 API 호출로 변경
      const threadId = parseInt(this.id)
      this.thread = threads.find(t => t.id === threadId)
      
      if (!this.thread) {
        // 존재하지 않는 글일 경우 처리
        this.$router.push('/not-found')
      }
    },
    toggleLike() {
      this.isLiked = !this.isLiked
      
      if (this.isLiked) {
        this.thread.likes++
      } else {
        this.thread.likes--
      }
      
      // API 연동 시 실제 좋아요 API 호출로 변경
    },
    addComment() {
      if (!this.newComment.trim()) return
      
      // API 연동 시 실제 댓글 작성 API 호출로 변경
      const newCommentObj = {
        id: this.thread.comments.length + 1,
        user: '현재 사용자', // 로그인한 사용자 정보로 변경
        content: this.newComment.trim(),
        createdAt: new Date().toISOString()
      }
      
      this.thread.comments.push(newCommentObj)
      this.newComment = ''
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
  created() {
    this.fetchThread()
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
</style>

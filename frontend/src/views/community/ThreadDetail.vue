<template>
  <div class="thread-detail-page">
    <main class="main-content" v-if="thread">
      <!-- 책 이미지 + 제목/저자 가로 배치 -->
      <section class="book-thread-top">
        <img
          class="book-cover-large"
          :src="thread.book?.cover || fallbackBookCover"
          :alt="thread.book?.title"
          @error="onBookImgError"
        />
        <div class="book-meta-block">
          <div class="book-title">{{ thread.book?.title }}</div>
          <div class="book-author">{{ thread.book?.author }}</div>
        </div>
      </section>

      <!-- 스레드 메타 및 액션 -->
      <section class="thread-header-row">
        <div class="thread-meta-info">
          <img
            class="author-image"
            :src="thread.user?.profile_image || fallbackProfile"
            :alt="thread.user?.nickname || thread.user?.username"
            @error="onProfileImgError"
          />
          <span class="author-name">{{ thread.user?.nickname || thread.user?.username }}</span>
          <span class="thread-date">{{ formattedDate }}</span>
        </div>
        <div class="thread-actions">
          <button class="like-button" :class="{ liked: isLiked }" @click="toggleLike" :disabled="likeLoading">
            <span v-if="isLiked">❤️</span>
            <span v-else>🤍</span>
            {{ thread.like_count }}
          </button>
        </div>
      </section>

      <!-- 스레드 본문 -->
      <section>
        <div class="thread-content">
          <p>{{ thread.content }}</p>
        </div>
      </section>

      <!-- 댓글 목록 -->
      <section class="comments-section">
        <CommentSection
          :comments="thread.comments"
          :user-id="userId"
          :thread-id="thread.id"
          @add-comment="addComment"
          @edit-comment="submitEditComment"
          @delete-comment="deleteComment"
          @open-detail="openCommentDetail"
          :comment-loading="commentLoading"
          :edit-comment-loading="editCommentLoading"
          :edit-comment-error="editCommentError"
          :editing-comment-id="editingCommentId"
          :edit-comment-content="editCommentContent"
          @start-edit-comment="startEditComment"
          @cancel-edit-comment="cancelEditComment"
          :show-comment-detail="showCommentDetail"
          :selected-comment-detail="selectedCommentDetail"
          :comment-detail-loading="commentDetailLoading"
          :comment-detail-error="commentDetailError"
          @close-detail="showCommentDetail = false"
          :new-comment="newComment"
          @update:new-comment="newComment = $event"
        />
      </section>
      <div v-if="error" class="error-state">{{ error }}</div>
    </main>
    <ErrorPage v-else type="loading" message="쓰레드를 불러오는 중입니다." />
    <Footer />
  </div>
</template>

<script>
import axios from 'axios'
import Footer from '@/components/common/Footer.vue'
import ErrorPage from '@/components/common/ErrorPage.vue'
import CommentSection from '@/components/comment/CommentSection.vue'
import { useAuthStore } from '@/stores/auth'
export default {
  name: 'ThreadDetailPage',
  components: {
    Footer,
    ErrorPage,
    CommentSection
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
      fallbackBookCover: 'https://cdn-icons-png.flaticon.com/512/29/29302.png',
      fallbackProfile: 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
      isLiked: false,
      likeLoading: false,
      error: null,
      userId: null,
      // 댓글 관련
      newComment: '',
      commentLoading: false,
      editingCommentId: null,
      editCommentContent: '',
      editCommentLoading: false,
      editCommentError: null,
      showCommentDetail: false,
      selectedCommentDetail: null,
      commentDetailLoading: false,
      commentDetailError: null,
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
    }
  },
  methods: {
    async fetchThread() {
      try {
        const response = await axios.get(`/api/threads/${this.id}/`)
        this.thread = {
          ...response.data,
          book: response.data.book || {},
          user: response.data.user || {},
          comments: response.data.comments || []
        }
        this.isLiked = response.data.is_liked || false
      } catch (err) {
        this.error = '쓰레드를 불러오는데 실패했습니다.'
        this.thread = null
      }
    },
    onBookImgError(e) {
      e.target.src = this.fallbackBookCover
    },
    onProfileImgError(e) {
      e.target.src = this.fallbackProfile
    },
    async toggleLike() {
      if (!this.thread) return
      this.likeLoading = true
      try {
        const response = await axios.post(`/api/threads/${this.thread.id}/like/`)
        this.isLiked = response.data.liked
        this.thread.like_count = response.data.like_count
      } finally {
        this.likeLoading = false
      }
    },
    // 댓글 관련 메서드 (paste.txt와 동일)
    async addComment(content) {
      if (!content.trim() || !this.thread) return
      this.commentLoading = true
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.post(
          `/api/threads/${this.thread.id}/comments/create/`,
          { content },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.thread.comments.push(response.data)
        this.newComment = ''
      } catch (err) {
        alert('댓글 등록에 실패했습니다.')
      } finally {
        this.commentLoading = false
      }
    },
    startEditComment(comment) {
      this.editingCommentId = comment.id
      this.editCommentContent = comment.content
      this.editCommentError = null
    },
    cancelEditComment() {
      this.editingCommentId = null
      this.editCommentContent = ''
      this.editCommentError = null
    },
    async submitEditComment({ comment, content }) {
      if (!content.trim()) {
        this.editCommentError = '댓글 내용을 입력하세요.'
        return
      }
      this.editCommentLoading = true
      this.editCommentError = null
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.put(
          `/api/threads/comments/${comment.id}/`,
          { content },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        const idx = this.thread.comments.findIndex(c => c.id === comment.id)
        if (idx !== -1) {
          this.thread.comments[idx] = {
            ...this.thread.comments[idx],
            ...response.data
          }
        }
        this.cancelEditComment()
      } catch (err) {
        this.editCommentError = '댓글 수정에 실패했습니다.'
      } finally {
        this.editCommentLoading = false
      }
    },
    async deleteComment(comment) {
      if (!confirm('정말 삭제하시겠습니까?')) return
      try {
        const token = localStorage.getItem('access_token')
        await axios.delete(
          `/api/threads/comments/${comment.id}/`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.thread.comments = this.thread.comments.filter(c => c.id !== comment.id)
      } catch (err) {
        alert('댓글 삭제에 실패했습니다.')
      }
    },
    async openCommentDetail(commentId) {
      this.showCommentDetail = true
      this.selectedCommentDetail = null
      this.commentDetailLoading = true
      this.commentDetailError = null
      try {
        const token = localStorage.getItem('access_token')
        const { data } = await axios.get(
          `/api/threads/comments/${commentId}/`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.selectedCommentDetail = data
      } catch (err) {
        this.commentDetailError = '댓글 정보를 불러올 수 없습니다.'
      } finally {
        this.commentDetailLoading = false
      }
    }
  },
  async created() {
    try {
      const authStore = useAuthStore()
      this.userId = authStore.user?.pk || authStore.user?.id || null
    } catch (e) {
      this.userId = null
    }
    await this.fetchThread()
  }
}
</script>

<style scoped>
:root {
  --color-bg: #F2F2F2;
  --color-card: #EAE4D5;
  --color-accent: #B6B09F;
  --color-text: #000000;
  --color-border: #B6B09F;
  --color-error: #dc3545;
}

.thread-detail-page {
  background: var(--color-bg);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  padding: 2.5rem 1rem 2rem 1rem;
  max-width: 900px;
  margin: 0 auto;
}

/* 책 이미지 + 제목/저자 가로 배치 */
.book-thread-top {
  display: flex;
  align-items: flex-start;
  gap: 2.2rem;
  background: var(--color-card);
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(182,176,159,0.07);
  border: 1.5px solid var(--color-border);
  padding: 2.1rem 2.6rem 2.1rem 2.6rem;
  margin-bottom: 2.1rem;
}
.book-cover-large {
  width: 210px;
  height: 300px;
  object-fit: cover;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(182,176,159,0.10);
}
.book-meta-block {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.2rem;
  margin-top: 1.2rem;
}
.book-title {
  font-size: 1.7rem;
  font-weight: 800;
  color: var(--color-text);
}
.book-author {
  font-size: 1.15rem;
  color: var(--color-accent);
  font-weight: 500;
  margin-top: 0.6rem;
}

/* 스레드 메타/액션 */
.thread-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}
.thread-meta-info {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.author-image {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  background: #efefef;
}
.author-name {
  font-weight: 600;
  color: var(--color-accent);
  font-size: 1.09rem;
}
.thread-date {
  font-size: 0.98rem;
  color: #888;
  margin-left: 0.7rem;
}
.thread-actions {
  display: flex;
  gap: 0.7rem;
  align-items: center;
}
.like-button {
  background: var(--color-bg);
  border: 1.5px solid var(--color-border);
  color: var(--color-accent);
  font-size: 1.13rem;
  border-radius: 6px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.13s, color 0.13s, border 0.13s;
}
.like-button.liked {
  background: #fff0f0;
  color: #dc3545;
  border-color: #dc3545;
}

/* 본문 */
.thread-content {
  background: #fff;
  border-radius: 10px;
  padding: 1.6rem 1.4rem;
  margin-bottom: 2.5rem;
  color: var(--color-text);
  font-size: 1.18rem;
  line-height: 1.7;
  box-shadow: 0 2px 8px rgba(182,176,159,0.07);
  border: 1.5px solid #e0e0e0;
}

/* 댓글 영역 */
.comments-section {
  margin-top: 3rem;
}

@media (max-width: 900px) {
  .main-content {
    padding: 1rem;
  }
  .book-thread-top {
    flex-direction: column;
    align-items: center;
    gap: 1.2rem;
    padding: 1.1rem 0.7rem;
  }
  .book-cover-large {
    width: 130px;
    height: 180px;
  }
  .book-meta-block {
    margin-top: 0.2rem;
    align-items: center;
  }
  .thread-content {
    padding: 1rem 0.5rem;
  }
}
</style>

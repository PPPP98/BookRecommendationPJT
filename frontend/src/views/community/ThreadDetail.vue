<template>
  <div class="thread-detail-page">
    <main class="main-content" v-if="thread">
      <!-- 📚 책 정보 카드 -->
      <section class="book-card">
        <img
          class="book-cover"
          :src="thread.book?.cover || fallbackBookCover"
          :alt="thread.book?.title"
          @error="onBookImgError"
        />
        <div class="book-meta">
          <div class="book-title">{{ thread.book?.title }}</div>
          <div class="book-author">{{ thread.book?.author }}</div>
          <div class="book-publisher" v-if="thread.book?.publisher">
            출판사: {{ thread.book.publisher }}
          </div>
          <div class="book-rating" v-if="thread.book?.customer_review_rank">
            평점:
            <span class="stars">
              <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= Math.round(thread.book.customer_review_rank) }">&#9733;</span>
            </span>
            <span class="rating-value">{{ Math.min(thread.book.customer_review_rank, 5).toFixed(1) }}/5</span>
          </div>
        </div>
      </section>

      <!-- 📝 스레드 헤더 및 액션 -->
      <section class="thread-header-card">
        <div class="thread-title">{{ thread.title }}</div>
        <div class="thread-meta">
          <div class="author-info">
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
            <button
              v-if="showFollowButton"
              class="follow-button"
              :class="{ following: isFollowing }"
              @click="toggleFollow"
              :disabled="followLoading"
            >
              {{ isFollowing ? '팔로잉' : '팔로우' }}
            </button>
            <button v-if="isMine" class="edit-button" @click="startEdit">수정</button>
            <button v-if="isMine" class="delete-button" @click="deleteThread">삭제</button>
          </div>
        </div>
      </section>

      <!-- ✏️ 스레드 본문/수정폼 -->
      <section>
        <ThreadEditForm
          v-if="editing"
          :title="editTitle"
          :content="editContent"
          :loading="editLoading"
          :error="editError"
          @update:title="editTitle = $event"
          @update:content="editContent = $event"
          @submit="submitEdit"
          @cancel="cancelEdit"
        />
        <div class="thread-content" v-else>
          <p>{{ thread.content }}</p>
        </div>
      </section>

      <!-- 💬 댓글 섹션 -->
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
import ThreadEditForm from '@/components/thread/ThreadEditForm.vue'
import CommentSection from '@/components/comment/CommentSection.vue'
import { useAuthStore } from '@/stores/auth'
export default {
  name: 'ThreadDetailPage',
  components: {
    Footer,
    ErrorPage,
    ThreadEditForm,
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
      isFollowing: false,
      followLoading: false,
      editing: false,
      editTitle: '',
      editContent: '',
      editLoading: false,
      editError: null,
      error: null,
      userId: null,
      showFollowButton: false,
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
    },
    isMine() {
      return (
        this.thread &&
        this.thread.user &&
        this.userId !== null &&
        String(this.userId) === String(this.thread.user.id || this.thread.user.pk)
      )
    },
    showFollowButton() {
      return (
        this.thread &&
        this.thread.user &&
        this.userId !== null &&
        String(this.userId) !== String(this.thread.user.id || this.thread.user.pk)
      )
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
        this.isFollowing = response.data.is_followed || false
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
    async toggleFollow() {
      if (!this.thread?.user?.id) return
      this.followLoading = true
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.post(
          `/api/accounts/${this.thread.user.id}/follow/`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.isFollowing = response.data.is_following
      } finally {
        this.followLoading = false
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
    // 댓글 관련 메서드
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

/* 전체 배경 */
.thread-detail-page {
  background: var(--color-bg);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  padding: 2.5rem 1rem 2rem 1rem;
  max-width: 800px;
  margin: 0 auto;
}

/* 책 정보 카드 */
.book-card {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  background: var(--color-card);
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(182,176,159,0.07);
  border: 1.5px solid var(--color-border);
  padding: 1.3rem 1.7rem;
  margin-bottom: 2rem;
}
.book-cover {
  width: 82px;
  height: 112px;
  object-fit: cover;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(182,176,159,0.10);
}
.book-meta {
  flex: 1;
}
.book-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.3rem;
}
.book-author {
  font-size: 1.05rem;
  color: var(--color-accent);
  margin-bottom: 0.3rem;
}
.book-publisher {
  font-size: 0.97rem;
  color: #7a7a7a;
  margin-bottom: 0.3rem;
}
.book-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.2rem;
  font-size: 0.98rem;
}
.stars {
  color: #f0ad4e;
}
.star {
  font-size: 1.1rem;
  color: #e0e0e0;
}
.star.filled {
  color: #f7b500;
  text-shadow: 0 1px 4px #ffecb3;
}
.rating-value {
  color: var(--color-accent);
  font-weight: 600;
  margin-left: 0.2rem;
}

/* 스레드 헤더 카드 */
.thread-header-card {
  background: var(--color-card);
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(182,176,159,0.07);
  border: 1.5px solid var(--color-border);
  padding: 1.2rem 1.7rem 1.1rem 1.7rem;
  margin-bottom: 2rem;
}
.thread-title {
  font-size: 1.18rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.7rem;
}
.thread-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.author-info {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.author-image {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  object-fit: cover;
  background: #efefef;
}
.author-name {
  font-weight: 600;
  color: var(--color-accent);
  font-size: 1.05rem;
}
.thread-date {
  font-size: 0.95rem;
  color: #888;
  margin-left: 0.5rem;
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
  font-size: 1.07rem;
  border-radius: 6px;
  padding: 0.4rem 1.1rem;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.13s, color 0.13s, border 0.13s;
}
.like-button.liked {
  background: #fff0f0;
  color: #dc3545;
  border-color: #dc3545;
}
.follow-button {
  background: var(--color-accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 1.2rem;
  font-weight: 600;
  font-size: 1.01rem;
  cursor: pointer;
  transition: background 0.13s;
}
.follow-button.following {
  background: #fff;
  color: var(--color-accent);
  border: 1.5px solid var(--color-accent);
}
.follow-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.edit-button {
  background: #fffbe6;
  color: #bfa100;
  border: 1.5px solid #bfa100;
  border-radius: 6px;
  padding: 0.4rem 1.2rem;
  font-weight: 600;
  font-size: 1.01rem;
  cursor: pointer;
  transition: background 0.13s;
}
.edit-button:hover {
  background: #fff3cd;
}
.delete-button {
  background: #fff0f0;
  color: #dc3545;
  border: 1.5px solid #dc3545;
  border-radius: 6px;
  padding: 0.4rem 1.2rem;
  font-weight: 600;
  font-size: 1.01rem;
  cursor: pointer;
  transition: background 0.13s;
}
.delete-button:hover {
  background: #ffeaea;
}
.thread-content {
  background: #fff;
  border-radius: 10px;
  padding: 1.3rem 1.2rem;
  margin-bottom: 2.5rem;
  color: var(--color-text);
  font-size: 1.13rem;
  line-height: 1.7;
  box-shadow: 0 2px 8px rgba(182,176,159,0.07);
  border: 1.5px solid #e0e0e0;
}
.error-state {
  color: var(--color-error);
  margin-top: 2rem;
  text-align: center;
  font-size: 1.1rem;
  font-weight: 600;
}

/* 댓글 영역은 위에서 제공한 스타일 재사용 가능 */
.comments-section {
  margin-top: 3rem;
}
@media (max-width: 600px) {
  .main-content {
    padding: 1rem;
  }
  .book-card,
  .thread-header-card {
    padding: 1rem 0.6rem;
    flex-direction: column;
    gap: 0.7rem;
  }
  .thread-content {
    padding: 1rem 0.5rem;
  }
}
</style>

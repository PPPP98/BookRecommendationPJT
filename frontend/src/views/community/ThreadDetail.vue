<template>
  <div class="thread-detail-page">
    <Navbar />
    <main class="main-content" v-if="thread">
      <ThreadHeader
        :thread="thread"
        :fallback-profile="fallbackProfile"
        :fallback-book-cover="fallbackBookCover"
        :formatted-date="formattedDate"
        @img-error="onProfileImgError"
        @book-img-error="onBookImgError"
      />
      <ThreadActions
        :thread="thread"
        :is-liked="isLiked"
        :like-loading="likeLoading"
        :is-following="isFollowing"
        :follow-loading="followLoading"
        :is-mine="isMine"
        :show-follow-button="showFollowButton"
        @toggle-like="toggleLike"
        @toggle-follow="toggleFollow"
        @start-edit="startEdit"
        @delete-thread="deleteThread"
      />
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
import ThreadHeader from '@/components/thread/ThreadHeader.vue'
import ThreadActions from '@/components/thread/ThreadActions.vue'
import ThreadEditForm from '@/components/thread/ThreadEditForm.vue'
import CommentSection from '@/components/comment/CommentSection.vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ThreadDetailPage',
  components: {
    Navbar,
    Footer,
    ErrorPage,
    ThreadHeader,
    ThreadActions,
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
      thread: null, // 반드시 선언!
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
    showFollowButtonComputed() {
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
        // 명세에 따라 모든 필드 그대로 할당
        this.thread = {
          ...response.data,
          book: response.data.book || {},
          user: response.data.user || {},
          comments: response.data.comments || []
        }
        this.isLiked = response.data.is_liked || false
        this.isFollowing = response.data.is_followed || false
        this.showFollowButton = this.showFollowButtonComputed
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
    // 댓글 관련 메서드 (paste.txt와 동일하게 유지, catch 블록 등도 포함)
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
          this.$set(this.thread.comments, idx, {
            ...this.thread.comments[idx],
            ...response.data
          })
        }
        this.cancelEditComment()
      } catch (err) {
        console.error('댓글 수정 에러:', err, err.response)
        if (err && err.response) {
          alert(
            '댓글 수정 실패: ' +
            (err.response.data?.detail || JSON.stringify(err.response.data) || err.message)
          );
        } else {
          alert('댓글 수정 실패: 네트워크/알 수 없는 오류');
        }
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
/* paste.txt의 기존 스타일 그대로 사용 */
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
.author-link {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: inherit;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.15s;
}
.author-link:hover .author-name {
  text-decoration: underline;
  color: #1976d2;
}
.author-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background: #efefef;
}
.book-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.book-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
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
.book-author {
  margin-bottom: 0.5rem;
  color: #444;
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
  display: flex;
  gap: 1rem;
  align-items: center;
}
.like-button {
  background: none;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.follow-button {
  background: #1976d2;
  color: #fff;
  border: none;
  padding: 0.5rem 1.1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.18s;
}
.follow-button.following {
  background: #f8f9fa;
  color: #1976d2;
  border: 1.5px solid #1976d2;
}
.follow-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.edit-button {
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

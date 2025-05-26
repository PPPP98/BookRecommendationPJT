<template>
  <div class="thread-detail-page">
    <Navbar />
    <main class="main-content" v-if="thread">
      <div class="thread-header">
        <h1>{{ thread.title }}</h1>
        <div class="author-info">
          <router-link
            v-if="thread.user && thread.user.id"
            :to="{ name: 'UserProfile', params: { id: thread.user.id } }"
            class="author-link"
          >
            <img
              :src="thread.user.profile_image || fallbackProfile"
              :alt="thread.user.nickname || thread.user.username"
              class="author-image"
              @error="onProfileImgError"
            />
            <span class="author-name">{{ thread.user.nickname || thread.user.username }}</span>
          </router-link>
          <span class="created-at">{{ formattedDate }}</span>
        </div>
      </div>

      <div class="book-info">
        <div class="book-title">{{ thread.book?.title }}</div>
        <div class="book-detail">
          <img
            class="book-cover"
            :src="thread.book?.cover || fallbackBookCover"
            :alt="thread.book?.title || '책 표지'"
            @error="onBookImgError"
          />
          <div class="book-meta">
            <div class="book-author">
              <strong>저자:</strong> {{ thread.book?.author }}
            </div>
            <div class="rating">
              <span>평점: </span>
              <span class="stars">{{ '⭐'.repeat(Math.floor(thread.rating || 0)) }}</span>
              <span class="rating-number">{{ thread.rating || 0 }}/5</span>
            </div>
          </div>
        </div>
      </div>

      <div class="thread-content">
        <p>{{ thread.content }}</p>
      </div>

      <div class="thread-actions">
        <button class="like-button" @click="toggleLike" :disabled="likeLoading">
          {{ isLiked ? '❤️' : '🤍' }} {{ thread.like_count || 0 }}명이 좋아합니다
        </button>
        <button
          v-if="showFollowButton"
          class="follow-button"
          :class="{ following: isFollowing }"
          @click="toggleFollow"
          :disabled="followLoading"
        >
          {{ isFollowing ? '언팔로우' : '팔로우' }}
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
        <h2>댓글 ({{ thread.comments?.length || 0 }})</h2>
        <div class="comment-form">
          <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
          <button @click="addComment" :disabled="!newComment.trim() || commentLoading">등록</button>
        </div>
        <div class="comments-list">
          <div
            v-for="comment in thread.comments || []"
            :key="comment.id"
            class="comment"
            @click="openCommentDetail(comment.id)"
            style="cursor:pointer"
          >
            <div class="comment-header">
              <span class="comment-author">{{ comment.user?.nickname || comment.user?.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              <template v-if="userId && String(userId) === String(comment.user?.id)">
                <button class="comment-edit-btn" @click.stop="startEditComment(comment)">수정</button>
                <button class="comment-delete-btn" @click.stop="deleteComment(comment)">삭제</button>
              </template>
            </div>
            <div v-if="isEditingComment(comment.id)" class="comment-edit-form">
              <textarea v-model="editCommentContent"></textarea>
              <div class="edit-actions">
                <button @click="submitEditComment(comment)" :disabled="editCommentLoading">저장</button>
                <button @click="cancelEditComment" :disabled="editCommentLoading">취소</button>
              </div>
              <div v-if="editCommentError" class="error-state">{{ editCommentError }}</div>
            </div>
            <p class="comment-content" v-else>{{ comment.content }}</p>
          </div>
        </div>
        <!-- 단일 댓글 상세 모달 -->
        <div v-if="showCommentDetail" class="modal-bg" @click.self="showCommentDetail = false">
          <div class="modal-content">
            <button class="close-btn" @click="showCommentDetail = false">닫기</button>
            <div v-if="commentDetailLoading" class="loading-state">불러오는 중...</div>
            <div v-else-if="commentDetailError" class="error-state">{{ commentDetailError }}</div>
            <div v-else-if="selectedCommentDetail" class="comment-detail">
              <div class="comment-header">
                <span class="comment-author">{{ selectedCommentDetail.user?.nickname || selectedCommentDetail.user?.username }}</span>
                <span class="comment-date">{{ formatDate(selectedCommentDetail.created_at) }}</span>
              </div>
              <p class="comment-content">{{ selectedCommentDetail.content }}</p>
            </div>
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
  components: { Navbar, Footer, ErrorPage },
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      thread: {
        book: {},
        user: {},
        comments: []
      },
      fallbackBookCover: 'https://cdn-icons-png.flaticon.com/512/29/29302.png',
      fallbackProfile: 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
      newComment: '',
      isLiked: false,
      likeLoading: false,
      commentLoading: false,
      error: null,
      userId: null,
      editing: false,
      editTitle: '',
      editContent: '',
      editLoading: false,
      editError: null,
      isFollowing: false,
      followLoading: false,
      // 댓글 상세/수정/삭제 관련
      showCommentDetail: false,
      selectedCommentDetail: null,
      commentDetailLoading: false,
      commentDetailError: null,
      editingCommentId: null,
      editCommentContent: '',
      editCommentLoading: false,
      editCommentError: null,
      deleteLoadingId: null
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
  async submitEditComment(comment) {
  if (!this.editCommentContent.trim()) {
    this.editCommentError = '댓글 내용을 입력하세요.'
    return
  }
  this.editCommentLoading = true
  this.editCommentError = null
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.put(
      `/api/threads/comments/${comment.id}/`,
      { content: this.editCommentContent },
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
    if (err.response) {
      alert(
        '댓글 수정 실패: ' +
        (err.response.data?.detail || JSON.stringify(err.response.data) || err.message)
      );
    }
    this.editCommentError = '댓글 수정에 실패했습니다.'
  } finally {
    this.editCommentLoading = false
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
        this.$router.push('/not-found')
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
    // 1️⃣ 댓글 생성
    async addComment() {
      if (!this.newComment.trim() || !this.thread) return
      this.commentLoading = true
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.post(
          `/api/threads/${this.thread.id}/comments/create/`,
          { content: this.newComment },
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
    // 2️⃣ 댓글 상세 조회 (모달)
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
    },
    // 댓글 수정 진입
    startEditComment(comment) {
      this.editingCommentId = comment.id
      this.editCommentContent = comment.content
      this.editCommentError = null
    },
    isEditingComment(commentId) {
      return this.editingCommentId === commentId
    },
    cancelEditComment() {
      this.editingCommentId = null
      this.editCommentContent = ''
      this.editCommentError = null
    },
    // 3️⃣ 댓글 수정
    async submitEditComment(comment) {
      if (!this.editCommentContent.trim()) {
        this.editCommentError = '댓글 내용을 입력하세요.'
        return
      }
      this.editCommentLoading = true
      this.editCommentError = null
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.put(
          `/api/threads/comments/${comment.id}/`,
          { content: this.editCommentContent },
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
        this.editCommentError = '댓글 수정에 실패했습니다.'
      } finally {
        this.editCommentLoading = false
      }
    },
    // 4️⃣ 댓글 삭제
    async deleteComment(comment) {
      if (!confirm('정말 삭제하시겠습니까?')) return
      this.deleteLoadingId = comment.id
      try {
        const token = localStorage.getItem('access_token')
        await axios.delete(
          `/api/threads/comments/${comment.id}/`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.thread.comments = this.thread.comments.filter(c => c.id !== comment.id)
      } catch (err) {
        alert('댓글 삭제에 실패했습니다.')
      } finally {
        this.deleteLoadingId = null
      }
    },
    catch (err) {
  console.error('댓글 수정 에러:', err, err.response)
  if (err.response) {
    alert(
      '댓글 수정 실패: ' +
      (err.response.data?.detail || JSON.stringify(err.response.data) || err.message)
    );
  }
  this.editCommentError = '댓글 수정에 실패했습니다.'
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

<template>
  <div class="comment" @click="$emit('open-detail', comment.id)" style="cursor:pointer">
    <div class="comment-header">
      <span class="comment-author">{{ comment.user?.nickname || comment.user?.username }}</span>
      <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
      <template v-if="userId && String(userId) === String(comment.user?.id)">
        <button class="comment-edit-btn" @click.stop="$emit('start-edit', comment)">수정</button>
        <button class="comment-delete-btn" @click.stop="$emit('delete', comment)">삭제</button>
      </template>
    </div>
    <!-- 댓글 수정 폼: 로컬 상태로 관리 -->
    <div v-if="editing" class="comment-edit-form" @click.stop>
      <textarea v-model="localEditContent"></textarea>
      <div class="edit-actions">
        <button @click.stop="onEdit" :disabled="editLoading || !localEditContent.trim()">저장</button>
        <button @click.stop="$emit('cancel-edit')" :disabled="editLoading">취소</button>
      </div>
      <div v-if="editError" class="error-state">{{ editError }}</div>
    </div>
    <p class="comment-content" v-else>{{ comment.content }}</p>
  </div>
</template>

<script>
export default {
  props: [
    'comment', 'userId', 'editing', 'editLoading', 'editError'
  ],
  emits: ['start-edit', 'cancel-edit', 'edit', 'delete', 'open-detail'],
  data() {
    return {
      localEditContent: ''
    }
  },
  watch: {
    editing(newVal) {
      if (newVal) {
        // 수정 폼이 열릴 때 현재 댓글 내용을 복사
        this.localEditContent = this.comment.content
      }
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    },
    onEdit() {
      // 빈 문자열 방지
      if (!this.localEditContent.trim()) return
      this.$emit('edit', { comment: this.comment, content: this.localEditContent })
    }
  }
}
</script>

<style scoped>
.comment {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 1rem 1.2rem;
  margin-bottom: 1.2rem;
  transition: box-shadow 0.13s;
}
.comment-header {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.2rem;
}
.comment-author {
  font-weight: 600;
  color: #1976d2;
}
.comment-date {
  font-size: 0.93rem;
  color: #888;
}
.comment-edit-btn,
.comment-delete-btn {
  margin-left: 0.7rem;
  background: none;
  border: none;
  color: #666;
  font-size: 0.93rem;
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  transition: background 0.13s;
}
.comment-edit-btn:hover {
  background: #e3f2fd;
  color: #1976d2;
}
.comment-delete-btn:hover {
  background: #ffeaea;
  color: #dc3545;
}
.comment-edit-form {
  margin-top: 0.4rem;
  background: #f7fafd;
  border-radius: 6px;
  padding: 0.7rem;
}
.comment-edit-form textarea {
  width: 100%;
  min-height: 60px;
  font-size: 1rem;
  border: 1px solid #dde2e6;
  border-radius: 4px;
  padding: 0.6rem;
  margin-bottom: 0.7rem;
  resize: vertical;
}
.edit-actions {
  display: flex;
  gap: 0.7rem;
}
.edit-actions button {
  padding: 0.4rem 1rem;
  border-radius: 4px;
  border: none;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
}
.edit-actions button:disabled {
  background: #e0e0e0;
  color: #aaa;
  cursor: not-allowed;
}
.edit-actions button:first-child {
  background: #1976d2;
  color: #fff;
}
.edit-actions button:last-child {
  background: #f8f9fa;
  color: #666;
}
.error-state {
  color: #dc3545;
  margin-top: 0.5rem;
  font-size: 0.93rem;
}
.comment-content {
  margin-top: 0.3rem;
  font-size: 1rem;
  color: #222;
  white-space: pre-wrap;
}
</style>

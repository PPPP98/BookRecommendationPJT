<template>
  <div class="comment" @click="$emit('open-detail', comment.id)">
    <div class="comment-header">
      <div class="comment-meta">
        <span class="comment-author">{{ comment.user?.nickname || comment.user?.username }}</span>
        <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
      </div>
      <div class="comment-actions" v-if="userId && String(userId) === String(comment.user?.id)">
        <button class="comment-edit-btn" @click.stop="$emit('start-edit', comment)">수정</button>
        <button class="comment-delete-btn" @click.stop="$emit('delete', comment)">삭제</button>
      </div>
    </div>
    <!-- 댓글 수정 폼 -->
    <div v-if="editing" class="comment-edit-form" @click.stop>
      <textarea v-model="localEditContent" :disabled="editLoading" maxlength="1000" />
      <div class="edit-actions">
        <button class="save-btn" @click.stop="onEdit" :disabled="editLoading || !localEditContent.trim()">저장</button>
        <button class="cancel-btn" @click.stop="$emit('cancel-edit')" :disabled="editLoading">취소</button>
      </div>
      <div v-if="editError" class="error-state">{{ editError }}</div>
    </div>
    <!-- 댓글 본문 -->
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
      if (!this.localEditContent.trim()) return
      this.$emit('edit', { comment: this.comment, content: this.localEditContent })
    }
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
  --color-btn-hover: #F2F2F2;
  --color-error: #dc3545;
}

.comment {
  background: var(--color-card);
  border-radius: 10px;
  border: 1.5px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(182, 176, 159, 0.07);
  padding: 1.2rem 1.5rem;
  margin-bottom: 1.2rem;
  transition: box-shadow 0.13s, border 0.13s;
  color: var(--color-text);
  cursor: pointer;
}
.comment:hover {
  box-shadow: 0 4px 16px rgba(182, 176, 159, 0.13);
  border-color: var(--color-accent);
}
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.3rem;
}
.comment-meta {
  display: flex;
  align-items: center;
  gap: 0.9rem;
}
.comment-author {
  font-weight: 600;
  color: var(--color-accent);
  font-size: 1.03rem;
}
.comment-date {
  font-size: 0.93rem;
  color: #888;
}
.comment-actions {
  display: flex;
  gap: 0.5rem;
}
.comment-edit-btn,
.comment-delete-btn {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: 0.93rem;
  font-weight: 500;
  border-radius: 5px;
  padding: 0.2rem 0.8rem;
  cursor: pointer;
  transition: background 0.13s, color 0.13s, border 0.13s;
}
.comment-edit-btn:hover {
  background: var(--color-accent);
  color: #fff;
  border-color: var(--color-accent);
}
.comment-delete-btn:hover {
  background: #fff0f0;
  color: #dc3545;
  border-color: #dc3545;
}
.comment-edit-form {
  margin-top: 0.5rem;
  background: var(--color-bg);
  border-radius: 7px;
  padding: 0.8rem;
  border: 1px solid var(--color-border);
}
.comment-edit-form textarea {
  width: 100%;
  min-height: 60px;
  font-size: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  padding: 0.7rem;
  margin-bottom: 0.7rem;
  background: #fff;
  color: var(--color-text);
  resize: vertical;
  transition: border 0.13s;
}
.comment-edit-form textarea:focus {
  border-color: var(--color-accent);
  outline: none;
}
.edit-actions {
  display: flex;
  gap: 0.7rem;
}
.save-btn {
  background: var(--color-accent);
  color: #fff;
  border: none;
  font-weight: 600;
  border-radius: 4px;
  padding: 0.4rem 1.2rem;
  font-size: 0.97rem;
  cursor: pointer;
  transition: background 0.13s;
}
.save-btn:disabled {
  background: #ccc;
  color: #fff;
  cursor: not-allowed;
}
.cancel-btn {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  border-radius: 4px;
  padding: 0.4rem 1.2rem;
  font-size: 0.97rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.13s, border 0.13s;
}
.cancel-btn:hover {
  background: #fff;
  border-color: var(--color-accent);
}
.error-state {
  color: var(--color-error);
  margin-top: 0.7rem;
  font-size: 0.97rem;
  text-align: left;
}
.comment-content {
  margin-top: 0.5rem;
  font-size: 1.05rem;
  color: var(--color-text);
  white-space: pre-wrap;
  word-break: break-word;
}
@media (max-width: 600px) {
  .comment {
    padding: 1rem 0.7rem;
  }
  .comment-edit-form {
    padding: 0.5rem;
  }
}
</style>

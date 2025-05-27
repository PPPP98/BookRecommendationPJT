<!-- 댓글 목록 -->
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
    <!-- 댓글 수정 폼: 모달처럼 화면 중앙에 크게 표시 -->
    <div v-if="editing" class="comment-edit-modal-bg">
      <div class="comment-edit-modal">
        <textarea v-model="localEditContent" :disabled="editLoading" maxlength="1000" />
        <div class="edit-actions">
          <button class="save-btn" @click.stop="onEdit" :disabled="editLoading || !localEditContent.trim()">저장</button>
          <button class="cancel-btn" @click.stop="$emit('cancel-edit')" :disabled="editLoading">취소</button>
        </div>
        <div v-if="editError" class="error-state">{{ editError }}</div>
      </div>
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
  position: relative;
  z-index: 1;
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

/* ====== 댓글 수정 모달 ====== */
.comment-edit-modal-bg {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.28);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.comment-edit-modal {
  background: #f4f6f8;
  border-radius: 16px;
  border: 2px solid var(--color-accent);
  box-shadow: 0 8px 32px rgba(0,0,0,0.13);
  padding: 2.5rem 2.4rem 2rem 2.4rem;
  min-width: 380px;
  max-width: 95vw;
  width: 520px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  position: relative;
}
.comment-edit-modal textarea {
  width: 100%;
  min-height: 120px;
  font-size: 1.2rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  padding: 1.1rem;
  margin-bottom: 1.3rem;
  background: #fff;
  color: var(--color-text);
  resize: vertical;
  transition: border 0.13s;
  box-sizing: border-box;
}
.comment-edit-modal textarea:focus {
  border-color: var(--color-accent);
  outline: none;
}
.edit-actions {
  display: flex;
  gap: 1.2rem;
  justify-content: flex-end;
  margin-bottom: 0.6rem;
}
.save-btn,
.cancel-btn {
  background: #000;
  color: #fff;
  border: none;
  font-weight: 700;
  border-radius: 8px;
  padding: 0.7rem 2.1rem;
  font-size: 1.08rem;
  cursor: pointer;
  transition: background 0.13s;
}
.save-btn:disabled,
.cancel-btn:disabled {
  background: #888;
  color: #fff;
  cursor: not-allowed;
}
.save-btn:hover,
.cancel-btn:hover {
  background: #222;
}
.error-state {
  color: var(--color-error);
  margin-top: 0.7rem;
  font-size: 1.07rem;
  text-align: left;
}
.comment-content {
  margin-top: 0.5rem;
  font-size: 1.05rem;
  color: var(--color-text);
  white-space: pre-wrap;
  word-break: break-word;
}
@media (max-width: 700px) {
  .comment-edit-modal {
    min-width: 0;
    width: 96vw;
    padding: 1.2rem 0.6rem 1.1rem 0.6rem;
  }
  .comment-edit-modal textarea {
    font-size: 1rem;
    padding: 0.8rem;
    min-height: 80px;
  }
}
</style>

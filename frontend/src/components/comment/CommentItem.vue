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
    <div v-if="editing" class="comment-edit-form">
      <textarea v-model="editContentProxy"></textarea>
      <div class="edit-actions">
        <button @click.stop="onEdit" :disabled="editLoading">저장</button>
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
    'comment', 'userId', 'editing', 'editContent', 'editLoading', 'editError'
  ],
  emits: ['start-edit', 'cancel-edit', 'edit', 'delete', 'open-detail'],
  computed: {
    editContentProxy: {
      get() { return this.editContent },
      set(val) { this.$emit('edit', { comment: this.comment, content: val }) }
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
      this.$emit('edit', { comment: this.comment, content: this.editContentProxy })
    }
  }
}
</script>

<!-- 댓글 상세 모달 -->
<template>
  <div class="modal-bg" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">닫기</button>
      <div v-if="loading" class="loading-state">불러오는 중...</div>
      <div v-else-if="error" class="error-state">{{ error }}</div>
      <div v-else-if="comment" class="comment-detail">
        <div class="comment-header">
          <span class="comment-author">{{ comment.user?.nickname || comment.user?.username }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ['comment', 'loading', 'error'],
  emits: ['close'],
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    }
  }
}
</script>

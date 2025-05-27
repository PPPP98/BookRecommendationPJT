<template>
  <div class="comments-list">
    <CommentItem
      v-for="comment in comments || []"
      :key="comment.id"
      :comment="comment"
      :user-id="userId"
      :editing="editingCommentId === comment.id"
      :edit-content="editCommentContent"
      :edit-loading="editCommentLoading"
      :edit-error="editCommentError"
      @start-edit="onStartEdit"
      @cancel-edit="onCancelEdit"
      @edit="onEdit"
      @delete="onDelete"
      @open-detail="onOpenDetail"
    />
  </div>
</template>
<script>
import CommentItem from './CommentItem.vue'
export default {
  components: { CommentItem },
  props: [
    'comments', 'userId', 'editingCommentId', 'editCommentContent',
    'editCommentLoading', 'editCommentError'
  ],
  emits: [
    'start-edit-comment', 'cancel-edit-comment', 'edit-comment',
    'delete-comment', 'open-detail'
  ],
  methods: {
    onStartEdit(comment) { this.$emit('start-edit-comment', comment) },
    onCancelEdit() { this.$emit('cancel-edit-comment') },
    onEdit(payload) { this.$emit('edit-comment', payload) },
    onDelete(comment) { this.$emit('delete-comment', comment) },
    onOpenDetail(commentId) { this.$emit('open-detail', commentId) }
  }
}
</script>

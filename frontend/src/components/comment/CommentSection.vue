<template>
  <div class="comments-section">
    <h2>댓글 ({{ comments?.length || 0 }})</h2>
    <CommentForm
      :new-comment="newComment"
      :loading="commentLoading"
      @submit="onAddComment"
      @update:new-comment="$emit('update:new-comment', $event)"
    />
    <CommentList
      :comments="comments"
      :user-id="userId"
      :editing-comment-id="editingCommentId"
      :edit-comment-content="editCommentContent"
      :edit-comment-loading="editCommentLoading"
      :edit-comment-error="editCommentError"
      @start-edit-comment="onStartEditComment"
      @cancel-edit-comment="onCancelEditComment"
      @edit-comment="onEditComment"
      @delete-comment="onDeleteComment"
      @open-detail="onOpenDetail"
    />
    <CommentDetailModal
      v-if="showCommentDetail"
      :comment="selectedCommentDetail"
      :loading="commentDetailLoading"
      :error="commentDetailError"
      @close="$emit('close-detail')"
    />
  </div>
</template>
<script>
import CommentForm from './CommentForm.vue'
import CommentList from './CommentList.vue'
import CommentDetailModal from './CommentDetailModal.vue'
export default {
  components: { CommentForm, CommentList, CommentDetailModal },
  props: [
    'comments', 'userId', 'threadId',
    'commentLoading', 'editCommentLoading', 'editCommentError',
    'editingCommentId', 'editCommentContent',
    'showCommentDetail', 'selectedCommentDetail',
    'commentDetailLoading', 'commentDetailError', 'newComment'
  ],
  emits: [
    'add-comment', 'edit-comment', 'delete-comment', 'open-detail',
    'start-edit-comment', 'cancel-edit-comment',
    'close-detail', 'update:new-comment'
  ],
  methods: {
    onAddComment(content) { this.$emit('add-comment', content) },
    onEditComment(payload) { this.$emit('edit-comment', payload) },
    onDeleteComment(comment) { this.$emit('delete-comment', comment) },
    onOpenDetail(commentId) { this.$emit('open-detail', commentId) },
    onStartEditComment(comment) { this.$emit('start-edit-comment', comment) },
    onCancelEditComment() { this.$emit('cancel-edit-comment') }
  }
}
</script>

<!-- 댓글 작성 폼 -->
<template>
  <div class="comment-form">
    <textarea v-model="contentProxy" placeholder="댓글을 작성하세요"></textarea>
    <button @click="onSubmit" :disabled="!contentProxy.trim() || loading">등록</button>
  </div>
</template>
<script>
export default {
  props: ['newComment', 'loading'],
  emits: ['submit', 'update:new-comment'],
  computed: {
    contentProxy: {
      get() { return this.newComment },
      set(val) { this.$emit('update:new-comment', val) }
    }
  },
  methods: {
    onSubmit() {
      this.$emit('submit', this.contentProxy)
    }
  }
}
</script>

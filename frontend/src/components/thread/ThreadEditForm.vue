<template>
  <div class="edit-form">
    <input v-model="titleProxy" placeholder="제목 수정" />
    <textarea v-model="contentProxy" rows="10" placeholder="내용 수정"></textarea>
    <div class="edit-actions">
      <button @click="$emit('submit')" class="submit-btn" :disabled="loading">저장</button>
      <button @click="$emit('cancel')" class="cancel-btn">취소</button>
    </div>
    <div v-if="error" class="error-state">{{ error }}</div>
  </div>
</template>
<script>
export default {
  props: ['title', 'content', 'loading', 'error'],
  emits: ['update:title', 'update:content', 'submit', 'cancel'],
  computed: {
    titleProxy: {
      get() { return this.title },
      set(val) { this.$emit('update:title', val) }
    },
    contentProxy: {
      get() { return this.content },
      set(val) { this.$emit('update:content', val) }
    }
  }
}
</script>

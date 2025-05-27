<!-- 댓글 작성 폼 -->
<template>
  <div class="comment-form">
    <div class="textarea-wrapper" :class="{ focused: isFocused }">
      <textarea
        v-model="contentProxy"
        placeholder="이 글에 대한 생각을 공유해보세요"
        @focus="isFocused = true"
        @blur="isFocused = false"
        @input="adjustHeight"
        ref="textarea"
        :maxlength="maxLength"
        :disabled="loading"
      ></textarea>
      <div class="form-footer">
        <span class="char-count" :class="{ 'near-limit': contentProxy.length > maxLength * 0.8 }">
          {{ contentProxy.length }}/{{ maxLength }}
        </span>
        <button 
          class="submit-btn" 
          @click="onSubmit" 
          :disabled="!isValid || loading"
        >
          <span v-if="loading" class="loading-spinner"></span>
          <span v-else>댓글 작성</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['newComment', 'loading'],
  emits: ['submit', 'update:new-comment'],
  data() {
    return {
      isFocused: false,
      maxLength: 300
    }
  },
  computed: {
    contentProxy: {
      get() { return this.newComment },
      set(val) { this.$emit('update:new-comment', val) }
    },
    isValid() {
      return this.contentProxy.trim().length > 0 && this.contentProxy.length <= this.maxLength
    }
  },
  methods: {
    onSubmit() {
      if (!this.isValid) return
      this.$emit('submit', this.contentProxy)
    },
    adjustHeight() {
      const textarea = this.$refs.textarea
      textarea.style.height = 'auto'
      textarea.style.height = textarea.scrollHeight + 'px'
    }
  }
}
</script>

<style scoped>
.comment-form {
  margin-bottom: 2rem;
}

.textarea-wrapper {
  background: #f8f9fa;
  border: 1.5px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.textarea-wrapper.focused {
  border-color: var(--color-accent);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  background: #fff;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 1.2rem;
  border: none;
  resize: none;
  font-size: 1.05rem;
  line-height: 1.5;
  font-family: inherit;
  background: transparent;
  color: #333;
}

textarea:focus {
  outline: none;
}

textarea:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
  color: #888;
}

textarea::placeholder {
  color: #888;
  opacity: 0.8;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.2rem;
  background: #fff;
  border-top: 1px solid #eee;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.03);
}

.char-count {
  color: #666;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.char-count.near-limit {
  color: #dc3545;
  font-weight: 600;
}

.submit-btn {
  background: #000;
  color: #fff;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background: #ffffff;
  color: #000;
  border: #000 1px solid;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #fff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 600px) {
  textarea {
    padding: 1rem;
    font-size: 1rem;
    min-height: 80px;
  }
  
  .form-footer {
    padding: 0.6rem 1rem;
  }
  
  .submit-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}
</style>

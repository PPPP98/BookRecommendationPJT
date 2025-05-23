<!-- 
  ErrorPage 컴포넌트
  역할: 에러, 로딩, 빈 상태를 표시
  Props:
    - type: String - 표시할 상태 유형 ('error', 'loading', 'empty')
    - message: String - 표시할 메시지
    - description: String - 부가 설명 (선택)
-->
<template>
  <div class="error-page">
    <div class="content">
      <!-- 로딩 상태 -->
      <template v-if="type === 'loading'">
        <div class="loading-spinner"></div>
        <h2>{{ message || '로딩 중...' }}</h2>
        <p v-if="description">{{ description }}</p>
      </template>

      <!-- 에러 상태 -->
      <template v-else-if="type === 'error'">
        <div class="icon error">❌</div>
        <h2>{{ message || '오류가 발생했습니다' }}</h2>
        <p v-if="description">{{ description }}</p>
        <div class="actions">
          <button @click="reload" class="action-button">
            새로고침
          </button>
          <button @click="goBack" class="action-button secondary">
            이전 페이지
          </button>
        </div>
      </template>

      <!-- 빈 상태 -->
      <template v-else-if="type === 'empty'">
        <div class="icon empty">📭</div>
        <h2>{{ message || '데이터가 없습니다' }}</h2>
        <p v-if="description">{{ description }}</p>
        <slot name="action"></slot>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorPage',
  props: {
    type: {
      type: String,
      required: true,
      validator: value => ['error', 'loading', 'empty'].includes(value)
    },
    message: String,
    description: String
  },
  methods: {
    reload() {
      window.location.reload()
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped>
.error-page {
  min-height: 50vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.content {
  max-width: 400px;
}

.icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

h2 {
  margin-bottom: 1rem;
  color: #333;
}

p {
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.action-button {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  border: none;
}

.action-button:not(.secondary) {
  background: #0066cc;
  color: white;
}

.action-button.secondary {
  background: white;
  border: 1px solid #0066cc;
  color: #0066cc;
}

/* 로딩 스피너 */
.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 2rem;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #0066cc;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

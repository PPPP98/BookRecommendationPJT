<!-- 
  Modal 컴포넌트
  역할: 팝업 메시지 표시
  기능:
    - 모달 표시/숨김
    - 커스텀 컨텐츠 지원
    - 버튼 커스터마이징
-->
<template>
  <div 
    v-if="modelValue" 
    class="modal-overlay" 
    @click="$emit('update:modelValue', false)"
    role="dialog" 
    aria-modal="true" 
    aria-labelledby="modal-title"
  >
    <div class="modal-content" @click.stop>
      <button class="close-button" @click="$emit('update:modelValue', false)" aria-label="닫기">&times;</button>
      <div class="modal-body">
        <slot></slot>
      </div>
      <div class="modal-footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  position: relative;
  animation: slideIn 0.3s ease;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
  }
  to {
    transform: translateY(0);
  }
}
</style>

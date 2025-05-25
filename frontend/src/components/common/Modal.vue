<!-- 
  Modal 컴포넌트
  역할: 팝업 메시지 표시
  기능:
    - 모달 표시/숨김
    - 커스텀 컨텐츠 지원
    - 버튼 커스터마이징
-->
<template>
  <div v-if="modelValue" class="modal-overlay" @click="$emit('update:modelValue', false)">
    <div class="modal-content" @click.stop>
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
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 90%;
  width: 400px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.modal-body {
  margin-bottom: 1.5rem;
  text-align: center;
}

.modal-footer {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.modal-footer button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.modal-footer button.primary {
  background-color: #0066cc;
  color: white;
}

.modal-footer button.secondary {
  background-color: #6c757d;
  color: white;
}
</style>

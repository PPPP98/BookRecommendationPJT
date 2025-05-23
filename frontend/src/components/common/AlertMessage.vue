<!-- 
  AlertMessage 컴포넌트
  역할: 사용자에게 알림 메시지를 표시하는 공통 컴포넌트
  Props:
    - message: String (필수) - 표시할 메시지
    - type: String (기본값: 'info') - 알림 타입 ('success', 'error', 'info', 'warning')
-->
<template>
  <div v-if="show" :class="['alert', `alert-${type}`]">
    {{ message }}
    <button class="close-btn" @click="closeAlert">&times;</button>
  </div>
</template>

<script>
export default {
  name: 'AlertMessage',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'info',
      validator: value => ['success', 'error', 'info', 'warning'].includes(value)
    },
    timeout: {
      type: Number,
      default: 3000
    }
  },
  data() {
    return {
      show: true
    }
  },
  mounted() {
    if (this.timeout) {
      setTimeout(this.closeAlert, this.timeout)
    }
  },
  methods: {
    closeAlert() {
      this.show = false
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.alert {
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
  position: relative;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-info {
  background-color: #cce5ff;
  color: #004085;
  border: 1px solid #b8daff;
}

.alert-warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.close-btn {
  position: absolute;
  right: 1rem;
  top: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: inherit;
}
</style>

<template>
  <div class="page first-page">
    <ImageGrid />
    <div class="login-section">
      <LoginModal />
    </div>
  </div>
</template>

<script setup>
import ImageGrid from '../../components/common/ImageGrid.vue'
import LoginModal from '../../components/user/LoginModal.vue'
import { useAuthStore } from '../../stores/auth'
</script>

<style scoped>
.page {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.first-page {
  background-color: white;
}

.login-section {
  position: absolute;
  top: 50%;
  right: 10%;
  transform: translateY(-50%);
  width: 30%;
  max-width: 450px;
  z-index: 20;
  background-color: transparent;
  border-radius: 10px;
}

@media (max-width: 1200px) {
  .login-section {
    width: 40%;
  }
}

@media (max-width: 768px) {
  .login-section {
    width: 90%;
    max-width: 400px;
    right: 50%;
    transform: translate(50%, -50%);
  }
}
</style>
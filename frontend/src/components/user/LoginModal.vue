<template>
  <div class="login-container">
    <!-- 로고 및 제목 -->
    <div class="logo-container">
      <img src="/default-profile.png.jpg" alt="Logo" class="logo" />
      <h2>아이디어를 얻으세요</h2>
      <p class="welcome-text">다음에 읽을 책을 추천해드립니다</p>
    </div>

    <!-- 로그인 폼 -->
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="input-group">
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          placeholder="이메일"
          required
        />
      </div>

      <div class="input-group">
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          placeholder="비밀번호"
          required
        />
      </div>

      <div class="password-options">
        <a href="#" class="forgot-password">비밀번호를 잊으셨나요?</a>
      </div>

      <button type="submit" class="login-button">로그인</button>
      
      <div class="divider">또는</div>
      
      <!-- 소셜 로그인 버튼 (더미) -->
      <button type="button" class="social-button facebook">
        <span>Facebook으로 계속하기</span>
      </button>
      
      <button type="button" class="social-button google">
        <span>Google 계정으로 계속하기</span>
      </button>

      <div class="signup-link">
        <span>아직 회원이 아니신가요?</span>
        <a href="#" @click.prevent="goToSignup">가입하기</a>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = () => {
  // 실제 로그인 로직은 여기에 구현
  console.log('로그인 시도:', email.value, password.value);
  // 성공 시 리다이렉트 로직 (임시)
  // router.push('/dashboard');
};

const goToSignup = () => {
  // 회원가입 페이지로 이동
  router.push('/signup');
};
</script>

<style scoped>
.login-container {
  background-color: rgba(255, 255, 255, 0.95);
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  z-index: 10;
  backdrop-filter: blur(8px); /* 배경에 블러 효과 강화 */
}

.logo-container {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-bottom: 1rem;
}

h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #000;
  margin-bottom: 0.5rem;
}

.welcome-text {
  font-size: 1rem;
  color: #B6B09F;
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.input-group {
  display: flex;
  flex-direction: column;
}

input {
  padding: 0.85rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(182, 176, 159, 0.3);
  font-size: 1rem;
  background-color: rgba(242, 242, 242, 0.5);
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

input:focus {
  border-color: #B6B09F;
  outline: none;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.password-options {
  display: flex;
  justify-content: flex-end;
  margin: 0.25rem 0;
}

.forgot-password {
  font-size: 0.8rem;
  color: #B6B09F;
  text-decoration: none;
}

.login-button {
  padding: 0.85rem;
  background-color: #B6B09F;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

.login-button:hover {
  background-color: #a79e8d;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.divider {
  text-align: center;
  color: #B6B09F;
  margin: 1rem 0;
  position: relative;
}

.divider::before, .divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 45%;
  height: 1px;
  background-color: #EAE4D5;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.social-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem;
  border-radius: 10px;
  border: 1px solid rgba(234, 228, 213, 0.7);
  background-color: rgba(255, 255, 255, 0.8);
  margin-bottom: 0.9rem;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: all 0.25s ease;
  font-weight: 500;
  transition: background-color 0.2s;
  color: #000;
}

.facebook {
  border-color: #EAE4D5;
}

.facebook:hover {
  background-color: #F0F8FF;
  border-color: #4267B2;
  box-shadow: 0 4px 8px rgba(66, 103, 178, 0.15);
  transform: translateY(-1px);
}

.google {
  border-color: #EAE4D5;
}

.google:hover {
  background-color: #FFF8F0;
  border-color: #DB4437;
  box-shadow: 0 4px 8px rgba(219, 68, 55, 0.15);
  transform: translateY(-1px);
}

.signup-link {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
  color: #B6B09F;
}

.signup-link a {
  color: #000;
  text-decoration: none;
  margin-left: 0.25rem;
  font-weight: 500;
}

.signup-link a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .login-container {
    max-width: 80%;
    margin: 0 auto;
  }
}
</style>

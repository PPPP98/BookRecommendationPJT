<!-- 
  LoginPage 컴포넌트
  역할: 사용자 로그인 페이지
  기능:
    - 이메일/비밀번호 로그인
    - 소셜 로그인 (카카오/네이버/구글)
    - 회원가입, 비밀번호 재설정 링크
-->
<template>
  <div class="login-page">
    <div class="login-container">
      <h1>로그인</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">이메일</label>
          <input 
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="이메일을 입력하세요"
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input 
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="비밀번호를 입력하세요"
            class="form-input"
          >
        </div>

        <div class="form-actions">
          <label class="remember-me">
            <input type="checkbox" v-model="form.rememberMe">
            로그인 상태 유지
          </label>
          <router-link to="/auth/password-reset" class="forgot-password">
            비밀번호를 잊으셨나요?
          </router-link>
        </div>

        <button type="submit" class="login-button" :disabled="isLoading">
          {{ isLoading ? '로그인 중...' : '로그인' }}
        </button>
      </form>

      <div class="social-login">
        <h2>소셜 계정으로 로그인</h2>
        <div class="social-buttons">
          <button @click="socialLogin('kakao')" class="social-button kakao">
            카카오 로그인
          </button>
          <button @click="socialLogin('naver')" class="social-button naver">
            네이버 로그인
          </button>
          <button @click="socialLogin('google')" class="social-button google">
            구글 로그인
          </button>
        </div>
      </div>

      <div class="signup-link">
        계정이 없으신가요?
        <router-link to="/auth/signup">회원가입</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: '',
        rememberMe: false
      },
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      try {
        this.isLoading = true
        // TODO: API 연동 시 구현
        // const response = await api.post('/auth/login', this.form)
        // this.$store.commit('setUser', response.data.user)
        // this.$router.push('/')
      } catch (error) {
        console.error('Login failed:', error)
        // TODO: 에러 처리
      } finally {
        this.isLoading = false
      }
    },
    async socialLogin(provider) {
      try {
        // TODO: API 연동 시 구현
        console.log(`Social login with ${provider}`)
        // window.location.href = `/api/auth/${provider}`
      } catch (error) {
        console.error('Social login failed:', error)
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
  padding: 2rem;
}

.login-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.social-login {
  margin-top: 2rem;
  text-align: center;
}

.social-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}

.social-button {
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.social-button.kakao {
  background: #FEE500;
  color: #000000;
}

.social-button.naver {
  background: #03C75A;
  color: white;
}

.social-button.google {
  background: white;
  border: 1px solid #ddd;
  color: #333;
}

.signup-link {
  text-align: center;
  margin-top: 2rem;
}

.signup-link a {
  color: #0066cc;
  text-decoration: none;
  margin-left: 0.5rem;
}

.forgot-password {
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}
</style>

<!-- 
  SignupPage 컴포넌트
  역할: 회원가입 페이지
  기능:
    - 이메일, 닉네임, 비밀번호 입력
    - 이메일/닉네임 중복 체크
    - 관심 카테고리 선택
    - 약관 동의
-->
<template>
  <div class="signup-page">
    <div class="signup-container">
      <h1>회원가입</h1>
      
      <form @submit.prevent="handleSignup" class="signup-form">
        <div class="form-group">
          <label for="email">이메일</label>
          <div class="input-with-button">
            <input 
              id="email"
              v-model="form.email"
              type="email"
              required
              placeholder="이메일을 입력하세요"
              :disabled="form.emailVerified"
              class="form-input"
            >
            <button 
              type="button" 
              @click="checkEmailDuplicate"
              :disabled="!form.email || form.emailVerified"
              class="check-button"
            >
              중복확인
            </button>
          </div>
          <span v-if="form.emailVerified" class="success-message">
            사용 가능한 이메일입니다
          </span>
        </div>

        <div class="form-group">
          <label for="username">닉네임</label>
          <div class="input-with-button">
            <input 
              id="username"
              v-model="form.username"
              type="text"
              required
              placeholder="닉네임을 입력하세요"
              :disabled="form.usernameVerified"
              class="form-input"
            >
            <button 
              type="button"
              @click="checkUsernameDuplicate"
              :disabled="!form.username || form.usernameVerified"
              class="check-button"
            >
              중복확인
            </button>
          </div>
          <span v-if="form.usernameVerified" class="success-message">
            사용 가능한 닉네임입니다
          </span>
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
          <p class="help-text">8자 이상, 영문/숫자/특수문자 조합</p>
        </div>

        <div class="form-group">
          <label for="passwordConfirm">비밀번호 확인</label>
          <input 
            id="passwordConfirm"
            v-model="form.passwordConfirm"
            type="password"
            required
            placeholder="비밀번호를 다시 입력하세요"
            class="form-input"
          >
          <span v-if="passwordMismatch" class="error-message">
            비밀번호가 일치하지 않습니다
          </span>
        </div>

        <div class="form-group">
          <label>관심 카테고리</label>
          <div class="categories-container">
            <label v-for="category in categories" :key="category" class="category-checkbox">
              <input 
                type="checkbox"
                :value="category"
                v-model="form.interests"
              >
              {{ category }}
            </label>
          </div>
        </div>

        <div class="form-group agreements">
          <label class="agreement-checkbox">
            <input 
              type="checkbox"
              v-model="form.agreeTerms"
              required
            >
            [필수] 이용약관 동의
          </label>
          <label class="agreement-checkbox">
            <input 
              type="checkbox"
              v-model="form.agreePrivacy"
              required
            >
            [필수] 개인정보 처리방침 동의
          </label>
          <label class="agreement-checkbox">
            <input 
              type="checkbox"
              v-model="form.agreeMarketing"
            >
            [선택] 마케팅 정보 수신 동의
          </label>
        </div>

        <button 
          type="submit" 
          class="signup-button"
          :disabled="!isFormValid || isLoading"
        >
          {{ isLoading ? '가입 중...' : '회원가입' }}
        </button>
      </form>

      <div class="login-link">
        이미 계정이 있으신가요?
        <router-link to="/auth/login">로그인</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignupPage',
  data() {
    return {
      form: {
        email: '',
        emailVerified: false,
        username: '',
        usernameVerified: false,
        password: '',
        passwordConfirm: '',
        interests: [],
        agreeTerms: false,
        agreePrivacy: false,
        agreeMarketing: false
      },
      categories: ['소설', '에세이', '경제/경영', '자기계발', '인문', '과학'],
      isLoading: false
    }
  },
  computed: {
    passwordMismatch() {
      return this.form.password && 
             this.form.passwordConfirm && 
             this.form.password !== this.form.passwordConfirm
    },
    isFormValid() {
      return this.form.emailVerified &&
             this.form.usernameVerified &&
             this.form.password &&
             this.form.password === this.form.passwordConfirm &&
             this.form.interests.length > 0 &&
             this.form.agreeTerms &&
             this.form.agreePrivacy
    }
  },
  methods: {
    async checkEmailDuplicate() {
      try {
        // TODO: API 연동 시 구현
        // const response = await api.post('/auth/check-email', { email: this.form.email })
        this.form.emailVerified = true
      } catch (error) {
        console.error('Email check failed:', error)
        // TODO: 에러 처리
      }
    },
    async checkUsernameDuplicate() {
      try {
        // TODO: API 연동 시 구현
        // const response = await api.post('/auth/check-username', { username: this.form.username })
        this.form.usernameVerified = true
      } catch (error) {
        console.error('Username check failed:', error)
        // TODO: 에러 처리
      }
    },
    async handleSignup() {
      try {
        this.isLoading = true
        // TODO: API 연동 시 구현
        // const response = await api.post('/auth/signup', this.form)
        // this.$router.push('/auth/login')
      } catch (error) {
        console.error('Signup failed:', error)
        // TODO: 에러 처리
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
  padding: 2rem;
}

.signup-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 500px;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
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

.input-with-button {
  display: flex;
  gap: 0.5rem;
}

.input-with-button .form-input {
  flex: 1;
}

.check-button {
  padding: 0 1rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.check-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.categories-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.category-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.agreements {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.agreement-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.signup-button {
  width: 100%;
  padding: 0.75rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.signup-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.help-text {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.25rem;
}

.success-message {
  color: #28a745;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.login-link {
  text-align: center;
  margin-top: 2rem;
}

.login-link a {
  color: #0066cc;
  text-decoration: none;
  margin-left: 0.5rem;
}
</style>

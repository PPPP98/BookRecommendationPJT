<!-- 
  PasswordResetPage 컴포넌트
  역할: 비밀번호 재설정 페이지
  기능:
    - 이메일 입력 및 인증 메일 발송
    - 인증 코드 입력
    - 새 비밀번호 설정
-->
<template>
  <div class="password-reset-page">
    <div class="password-reset-container">
      <h1>비밀번호 재설정</h1>
      
      <!-- Step 1: 이메일 입력 -->
      <form v-if="step === 1" @submit.prevent="sendVerificationEmail" class="reset-form">
        <div class="form-group">
          <label for="email">이메일</label>
          <input 
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="가입된 이메일을 입력하세요"
            class="form-input"
          >
        </div>

        <button type="submit" class="submit-button" :disabled="isLoading">
          {{ isLoading ? '전송 중...' : '인증 메일 보내기' }}
        </button>
      </form>

      <!-- Step 2: 인증 코드 입력 -->
      <form v-if="step === 2" @submit.prevent="verifyCode" class="reset-form">
        <div class="form-group">
          <label for="code">인증 코드</label>
          <input 
            id="code"
            v-model="form.verificationCode"
            type="text"
            required
            placeholder="이메일로 받은 인증 코드를 입력하세요"
            class="form-input"
          >
        </div>

        <div class="timer" v-if="timeLeft > 0">
          남은 시간: {{ formattedTimeLeft }}
        </div>

        <button 
          type="button" 
          @click="sendVerificationEmail" 
          class="resend-button"
          :disabled="timeLeft > 0"
        >
          인증 메일 다시 보내기
        </button>

        <button type="submit" class="submit-button" :disabled="isLoading">
          {{ isLoading ? '확인 중...' : '인증 코드 확인' }}
        </button>
      </form>

      <!-- Step 3: 새 비밀번호 설정 -->
      <form v-if="step === 3" @submit.prevent="resetPassword" class="reset-form">
        <div class="form-group">
          <label for="newPassword">새 비밀번호</label>
          <input 
            id="newPassword"
            v-model="form.newPassword"
            type="password"
            required
            placeholder="새 비밀번호를 입력하세요"
            class="form-input"
          >
          <p class="help-text">8자 이상, 영문/숫자/특수문자 조합</p>
        </div>

        <div class="form-group">
          <label for="newPasswordConfirm">비밀번호 확인</label>
          <input 
            id="newPasswordConfirm"
            v-model="form.newPasswordConfirm"
            type="password"
            required
            placeholder="새 비밀번호를 다시 입력하세요"
            class="form-input"
          >
          <span v-if="passwordMismatch" class="error-message">
            비밀번호가 일치하지 않습니다
          </span>
        </div>

        <button 
          type="submit" 
          class="submit-button"
          :disabled="isLoading || passwordMismatch"
        >
          {{ isLoading ? '변경 중...' : '비밀번호 변경' }}
        </button>
      </form>

      <!-- Step 4: 완료 -->
      <div v-if="step === 4" class="completion-message">
        <h2>비밀번호가 변경되었습니다</h2>
        <p>새로운 비밀번호로 로그인해주세요.</p>
        <router-link to="/auth/login" class="login-link">
          로그인 페이지로 이동
        </router-link>
      </div>

      <div class="back-to-login">
        <router-link to="/auth/login">로그인 페이지로 돌아가기</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PasswordResetPage',
  data() {
    return {
      step: 1,
      form: {
        email: '',
        verificationCode: '',
        newPassword: '',
        newPasswordConfirm: ''
      },
      isLoading: false,
      timeLeft: 0,
      timer: null
    }
  },
  computed: {
    passwordMismatch() {
      return this.form.newPassword && 
             this.form.newPasswordConfirm && 
             this.form.newPassword !== this.form.newPasswordConfirm
    },
    formattedTimeLeft() {
      const minutes = Math.floor(this.timeLeft / 60)
      const seconds = this.timeLeft % 60
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    }
  },
  methods: {
    startTimer() {
      this.timeLeft = 180 // 3 minutes
      clearInterval(this.timer)
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--
        } else {
          clearInterval(this.timer)
        }
      }, 1000)
    },
    async sendVerificationEmail() {
      try {
        this.isLoading = true
        // TODO: API 연동 시 구현
        // await api.post('/auth/password-reset/request', { email: this.form.email })
        this.step = 2
        this.startTimer()
      } catch (error) {
        console.error('Failed to send verification email:', error)
        // TODO: 에러 처리
      } finally {
        this.isLoading = false
      }
    },
    async verifyCode() {
      try {
        this.isLoading = true
        // TODO: API 연동 시 구현
        // await api.post('/auth/password-reset/verify', {
        //   email: this.form.email,
        //   code: this.form.verificationCode
        // })
        this.step = 3
      } catch (error) {
        console.error('Failed to verify code:', error)
        // TODO: 에러 처리
      } finally {
        this.isLoading = false
      }
    },
    async resetPassword() {
      try {
        this.isLoading = true
        // TODO: API 연동 시 구현
        // await api.post('/auth/password-reset/complete', {
        //   email: this.form.email,
        //   code: this.form.verificationCode,
        //   password: this.form.newPassword
        // })
        this.step = 4
      } catch (error) {
        console.error('Failed to reset password:', error)
        // TODO: 에러 처리
      } finally {
        this.isLoading = false
      }
    }
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  }
}
</script>

<style scoped>
.password-reset-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
  padding: 2rem;
}

.password-reset-container {
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

.submit-button {
  width: 100%;
  padding: 0.75rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.submit-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.resend-button {
  width: 100%;
  padding: 0.75rem;
  background: white;
  color: #0066cc;
  border: 1px solid #0066cc;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.resend-button:disabled {
  color: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}

.timer {
  text-align: center;
  color: #dc3545;
  margin-bottom: 1rem;
}

.help-text {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.25rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.completion-message {
  text-align: center;
}

.completion-message h2 {
  color: #28a745;
  margin-bottom: 1rem;
}

.back-to-login {
  text-align: center;
  margin-top: 2rem;
}

.back-to-login a, .login-link {
  color: #0066cc;
  text-decoration: none;
}
</style>

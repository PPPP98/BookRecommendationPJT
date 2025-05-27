<template>
  <div class="login-page">
    <div class="login-container">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">아이디 또는 이메일</label>
          <input
            id="email"
            v-model="form.email"
            type="text"
            required
            placeholder="아이디 또는 이메일을 입력하세요"
            class="form-input"
          />
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
          />
        </div>
        <div class="form-actions">
          <label class="remember-me">
            <input type="checkbox" v-model="form.rememberMe" />
            로그인 상태 유지
          </label>
          <router-link to="/auth/password-reset" class="forgot-password">
            비밀번호를 잊으셨나요?
          </router-link>
        </div>
        <button type="submit" class="login-button" :disabled="isLoading">
          {{ isLoading ? "로그인 중..." : "로그인" }}
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
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      form: {
        email: "",
        password: "",
        rememberMe: false,
      },
      isLoading: false,
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      this.errorMessage = "";

      try {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        if (this.form.email.includes('@') && !emailPattern.test(this.form.email.trim())) {
          this.errorMessage = "유효한 이메일 주소를 입력해주세요.";
          this.isLoading = false;
          return;
        }
        const loginData = {
          username: this.form.email.trim(),
          password: this.form.password,
        };
        const response = await axios.post("/api/accounts/login/", loginData);
        const { access, refresh, user } = response.data;
        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh || "");
        localStorage.setItem("user", JSON.stringify(user));
        axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
        if (this.form.rememberMe) {
          localStorage.setItem("rememberMe", "true");
        } else {
          localStorage.removeItem("rememberMe");
        }
        this.$router.push("/");
      } catch (error) {
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          if (typeof errorData === "string") {
            this.errorMessage = errorData;
          } else if (errorData.detail) {
            this.errorMessage = errorData.detail;
          } else if (errorData.non_field_errors) {
            this.errorMessage = errorData.non_field_errors.join(", ");
          } else {
            const errorMessages = [];
            for (const field in errorData) {
              if (Array.isArray(errorData[field])) {
                errorMessages.push(`${field}: ${errorData[field].join(", ")}`);
              } else {
                errorMessages.push(`${field}: ${errorData[field]}`);
              }
            }
            this.errorMessage = errorMessages.length > 0
              ? errorMessages.join("\n")
              : "로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.";
          }
        } else {
          this.errorMessage = "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
        }
      } finally {
        this.isLoading = false;
      }
    },
    async socialLogin(provider) {
      try {
        const socialLoginUrl = `/api/auth/${provider}`;
        window.location.href = socialLoginUrl;
      } catch (error) {
        this.errorMessage = "소셜 로그인에 실패했습니다. 다시 시도해주세요.";
      }
    },
  },
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
}
.login-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: 2.5rem auto 0 auto; /* 로그인 폼만 아래로 내림 */
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
  background: #fee500;
  color: #000000;
}
.social-button.naver {
  background: #03c75a;
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
.error-message {
  color: red;
  text-align: center;
  margin-top: 1rem;
}
@media (max-width: 1200px) {
  .login-container {
    max-width: 600px;
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .login-container {
    padding: 1rem;
  }
  .form-input {
    font-size: 0.9rem;
  }
  .login-button {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 0.5rem;
  }
  .form-input {
    font-size: 0.8rem;
  }
  .login-button {
    font-size: 0.9rem;
  }
}
</style>

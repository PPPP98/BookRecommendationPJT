<template>
  <div class="login-page">
    <div class="login-container">
      <h1>로그인</h1>

      <!-- 로그인 폼 -->
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

      <!-- 소셜 로그인 -->
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

      <!-- 회원가입 링크 -->
      <div class="signup-link">
        계정이 없으신가요?
        <router-link to="/auth/signup">회원가입</router-link>
      </div>

      <!-- 에러 메시지 -->
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
    // 로그인 처리
    async handleLogin() {
      this.isLoading = true;
      this.errorMessage = "";

      try {
        // 이메일 형식 검증 (이메일 입력 시에만 적용)
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        // 이메일 형식인 경우에만 유효성 검사 실행
        if (this.form.email.includes('@') && !emailPattern.test(this.form.email.trim())) {
          this.errorMessage = "유효한 이메일 주소를 입력해주세요.";
          return;
        }

        // 로그인 데이터 전송 (API 명세에 맞게 구성)
        // API 명세: POST /api/accounts/login/
        // dj-rest-auth는 기본적으로 username과 password를 요구합니다
        const loginData = {
          username: this.form.email.trim(), // 이메일을 username으로 사용
          password: this.form.password,
        };

        console.log("로그인 시도:", { username: loginData.username });
        
        const response = await axios.post("/api/accounts/login/", loginData);
        console.log("로그인 응답:", response.data);
        console.log("사용자 정보:", response.data.user);
        console.log("토큰 정보:", { 
          access: response.data.access,
          refresh: response.data.refresh 
        });

        // 응답 데이터에서 토큰과 사용자 정보 저장
        const { access, refresh, user } = response.data;
        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh || ""); // refresh 토큰이 없는 경우 빈 문자열 저장
        localStorage.setItem("user", JSON.stringify(user));

        // 인증 헤더 설정
        axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;

        // 로그인 상태 유지 옵션 처리
        if (this.form.rememberMe) {
          localStorage.setItem("rememberMe", "true");
        } else {
          localStorage.removeItem("rememberMe");
        }

        // 메인 페이지로 이동
        this.$router.push("/");
      } catch (error) {
        console.error("Login failed:", error);

        // DRF의 에러 응답 처리
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          
          if (typeof errorData === "string") {
            this.errorMessage = errorData;
          } else if (errorData.detail) {
            this.errorMessage = errorData.detail;
          } else if (errorData.non_field_errors) {
            // dj-rest-auth는 종종 non_field_errors에 인증 관련 오류를 담습니다
            this.errorMessage = errorData.non_field_errors.join(", ");
          } else {
            // 필드별 에러 메시지 처리 (SignupPage와 유사하게)
            const errorMessages = [];
            for (const field in errorData) {
              if (Array.isArray(errorData[field])) {
                errorMessages.push(`${field}: ${errorData[field].join(", ")}`);
              } else {
                errorMessages.push(`${field}: ${errorData[field]}`);
              }
            }
            
            if (errorMessages.length > 0) {
              this.errorMessage = errorMessages.join("\n");
            } else {
              this.errorMessage = "로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.";
            }
          }
        } else {
          this.errorMessage = "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    // 소셜 로그인 처리
    async socialLogin(provider) {
      try {
        console.log(`소셜 로그인 시도: ${provider}`);
        
        // 소셜 로그인 엔드포인트로 리다이렉트
        const socialLoginUrl = `/api/auth/${provider}`;
        console.log(`리다이렉트 URL: ${socialLoginUrl}`);
        
        window.location.href = socialLoginUrl;
      } catch (error) {
        console.error("Social login failed:", error);
        this.errorMessage = "소셜 로그인에 실패했습니다. 다시 시도해주세요.";
      }
    },
  },
};
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
</style>
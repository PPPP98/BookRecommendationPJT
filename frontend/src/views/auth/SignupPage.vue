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
          <label for="username">아이디</label>
          <div class="input-with-button">
            <input
              id="username"
              v-model="username"
              type="username"
              required
              placeholder="아이디를 입력하세요"
              :disabled="usernameVerified"
              class="form-input"
            />
            <button
              type="button"
              @click="checkUsernameDuplicate"
              :disabled="!username || usernameVerified"
              class="check-button"
            >
              중복확인
            </button>
          </div>
          <span v-if="usernameChecked" :class="usernameVerified ? 'success-message' : 'error-message'">
            {{ usernameVerified ? '사용 가능한 아이디입니다' : '사용할 수 없는 아이디입니다' }}
          </span>
        </div>

        <div class="form-group">
          <label for="email">이메일</label>
          <div class="input-with-button">
            <input
              id="email"
              v-model="email"
              type="text"
              required
              placeholder="이메일을 입력하세요"
              :disabled="emailVerified"
              class="form-input"
            />
            <button
              type="button"
              @click="checkEmailDuplicate"
              :disabled="!email || emailVerified"
              class="check-button"
            >
              중복확인
            </button>
          </div>
          <span v-if="emailChecked" :class="emailVerified ? 'success-message' : 'error-message'">
            {{ emailVerified ? '사용 가능한 이메일입니다' : '사용할 수 없는 이메일입니다' }}
          </span>
        </div>

        <div class="form-group">
          <label for="nickname">닉네임</label>
          <div class="input-with-button">
            <input
              id="nickname"
              v-model="nickname"
              type="text"
              required
              placeholder="닉네임을 입력하세요"
              :disabled="nicknameVerified"
              class="form-input"
            />
            <button
              type="button"
              @click="checkNicknameDuplicate"
              :disabled="!nickname || nicknameVerified"
              class="check-button"
            >
              중복확인
            </button>
          </div>
          <span v-if="nicknameChecked" :class="nicknameVerified ? 'success-message' : 'error-message'">
            {{ nicknameVerified ? '사용 가능한 닉네임입니다' : '사용할 수 없는 닉네임입니다' }}
          </span>
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="비밀번호를 입력하세요"
            class="form-input"
          />
          <div class="password-validation">
            <p :class="[
              'validation-message',
              { 'success-message': passwordValidation.isValid, 'error-message': password && !passwordValidation.isValid }
            ]" v-if="password">
              {{ passwordValidation.isValid ? '사용 가능한 비밀번호입니다' : '다음 요구사항을 충족해야 합니다:' }}
            </p>
            <ul v-if="password && !passwordValidation.isValid" class="validation-list">
              <li :class="{ 'valid': passwordValidation.lengthValid }">8자 이상</li>
              <li :class="{ 'valid': passwordValidation.hasLetter }">영문자 포함</li>
              <li :class="{ 'valid': passwordValidation.hasNumber }">숫자 포함</li>
              <li :class="{ 'valid': passwordValidation.hasSpecial }">특수문자 포함 (@$!%*#?&)</li>
            </ul>
          </div>
        </div>

        <div class="form-group">
          <label for="passwordConfirm">비밀번호 확인</label>
          <input
            id="passwordConfirm"
            v-model="passwordConfirm"
            type="password"
            required
            placeholder="비밀번호를 다시 입력하세요"
            class="form-input"
          />
          <span v-if="passwordMismatch" class="error-message">
            비밀번호가 일치하지 않습니다
          </span>
        </div>

        <div class="form-group">
          <label>관심 카테고리</label>
          <div class="categories-container">
            <label
              v-for="category in categories"
              :key="category.id"
              class="category-checkbox"
            >
              <input type="checkbox" :value="category.name" v-model="interestedCategories" />
              {{ category.name }}
            </label>
          </div>
        </div>

        <div class="form-group">
          <label for="bio">자기소개</label>
          <textarea
            id="bio"
            v-model="bio"
            rows="3"
            placeholder="자기소개를 입력하세요 (선택)"
            class="form-input"
          ></textarea>
          <p class="help-text">자기소개는 선택 사항입니다</p>
        </div>

        <div class="form-group agreements">
          <label class="agreement-checkbox">
            <input type="checkbox" v-model="agreement.agreeTerms" required />
            [필수] 이용약관 동의
          </label>
          <label class="agreement-checkbox">
            <input type="checkbox" v-model="agreement.agreePrivacy" required />
            [필수] 개인정보 처리방침 동의
          </label>
          <label class="agreement-checkbox">
            <input type="checkbox" v-model="agreement.agreeMarketing" />
            [선택] 마케팅 정보 수신 동의
          </label>
        </div>

        <button
          type="submit"
          class="signup-button"
          :disabled="!isFormValid || isLoading"
        >
          {{ isLoading ? "가입 중..." : "회원가입" }}
        </button>
      </form>

      <div class="login-link">
        이미 계정이 있으신가요?
        <router-link to="/auth/login">로그인</router-link>
      </div>

      <!-- 모달 컴포넌트 -->
      <Modal v-model="showSuccessModal" title="가입 완료">
        <p>회원가입이 성공적으로 완료되었습니다.</p>
        <p>서비스를 이용하시려면 로그인해주세요.</p>
        <template #footer>
          <button @click="goToLogin" class="primary-button">로그인하기</button>
          <button @click="goToMain" class="secondary-button">메인으로</button>
        </template>
      </Modal>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Modal from '@/components/common/Modal.vue'

export default {
  components: {
    Modal
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    // 모달 상태 관리
    const showSuccessModal = ref(false)

    // 페이지 이동 함수
    const goToLogin = () => {
      router.push('/auth/login')
    }

    const goToMain = () => {
      router.push('/')
    }
    
    // 폼 데이터
    const username = ref('')
    const email = ref('')
    const nickname = ref('')
    const password = ref('')
    const passwordConfirm = ref('')
    const isLoading = ref(false)
    const bio = ref('')
    const interestedCategories = ref([])
    
    // 상태 메시지 관리
    const statusMessage = ref('')
    const messageType = ref('') // 'success' 또는 'error'

    // 메시지 표시 함수
    const showMessage = (message, type = 'error') => {
      statusMessage.value = message
      messageType.value = type
      // 3초 후 메시지 제거
      setTimeout(() => {
        statusMessage.value = ''
        messageType.value = ''
      }, 3000)
    }

    const agreement = ref({
      agreeTerms: false,
      agreePrivacy: false,
      agreeMarketing: false
    })

    const categories = [
      { id: 1, name: '소설/시/희곡' },
      { id: 2, name: '경제/경영' },
      { id: 3, name: '자기계발' },
      { id: 4, name: '인문/교양' },
      { id: 5, name: '취미/실용' },
      { id: 6, name: '어린이/청소년' },
      { id: 7, name: '과학' }
    ]

    // 비밀번호 일치 여부 확인
    const passwordMismatch = computed(() => {
      return password.value && passwordConfirm.value && password.value !== passwordConfirm.value
    })

    // 이메일 유효성 검사
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/
    
    // 비밀번호 유효성 검사
    const passwordValidation = computed(() => {
      if (!password.value) {
        return {
          lengthValid: false,
          hasLetter: false,
          hasNumber: false,
          hasSpecial: false,
          isValid: false
        }
      }
      
      const lengthValid = password.value.length >= 8
      const hasLetter = /[A-Za-z]/.test(password.value)
      const hasNumber = /\d/.test(password.value)
      const hasSpecial = /[@$!%*#?&]/.test(password.value)
      
      return {
        lengthValid,
        hasLetter,
        hasNumber,
        hasSpecial,
        isValid: lengthValid && hasLetter && hasNumber && hasSpecial
      }
    })

    // 폼 유효성 검사
    const isFormValid = computed(() => {
      // 기본 필드 값 검증
      const hasRequiredFields = username.value && email.value && nickname.value && 
        password.value && passwordConfirm.value

      // 이메일 형식 검증
      const emailValid = email.value ? emailPattern.test(email.value) : false

      // 비밀번호 검증
      const passwordValid = 
        password.value && 
        passwordConfirm.value && 
        password.value === passwordConfirm.value && 
        passwordValidation.value.isValid

      // 중복 검사 완료 여부
      const duplicateChecksValid = 
        usernameVerified.value && 
        emailVerified.value && 
        nicknameVerified.value

      // 필수 약관 동의
      const agreementsValid = 
        agreement.value.agreeTerms && 
        agreement.value.agreePrivacy

      // 디버깅용 로그
      console.log('Form Validation Status:', {
        hasRequiredFields,
        emailValid,
        passwordValid,
        duplicateChecksValid,
        agreementsValid,
        passwordValidationStatus: passwordValidation.value
      })

      return hasRequiredFields && 
        emailValid && 
        passwordValid && 
        duplicateChecksValid && 
        agreementsValid
    })

    // 중복 확인 상태값 추가
    const usernameVerified = ref(false)
    const emailVerified = ref(false)
    const nicknameVerified = ref(false)
    const usernameChecked = ref(false)
    const emailChecked = ref(false)
    const nicknameChecked = ref(false)

    // 중복 확인 함수들
    const checkUsernameDuplicate = async () => {
      try {
        const response = await axios.get(`/api/accounts/check-username/?username=${username.value}`)
        usernameVerified.value = !response.data.exists
        usernameChecked.value = true
        if (!usernameVerified.value) {
          username.value = ''
        }
      } catch (error) {
        console.error('Username check failed:', error)
        showMessage('아이디 중복 확인 중 오류가 발생했습니다.')
        usernameChecked.value = false
      }
    }

    const checkEmailDuplicate = async () => {
      try {
        const response = await axios.get(`/api/accounts/check-email/?email=${email.value}`)
        emailVerified.value = !response.data.exists
        emailChecked.value = true
        if (!emailVerified.value) {
          email.value = ''
        }
      } catch (error) {
        console.error('Email check failed:', error)
        showMessage('이메일 중복 확인 중 오류가 발생했습니다.')
        emailChecked.value = false
      }
    }

    const checkNicknameDuplicate = async () => {
      try {
        const response = await axios.get(`/api/accounts/check-nickname/?nickname=${nickname.value}`)
        nicknameVerified.value = !response.data.exists
        nicknameChecked.value = true
        if (!nicknameVerified.value) {
          nickname.value = ''
        }
      } catch (error) {
        console.error('Nickname check failed:', error)
        showMessage('닉네임 중복 확인 중 오류가 발생했습니다.')
        nicknameChecked.value = false
      }
    }

    // 회원가입 제출 함수
    const handleSignup = async () => {
      if (!isFormValid.value) return

      isLoading.value = true
      
      try {
        // 선택된 카테고리 이름을 ID로 변환
        const selectedCategoryIds = interestedCategories.value.map(categoryName => {
          const category = categories.find(c => c.name === categoryName)
          return category ? category.id : null
        }).filter(id => id !== null)

        const signupData = {
          username: username.value,
          email: email.value,
          nickname: nickname.value,
          password1: password.value,
          password2: passwordConfirm.value,
          interested_categories: selectedCategoryIds
        }
        
        // bio가 있는 경우에만 추가
        if (bio.value) {
          signupData.bio = bio.value
        }
        
        await authStore.signup(signupData)
        // 성공 모달 표시
        showSuccessModal.value = true
      } catch (error) {
        console.error('회원가입 실패:', error)
        
        // DRF의 에러 응답 처리
        if (error.response && error.response.data) {
          const errorData = error.response.data
          
          if (typeof errorData === 'string') {
            showMessage(errorData)
          } else {
            // 필드별 에러 메시지 처리
            const errorMessages = []
            for (const field in errorData) {
              if (Array.isArray(errorData[field])) {
                errorMessages.push(`${field}: ${errorData[field].join(', ')}`)
              } else {
                errorMessages.push(`${field}: ${errorData[field]}`)
              }
            }
            showMessage('회원가입 실패:\n' + errorMessages.join('\n'))
          }
        } else {
          showMessage('서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
        }
      } finally {
        isLoading.value = false
      }
    }

    return {
      username,
      email,
      nickname,
      password,
      passwordConfirm,
      bio,
      categories,
      interestedCategories,
      agreement,
      isLoading,
      passwordMismatch,
      isFormValid,
      handleSignup,
      usernameVerified,
      emailVerified,
      nicknameVerified,
      checkUsernameDuplicate,
      checkEmailDuplicate,
      checkNicknameDuplicate,
      usernameChecked,
      emailChecked,
      nicknameChecked,
      statusMessage,
      messageType,
      passwordValidation,
      showSuccessModal,
      goToLogin,
      goToMain
    }
  }
}
</script>

<style scoped>
.password-validation {
  margin-top: 0.5rem;
}

.validation-list {
  list-style: none;
  padding-left: 0;
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #dc3545;
}

.validation-list li {
  margin: 0.25rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.validation-list li::before {
  content: "✕";
  position: absolute;
  left: 0;
  color: #dc3545;
}

.validation-list li.valid {
  color: #28a745;
}

.validation-list li.valid::before {
  content: "✓";
  color: #28a745;
}
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.status-message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
}

.status-message.success {
  background: #d4edda;
  color: #155724;
}

.status-message.error {
  background: #f8d7da;
  color: #721c24;
}

/* 모달 버튼 스타일 */
.primary-button {
  padding: 0.75rem 1.5rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  margin-left: 0.5rem;
}

.primary-button:hover {
  background: #0052a3;
}

.secondary-button {
  padding: 0.75rem 1.5rem;
  background: #ffffff;
  color: #0066cc;
  border: 1px solid #0066cc;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.secondary-button:hover {
  background: #f8f9fa;
}
</style>

// stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref({
    id: null,
    username: null,
    email: null,
    nickname: null,
    profile_image: null
  })
  const accessToken = ref(null)
  const refreshToken = ref(null)
  const router = useRouter()

  const isAuthenticated = computed(() => {
    return !!accessToken.value && (!!user.value.pk || !!user.value.id)
  })

  // ✅ setUser: store와 localStorage의 user를 모두 갱신
  const setUser = (newUser) => {
    user.value = { ...newUser }
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  // 앱 시작/새로고침 시 localStorage에서 상태 복원
  const initializeAuth = () => {
    const savedUser = localStorage.getItem('user')
    const savedToken = localStorage.getItem('access_token')
    const savedRefreshToken = localStorage.getItem('refresh_token')

    if (savedUser && savedToken) {
      user.value = JSON.parse(savedUser)
      accessToken.value = savedToken
      refreshToken.value = savedRefreshToken
      axios.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`
    } else {
      logout()
    }
  }

  // 회원가입
  const signup = async (formData) => {
    try {
      const response = await axios.post('/api/accounts/registration/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      })
      if (response.data.user) {
        user.value = {
          id: response.data.user.pk || response.data.user.id,
          username: response.data.user.username,
          email: response.data.user.email,
          nickname: response.data.user.nickname,
          profile_image: response.data.user.profile_image
        }
        localStorage.setItem('user', JSON.stringify(user.value))
      }
      if (response.data.access_token) {
        accessToken.value = response.data.access_token
        refreshToken.value = response.data.refresh_token
        localStorage.setItem('access_token', response.data.access_token)
        localStorage.setItem('refresh_token', response.data.refresh_token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
      }
      return response.data
    } catch (error) {
      console.error('회원가입 실패:', error)
      if (error.response && error.response.data) {
        const errorData = error.response.data
        if (typeof errorData === 'string') {
          alert(`회원가입 실패: ${errorData}`)
        } else {
          const errorMessages = []
          for (const field in errorData) {
            if (Array.isArray(errorData[field])) {
              errorMessages.push(`${field}: ${errorData[field].join(', ')}`)
            } else {
              errorMessages.push(`${field}: ${errorData[field]}`)
            }
          }
          alert(`회원가입 실패:\n${errorMessages.join('\n')}`)
        }
      } else {
        alert('회원가입 중 알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
      }
      throw error
    }
  }

  // 로그인
  const login = async (payload) => {
    try {
      console.log('로그인 시도 중...');
      const response = await axios.post('/api/accounts/login/', payload)
      const { access, refresh, user: userData } = response.data
      if (access && userData) {
        console.log('로그인 성공, 인증 데이터 설정 중');
        user.value = {
          id: userData.pk || userData.id,
          username: userData.username,
          email: userData.email,
          nickname: userData.nickname,
          profile_image: userData.profile_image
        }
        accessToken.value = access
        refreshToken.value = refresh || null
        localStorage.setItem('user', JSON.stringify(user.value))
        localStorage.setItem('access_token', access)
        if (refresh) {
          localStorage.setItem('refresh_token', refresh)
        }
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
        console.log('인증 상태 업데이트 완료, isAuthenticated:', isAuthenticated.value);
        return response
      } else {
        throw new Error('Invalid login response')
      }
    } catch (error) {
      console.error('로그인 실패:', error)
      if (error.response && error.response.data) {
        const errorData = error.response.data
        if (typeof errorData === 'string') {
          alert(`로그인 실패: ${errorData}`)
        } else if (errorData.detail) {
          alert(`로그인 실패: ${errorData.detail}`)
        } else {
          alert('로그인 중 알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
        }
      } else {
        alert('서버와의 연결에 문제가 발생했습니다. 인터넷 연결을 확인해주세요.')
      }
      throw error
    }
  }

  // 로그아웃
  const logout = () => {
    user.value = {
      id: null,
      username: null,
      email: null,
      nickname: null,
      profile_image: null
    }
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete axios.defaults.headers.common['Authorization']
    // router.push('/auth/login') // 주석 처리하여 리다이렉트 비활성화
  }

  return {
    user,
    isAuthenticated,
    accessToken,
    refreshToken,
    login,
    logout,
    signup,
    initializeAuth,
    setUser // 반드시 반환!
  }
})

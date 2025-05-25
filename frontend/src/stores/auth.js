import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const user = ref({
        id: null,
        username: null,
        email: null,
    })
    const accessToken = ref(null)
    const refreshToken = ref(null)
    const router = useRouter()

    const isAuthenticated = computed(() => {
        // user.id 대신 user.pk를 체크 (Django REST Framework에서는 pk를 사용)
        return !!accessToken.value && (!!user.value.pk || !!user.value.id)
    })

    const initializeAuth = () => {
        // localStorage에서 사용자 정보와 토큰 복원
        const savedUser = localStorage.getItem('user')
        const savedToken = localStorage.getItem('access_token')
        const savedRefreshToken = localStorage.getItem('refresh_token')

        if (savedUser && savedToken) {
            user.value = JSON.parse(savedUser)
            accessToken.value = savedToken
            refreshToken.value = savedRefreshToken
            axios.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`
        }
    }

    const signup = async (payload) => {
        try {
            const response = await axios.post('/api/accounts/registration/', payload)
            
            // 회원가입 성공 시 사용자 정보와 토큰 저장
            if (response.data.user) {
                user.value = {
                    id: response.data.user.pk,
                    username: response.data.user.username,
                    email: response.data.user.email
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
            throw error
        }
    }
    
    const login = async (payload) => {
        try {
            const response = await axios.post('/api/accounts/login/', payload)
            const { access, refresh, user: userData } = response.data
            
            if (access && userData) {
                user.value = userData
                accessToken.value = access
                refreshToken.value = refresh || null
                
                localStorage.setItem('user', JSON.stringify(userData))
                localStorage.setItem('access_token', access)
                if (refresh) {
                    localStorage.setItem('refresh_token', refresh)
                }
                
                axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
                return response
            } else {
                throw new Error('Invalid login response')
            }
        } catch (error) {
            console.error('Login error:', error)
            throw error
        }
    }
    
    const logout = () => {
        user.value = {
            id: null,
            username: null,
            email: null,
        }
        accessToken.value = null
        refreshToken.value = null
        
        localStorage.removeItem('user')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        
        delete axios.defaults.headers.common['Authorization']
        router.push('/auth/login')
    }
    
    return { user, isAuthenticated, accessToken, refreshToken, login, logout, signup, initializeAuth }
})
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const user = ref({
        id: null,
        username: null,
        email: null,
    })
    const accessToken = ref(null)
    const refreshToken = ref(null)
    const router = useRouter()

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
            }
            
            if (response.data.access_token) {
                accessToken.value = response.data.access_token
                refreshToken.value = response.data.refresh_token
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
            user.value = response.data.user
            accessToken.value = response.data.access_token
            refreshToken.value = response.data.refresh_token
            axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
            return response
        } catch (error) {
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
        delete axios.defaults.headers.common['Authorization']
        router.push('/auth/login')
    }
    
    return { user, accessToken, refreshToken, login, logout, signup }
})
<template>
  <button
    :class="['follow-btn', { following: isFollowing }]"
    @click="toggleFollow"
    :disabled="loading"
  >
    {{ isFollowing ? '언팔로우' : '팔로우' }}
  </button>
</template>

<script>
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

export default {
  props: {
    userId: { type: Number, required: true },
    isFollowing: { type: Boolean, required: true }
  },
  emits: ['update'],
  data() {
    return { loading: false }
  },
  setup() {
    const authStore = useAuthStore()
    const { accessToken } = storeToRefs(authStore)
    return { accessToken }
  },
  methods: {
    async toggleFollow() {
      if (!this.accessToken) {
        alert('로그인이 필요합니다.')
        return
      }
      this.loading = true
      try {
        const response = await axios.post(
          `/api/accounts/${this.userId}/follow/`,
          {},
          { headers: { Authorization: `Bearer ${this.accessToken}` } }
        )
        // 응답: { id, is_following, follower_count, following_count }
        this.$emit('update', response.data)
      } catch (e) {
        alert('팔로우/언팔로우에 실패했습니다.')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.follow-btn {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  border: 1px solid #1976d2;
  background: white;
  color: #1976d2;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.follow-btn.following {
  background: #1976d2;
  color: white;
}
.follow-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

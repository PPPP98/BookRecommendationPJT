<template>
  <div class="follow-list">
    <h2>{{ type === 'followers' ? '팔로워' : '팔로잉' }}</h2>
    
    <div class="users-container">
      <div v-for="user in users" :key="user.id" class="user-item">
        <img
          :src="user.profile_image || '/default-profile.png'"
          :alt="user.username || '프로필'"
          class="user-image"
          @error="onImgError"
        >
        <div class="user-info">
          <h3>{{ user.username }}</h3>
          <p class="user-stats">
            글 {{ Array.isArray(user.threads) ? user.threads.length : 0 }} | 
            팔로워 {{ Array.isArray(user.followers) ? user.followers.length : 0 }}
          </p>
        </div>
        <button 
          v-if="user.id !== currentUserId"
          @click="toggleFollow(user)"
          :class="['follow-button', { 'following': user.is_following }]"
          :disabled="loadingMap[user.id]"
        >
          {{ user.is_following ? '팔로잉' : '팔로우' }}
        </button>
      </div>
    </div>

    <div v-if="users.length === 0" class="empty-state">
      {{ type === 'followers' ? '팔로워가' : '팔로잉하는 사용자가' }} 없습니다.
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

export default {
  name: 'FollowList',
  props: {
    users: {
      type: Array,
      required: true
    },
    type: {
      type: String,
      required: true,
      validator: value => ['followers', 'following'].includes(value)
    },
    currentUserId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      loadingMap: {} // userId: true/false
    }
  },
  setup() {
    const authStore = useAuthStore()
    const { accessToken } = storeToRefs(authStore)
    return { accessToken }
  },
  methods: {
    async toggleFollow(user) {
      if (!this.accessToken) {
        alert('로그인이 필요합니다.')
        return
      }
      this.$set(this.loadingMap, user.id, true)
      try {
        const response = await axios.post(
          `/api/accounts/${user.id}/follow/`,
          {},
          { headers: { Authorization: `Bearer ${this.accessToken}` } }
        )
        // 응답: { id, is_following, follower_count, following_count }
        user.is_following = response.data.is_following
        // 필요시 user.follower_count 등도 갱신
        this.$emit(user.is_following ? 'follow' : 'unfollow', user.id)
      } catch (e) {
        alert('팔로우/언팔로우에 실패했습니다.')
      } finally {
        this.$set(this.loadingMap, user.id, false)
      }
    },
    onImgError(e) {
      if (!e.target.src.endsWith('/default-profile.png')) {
        e.target.src = '/default-profile.png'
      }
    }
  }
}
</script>

<style scoped>
.follow-list {
  margin: 2rem 0;
}

.users-container {
  margin-top: 1rem;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.user-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 1rem;
}

.user-info {
  flex: 1;
}

.user-info h3 {
  margin: 0;
  font-size: 1.1rem;
}

.user-stats {
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
  color: #666;
}

.follow-button {
  padding: 0.5rem 1rem;
  border: 1px solid #0066cc;
  border-radius: 4px;
  background: white;
  color: #0066cc;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.follow-button.following {
  background: #0066cc;
  color: white;
}

.follow-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>

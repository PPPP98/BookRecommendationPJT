<!-- 
  FollowList 컴포넌트
  역할: 팔로워/팔로잉 목록을 표시
  Props:
    - users: Array - 사용자 목록
    - type: String - 'followers' 또는 'following'
    - currentUserId: Number - 현재 로그인한 사용자 ID
  이벤트:
    - @follow: 팔로우 시 발생
    - @unfollow: 언팔로우 시 발생
-->
<template>
  <div class="follow-list">
    <h2>{{ type === 'followers' ? '팔로워' : '팔로잉' }}</h2>
    
    <div class="users-container">
      <div v-for="user in users" :key="user.id" class="user-item">
        <img :src="user.profile_image" :alt="user.username" class="user-image">
        <div class="user-info">
          <h3>{{ user.username }}</h3>
          <p class="user-stats">
            글 {{ user.threads.length }} | 팔로워 {{ user.followers.length }}
          </p>
        </div>
        <button 
          v-if="user.id !== currentUserId"
          @click="handleFollowAction(user)"
          :class="['follow-button', { 'following': isFollowing(user.id) }]"
        >
          {{ isFollowing(user.id) ? '팔로잉' : '팔로우' }}
        </button>
      </div>
    </div>

    <div v-if="users.length === 0" class="empty-state">
      {{ type === 'followers' ? '팔로워가' : '팔로잉하는 사용자가' }} 없습니다.
    </div>
  </div>
</template>

<script>
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
  methods: {
    isFollowing(userId) {
      // TODO: 실제 팔로우 여부 확인 로직 구현
      return true
    },
    handleFollowAction(user) {
      if (this.isFollowing(user.id)) {
        this.$emit('unfollow', user.id)
      } else {
        this.$emit('follow', user.id)
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
}

.follow-button.following {
  background: #0066cc;
  color: white;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>

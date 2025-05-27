<template>
  <div class="modal-bg" @click.self="$emit('close')">
    <div class="modal-list liked-books-modal-list">
      <h4>{{ type === 'followers' ? '팔로워 전체 목록' : '팔로잉 전체 목록' }}</h4>
      <div class="custom-card-grid">
        <router-link
          v-for="u in users"
          :key="u.id"
          :to="{ name: 'UserProfile', params: { id: u.id } }"
          class="user-card-link"
        >
          <div class="user-card">
            <div class="user-card-img-wrap">
              <img
                :src="u.profile_image || fallbackProfile"
                :alt="u.nickname"
                class="user-card-img"
                @error="onProfileImgError"
              />
            </div>
            <div class="user-card-name">{{ u.nickname }}</div>
            <div class="user-card-bio" v-if="u.bio">{{ u.bio }}</div>
          </div>
        </router-link>
      </div>
      <div class="pagination">
        <button v-if="prev" @click="$emit('page', prev)">이전</button>
        <button v-if="next" @click="$emit('page', next)">다음</button>
      </div>
      <div v-if="loading" class="loading-state">목록을 불러오는 중...</div>
      <div v-if="error" class="error-state">{{ error }}</div>
      <button class="modal-close-btn" @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    users: Array,
    type: String, // 'followers' or 'following'
    prev: String,
    next: String,
    loading: Boolean,
    error: String,
    fallbackProfile: String
  },
  emits: ['close', 'page'],
  methods: {
    onProfileImgError(e) {
      if (this.fallbackProfile) e.target.src = this.fallbackProfile
    }
  }
}
</script>

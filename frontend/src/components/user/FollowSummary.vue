<template>
  <div class="profile-summary-row">
    <div class="summary-block">
      <h3>팔로워</h3>
      <div class="summary-count">{{ followerCount }}</div>
      <button class="summary-link" @click="$emit('show-followers')">전체 보기</button>
    </div>
    <div class="summary-block">
      <h3>팔로잉</h3>
      <div class="summary-count">{{ followingCount }}</div>
      <button class="summary-link" @click="$emit('show-following')">전체 보기</button>
    </div>
    <div class="summary-block recent-following-block">
      <h3>최근 팔로잉</h3>
      <div class="custom-card-grid">
        <router-link
          v-for="u in recentFollowing"
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
          </div>
        </router-link>
        <div v-if="!recentFollowing || recentFollowing.length === 0" class="empty-state">
          없음
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    followerCount: Number,
    followingCount: Number,
    recentFollowing: Array,
    fallbackProfile: String
  },
  emits: ['show-followers', 'show-following'],
  methods: {
    onProfileImgError(e) {
      if (this.fallbackProfile) e.target.src = this.fallbackProfile
    }
  }
}
</script>

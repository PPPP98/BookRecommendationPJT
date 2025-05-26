<template>
  <div v-if="user">
    <div class="profile-card">
      <img :src="user.profile_image || fallbackProfile" class="profile-card-img" @error="onProfileImgError" />
      <div class="profile-card-main">
        <div class="profile-card-nickname">{{ user.nickname }}</div>
        <div class="profile-card-bio" v-if="user.bio">{{ user.bio }}</div>
        <div class="profile-card-meta">
          <span v-if="user.articles_count !== undefined">
            작성글 <b>{{ user.articles_count }}</b>
          </span>
          <span>
            팔로워 <b>{{ user.follower_count }}</b>
          </span>
          <span>
            팔로잉 <b>{{ user.following_count }}</b>
          </span>
        </div>
        <div class="profile-card-categories" v-if="user.interested_categories && user.interested_categories.length">
          <span class="category-tag" v-for="cat in user.interested_categories" :key="cat.id">
            {{ cat.name }}
          </span>
        </div>
      </div>
      <button v-if="$attrs.isMine" class="edit-btn" @click="$emit('edit')">수정</button>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    user: Object,
    fallbackProfile: String
  },
  methods: {
    onProfileImgError(e) {
      e.target.src = this.fallbackProfile
    }
  }
}
</script>

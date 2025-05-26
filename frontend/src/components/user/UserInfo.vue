<template>
  <div class="user-info">
    <div class="profile-section">
      <div class="profile-image-container">
        <img
          :src="profileImageUrl"
          :alt="user.nickname || '프로필'"
          class="profile-image"
          @error="onImgError"
        >
        <button v-if="editable" @click="handleImageUpload" class="upload-button">
          이미지 변경
        </button>
      </div>
      <div class="info-section">
        <template v-if="isEditing">
          <div class="form-group">
            <label>닉네임</label>
            <input v-model="editedUser.nickname" type="text" class="form-input">
          </div>
          <div class="form-group">
            <label>이메일</label>
            <input v-model="editedUser.email" type="email" class="form-input" disabled>
          </div>
          <div class="form-group">
            <label>관심 카테고리</label>
            <div class="interests-container">
              <label v-for="category in categories" :key="category" class="interest-label">
                <input 
                  type="checkbox" 
                  :value="category"
                  v-model="editedUser.interests"
                >
                {{ category }}
              </label>
            </div>
          </div>
          <div class="action-buttons">
            <button @click="saveChanges" class="save-button">저장</button>
            <button @click="cancelEdit" class="cancel-button">취소</button>
          </div>
        </template>
        <template v-else>
          <h2>{{ user.nickname }}</h2>
          <p class="email">{{ user.email }}</p>
          <div class="interests">
            <span>관심 카테고리:</span>
            <span
              class="interest-tag"
              v-for="interest in user.interests || []"
              :key="interest"
            >
              {{ interest }}
            </span>
          </div>
          <div class="stats">
            <div class="stat">
              팔로워 {{ user.follower_count ?? (user.followers && user.followers.length) ?? 0 }}명
            </div>
            <div class="stat">
              팔로잉 {{ user.following_count ?? (user.following && user.following.length) ?? 0 }}명
            </div>
            <div class="stat">
              작성글 {{ user.articles_count ?? (user.threads && user.threads.length) ?? 0 }}개
            </div>
          </div>
          <button v-if="editable" @click="startEdit" class="edit-button">
            정보 수정
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
const CDN_PROFILE = 'https://cdn-icons-png.flaticon.com/512/149/149071.png'
const BACKEND_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default {
  name: 'UserInfo',
  props: {
    user: {
      type: Object,
      required: true
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isEditing: false,
      editedUser: null,
      categories: ['소설', '에세이', '경제/경영', '자기계발', '인문', '과학'],
      defaultProfile: CDN_PROFILE
    }
  },
  computed: {
    profileImageUrl() {
      if (!this.user?.profile_image) return this.defaultProfile
      if (this.user.profile_image.startsWith('http')) return this.user.profile_image
      return `${BACKEND_URL}${this.user.profile_image}`
    }
  },
  methods: {
    startEdit() {
      this.editedUser = {
        ...this.user,
        interests: Array.isArray(this.user.interests) ? [...this.user.interests] : []
      }
      this.isEditing = true
    },
    cancelEdit() {
      this.editedUser = null
      this.isEditing = false
    },
    saveChanges() {
      this.$emit('update', this.editedUser)
      this.isEditing = false
    },
    handleImageUpload() {
      // TODO: 이미지 업로드 구현
    },
    onImgError(e) {
      if (e.target.src !== this.defaultProfile) {
        e.target.src = this.defaultProfile
      }
    }
  }
}
</script>

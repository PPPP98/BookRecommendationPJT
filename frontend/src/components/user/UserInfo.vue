<template>
  <div class="user-info">
    <div class="profile-section">
      <div class="profile-image-container">
        <img
          :src="user.profile_image || '/default-profile.png'"
          :alt="user.username || '프로필'"
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
            <input v-model="editedUser.username" type="text" class="form-input">
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
          <h2>{{ user.username }}</h2>
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
              팔로워 {{ (user.followers && user.followers.length) || 0 }}명
            </div>
            <div class="stat">
              팔로잉 {{ (user.following && user.following.length) || 0 }}명
            </div>
            <div class="stat">
              작성글 {{ (user.threads && user.threads.length) || 0 }}개
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
      categories: ['소설', '에세이', '경제/경영', '자기계발', '인문', '과학']
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
      if (!e.target.src.endsWith('/default-profile.png')) {
        e.target.src = '/default-profile.png'
      }
    }
  }
}
</script>

<style scoped>
.user-info { padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.profile-section { display: flex; gap: 2rem;}
.profile-image-container { text-align: center;}
.profile-image { width: 150px; height: 150px; border-radius: 50%; margin-bottom: 1rem;}
.info-section { flex: 1;}
.form-group { margin-bottom: 1rem;}
.form-group label { display: block; margin-bottom: 0.5rem;}
.form-input { width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px;}
.interests-container { display: flex; flex-wrap: wrap; gap: 1rem;}
.interest-label { display: flex; align-items: center; gap: 0.5rem;}
.interest-tag { background: #e9ecef; padding: 0.25rem 0.5rem; border-radius: 4px; margin-right: 0.5rem;}
.stats { display: flex; gap: 2rem; margin: 1rem 0;}
.edit-button { background: #0066cc; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer;}
.save-button { background: #28a745; color: white; margin-right: 1rem;}
.cancel-button { background: #dc3545; color: white;}
</style>

<template>
  <form class="profile-edit-form" @submit.prevent="submitEdit">
    <div class="form-row">
      <label>프로필 이미지</label>
      <input type="file" accept="image/*" @change="onFileChange" />
      <img
        :src="previewImage || user.profile_image || fallbackProfile"
        class="profile-edit-img"
        @error="onProfileImgError"
      />
    </div>
    <NicknameField v-model="editForm.nickname" />
    <div class="form-row">
      <label for="bio">자기소개</label>
      <textarea id="bio" v-model="editForm.bio" maxlength="100" />
    </div>
    <div class="form-row">
      <label>관심 카테고리</label>
      <div class="category-checkboxes">
        <label v-for="cat in allCategories" :key="cat.id" class="category-checkbox">
          <input
            type="checkbox"
            :value="cat.id"
            v-model="editForm.interested_categories"
          />
          {{ cat.name }}
        </label>
      </div>
    </div>
    <div class="edit-actions">
      <button type="submit" class="save-btn" :disabled="editLoading">저장</button>
      <button type="button" class="cancel-btn" @click="$emit('cancel')" :disabled="editLoading">취소</button>
    </div>
    <div v-if="editError" class="error-state">{{ editError }}</div>
  </form>
</template>
<script>
import NicknameField from './NicknameField.vue'
import axios from 'axios'
export default {
  props: ['user', 'allCategories', 'fallbackProfile', 'editLoading', 'editError'],
  components: { NicknameField },
  data() {
    return {
      editForm: {
        nickname: this.user.nickname || '',
        bio: this.user.bio || '',
        profile_image: null,
        interested_categories: (this.user.interested_categories || []).map(cat => cat.id)
      },
      previewImage: '',
      editError: null
    }
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0]
      if (file) {
        this.editForm.profile_image = file
        this.previewImage = URL.createObjectURL(file)
      }
    },
    onProfileImgError(e) {
      e.target.src = this.fallbackProfile
    },
    async submitEdit() {
      this.$emit('start-loading')
      this.editError = null
      try {
        const formData = new FormData()
        formData.append('nickname', this.editForm.nickname)
        formData.append('bio', this.editForm.bio)
        if (this.editForm.profile_image instanceof File) {
          formData.append('profile_image', this.editForm.profile_image)
        }
        if (this.editForm.interested_categories && this.editForm.interested_categories.length > 0) {
          this.editForm.interested_categories.forEach(id => {
            formData.append('interested_categories', id)
          })
        }
        const token = localStorage.getItem('access_token')
        const { data } = await axios.put('/api/accounts/profile/', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        this.$emit('update', data)
      } catch (err) {
        this.editError = err.response?.data?.detail || '회원 정보 수정에 실패했습니다.'
      } finally {
        this.$emit('end-loading')
      }
    }
  }
}
</script>

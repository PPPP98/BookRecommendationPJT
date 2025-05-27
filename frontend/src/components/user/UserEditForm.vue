<template>
  <form class="profile-edit-form" @submit.prevent="onSubmit">
    <div class="form-row">
      <label>프로필 이미지</label>
      <input type="file" accept="image/*" @change="onFileChange" />
      <img
        :src="previewImage || user.profile_image || fallbackProfile"
        class="profile-edit-img"
        @error="onProfileImgError"
      />
    </div>
    <div class="form-row">
      <label for="nickname">닉네임</label>
      <input id="nickname" v-model="form.nickname" required maxlength="30" />
    </div>
    <div class="form-row">
      <label for="bio">자기소개</label>
      <textarea id="bio" v-model="form.bio" maxlength="100" />
    </div>
    <div class="form-row">
      <label>관심 카테고리</label>
      <div class="category-checkboxes">
        <label
          v-for="cat in allCategories"
          :key="cat.id"
          class="category-checkbox"
        >
          <input
            type="checkbox"
            :value="cat.id"
            v-model="form.interested_categories"
          />
          {{ cat.name }}
        </label>
      </div>
    </div>
    <div class="edit-actions">
      <button type="submit" class="save-btn" :disabled="loading">저장</button>
      <button type="button" class="cancel-btn" @click="$emit('cancel')" :disabled="loading">취소</button>
    </div>
    <div v-if="error" class="error-state">{{ error }}</div>
  </form>
</template>

<script>
import axios from "axios";

export default {
  name: "UserEditForm",
  props: {
    user: { type: Object, required: true },
    allCategories: { type: Array, required: true },
    fallbackProfile: { type: String, default: "" }
  },
  emits: ["update", "cancel"],
  data() {
    return {
      form: {
        nickname: this.user.nickname || "",
        bio: this.user.bio || "",
        profile_image: null,
        interested_categories: (this.user.interested_categories || []).map(cat => cat.id),
      },
      previewImage: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      if (file) {
        this.form.profile_image = file;
        this.previewImage = URL.createObjectURL(file);
      }
    },
    onProfileImgError(e) {
      if (this.fallbackProfile) e.target.src = this.fallbackProfile;
    },
    async onSubmit() {
      this.loading = true;
      this.error = null;
      try {
        const formData = new FormData();
        formData.append("nickname", this.form.nickname);
        formData.append("bio", this.form.bio);
        this.form.interested_categories.forEach(id => {
          formData.append("interested_categories", id);
        });
        if (this.form.profile_image instanceof File) {
          formData.append("profile_image", this.form.profile_image);
        }
        const token = localStorage.getItem("access_token");
        const { data } = await axios.put("/api/accounts/profile/", formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        });
        this.$emit("update", data);
        this.previewImage = "";
      } catch (err) {
        this.error = err.response?.data?.detail || "회원 정보 수정에 실패했습니다.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* paste.txt의 .profile-edit-form 스타일을 그대로 복사해 사용하세요 */
</style>

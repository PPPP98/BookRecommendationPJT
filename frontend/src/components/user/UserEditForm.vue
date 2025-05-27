<template>
  <form class="profile-edit-form" @submit.prevent="onSubmit">
    <div class="loading-state" v-if="loading">
      <span>저장 중...</span>
    </div>

    <div class="form-row">
      <label>프로필 이미지</label>
      <div class="image-upload">
        <div class="image-preview" @click="triggerFileInput">
          <img
            :src="previewImage || user.profile_image || fallbackProfile"
            @error="onProfileImgError"
            alt="프로필 이미지"
          />
        </div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="onFileChange"
          class="hidden"
          style="display: none;"
        />
      </div>
    </div>

    <div class="form-row">
      <label for="nickname">닉네임</label>
      <div class="input-with-validation">
        <input 
          type="text" 
          id="nickname" 
          v-model="form.nickname" 
          required 
          maxlength="30"
          @input="checkNickname"
        />
        <span 
          v-if="form.nickname && form.nickname !== user.nickname"
          class="validation-feedback"
          :class="{ 'valid': !nicknameExists, 'invalid': nicknameExists }"
        >
          {{ nicknameExists ? '이미 사용 중인 닉네임입니다' : '사용 가능한 닉네임입니다' }}
        </span>
      </div>
    </div>

    <div class="form-row">
      <label for="bio">자기소개</label>
      <textarea 
        id="bio" 
        v-model="form.bio" 
        maxlength="100"
        placeholder="자신을 소개해주세요 (최대 100자)"
      ></textarea>
    </div>

    <div class="form-row">
      <label>관심 카테고리</label>
      <div class="category-section">
        <div class="category-checkboxes">
          <label
            v-for="category in categories"
            :key="category.id"
            class="category-checkbox"
          >
            <input
              type="checkbox"
              :value="category.id"
              v-model="form.interested_categories"
            />
            {{ category.name }}
          </label>
        </div>
      </div>
    </div>

    <div class="edit-actions">
      <button 
        type="submit" 
        class="save-btn" 
        :disabled="loading || nicknameExists || (form.nickname !== user.nickname && !nicknameValid)"
      >
        {{ loading ? '저장 중...' : '저장' }}
      </button>
      <button 
        type="button" 
        class="cancel-btn" 
        @click="confirmCancel" 
        :disabled="loading"
      >
        취소
      </button>
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
    fallbackProfile: { type: String, default: "" }
  },
  emits: ["update", "cancel"],
  data() {
    return {
      categories: [
        { id: 1, name: '소설/시/희곡' },
        { id: 2, name: '경제/경영' },
        { id: 3, name: '자기계발' },
        { id: 4, name: '인문/교양' },
        { id: 5, name: '취미/실용' },
        { id: 6, name: '어린이/청소년' },
        { id: 7, name: '과학' }
      ],
      form: {
        nickname: this.user.nickname || "",
        bio: this.user.bio || "",
        profile_image: null,
        interested_categories: (this.user.interested_categories || []).map(cat => cat.id),
      },
      previewImage: "",
      loading: false,
      error: null,
      nicknameExists: false,
      nicknameValid: false,
      nicknameCheckTimeout: null,
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileChange(e) {
      const file = e.target.files[0];
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          this.error = "이미지 크기는 5MB를 초과할 수 없습니다.";
          return;
        }
        this.form.profile_image = file;
        this.previewImage = URL.createObjectURL(file);
      }
    },
    onProfileImgError(e) {
      if (this.fallbackProfile) e.target.src = this.fallbackProfile;
    },
    checkNickname() {
      if (this.form.nickname === this.user.nickname) {
        this.nicknameExists = false;
        this.nicknameValid = true;
        return;
      }

      // 디바운스 처리
      if (this.nicknameCheckTimeout) {
        clearTimeout(this.nicknameCheckTimeout);
      }

      this.nicknameCheckTimeout = setTimeout(async () => {
        if (!this.form.nickname || this.form.nickname.length < 2) {
          this.nicknameExists = false;
          this.nicknameValid = false;
          return;
        }

        try {
          const { data } = await axios.get(`/api/accounts/check-nickname/`, {
            params: { nickname: this.form.nickname }
          });
          this.nicknameExists = data.exists;
          this.nicknameValid = !data.exists;
        } catch (error) {
          console.error("닉네임 중복 확인 실패:", error);
          this.nicknameExists = false;
          this.nicknameValid = false;
        }
      }, 500);
    },
    confirmCancel() {
      if (
        this.form.nickname !== this.user.nickname ||
        this.form.bio !== this.user.bio ||
        this.form.profile_image ||
        JSON.stringify(this.form.interested_categories.sort()) !== 
        JSON.stringify((this.user.interested_categories || []).map(cat => cat.id).sort())
      ) {
        if (confirm('변경사항이 있습니다. 정말로 취소하시겠습니까?')) {
          this.$emit('cancel');
        }
      } else {
        this.$emit('cancel');
      }
    },
    async onSubmit() {
      if (this.nicknameExists) {
        this.error = "이미 사용 중인 닉네임입니다.";
        return;
      }
      
      this.loading = true;
      this.error = null;
      try {
        const formData = new FormData();
        formData.append("nickname", this.form.nickname);
        formData.append("bio", this.form.bio);
        
        // 선택된 카테고리 ID를 FormData에 추가
        this.form.interested_categories.forEach(categoryId => {
          formData.append("interested_categories", categoryId);
        });
        
        // 프로필 이미지가 변경된 경우에만 추가
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
.profile-edit-form {
  background: #fff;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  /* max-width: 1600px; */
  /* margin: 0 auto 2rem auto; */
  position: relative;
}

.form-row {
  margin-bottom: 2.5rem;
}

.form-row label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 1rem;
}

.form-row input[type="text"],
.form-row textarea {
  width: 100%;
  padding: 1em 1.2em;
  border: 1.5px solid #ececec;
  border-radius: 12px;
  font-size: 1rem;
  background: #fafbfc;
  transition: all 0.2s;
  line-height: 1.5;
}

.form-row input[type="text"]:focus,
.form-row textarea:focus {
  border-color: #7c3aed;
  outline: none;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.form-row textarea {
  min-height: 100px;
  resize: vertical;
}

.image-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.image-preview {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background: #f5f5f5;
  cursor: pointer;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-preview:hover::after {
  content: "이미지 변경";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  font-size: 0.8rem;
  padding: 0.5em;
  text-align: center;
}

.input-with-validation {
  position: relative;
}

.validation-feedback {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.85rem;
}

.validation-feedback.valid {
  color: #10b981;
}

.validation-feedback.invalid {
  color: #ef4444;
}

.category-section {
  background: #fafbfc;
  border-radius: 12px;
  padding: 1rem;
}

.category-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.8rem;
}

.category-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #444;
  cursor: pointer;
  padding: 0.3em;
  border-radius: 8px;
  transition: background 0.2s;
}

.category-checkbox:hover {
  background: #f0f0f0;
}

.category-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1.5px solid #ececec;
  cursor: pointer;
}

.edit-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.save-btn,
.cancel-btn {
  padding: 0.6em 2em;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn {
  background: #7c3aed;
  color: white;
  border: none;
}

.save-btn:hover {
  background: #6b21e8;
}

.save-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.cancel-btn {
  background: #fff;
  color: #666;
  border: 1.5px solid #ececec;
}

.cancel-btn:hover {
  background: #f5f5f5;
  color: #7c3aed;
}

.error-state {
  color: #ef4444;
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.loading-state {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}
</style>

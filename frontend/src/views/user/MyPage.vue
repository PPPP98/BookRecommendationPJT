<template>
  <div class="my-page">
    <main class="main-content" v-if="user">
      <!-- 프로필 카드 -->
      <section class="profile-card">
        <img :src="user.profile_image || fallbackProfile" alt="프로필" class="profile-img" @error="onImgError" />
        <div class="profile-main">
          <div class="nickname">{{ user.nickname }}</div>
          <div class="bio" v-if="user.bio">{{ user.bio }}</div>
          <div class="meta">
            <span>팔로워 <b>{{ user.follower_count }}</b></span>
            <span>팔로잉 <b>{{ user.following_count }}</b></span>
          </div>
          <div class="categories" v-if="user.interested_categories && user.interested_categories.length">
            <span v-for="cat in user.interested_categories" :key="cat.id" class="category-tag">{{ cat.name }}</span>
          </div>
          <div class="profile-actions">
            <button v-if="isMine" class="edit-btn" @click="editMode = true">정보수정</button>
            <button v-else class="follow-btn" @click="toggleFollow" :disabled="followLoading">
              {{ user.is_following ? '언팔로우' : '팔로우' }}
            </button>
          </div>
        </div>
      </section>

      <!-- 정보 수정 폼 (생략, 기존과 동일) -->
      <section v-if="isMine && editMode" class="profile-edit-section">
        <!-- ...생략... -->
      </section>

      <!-- 팔로워/팔로잉/찜한 도서/최근 팔로잉 -->
      <section class="profile-lists">
        <div>
          <h3>팔로워</h3>
          <ul>
            <li v-for="f in followers" :key="f.id">
              <router-link :to="{ name: 'UserProfile', params: { id: f.id } }" class="user-link">
                <img :src="f.profile_image || fallbackProfile" class="avatar-img" />
                <span class="user-nickname">{{ f.nickname }}</span>
              </router-link>
            </li>
          </ul>
        </div>
        <div>
          <h3>팔로잉</h3>
          <ul>
            <li v-for="f in following" :key="f.id">
              <router-link :to="{ name: 'UserProfile', params: { id: f.id } }" class="user-link">
                <img :src="f.profile_image || fallbackProfile" class="avatar-img" />
                <span class="user-nickname">{{ f.nickname }}</span>
              </router-link>
            </li>
          </ul>
        </div>
        <div>
          <h3>찜한 도서</h3>
          <div class="liked-books-grid">
            <BookCard
              v-for="book in likedBooks"
              :key="book.id"
              :book="book"
              @click="$router.push({ name: 'BookDetail', params: { id: book.id } })"
            />
          </div>
        </div>
        <div>
          <h3>최근 팔로잉</h3>
          <ul>
            <li v-for="f in recentFollowing" :key="f.id">
              <router-link :to="{ name: 'UserProfile', params: { id: f.id } }" class="user-link">
                <img :src="f.profile_image || fallbackProfile" class="avatar-img" />
                <span class="user-nickname">{{ f.nickname }}</span>
                <span v-if="f.latest_activity" class="recent-following-activity">{{ f.latest_activity }}</span>
              </router-link>
            </li>
          </ul>
        </div>
      </section>
    </main>
    <div v-else-if="loading" class="loading">프로필 정보를 불러오는 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import BookCard from '@/components/books/BookCard.vue'

export default {
  name: 'MyPage',
  components: { BookCard },
  props: {
    id: { type: [Number, String], default: null }
  },
  setup(props) {
    const authStore = useAuthStore()
    const currentUser = computed(() => authStore.user)
    const user = ref(null)
    const isMine = ref(false)
    const editMode = ref(false)
    const editForm = ref({
      nickname: '',
      bio: '',
      profile_image: null,
      interested_categories: []
    })
    const previewImg = ref('')
    const editLoading = ref(false)
    const editError = ref(null)
    const allCategories = ref([])
    const followers = ref([])
    const following = ref([])
    const likedBooks = ref([])
    const recentFollowing = ref([])
    const followLoading = ref(false)
    const loading = ref(false)
    const error = ref(null)
    const fallbackProfile = '/default-profile.png.jpg'

    async function fetchUser() {
      loading.value = true
      try {
        let url, mine = false
        if (!props.id || (currentUser.value && +props.id === currentUser.value.id)) {
          url = '/api/accounts/profile/'
          mine = true
        } else {
          url = `/api/accounts/${props.id}/profile/`
        }
        const { data } = await axios.get(url)
        user.value = data
        isMine.value = mine
        if (mine) {
          editForm.value.nickname = data.nickname
          editForm.value.bio = data.bio
          editForm.value.interested_categories = (data.interested_categories || []).map(c => c.id)
        }
      } catch (e) {
        error.value = '프로필 정보를 불러오는데 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    async function fetchFollowers() {
      if (!user.value?.id) return
      const { data } = await axios.get(`/api/accounts/${user.value.id}/followers/`, { params: { page_size: 10 } })
      followers.value = data.results || []
    }
    async function fetchFollowing() {
      if (!user.value?.id) return
      const { data } = await axios.get(`/api/accounts/${user.value.id}/following/`, { params: { page_size: 10 } })
      following.value = data.results || []
    }
    async function fetchLikedBooks() {
      if (!user.value?.id) return
      const { data } = await axios.get(`/api/accounts/${user.value.id}/liked-books/`, { params: { page_size: 10 } })
      // BookCard에 필요한 필드만 매핑
      likedBooks.value = (data.results || []).map(b => ({
        ...b,
        cover_image: b.cover, // BookCard가 cover_image를 쓴다면
      }))
    }
    async function fetchRecentFollowing() {
      if (!user.value?.id) return
      const { data } = await axios.get(`/api/accounts/${user.value.id}/following/`, {
        params: { ordering: '-created', page_size: 5 }
      })
      recentFollowing.value = data.results ? data.results.slice(0, 5) : []
    }

    async function toggleFollow() {
      if (!user.value?.id) return
      followLoading.value = true
      try {
        const token = localStorage.getItem('access_token')
        const { data } = await axios.post(
          `/api/accounts/${user.value.id}/follow/`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        )
        user.value.is_following = data.is_following
        user.value.follower_count = data.follower_count
        user.value.following_count = data.following_count
      } catch (e) {
        alert('팔로우/언팔로우에 실패했습니다.')
      } finally {
        followLoading.value = false
      }
    }

    function onImgError(e) {
      e.target.src = fallbackProfile
    }

    async function reloadAll() {
      await fetchUser()
      await Promise.all([
        fetchFollowers(),
        fetchFollowing(),
        fetchLikedBooks()
      ])
      await fetchRecentFollowing()
    }

    onMounted(reloadAll)
    watch(() => props.id, reloadAll)

    return {
      user, isMine, editMode, editForm, previewImg, editLoading, editError,
      allCategories, followers, following, likedBooks, recentFollowing, followLoading, loading, error,
      fallbackProfile,
      toggleFollow, onImgError
    }
  }
}
</script>

<style scoped>
.avatar-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 0.5em;
  vertical-align: middle;
  border: 1.5px solid #e3e3e3;
}
.user-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #222;
  gap: 0.5em;
  font-weight: 500;
}
.user-link:hover .user-nickname {
  color: #1976d2;
  text-decoration: underline;
}
.user-nickname {
  font-size: 1rem;
}
.liked-books-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.1rem;
  margin-top: 0.7rem;
}
.recent-following-activity {
  color: #888;
  font-size: 0.93rem;
  margin-left: 0.5em;
}
/* 이하 기존 스타일 유지 */

.avatar-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 0.5em;
  vertical-align: middle;
  border: 1.5px solid #e3e3e3;
}
.user-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #222;
  gap: 0.5em;
  font-weight: 500;
}
.user-link:hover .user-nickname {
  color: #1976d2;
  text-decoration: underline;
}
.user-nickname {
  font-size: 1rem;
}
.liked-books-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.1rem;
  margin-top: 0.7rem;
}
.recent-following-activity {
  color: #888;
  font-size: 0.93rem;
  margin-left: 0.5em;
}
/* 이하 기존 스타일 유지 */
.my-page {
  min-height: 100vh;
  background: #fafbfc;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
  color: #222;
}
.main-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 2.5rem 1.2rem 2rem 1.2rem;
}
.profile-card {
  display: flex;
  align-items: flex-start;
  gap: 1.7rem;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 2rem 1.5rem;
  margin-bottom: 2.2rem;
}
.profile-img {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  background: #f5f5f5;
}
.profile-main {
  flex: 1;
}
.nickname {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
}
.bio {
  font-size: 1rem;
  color: #666;
  margin-bottom: 0.7rem;
}
.meta {
  font-size: 0.95rem;
  color: #888;
  margin-bottom: 0.6rem;
  display: flex;
  gap: 1.2rem;
}
.categories {
  margin-bottom: 0.7rem;
}
.category-tag {
  background: #f5f5f5;
  color: #1976d2;
  border-radius: 7px;
  padding: 0.2em 0.8em;
  margin-right: 0.4em;
  font-size: 0.93rem;
}
.profile-actions {
  margin-top: 0.7rem;
}
.edit-btn, .follow-btn {
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 7px;
  padding: 0.4em 1.2em;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.13s;
}
.edit-btn:hover, .follow-btn:hover {
  background: #1254a1;
}
.profile-edit-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 2rem 1.5rem;
  margin-bottom: 2.2rem;
}
.profile-edit-section form > div {
  margin-bottom: 1rem;
}
.profile-edit-section label {
  font-weight: 600;
  margin-bottom: 0.3em;
  display: block;
}
.profile-edit-section input[type="text"],
.profile-edit-section textarea {
  width: 100%;
  padding: 0.7em;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  margin-top: 0.2em;
}
.profile-edit-section .category-checkbox {
  margin-right: 1.1em;
}
.edit-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.edit-actions button {
  padding: 0.5em 1.3em;
  border-radius: 7px;
  border: none;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
}
.edit-actions button[type="submit"] {
  background: #1976d2;
  color: #fff;
}
.edit-actions button[type="button"] {
  background: #f5f5f5;
  color: #666;
}
.error {
  color: #dc3545;
  margin-top: 1rem;
  font-size: 0.98rem;
}
.loading {
  text-align: center;
  font-size: 1.1rem;
  margin-top: 3rem;
}
.profile-lists {
  display: flex;
  gap: 2.5rem;
  margin-top: 2.2rem;
  flex-wrap: wrap;
}
.profile-lists > div {
  flex: 1 1 180px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 1.2rem 1rem;
  min-width: 180px;
}
.profile-lists h3 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1976d2;
  margin-bottom: 0.7rem;
}
.profile-lists ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.profile-lists li {
  font-size: 0.97rem;
  color: #333;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}
.nickname-row {
  margin-bottom: 1rem;
}
.nickname-input-group {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-top: 0.2em;
}
.check-btn {
  background: #f5f6fa;
  color: #1976d2;
  border: 1.5px solid #ececec;
  border-radius: 7px;
  padding: 0.3em 1em;
  font-weight: 600;
  font-size: 0.97rem;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
}
.check-btn:disabled {
  background: #eee;
  color: #aaa;
  cursor: not-allowed;
}
.nickname-status {
  min-width: 70px;
  font-size: 0.95rem;
  margin-left: 0.2em;
}
.nickname-status.valid {
  color: #1976d2;
  font-weight: 700;
}
.nickname-status.invalid {
  color: #dc3545;
  font-weight: 700;
}
input.invalid {
  border-color: #dc3545;
}
.recent-following-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 0.5em;
  vertical-align: middle;
}
.recent-following-nickname {
  font-weight: 600;
  margin-right: 0.6em;
}
.recent-following-activity {
  color: #888;
  font-size: 0.93rem;
}
@media (max-width: 900px) {
  .main-content { padding: 1.2rem 0.3rem 2rem 0.3rem; }
  .profile-card { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .profile-lists { flex-direction: column; gap: 1.2rem; }
}
</style>

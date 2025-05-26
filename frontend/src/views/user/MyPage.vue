<template>
  <div class="my-page">
    <Navbar />
    <main class="main-content">

      <!-- 회원 정보 카드 -->
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
        </div>
      </div>

      <!-- 회원정보 수정 폼 (내 프로필일 때만) -->
       <div v-if="user && isMine">
        <div class="profile-edit-header">
          <h2>회원 정보 수정</h2>
          <button v-if="!editMode" class="edit-btn" @click="startEdit">수정</button>
        </div>
        <UserEditForm
          v-if="editMode"
          :user="user"
          :all-categories="allCategories"
          :fallback-profile="fallbackProfile"
          :edit-loading="editLoading"
          :edit-error="editError"
          @update="onUserUpdated"
          @cancel="cancelEdit"
          @start-loading="editLoading = true"
          @end-loading="editLoading = false"
        />
      </div>

      <div v-else-if="loadingUser" class="loading-state">프로필 정보를 불러오는 중...</div>
      <div v-else-if="errorUser" class="error-state">{{ errorUser }}</div>

      <!-- 팔로워, 팔로잉, 최근 팔로잉 -->
      <div v-if="user" class="profile-summary-row">
        <div class="summary-block">
          <h3>팔로워</h3>
          <div class="summary-count">{{ user.follower_count }}</div>
          <button class="summary-link" @click.stop="showFollowerList = !showFollowerList">전체 보기</button>
        </div>
        <div class="summary-block">
          <h3>팔로잉</h3>
          <div class="summary-count">{{ user.following_count }}</div>
          <button class="summary-link" @click.stop="showFollowingList = !showFollowingList">전체 보기</button>
        </div>
        <div class="summary-block recent-following-block">
          <h3>최근 팔로잉</h3>
          <div class="custom-card-grid">
            <router-link
              v-for="u in user.recent_following || []"
              :key="u.id"
              :to="{ name: 'UserProfile', params: { id: u.id } }"
              class="user-card-link"
            >
              <div class="user-card">
                <div class="user-card-img-wrap">
                  <img :src="u.profile_image || fallbackProfile" :alt="u.nickname" class="user-card-img" @error="onProfileImgError" />
                </div>
                <div class="user-card-name">{{ u.nickname }}</div>
              </div>
            </router-link>
            <div v-if="!user.recent_following || user.recent_following.length === 0" class="empty-state">
              없음
            </div>
          </div>
        </div>
      </div>

      <!-- 팔로워 전체 목록 모달 -->
      <div v-if="showFollowerList" class="modal-bg" @click.self="showFollowerList = false">
        <div class="modal-list liked-books-modal-list">
          <h4>팔로워 전체 목록</h4>
          <div class="custom-card-grid">
            <router-link
              v-for="u in followers"
              :key="u.id"
              :to="{ name: 'UserProfile', params: { id: u.id } }"
              class="user-card-link"
            >
              <div class="user-card">
                <div class="user-card-img-wrap">
                  <img :src="u.profile_image || fallbackProfile" :alt="u.nickname" class="user-card-img" @error="onProfileImgError" />
                </div>
                <div class="user-card-name">{{ u.nickname }}</div>
                <div class="user-card-bio" v-if="u.bio">{{ u.bio }}</div>
              </div>
            </router-link>
          </div>
          <div class="pagination">
            <button v-if="followersPrev" @click="fetchFollowers(followersPrev)">이전</button>
            <button v-if="followersNext" @click="fetchFollowers(followersNext)">다음</button>
          </div>
          <div v-if="loadingFollowers" class="loading-state">팔로워 목록을 불러오는 중...</div>
          <div v-if="errorFollowers" class="error-state">{{ errorFollowers }}</div>
        </div>
      </div>
      <!-- 팔로잉 전체 목록 모달 -->
      <div v-if="showFollowingList" class="modal-bg" @click.self="showFollowingList = false">
        <div class="modal-list liked-books-modal-list">
          <h4>팔로잉 전체 목록</h4>
          <div class="custom-card-grid">
            <router-link
              v-for="u in following"
              :key="u.id"
              :to="{ name: 'UserProfile', params: { id: u.id } }"
              class="user-card-link"
            >
              <div class="user-card">
                <div class="user-card-img-wrap">
                  <img :src="u.profile_image || fallbackProfile" :alt="u.nickname" class="user-card-img" @error="onProfileImgError" />
                </div>
                <div class="user-card-name">{{ u.nickname }}</div>
                <div class="user-card-bio" v-if="u.bio">{{ u.bio }}</div>
              </div>
            </router-link>
          </div>
          <div class="pagination">
            <button v-if="followingPrev" @click="fetchFollowing(followingPrev)">이전</button>
            <button v-if="followingNext" @click="fetchFollowing(followingNext)">다음</button>
          </div>
          <div v-if="loadingFollowing" class="loading-state">팔로잉 목록을 불러오는 중...</div>
          <div v-if="errorFollowing" class="error-state">{{ errorFollowing }}</div>
        </div>
      </div>

      <!-- 최근 찜한 도서 등 이하 동일 -->
      <div v-if="user" class="recent-liked-books-section">
        <div class="recent-liked-books-header">
          <h3>최근 찜한 도서</h3>
          <button class="summary-link" @click="openLikedBooksModal">더보기</button>
        </div>
        <div class="books-container small horizontal-scroll">
          <div
            v-for="book in (likedBooks || []).slice(0, 5)"
            :key="book.id"
            class="custom-card"
            @click="navigateToBook(book.id)"
          >
            <BookCard :book="book" />
            <div class="multi-ellipsis card-title">{{ book.title }}</div>
          </div>
        </div>
        <div v-if="!likedBooks?.length" class="empty-state">
          찜한 도서가 없습니다.
        </div>
      </div>
      <div v-if="showLikedBooksList" class="modal-bg" @click.self="closeLikedBooksModal">
        <div class="modal-list liked-books-modal-list">
          <h4>찜한 도서 전체 목록</h4>
          <div class="custom-card-grid">
            <div
              v-for="book in likedBooks"
              :key="book.id"
              class="custom-card"
              @click="navigateToBook(book.id)"
            >
              <BookCard :book="book" />
              <div class="multi-ellipsis card-title">{{ book.title }}</div>
            </div>
          </div>
          <div class="pagination">
            <button v-if="likedBooksPrev" @click="fetchLikedBooks(likedBooksPrev)">이전</button>
            <button v-if="likedBooksNext" @click="fetchLikedBooks(likedBooksNext)">다음</button>
          </div>
          <div v-if="loadingLikedBooks" class="loading-state">도서 목록을 불러오는 중...</div>
          <div v-if="errorLikedBooks" class="error-state">{{ errorLikedBooks }}</div>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import UserInfo from '@/components/user/UserInfo.vue'
import BookCard from '@/components/books/BookCard.vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import UserEditForm from '@/components/user/UserEditForm.vue'

export default {
  name: 'MyPage',
  components: {
  Navbar,
  Footer,
  UserInfo,
  BookCard,
  UserEditForm
},
  data() {
    return {
      user: null,
      loadingUser: false,
      errorUser: null,
      followers: [],
      followersNext: null,
      followersPrev: null,
      loadingFollowers: false,
      errorFollowers: null,
      following: [],
      followingNext: null,
      followingPrev: null,
      loadingFollowing: false,
      errorFollowing: null,
      likedBooks: [],
      likedBooksNext: null,
      likedBooksPrev: null,
      loadingLikedBooks: false,
      errorLikedBooks: null,
      currentUserId: 0,
      isMine: false,
      showFollowerList: false,
      showFollowingList: false,
      showLikedBooksList: false,
      editMode: false,
      editForm: {
        nickname: '',
        bio: '',
        profile_image: null,
        interested_categories: []
      },
      allCategories: [],
      previewImage: '',
      editLoading: false,
      editError: null,
      fallbackProfile: 'https://cdn-icons-png.flaticon.com/512/149/149071.png'
    }
  },
  async mounted() {
    this.currentUserId = await this.fetchCurrentUserId()
    const userId = this.$route.params.id ? Number(this.$route.params.id) : this.currentUserId
    this.isMine = userId === this.currentUserId
    await Promise.all([
      this.fetchUserProfile(userId),
      this.fetchAllCategories(),
      this.fetchFollowers(userId),
      this.fetchFollowing(userId),
      this.fetchLikedBooks(userId)
    ])
  },
  methods: {
    async fetchCurrentUserId() {
      try {
        const token = localStorage.getItem('access_token')
        const { data } = await axios.get('/api/accounts/profile/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        return data.id
      } catch {
        return 0
      }
    },
    onUserUpdated(updatedUser) {
      this.user = updatedUser
      this.editMode = false
    },
    cancelEdit() {
      this.editMode = false
      this.editError = null
    },
    async fetchUserProfile(userId) {
      this.loadingUser = true
      this.errorUser = null
      try {
        let url, headers = {}
        if (userId === this.currentUserId) {
          url = '/api/accounts/profile/'
          headers = { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        } else {
          url = `/api/accounts/${userId}/profile/`
          headers = {}
        }
        const { data } = await axios.get(url, { headers })
        this.user = data
      } catch {
        this.user = null
        this.errorUser = '프로필 정보를 불러올 수 없습니다.'
      } finally {
        this.loadingUser = false
      }
    },
    async fetchAllCategories() {
      try {
        const { data } = await axios.get('/api/books/categories/')
        if (Array.isArray(data.categories)) {
          this.allCategories = data.categories
        } else if (Array.isArray(data)) {
          this.allCategories = data
        }
      } catch {
        this.allCategories = []
      }
    },
    async fetchFollowers(urlOrUserId) {
      this.loadingFollowers = true
      this.errorFollowers = null
      let url = typeof urlOrUserId === 'string'
        ? urlOrUserId
        : `/api/accounts/${urlOrUserId}/followers/`
      try {
        const { data } = await axios.get(url)
        this.followers = data.results || []
        this.followersNext = data.next
        this.followersPrev = data.previous
      } catch {
        this.followers = []
        this.followersNext = null
        this.followersPrev = null
        this.errorFollowers = '팔로워 목록을 불러올 수 없습니다.'
      } finally {
        this.loadingFollowers = false
      }
    },
    async fetchFollowing(urlOrUserId) {
      this.loadingFollowing = true
      this.errorFollowing = null
      let url = typeof urlOrUserId === 'string'
        ? urlOrUserId
        : `/api/accounts/${urlOrUserId}/following/`
      try {
        const { data } = await axios.get(url)
        this.following = data.results || []
        this.followingNext = data.next
        this.followingPrev = data.previous
      } catch {
        this.following = []
        this.followingNext = null
        this.followingPrev = null
        this.errorFollowing = '팔로잉 목록을 불러올 수 없습니다.'
      } finally {
        this.loadingFollowing = false
      }
    },
    async fetchLikedBooks(urlOrUserId) {
      this.loadingLikedBooks = true
      this.errorLikedBooks = null
      let url = typeof urlOrUserId === 'string'
        ? urlOrUserId
        : `/api/accounts/${urlOrUserId}/liked-books/`
      try {
        const { data } = await axios.get(url)
        this.likedBooks = data.results || []
        this.likedBooksNext = data.next
        this.likedBooksPrev = data.previous
      } catch {
        this.likedBooks = []
        this.likedBooksNext = null
        this.likedBooksPrev = null
        this.errorLikedBooks = '도서 목록을 불러올 수 없습니다.'
      } finally {
        this.loadingLikedBooks = false
      }
    },
    openLikedBooksModal() {
      this.showLikedBooksList = true
      this.fetchLikedBooks(this.user.id)
    },
    closeLikedBooksModal() {
      this.showLikedBooksList = false
      // 페이지네이션 상태만 초기화
      this.likedBooksNext = null
      this.likedBooksPrev = null
      this.errorLikedBooks = null
    },
    async followUser(userId) {
      try {
        const { data } = await axios.post(
          `/api/accounts/${userId}/follow/`
        )
        if (this.user && this.user.id === userId) {
          this.user.is_following = data.is_following
          this.user.follower_count = data.follower_count
          this.user.following_count = data.following_count
        }
      } catch (e) {
        alert('팔로우/언팔로우에 실패했습니다.')
      }
    },
    async unfollowUser(userId) {
      await this.followUser(userId)
    },
    handleFollowToggle(updatedProfile) {
      this.user = updatedProfile
    },
    navigateToBook(bookId) {
      this.$router.push({ name: 'BookDetail', params: { id: bookId } })
    },
    startEdit() {
      this.editMode = true
      this.editForm.nickname = this.user.nickname || ''
      this.editForm.bio = this.user.bio || ''
      this.editForm.profile_image = null
      this.previewImage = ''
      this.editForm.interested_categories = (this.user.interested_categories || []).map(cat => cat.id)
      this.editError = null
    },
    cancelEdit() {
      this.editMode = false
      this.editError = null
      this.previewImage = ''
    },
    onFileChange(e) {
      const file = e.target.files[0]
      if (file) {
        this.editForm.profile_image = file
        this.previewImage = URL.createObjectURL(file)
      }
    },
    async submitEdit() {
      this.editLoading = true
      this.editError = null
      try {
        const formData = new FormData()
        if (this.editForm.nickname) formData.append('nickname', this.editForm.nickname)
        if (this.editForm.bio) formData.append('bio', this.editForm.bio)
        if (this.editForm.interested_categories && this.editForm.interested_categories.length > 0) {
          this.editForm.interested_categories.forEach(id => {
            formData.append('interested_categories', id)
          })
        }
        if (this.editForm.profile_image instanceof File) {
          formData.append('profile_image', this.editForm.profile_image)
        }
        const token = localStorage.getItem('access_token')
        const { data } = await axios.put('/api/accounts/profile/', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        // 응답으로 user 정보 갱신
        this.user.nickname = data.nickname
        this.user.bio = data.bio
        this.user.profile_image = data.profile_image
        this.user.interested_categories = this.allCategories.filter(cat =>
          data.interested_categories.includes(cat.id)
        )
        this.editMode = false
        this.previewImage = ''
        // --------- Pinia 사용자 정보도 함께 갱신 ---------
        const authStore = useAuthStore()
        if (this.isMine) {
          authStore.setUser({
            ...authStore.user,
            profile_image: data.profile_image,
            nickname: data.nickname,
            bio: data.bio,
            interested_categories: this.user.interested_categories
          })
        }
      } catch (err) {
        this.editError = err.response?.data?.detail || '회원 정보 수정에 실패했습니다.'
      } finally {
        this.editLoading = false
      }
    },
    onProfileImgError(e) {
      e.target.src = this.fallbackProfile
    }
  }
}
</script>

<style scoped>
.my-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* 회원 정보 카드 */
.profile-card {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  padding: 1.5rem 1rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  margin-bottom: 2rem;
}
.profile-card-img {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  background: #f0f0f0;
  flex-shrink: 0;
}
.profile-card-main {
  flex: 1;
}
.profile-card-nickname {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
  color: #222;
}
.profile-card-bio {
  font-size: 1.1rem;
  color: #444;
  margin-bottom: 0.7rem;
}
.profile-card-meta {
  display: flex;
  gap: 1.2rem;
  font-size: 1rem;
  margin-bottom: 0.7rem;
  color: #1976d2;
}
.profile-card-categories {
  margin-top: 0.5rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.category-tag {
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 12px;
  padding: 0.18rem 0.9rem;
  font-size: 0.98rem;
  font-weight: 500;
  margin-bottom: 0.1rem;
}

/* 팔로워/팔로잉/최근팔로잉 카드 */
.profile-summary-row {
  display: flex;
  gap: 2rem;
  margin: 2rem 0 2rem 0;
  align-items: flex-start;
}
.summary-block {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  min-width: 150px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.summary-count {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
}
.summary-link {
  background: none;
  border: none;
  color: #1976d2;
  cursor: pointer;
  padding: 0;
  font-size: 0.95rem;
  text-decoration: underline;
}
.recent-following-block {
  min-width: 220px;
}
.recent-following-list {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

/* 카드(팔로워/팔로잉/최근팔로잉/찜한도서) */
.custom-card,
.user-card {
  min-width: 120px;
  max-width: 140px;
  height: 200px;
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  transition: box-shadow 0.2s, border 0.2s;
  box-sizing: border-box;
  padding: 0.5rem 0.5rem 0.5rem 0.5rem;
}
.custom-card:hover,
.user-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  border: 1.5px solid #1976d2;
}
.user-card-img-wrap {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  background: #f8f8f8;
  margin-bottom: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.user-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.user-card-name {
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  text-align: center;
  word-break: break-all;
}
.user-card-bio {
  font-size: 0.92rem;
  color: #666;
  text-align: center;
  margin-top: 0.1rem;
  word-break: break-all;
}
.card-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-top: 0.5rem;
  margin-bottom: 0.2rem;
}
.card-desc {
  font-size: 0.85rem;
  color: #666;
}
.multi-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  white-space: normal;
  width: 100%;
  max-width: 120px;
  line-height: 1.3;
  min-height: 2.6em;
}
.recent-following-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  background: #f0f0f0;
}
.recent-following-nickname {
  font-size: 0.85rem;
  text-align: center;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 찜한 도서 */
.recent-liked-books-section {
  margin-top: 2rem;
}
.recent-liked-books-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.books-container.small.horizontal-scroll {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}
.empty-state {
  color: #888;
  padding: 1rem 0;
  font-size: 0.95rem;
}

/* 모달 */
.modal-bg {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  z-index: 1000;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.modal-list.liked-books-modal-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.12);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  margin-top: 4rem;
  min-width: 320px;
  max-width: 700px;
  width: 100%;
  max-height: 700px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.custom-card-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(120px, 1fr));
  gap: 1rem;
}
.pagination {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}
.loading-state {
  color: #1976d2;
  padding: 1rem 0;
}
.error-state {
  color: #dc3545;
  padding: 1rem 0;
}
@media (max-width: 1200px) {
  .main-content {
    padding: 1.5rem;
  }
  .profile-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .profile-card-img {
    width: 80px;
    height: 80px;
  }
  .profile-card-meta {
    justify-content: center;
  }
}

@media (max-width: 900px) {
  .profile-summary-row {
    flex-direction: column;
    gap: 1rem;
  }
  .summary-block {
    width: 100%;
    min-width: 0;
  }
  .modal-list.liked-books-modal-list {
    max-width: 98vw;
  }
}
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  .profile-summary-row {
    flex-direction: column;
    gap: 1rem;
  }
  .custom-card-grid {
    grid-template-columns: repeat(2, minmax(120px, 1fr));
  }
}
@media (max-width: 480px) {
  .profile-card-img {
    width: 60px;
    height: 60px;
  }
  .profile-card-nickname {
    font-size: 1.2rem;
  }
  .profile-card-meta {
    font-size: 0.9rem;
  }
  .custom-card {
    min-width: 100px;
    max-width: 120px;
    height: 180px;
  }
}
</style>

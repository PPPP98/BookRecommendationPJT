<template>
  <div class="my-page">
    <Navbar />
    <main class="main-content">
      <UserInfo
        v-if="user"
        :user="user"
        :isMine="isMine"
        @follow-toggle="handleFollowToggle"
      />
      <div v-else-if="loadingUser" class="loading-state">프로필 정보를 불러오는 중...</div>
      <div v-else-if="errorUser" class="error-state">{{ errorUser }}</div>

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
            <div
              v-for="u in user.recent_following || []"
              :key="u.id"
              class="custom-card user-card"
              @click="navigateToProfile(u.id)"
            >
              <div class="custom-card-image-wrap">
                <img :src="u.profile_image" :alt="u.nickname" class="custom-card-image" />
              </div>
              <div class="multi-ellipsis card-title">{{ u.nickname }}</div>
            </div>
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
            <div
              v-for="u in followers"
              :key="u.id"
              class="custom-card user-card"
              @click="navigateToProfile(u.id)"
            >
              <div class="custom-card-image-wrap">
                <img :src="u.profile_image" :alt="u.nickname" class="custom-card-image" />
              </div>
              <div class="multi-ellipsis card-title">{{ u.nickname }}</div>
              <div class="multi-ellipsis card-desc">{{ u.bio }}</div>
            </div>
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
            <div
              v-for="u in following"
              :key="u.id"
              class="custom-card user-card"
              @click="navigateToProfile(u.id)"
            >
              <div class="custom-card-image-wrap">
                <img :src="u.profile_image" :alt="u.nickname" class="custom-card-image" />
              </div>
              <div class="multi-ellipsis card-title">{{ u.nickname }}</div>
              <div class="multi-ellipsis card-desc">{{ u.bio }}</div>
            </div>
          </div>
          <div class="pagination">
            <button v-if="followingPrev" @click="fetchFollowing(followingPrev)">이전</button>
            <button v-if="followingNext" @click="fetchFollowing(followingNext)">다음</button>
          </div>
          <div v-if="loadingFollowing" class="loading-state">팔로잉 목록을 불러오는 중...</div>
          <div v-if="errorFollowing" class="error-state">{{ errorFollowing }}</div>
        </div>
      </div>

      <!-- 최근 찜한 도서(가로 스크롤, 카드 크기/2줄 말줄임) + 더보기 버튼 -->
      <div v-if="user" class="recent-liked-books-section">
        <div class="recent-liked-books-header">
          <h3>최근 찜한 도서</h3>
          <button class="summary-link" @click="openLikedBooksModal">더보기</button>
        </div>
        <div class="books-container small horizontal-scroll">
          <div
            v-for="book in user.recent_liked_books || []"
            :key="book.id"
            class="custom-card"
            @click="navigateToBook(book.id)"
          >
            <div class="custom-card-image-wrap">
              <img :src="book.cover" :alt="book.title" class="custom-card-image" />
            </div>
            <div class="multi-ellipsis card-title">{{ book.title }}</div>
          </div>
        </div>
        <div v-if="!user.recent_liked_books || user.recent_liked_books.length === 0" class="empty-state">
          찜한 도서가 없습니다.
        </div>
      </div>

      <!-- 좋아요한 도서 전체 목록 모달 (가로 5개씩, 세로 스크롤, 페이지네이션) -->
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
              <div class="custom-card-image-wrap">
                <img :src="book.cover" :alt="book.title" class="custom-card-image" />
              </div>
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
import axios from 'axios'

export default {
  name: 'MyPage',
  components: {
    Navbar,
    Footer,
    UserInfo
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
      showLikedBooksList: false
    }
  },
  async mounted() {
    this.currentUserId = await this.fetchCurrentUserId()
    const userId = this.$route.params.id ? Number(this.$route.params.id) : this.currentUserId
    this.isMine = userId === this.currentUserId
    await Promise.all([
      this.fetchUserProfile(userId),
      this.fetchFollowers(userId),
      this.fetchFollowing(userId),
      this.fetchLikedBooks(userId)
    ])
  },
  methods: {
    async fetchCurrentUserId() {
      return 1
    },
    async fetchUserProfile(userId) {
      this.loadingUser = true
      this.errorUser = null
      try {
        const { data } = await axios.get(`/api/accounts/${userId}/profile/`)
        this.user = data
      } catch {
        this.user = null
        this.errorUser = '프로필 정보를 불러올 수 없습니다.'
      } finally {
        this.loadingUser = false
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
      this.likedBooks = []
      this.likedBooksNext = null
      this.likedBooksPrev = null
      this.errorLikedBooks = null
    },
    handleFollowToggle(updatedProfile) {
      this.user = updatedProfile
    },
    navigateToProfile(userId) {
      this.$router.push({ name: 'UserProfile', params: { id: userId } })
    },
    navigateToBook(bookId) {
      this.$router.push({ name: 'BookDetail', params: { id: bookId } })
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
.custom-card-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(120px, 1fr));
  gap: 1rem;
}
.custom-card {
  min-width: 120px;
  max-width: 140px;
  height: 220px;
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
  padding: 0.5rem;
  overflow: hidden;
}
.custom-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  border: 1.5px solid #1976d2;
}
.custom-card-image-wrap {
  width: 100%;
  height: 120px;
  border-radius: 6px;
  overflow: hidden;
  background: #f8f8f8;
  flex-shrink: 0;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.custom-card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.card-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.2rem;
  min-height: 2.6em;
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
}
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
  .custom-card-grid {
    grid-template-columns: repeat(2, minmax(120px, 1fr));
  }
}
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  .books-container.small.horizontal-scroll {
    gap: 0.5rem;
  }
  .custom-card-grid {
    grid-template-columns: repeat(2, minmax(120px, 1fr));
  }
}
</style>

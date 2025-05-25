<template>
  <div class="my-page">
    <Navbar />
    <main class="main-content">
      <UserInfo 
        :user="user"
        :editable="true"
        @update="updateUserInfo"
      />
      <div class="sections-container">
        <div class="main-section">
          <MyThreadList
            :threads="threads"
            :comments="comments"
            @delete-thread="deleteThread"
            @delete-comment="deleteComment"
          />
          <BookLikeList
            :books="likedBooks"
            :editable="true"
            @unlike="unlikeBook"
          />
        </div>
        <div class="side-section">
          <FollowList
            :users="followers"
            type="followers"
            :currentUserId="user.id ?? 0"
            @follow="followUser"
            @unfollow="unfollowUser"
          />
          <FollowList
            :users="following"
            type="following"
            :currentUserId="user.id ?? 0"
            @follow="followUser"
            @unfollow="unfollowUser"
          />
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
import BookLikeList from '@/components/books/BookLikeList.vue'
import FollowList from '@/components/user/FollowList.vue'
import MyThreadList from '@/components/thread/MyThreadList.vue'
import axios from 'axios'

export default {
  name: 'MyPage',
  components: {
    Navbar,
    Footer,
    UserInfo,
    BookLikeList,
    FollowList,
    MyThreadList
  },
  data() {
    return {
      user: {
        id: 0,
        username: '',
        email: '',
        profile_image: '/default-profile.png'
      },
      threads: [],
      comments: [],
      followers: [],
      following: [],
      likedBooks: []
    }
  },
  async mounted() {
    const userId = await this.fetchCurrentUserId()
    await Promise.all([
      this.fetchUserProfile(userId),
      this.fetchFollowers(userId),
      this.fetchFollowing(userId),
      this.fetchLikedBooks(userId),
      this.fetchMyThreads(userId),
      this.fetchMyComments(userId)
    ])
  },
  methods: {
    async fetchCurrentUserId() {
      // 실제 프로젝트에서는 store나 쿠키에서 가져오세요
      // 예: const { data } = await axios.get('/api/accounts/me/')
      // return data.id
      // 여기서는 임시로 1로 가정
      return 1
    },
    async fetchUserProfile(userId) {
      try {
        const { data } = await axios.get(`/api/accounts/${userId}/profile/`)
        this.user = {
          id: data.id ?? 0,
          username: data.username ?? '',
          email: data.email ?? '',
          profile_image: data.profile_image || '/default-profile.png'
        }
      } catch {
        this.user = {
          id: 0,
          username: '',
          email: '',
          profile_image: '/default-profile.png'
        }
      }
    },
    async fetchFollowers(userId) {
      try {
        const { data } = await axios.get(`/api/accounts/${userId}/followers/`)
        this.followers = data.results || []
      } catch {
        this.followers = []
      }
    },
    async fetchFollowing(userId) {
      try {
        const { data } = await axios.get(`/api/accounts/${userId}/following/`)
        this.following = data.results || []
      } catch {
        this.following = []
      }
    },
    async fetchLikedBooks(userId) {
      try {
        const { data } = await axios.get(`/api/accounts/${userId}/liked-books/`)
        this.likedBooks = data.results || []
      } catch {
        this.likedBooks = []
      }
    },
    async fetchMyThreads(userId) {
      try {
        // 실제 API 경로에 맞게 수정하세요!
        const { data } = await axios.get(`/api/threads/?user=${userId}`)
        this.threads = data.results || []
      } catch {
        this.threads = []
      }
    },
    async fetchMyComments(userId) {
      try {
        // 실제 API 경로에 맞게 수정하세요!
        const { data } = await axios.get(`/api/threads/comments/?user=${userId}`)
        this.comments = data.results || []
      } catch {
        this.comments = []
      }
    },
    async updateUserInfo(updatedInfo) {
      try {
        const response = await axios.patch(
          `/api/accounts/${this.user.id}/profile/`,
          updatedInfo
        )
        this.user = {
          ...this.user,
          ...response.data,
          profile_image: response.data.profile_image || '/default-profile.png'
        }
        alert('프로필 정보가 성공적으로 수정되었습니다.')
      } catch (error) {
        alert('프로필 정보 수정에 실패했습니다.')
      }
    },
    async unlikeBook(bookId) {
      // TODO: API 연동 시 구현
      console.log('Unlike book:', bookId)
    },
    async followUser(userId) {
      // TODO: API 연동 시 구현
      console.log('Follow user:', userId)
    },
    async unfollowUser(userId) {
      // TODO: API 연동 시 구현
      console.log('Unfollow user:', userId)
    },
    async deleteThread(threadId) {
      // TODO: API 연동 시 구현
      console.log('Delete thread:', threadId)
    },
    async deleteComment(commentId) {
      // TODO: API 연동 시 구현
      console.log('Delete comment:', commentId)
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
.sections-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}
.main-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.side-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
@media (max-width: 768px) {
  .sections-container {
    grid-template-columns: 1fr;
  }
}
</style>

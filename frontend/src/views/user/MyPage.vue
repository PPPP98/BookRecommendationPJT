<!-- 
  MyPage 컴포넌트
  역할: 사용자의 프로필과 활동 내역을 표시하는 마이페이지
  기능:
    - 사용자 정보 표시 및 수정
    - 찜한 도서 목록
    - 팔로워/팔로잉 목록
    - 작성한 글/댓글 목록
  데이터 구조:
    - user: Object - 사용자 정보
    - likedBooks: Array - 찜한 도서 목록
    - followers/following: Array - 팔로워/팔로잉 목록
    - threads/comments: Array - 작성한 글/댓글 목록
-->
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
            :threads="user.threads"
            :comments="user.comments"
            @delete-thread="deleteThread"
            @delete-comment="deleteComment"
          />
        </div>

        <div class="side-section">
          <BookLikeList
            :books="likedBooks"
            :editable="true"
            @unlike="unlikeBook"
          />

          <FollowList
            :users="followers"
            type="followers"
            :currentUserId="user.id"
            @follow="followUser"
            @unfollow="unfollowUser"
          />

          <FollowList
            :users="following"
            type="following"
            :currentUserId="user.id"
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
import { users } from '@/mocks/users'
import { books } from '@/mocks/books'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import UserInfo from '@/components/user/UserInfo.vue'
import BookLikeList from '@/components/books/BookLikeList.vue'
import FollowList from '@/components/user/FollowList.vue'
import MyThreadList from '@/components/thread/MyThreadList.vue'

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
    // 현재 로그인한 사용자를 mock 데이터에서 가져옴
    const currentUser = users[0]
    
    return {
      user: currentUser,
      likedBooks: books.filter(book => currentUser.favorite_books.includes(book.id)),
      followers: users.filter(user => currentUser.followers.includes(user.id)),
      following: users.filter(user => currentUser.following.includes(user.id))
    }
  },
  methods: {
    // 사용자 정보 수정
    async updateUserInfo(updatedInfo) {
      // TODO: API 연동 시 구현
      console.log('Update user info:', updatedInfo)
    },

    // 도서 찜 해제
    async unlikeBook(bookId) {
      // TODO: API 연동 시 구현
      console.log('Unlike book:', bookId)
    },

    // 팔로우
    async followUser(userId) {
      // TODO: API 연동 시 구현
      console.log('Follow user:', userId)
    },

    // 언팔로우
    async unfollowUser(userId) {
      // TODO: API 연동 시 구현
      console.log('Unfollow user:', userId)
    },

    // 글 삭제
    async deleteThread(threadId) {
      // TODO: API 연동 시 구현
      console.log('Delete thread:', threadId)
    },

    // 댓글 삭제
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
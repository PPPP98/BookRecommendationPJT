<template>
  <div class="dashboard-page">
    <!-- 상단 네비게이션 -->

    <!-- 상단 배경 이미지 -->
    <div class="dashboard-hero-bg"></div>

    <div class="dashboard-main-layout">
      <!-- 사이드바 -->
      <aside class="dashboard-sidebar">
        <div class="sidebar-profile-card">
          <img
            class="sidebar-profile-img"
            :src="profile.profile_image || fallbackProfile"
            alt="profile"
          />
          <div class="sidebar-profile-title">
            {{ profile.nickname || "Book Community" }}
          </div>
          <button class="sidebar-theme-btn" @click="goToEditProfile">정보 수정하기</button>
        </div>
        <div class="sidebar-links-row">
          <div>
            <p>팔로워 : {{ profile.follower_count }}</p>
            <p>팔로잉 : {{ profile.following_count }}</p>
          </div>
        </div>
        <div class="sidebar-welcome">
          <div class="sidebar-welcome-title">자기소개</div>
          <div class="sidebar-welcome-desc">
            {{
              profile.bio || "자기소개가 없습니다"
            }}
          </div>
        </div>
        
        <!-- 관심 카테고리 섹션 추가 -->
        <div class="sidebar-categories" v-if="profile.interested_categories && profile.interested_categories.length > 0">
          <div class="sidebar-welcome-title">관심 카테고리</div>
          <div class="category-tags">
            <span 
              v-for="category in profile.interested_categories" 
              :key="category.id" 
              class="category-tag"
            >
              {{ category.name }}
            </span>
          </div>
        </div>
      </aside>

      <!-- 메인 컨텐츠 -->
      <main class="dashboard-main-content">
        <!-- 프로필 수정 폼 -->
        <UserEditForm
          v-if="isEditing"
          :user="profile"
          :all-categories="categories"
          :fallback-profile="fallbackProfile"
          @update="handleEditComplete"
          @cancel="isEditing = false"
        />
        <!-- 탭 메뉴 -->
        <nav v-if="!isEditing" class="dashboard-tabs">
          <span
            v-for="tab in tabs"
            :key="tab.value"
            class="tab"
            :class="{ active: activeTab === tab.value }"
            @click="changeTab(tab.value)"
            >{{ tab.label }}</span
          >
        </nav>

        <!-- 카드 그리드 -->
        <div v-if="!isEditing && activeTab === 'library'" class="dashboard-card-grid">
          <div
            v-for="book in books"
            :key="book.id"
            class="dashboard-book-card"
            @click="
              $router.push({ name: 'BookDetail', params: { id: book.id } })
            "
          >
            <img
              :src="book.cover"
              class="dashboard-book-img"
              :alt="book.title"
            />
            <div class="book-info-overlay">
              <h3 class="book-title">{{ book.title }}</h3>
              <p class="book-author">{{ book.author }}</p>
            </div>
          </div>
        </div>

        <!-- 좋아요한 도서 목록 -->
        <div v-else-if="!isEditing && activeTab === 'liked'" class="dashboard-card-grid">
          <div
            v-for="book in likedBooks"
            :key="book.id"
            class="dashboard-book-card"
            @click="
              $router.push({ name: 'BookDetail', params: { id: book.id } })
            "
          >
            <img
              :src="book.cover"
              class="dashboard-book-img"
              :alt="book.title"
            />
            <div class="book-info-overlay">
              <h3 class="book-title">{{ book.title }}</h3>
              <p class="book-author">{{ book.author }}</p>
            </div>
          </div>
        </div>

        <!-- 팔로잉 목록 -->
        <div v-else-if="!isEditing && activeTab === 'following'" class="user-list-grid">
          <div
            v-for="user in followings"
            :key="user.id"
            class="user-card"
          >
            <div class="user-card-content">
              <img
                :src="user.profile_image || fallbackProfile"
                class="user-profile-img"
                :alt="user.nickname"
              />
              <div class="user-info">
                <h3 class="user-nickname">{{ user.nickname }}</h3>
                <p class="user-bio">{{ user.bio || "자기소개가 없습니다" }}</p>
              </div>
              <button 
                class="follow-btn" 
                :class="{ 'following': user.is_following }"
                @click.stop="toggleFollow(user)"
              >
                {{ user.is_following ? '팔로잉' : '팔로우' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 팔로워 목록 -->
        <div v-else-if="!isEditing && activeTab === 'followers'" class="user-list-grid">
          <div
            v-for="user in followers"
            :key="user.id"
            class="user-card"
          >
            <div class="user-card-content">
              <img
                :src="user.profile_image || fallbackProfile"
                class="user-profile-img"
                :alt="user.nickname"
              />
              <div class="user-info">
                <h3 class="user-nickname">{{ user.nickname }}</h3>
                <p class="user-bio">{{ user.bio || "자기소개가 없습니다" }}</p>
              </div>
              <button 
                class="follow-btn" 
                :class="{ 'following': user.is_following }"
                @click.stop="toggleFollow(user)"
              >
                {{ user.is_following ? '팔로잉' : '팔로우' }}
              </button>
            </div>
          </div>
        </div>

        <button 
          class="dashboard-load-more" 
          v-if="!isEditing && shouldShowLoadMore" 
          @click="loadMore"
        >
          더 보기
        </button>
      </main>
    </div>


  </div>
</template>

<script>
import axios from "axios";
import UserEditForm from '@/components/user/UserEditForm.vue';

export default {
  name: "DashboardPage",
  components: {
    UserEditForm
  },
  data() {
    return {
      categories: [],
      isEditing: false,
      profile: {
        id: null,
        username: "",
        profile_image: "",
        nickname: "",
        bio: "",
        follower_count: 0,
        following_count: 0,
        is_following: false,
        interested_categories: [],
      },
      followers: [],
      followings: [],
      likedBooks: [],
      followersPage: 1,
      followingsPage: 1,
      likedBooksPage: 1,
      followersHasMore: true,
      followingsHasMore: true,
      likedBooksHasMore: true,
      fallbackProfile: "/default-profile.png.jpg",
      sidebarLinks: {
        left: [
          { label: "Recommendations" },
          { label: "Challenges" },
          { label: "Bookworms" },
          { label: "Connections" },
        ],
        right: [
          { label: "Top Picks" },
          { label: "Favorites" },
          { label: "Community" },
          { label: "Engagements" },
        ],
      },
      tabs: [
        { label: "좋아요한 도서", value: "liked" },
        { label: "Following", value: "following" },
        { label: "Followers", value: "followers" },
      ],
      activeTab: "liked",
      books: [],
      page: 1,
      hasMore: true,
      search: "",
    };
  },
  computed: {
    shouldShowLoadMore() {
      if (this.activeTab === 'following') {
        return this.followingsHasMore;
      } else if (this.activeTab === 'followers') {
        return this.followersHasMore;
      } else if (this.activeTab === 'liked') {
        return this.likedBooksHasMore;
      } else {
        return this.hasMore;
      }
    }
  },
  mounted() {
    Promise.all([
      this.fetchProfile(),
      this.fetchCategories(),
      this.fetchSidebarLinks()
    ]).then(() => {
      // 프로필 정보가 로드된 후 관련 데이터 로드
      if (this.profile.id) {
        if (this.activeTab === 'following') {
          this.fetchFollowings();
        } else if (this.activeTab === 'followers') {
          this.fetchFollowers();
        } else if (this.activeTab === 'liked') {
          this.fetchLikedBooks();
        } else {
          this.fetchBooks();
        }
      }
    });
  },
  watch: {
    activeTab(newTab) {
      if (newTab === 'following') {
        this.fetchFollowings(true);
      } else if (newTab === 'followers') {
        this.fetchFollowers(true);
      } else if (newTab === 'liked') {
        this.fetchLikedBooks(true);
      } else {
        this.fetchBooks(true);
      }
    }
  },
  methods: {
    async fetchCategories() {
      try {
        const { data } = await axios.get("/api/books/categories/");
        this.categories = data;
      } catch (error) {
        console.error("카테고리 목록을 불러오는데 실패했습니다:", error);
        this.categories = [];
      }
    },
    async fetchProfile() {
      try {
        const { data } = await axios.get("/api/accounts/profile/");
        this.profile = {
          id: data.id,
          username: data.username,
          profile_image: data.profile_image,
          nickname: data.nickname,
          bio: data.bio,
          follower_count: data.follower_count,
          following_count: data.following_count,
          is_following: data.is_following,
          interested_categories: data.interested_categories || [],
        };
      } catch (error) {
        console.error("프로필 정보를 불러오는데 실패했습니다:", error);
        // fallback to default
      }
    },
    async fetchSidebarLinks() {
      try {
        const { data } = await axios.get("/api/dashboard/sidebar-links/");
        this.sidebarLinks = data;
      } catch {
        // fallback to default
      }
    },
    async fetchBooks(reset = true) {
      try {
        if (reset) {
          this.page = 1;
          this.books = [];
        }
        const { data } = await axios.get("/api/dashboard/books/", {
          params: {
            tab: this.activeTab,
            page: this.page,
            search: this.search,
          },
        });
        this.books = reset ? data.results : [...this.books, ...data.results];
        this.hasMore = !!data.next;
      } catch {
        this.books = [];
        this.hasMore = false;
      }
    },
    async fetchFollowings(reset = true) {
      try {
        if (reset) {
          this.followingsPage = 1;
          this.followings = [];
        }
        
        if (!this.profile.id) return;
        
        const { data } = await axios.get(`/api/accounts/${this.profile.id}/following/`, {
          params: {
            page: this.followingsPage,
            page_size: 50,
          },
        });
        
        this.followings = reset ? data.results : [...this.followings, ...data.results];
        this.followingsHasMore = !!data.next;
      } catch (error) {
        console.error("팔로잉 목록을 불러오는데 실패했습니다:", error);
        this.followings = [];
        this.followingsHasMore = false;
      }
    },
    async fetchFollowers(reset = true) {
      try {
        if (reset) {
          this.followersPage = 1;
          this.followers = [];
        }
        
        if (!this.profile.id) return;
        
        const { data } = await axios.get(`/api/accounts/${this.profile.id}/followers/`, {
          params: {
            page: this.followersPage,
            page_size: 50,
          },
        });
        
        this.followers = reset ? data.results : [...this.followers, ...data.results];
        this.followersHasMore = !!data.next;
      } catch (error) {
        console.error("팔로워 목록을 불러오는데 실패했습니다:", error);
        this.followers = [];
        this.followersHasMore = false;
      }
    },
    async fetchLikedBooks(reset = true) {
      try {
        if (reset) {
          this.likedBooksPage = 1;
          this.likedBooks = [];
        }
        
        if (!this.profile.id) return;
        
        const { data } = await axios.get(`/api/accounts/${this.profile.id}/liked-books/`, {
          params: {
            page: this.likedBooksPage,
            page_size: 50,
          },
        });
        
        this.likedBooks = reset ? data.results : [...this.likedBooks, ...data.results];
        this.likedBooksHasMore = !!data.next;
      } catch (error) {
        console.error("좋아요한 도서 목록을 불러오는데 실패했습니다:", error);
        this.likedBooks = [];
        this.likedBooksHasMore = false;
      }
    },
    changeTab(tab) {
      if (this.activeTab !== tab) {
        this.activeTab = tab;
      }
    },
    loadMore() {
      if (this.activeTab === 'following') {
        if (!this.followingsHasMore) return;
        this.followingsPage += 1;
        this.fetchFollowings(false);
      } else if (this.activeTab === 'followers') {
        if (!this.followersHasMore) return;
        this.followersPage += 1;
        this.fetchFollowers(false);
      } else if (this.activeTab === 'liked') {
        if (!this.likedBooksHasMore) return;
        this.likedBooksPage += 1;
        this.fetchLikedBooks(false);
      } else {
        if (!this.hasMore) return;
        this.page += 1;
        this.fetchBooks(false);
      }
    },
    goToEditProfile() {
      this.isEditing = true;
    },

    handleEditComplete() {
      this.isEditing = false;
      this.fetchProfile();
    },
    async toggleFollow(user) {
      try {
        if (user.is_following) {
          // 언팔로우 API 호출
          await axios.delete(`/api/accounts/${user.id}/follow/`);
        } else {
          // 팔로우 API 호출
          await axios.post(`/api/accounts/${user.id}/follow/`);
        }
        
        // 상태 업데이트
        user.is_following = !user.is_following;
        
        // 팔로잉/팔로워 카운트 업데이트를 위해 프로필 다시 가져오기
        await this.fetchProfile();
      } catch (error) {
        console.error("팔로우 상태 변경에 실패했습니다:", error);
      }
    },
  },
};
</script>

<style scoped>
/* ... (스타일은 앞선 답변과 동일, 이미지 참고) ... */
.dashboard-page {
  background: #fff;
  min-height: 100vh;
  font-family: "Inter", Arial, sans-serif;
  color: #222;
}
.dashboard-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  height: 56px;
  border-bottom: 1px solid #ececec;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}
.navbar-left span,
.navbar-left b {
  margin-right: 1.3rem;
  font-size: 1.08rem;
  cursor: pointer;
}
.navbar-left b {
  font-weight: 700;
}
.dashboard-search {
  width: 320px;
  padding: 0.6em 2.2em 0.6em 1em;
  border-radius: 22px;
  border: 1px solid #ececec;
  font-size: 1rem;
  background: #fafbfc;
}
.search-icon {
  position: absolute;
  left: 10.5rem;
  top: 1.7rem;
  color: #bbb;
  font-size: 1.1rem;
}
.navbar-center {
  position: relative;
  flex: 1;
  display: flex;
  justify-content: center;
}
.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.1rem;
}
.join-btn {
  background: #7c3aed;
  color: #fff;
  border: none;
  border-radius: 18px;
  padding: 0.5em 1.7em;
  font-weight: 700;
  font-size: 1.01rem;
  cursor: pointer;
  margin-right: 0.7rem;
}
.navbar-profile {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #eee;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.navbar-profile img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.dashboard-hero-bg {
  width: 100%;
  height: 160px;
  background: url("https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1200&q=80")
    center/cover no-repeat;
  margin-bottom: 0;
}
.dashboard-main-layout {
  display: flex;
  max-width: 1200px;
  margin: 70px auto 0 auto;
  gap: 2.5rem;
  position: relative;
  z-index: 1;
}
.dashboard-sidebar {
  width: 290px;
  min-width: 230px;
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 2px 18px rgba(0, 0, 0, 0.06);
  padding: 2.1rem 1.5rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.sidebar-profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.3rem;
}
.sidebar-profile-img {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 0.8rem;
  background: #f5f5f5;
}
.sidebar-profile-title {
  font-size: 1.13rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
  letter-spacing: -0.01em;
}
.sidebar-profile-desc {
  font-size: 0.97rem;
  color: #888;
  margin-bottom: 0.7rem;
}
.sidebar-theme-btn {
  background: #f5f6fa;
  color: #7c3aed;
  border: 1.5px solid #ececec;
  border-radius: 16px;
  padding: 0.4em 1.3em;
  font-weight: 600;
  font-size: 0.97rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
}
.sidebar-theme-btn:hover {
  background: #ece9fd;
  color: #5b21b6;
}
.sidebar-links-row {
  width: 100%;
  margin-bottom: 1.2rem;
  display: flex;
  justify-content: space-between;
  gap: 1.2rem;
}
.sidebar-links-row > div {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.sidebar-link {
  color: #181818;
  text-decoration: none;
  font-size: 0.98rem;
  border-radius: 7px;
  padding: 0.2em 0.5em;
  transition: background 0.13s, color 0.13s;
  cursor: pointer;
}
.sidebar-link:hover {
  background: #f5f5f5;
  color: #7c3aed;
}
.sidebar-welcome {
  width: 100%;
  background: #fafbfc;
  border-radius: 12px;
  padding: 1rem 1rem 0.8rem 1rem;
  margin-top: 1.1rem;
}
.sidebar-welcome-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #7c3aed;
  margin-bottom: 0.3rem;
}
.sidebar-welcome-desc {
  font-size: 0.97rem;
  color: #444;
  line-height: 1.5;
}
.sidebar-categories {
  width: 100%;
  background: #fafbfc;
  border-radius: 12px;
  padding: 1rem 1rem 0.8rem 1rem;
  margin-top: 1.1rem;
}
.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.category-tag {
  background: #ece9fd;
  color: #7c3aed;
  border-radius: 12px;
  padding: 0.3em 0.8em;
  font-size: 0.85rem;
  font-weight: 500;
}
.dashboard-main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.dashboard-tabs {
  display: flex;
  gap: 1.3rem;
  margin-bottom: 1.7rem;
  border-bottom: 1.5px solid #ececec;
  padding-bottom: 0.7rem;
}
.tab {
  color: #222;
  font-size: 1.04rem;
  font-weight: 500;
  padding: 0.4em 1.2em;
  border-radius: 14px 14px 0 0;
  background: none;
  cursor: pointer;
  border: none;
  transition: background 0.16s, color 0.16s;
}
.tab.active,
.tab:hover {
  background: #f5f5f5;
  color: #7c3aed;
}
.dashboard-card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem 1.5rem;
  margin-bottom: 2.5rem;
}
.dashboard-book-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  overflow: hidden;
  min-height: 160px;
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.11s;
  position: relative;
}

.dashboard-book-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px) scale(1.02);
}

.dashboard-book-card:hover .book-info-overlay {
  opacity: 1;
}

.book-info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.book-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 5px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-author {
  font-size: 0.85rem;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.dashboard-book-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

/* 팔로잉/팔로워 목록 스타일 */
.user-list-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.user-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  overflow: hidden;
  padding: 1rem;
  transition: box-shadow 0.15s, transform 0.11s;
}

.user-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

.user-card-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-profile-img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  background: #f5f5f5;
}

.user-info {
  flex: 1;
}

.user-nickname {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.user-bio {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.follow-btn {
  background: #f5f6fa;
  color: #7c3aed;
  border: 1.5px solid #ececec;
  border-radius: 16px;
  padding: 0.4em 1.3em;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
}

.follow-btn:hover {
  background: #ece9fd;
  color: #5b21b6;
}

.follow-btn.following {
  background: #7c3aed;
  color: #fff;
  border-color: #7c3aed;
}

.follow-btn.following:hover {
  background: #6b21e8;
}

.dashboard-load-more {
  display: block;
  margin: 1.5rem auto 0 auto;
  background: #fff;
  color: #888;
  border: 1.5px solid #ececec;
  border-radius: 18px;
  padding: 0.6em 2.2em;
  font-weight: 600;
  font-size: 1.07rem;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}
.dashboard-load-more:hover {
  background: #ece9fd;
  color: #7c3aed;
}
.dashboard-footer {
  background: #fafafa;
  border-top: 1px solid #ececec;
  padding: 2.2rem 0 1.7rem 0;
  font-size: 1rem;
  color: #888;
  margin-top: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 2.5rem;
  justify-content: center;
}
.footer-brand {
  min-width: 200px;
}
.footer-title {
  font-size: 1.12rem;
  font-weight: 700;
  color: #181818;
  margin-bottom: 0.5rem;
}
.footer-desc {
  font-size: 0.98rem;
  color: #888;
}
.footer-col {
  min-width: 180px;
}
.footer-col h4 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 0.7rem;
}
.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-col li {
  margin-bottom: 0.5rem;
}
@media (max-width: 1100px) {
  .dashboard-main-layout {
    flex-direction: column;
    gap: 1.5rem;
  }
  .dashboard-sidebar {
    width: 100%;
    min-width: 0;
    margin-bottom: 1.5rem;
  }
  .dashboard-main-content {
    width: 100%;
  }
  .dashboard-card-grid {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 700px) {
  .dashboard-main-layout {
    flex-direction: column;
    gap: 1rem;
  }
  .dashboard-sidebar {
    padding: 1.2rem 0.7rem;
  }
  .dashboard-main-content {
    padding: 0 0.5rem;
  }
  .dashboard-card-grid {
    grid-template-columns: 1fr;
  }
}
</style>

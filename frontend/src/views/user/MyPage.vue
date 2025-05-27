<template>
  <div class="dashboard-page">
    <!-- 상단 네비게이션 -->
    
    <!-- 상단 배경 이미지 -->
    <div class="dashboard-hero-bg"></div>

    <div class="dashboard-main-layout">
      <!-- 사이드바 -->
      <aside class="dashboard-sidebar">
        <div class="sidebar-profile-card">
          <img class="sidebar-profile-img" :src="profile.profile_image || fallbackProfile" alt="profile" />
          <div class="sidebar-profile-title">{{ profile.nickname || 'Book Community' }}</div>
          <div class="sidebar-profile-desc">{{ profile.bio || 'Reading Nook, Cozy Vibes' }}</div>
          <button class="sidebar-theme-btn">Customize Theme</button>
        </div>
        <div class="sidebar-links-row">
          <div>
            <div class="sidebar-follow-btns">
          <button class="sidebar-follow-btn" @click="showSection('followers')">팔로워</button>
          <button class="sidebar-follow-btn" @click="showSection('following')">팔로잉</button>
          <button class="sidebar-follow-btn" @click="showSection('recentFollowing')">최근 팔로잉</button>
          <button class="sidebar-follow-btn" @click="showSection('likedBooks')">찜한 도서</button>
        </div>
          </div>
        </div>
        <div class="sidebar-welcome">
          <div class="sidebar-welcome-title">WELCOME</div>
          <div class="sidebar-welcome-desc">
            {{ profile.welcome || 'Welcome to the Book Community! Dive into a world of books with our vibrant community. Share your love for reading, discover new titles, and engage in lively discussions. Join us on this literary journey!' }}
          </div>
        </div>
      </aside>

      <!-- 메인 컨텐츠 -->
      <main class="dashboard-main-content">
        <!-- 탭 메뉴 -->
        <nav class="dashboard-tabs">
          <span
            v-for="tab in tabs"
            :key="tab.value"
            class="tab"
            :class="{ active: activeTab === tab.value }"
            @click="changeTab(tab.value)"
          >{{ tab.label }}</span>
        </nav>

        <!-- 카드 그리드 -->
        <div class="dashboard-card-grid">
          <div
            v-for="book in books"
            :key="book.id"
            class="dashboard-book-card"
            @click="$router.push({ name: 'BookDetail', params: { id: book.id } })"
          >
            <img :src="book.cover" class="dashboard-book-img" :alt="book.title" />
          </div>
        </div>
        <button class="dashboard-load-more" v-if="hasMore" @click="loadMore">Load More</button>
      </main>
    </div>

    <!-- 푸터 -->
    <footer class="dashboard-footer">
      <div class="footer-brand">
        <div class="footer-title">Book Community</div>
        <div class="footer-desc">Inspiring readers since 2018</div>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li>Our story</li>
          <li>Opportunities</li>
          <li>Get in touch</li>
          <li>Articles</li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Join the discussion</h4>
        <ul>
          <li>Support Center</li>
          <li>Join as Premium</li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Connect with us</h4>
        <ul>
          <li>Facebook</li>
          <li>Twitter</li>
          <li>Instagram</li>
        </ul>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DashboardPage',
  data() {
    return {
      profile: {
        profile_image: '',
        nickname: '',
        bio: '',
        welcome: ''
      },
      fallbackProfile: '/default-profile.png.jpg',
      sidebarLinks: {
        left: [
          { label: 'Recommendations' },
          { label: 'Challenges' },
          { label: 'Bookworms' },
          { label: 'Connections' }
        ],
        right: [
          { label: 'Top Picks' },
          { label: 'Favorites' },
          { label: 'Community' },
          { label: 'Engagements' }
        ]
      },
      tabs: [
        { label: 'All', value: 'all' },
        { label: 'My Library', value: 'library' },
        { label: 'My', value: 'my' },
        { label: 'Collections', value: 'collections' },
        { label: 'Followed', value: 'followed' },
        { label: 'Recent', value: 'recent' }
      ],
      activeTab: 'all',
      books: [],
      page: 1,
      hasMore: true,
      search: ''
    }
  },
  mounted() {
    this.fetchProfile()
    this.fetchSidebarLinks()
    this.fetchBooks()
  },
  methods: {
    async fetchProfile() {
      try {
        const { data } = await axios.get('/api/accounts/profile/')
        this.profile = {
          profile_image: data.profile_image,
          nickname: data.nickname,
          bio: data.bio,
          welcome: data.welcome
        }
      } catch {
        // fallback to default
      }
    },
    async fetchSidebarLinks() {
      try {
        const { data } = await axios.get('/api/dashboard/sidebar-links/')
        this.sidebarLinks = data
      } catch {
        // fallback to default
      }
    },
    async fetchBooks(reset = true) {
      try {
        if (reset) {
          this.page = 1
          this.books = []
        }
        const { data } = await axios.get('/api/dashboard/books/', {
          params: {
            tab: this.activeTab,
            page: this.page,
            search: this.search
          }
        })
        this.books = reset ? data.results : [...this.books, ...data.results]
        this.hasMore = !!data.next
      } catch {
        this.books = []
        this.hasMore = false
      }
    },
    changeTab(tab) {
      if (this.activeTab !== tab) {
        this.activeTab = tab
        this.fetchBooks(true)
      }
    },
    loadMore() {
      if (!this.hasMore) return
      this.page += 1
      this.fetchBooks(false)
    }
  }
}
</script>

<style scoped>
/* ... (스타일은 앞선 답변과 동일, 이미지 참고) ... */
.dashboard-page {
  background: #fff;
  min-height: 100vh;
  font-family: 'Inter', Arial, sans-serif;
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
  background: url('https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
  margin-bottom: 0;
}
.dashboard-main-layout {
  display: flex;
  max-width: 1200px;
  margin: -70px auto 0 auto;
  gap: 2.5rem;
  position: relative;
  z-index: 1;
}
.dashboard-sidebar {
  width: 290px;
  min-width: 230px;
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 2px 18px rgba(0,0,0,0.06);
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
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  overflow: hidden;
  min-height: 160px;
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.11s;
}
.dashboard-book-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  transform: translateY(-4px) scale(1.02);
}
.dashboard-book-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
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
  .dashboard-main-layout { flex-direction: column; gap: 1.5rem; }
  .dashboard-sidebar { width: 100%; min-width: 0; margin-bottom: 1.5rem; }
  .dashboard-main-content { width: 100%; }
  .dashboard-card-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 700px) {
  .dashboard-main-layout { flex-direction: column; gap: 1rem; }
  .dashboard-sidebar { padding: 1.2rem 0.7rem; }
  .dashboard-main-content { padding: 0 0.5rem; }
  .dashboard-card-grid { grid-template-columns: 1fr; }
}
</style>

<!-- 
  Navbar 컴포넌트
  역할: 상단 네비게이션 바
  기능:
    - 로고 및 메인 메뉴
    - 검색 바
    - 로그인/회원가입 또는 사용자 메뉴
  Props:
    - user: Object - 현재 로그인한 사용자 정보 (선택)
-->
<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- 로고 -->
      <router-link to="/" class="logo">
        📚 Book Community
      </router-link>

      <!-- 메인 메뉴 -->
      <div class="main-menu">
        <router-link to="/books" class="menu-item">도서</router-link>
        <router-link to="/community" class="menu-item">커뮤니티</router-link>
        <router-link to="/libraries" class="menu-item">도서관 찾기</router-link>
      </div>

      <!-- 검색 바 -->
      <div class="search-container">
        <input 
          type="text"
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          placeholder="도서 검색..."
          class="search-input"
        >
        <button @click="handleSearch" class="search-button">
          🔍
        </button>
      </div>

      <!-- 사용자 메뉴 -->
      <div class="user-menu">
        <template v-if="user">
          <!-- 로그인 상태 -->
          <div class="user-profile" @click="toggleDropdown">
            <img :src="user.profile_image" :alt="user.username" class="profile-image">
            <span class="username">{{ user.username }}</span>
            
            <!-- 드롭다운 메뉴 -->
            <div v-if="showDropdown" class="dropdown-menu">
              <router-link to="/mypage" class="dropdown-item">마이페이지</router-link>
              <router-link to="/mypage/likes" class="dropdown-item">찜한 도서</router-link>
              <router-link to="/mypage/threads" class="dropdown-item">내가 쓴 글</router-link>
              <a @click="handleLogout" class="dropdown-item">로그아웃</a>
            </div>
          </div>
        </template>
        <template v-else>
          <!-- 비로그인 상태 -->
          <router-link to="/auth/login" class="auth-button login">로그인</router-link>
          <router-link to="/auth/signup" class="auth-button signup">회원가입</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  props: {
    user: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      searchQuery: '',
      showDropdown: false
    }
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({
          path: '/books',
          query: { search: this.searchQuery }
        })
      }
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown
    },
    handleLogout() {
      // TODO: API 연동 시 구현
      // await api.post('/auth/logout')
      // this.$store.commit('clearUser')
      this.$router.push('/auth/login')
    }
  },
  mounted() {
    // 드롭다운 외부 클릭 시 닫기
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.user-profile')) {
        this.showDropdown = false
      }
    })
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleOutsideClick)
  }
}
</script>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}

.main-menu {
  display: flex;
  gap: 2rem;
}

.menu-item {
  text-decoration: none;
  color: #333;
  font-weight: 500;
}

.menu-item:hover {
  color: #0066cc;
}

.search-container {
  display: flex;
  gap: 0.5rem;
  max-width: 300px;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-button {
  padding: 0.5rem 1rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-button {
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.auth-button.login {
  color: #0066cc;
}

.auth-button.signup {
  background: #0066cc;
  color: white;
}

.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.profile-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem 0;
  min-width: 150px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dropdown-item {
  display: block;
  padding: 0.5rem 1rem;
  color: #333;
  text-decoration: none;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

@media (max-width: 768px) {
  .main-menu {
    display: none;
  }
  
  .search-container {
    max-width: none;
  }
}
</style>
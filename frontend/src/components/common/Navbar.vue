<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- 로고 -->
      <router-link to="/" class="logo" aria-label="홈으로 이동">
        📚 Book Community
      </router-link>

      <!-- 메인 메뉴 -->
      <div class="main-menu">
        <router-link to="/books" class="menu-item" aria-label="도서 페이지로 이동">도서</router-link>
        <router-link to="/community" class="menu-item" aria-label="커뮤니티 페이지로 이동">커뮤니티</router-link>
        <router-link to="/libraries" class="menu-item" aria-label="도서관 찾기 페이지로 이동">도서관 찾기</router-link>
      </div>

      <!-- 검색 바 -->
      <div class="search-container">
        <input 
          type="text"
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          placeholder="도서 검색..."
          class="search-input"
          aria-label="도서 검색 입력창"
        >
        <button @click="handleSearch" class="search-button" aria-label="검색 버튼">
          🔍
        </button>
      </div>

      <!-- 사용자 메뉴 -->
      <div class="user-menu">
        <template v-if="isAuthenticated">
          <!-- 로그인 상태 -->
          <div class="user-profile"
               @click="toggleDropdown"
               @keydown.enter="toggleDropdown"
               @keydown.esc="closeDropdown"
               tabindex="0"
               aria-label="사용자 메뉴 열기"
               :aria-expanded="showDropdown">
            <img :src="user?.profile_image || '/default-profile.png'" :alt="user?.username || '프로필'" class="profile-image">
            <span class="username">{{ user?.username }}</span>
            <div v-if="showDropdown" class="dropdown-menu" @keydown.tab="handleTabKey">
              <router-link to="/mypage" class="dropdown-item" aria-label="마이페이지로 이동">마이페이지</router-link>
              <router-link to="/mypage/likes" class="dropdown-item" aria-label="찜한 도서 페이지로 이동">찜한 도서</router-link>
              <router-link to="/mypage/threads" class="dropdown-item" aria-label="내가 쓴 글 페이지로 이동">내가 쓴 글</router-link>
              <a @click="handleLogout" class="dropdown-item" aria-label="로그아웃">로그아웃</a>
            </div>
          </div>
        </template>
        <template v-else>
          <!-- 비로그인 상태 -->
          <router-link to="/auth/login" class="auth-button login" aria-label="로그인 페이지로 이동">로그인</router-link>
          <router-link to="/auth/signup" class="auth-button signup" aria-label="회원가입 페이지로 이동">회원가입</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { user, isAuthenticated } = storeToRefs(authStore)
const router = useRouter()

const searchQuery = ref('')
const showDropdown = ref(false)

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/books',
      query: { search: searchQuery.value }
    })
  }
}

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) {
    nextTick(() => {
      const firstItem = document.querySelector('.dropdown-item')
      if (firstItem) firstItem.focus()
    })
  }
}

function closeDropdown() {
  showDropdown.value = false
}

function handleTabKey(event) {
  const focusableItems = document.querySelectorAll('.dropdown-item')
  const firstItem = focusableItems[0]
  const lastItem = focusableItems[focusableItems.length - 1]
  if (event.shiftKey && document.activeElement === firstItem) {
    event.preventDefault()
    lastItem.focus()
  } else if (!event.shiftKey && document.activeElement === lastItem) {
    event.preventDefault()
    firstItem.focus()
  }
}

function handleLogout() {
  authStore.logout()
  showDropdown.value = false
  // 라우터 이동은 store에서 처리하거나, 여기서 처리해도 무방
  // router.push('/auth/login')
}

onMounted(() => {
  authStore.initializeAuth()
})
</script>

<style scoped>
/* 기존 스타일 그대로 사용 */
.navbar {
  background-color: #fff;
  border-bottom: 1px solid #eaeaea;
  padding: 0.5rem 1rem;
}
.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}
.main-menu {
  display: flex;
  gap: 1.5rem;
}
.menu-item {
  position: relative;
  padding: 0.5rem 1rem;
  color: #333;
  text-decoration: none;
  border-radius: 0.25rem;
  transition: background-color 0.3s;
}
.menu-item:hover,
.menu-item:focus {
  background-color: #f0f0f0;
}
.search-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.search-input {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  width: 250px;
}
.search-button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background-color 0.3s;
}
.search-button:hover {
  background-color: #0056b3;
}
.user-menu {
  position: relative;
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}
.profile-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}
.username {
  font-weight: 500;
  color: #333;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #fff;
  border: 1px solid #eaeaea;
  border-radius: 0.25rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
.dropdown-item {
  display: block;
  padding: 0.5rem 1rem;
  color: #333;
  text-decoration: none;
  transition: background-color 0.3s;
}
.dropdown-item:hover,
.dropdown-item:focus {
  background-color: #f0f0f0;
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
</style>

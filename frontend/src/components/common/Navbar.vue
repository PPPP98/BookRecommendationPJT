<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- 로고 -->
      <router-link to="/" class="logo" aria-label="홈으로 이동">
         Book Framework
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
          @input="onInput"
          @keyup.enter="handleSearch"
          placeholder="도서 검색..."
          class="search-input"
          aria-label="도서 검색 입력창"
          autocomplete="off"
        >
        <button
  @click="handleSearch"
  class="search-button search-icon-btn"
  aria-label="검색 버튼"
  type="button"
>
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
    <rect width="20" height="20" rx="6" fill="black"/>
    <circle cx="9" cy="9" r="5" stroke="white" stroke-width="2" fill="none"/>
    <rect x="13" y="13" width="2" height="6" rx="1" transform="rotate(45 13 13)" fill="white"/>
  </svg>
</button>

        <ul v-if="suggestions.length" class="suggestions-list">
          <li
            v-for="item in suggestions"
            :key="item.text + item.type"
            @mousedown.prevent="selectSuggestion(item)"
          >
            <span class="label">{{ item.type === 'title' ? '제목' : '저자' }} :</span>
            <span class="highlighted-text" v-html="highlightMatch(item.text, searchQuery)" />
          </li>
        </ul>
      </div>
      <!-- 사용자 메뉴 -->
      <div class="user-menu">
        <template v-if="isAuthenticated">
          <div
            class="user-profile"
            @click="toggleDropdown"
            @keydown.enter="toggleDropdown"
            @keydown.esc="closeDropdown"
            tabindex="0"
            aria-label="사용자 메뉴 열기"
            :aria-expanded="showDropdown"
          >
            <img
              :src="user?.profile_image || defaultProfile"
              :alt="user?.nickname || '프로필'"
              class="profile-image"
              @error="onImgError"
            >
            <span class="username">{{ user?.nickname }}</span>
            <div v-if="showDropdown" class="dropdown-menu" @keydown.tab="handleTabKey">
              <router-link to="/mypage" class="dropdown-item" aria-label="마이페이지로 이동">마이페이지</router-link>
              <router-link to="/mypage/likes" class="dropdown-item" aria-label="찜한 도서 페이지로 이동">찜한 도서</router-link>
              <router-link to="/mypage/threads" class="dropdown-item" aria-label="내가 쓴 글 페이지로 이동">내가 쓴 글</router-link>
              <a @click="handleLogout" class="dropdown-item" aria-label="로그아웃">로그아웃</a>
            </div>
          </div>
        </template>
        <template v-else>
          <router-link to="/auth/login" class="auth-button login" aria-label="로그인 페이지로 이동">로그인</router-link>
          <router-link to="/auth/signup" class="auth-button signup" aria-label="회원가입 페이지로 이동">회원가입</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import axios from 'axios'

const authStore = useAuthStore()
const { user, isAuthenticated } = storeToRefs(authStore)
const router = useRouter()

const searchQuery = ref('')
const showDropdown = ref(false)
const suggestions = ref([])
const defaultProfile = 'https://cdn-icons-png.flaticon.com/512/149/149071.png'
let timer = null

function onInput() {
  clearTimeout(timer)
  if (!searchQuery.value.trim()) {
    suggestions.value = []
    return
  }
  timer = setTimeout(fetchSuggestions, 200)
}

function reorderSuggestions(list, query) {
  if (!query) return list
  const q = query.trim().toLowerCase()
  const exact = list.filter(item => item.text.toLowerCase() === q)
  const rest = list.filter(item => item.text.toLowerCase() !== q)
  return [...exact, ...rest]
}

async function fetchSuggestions() {
  try {
    const resp = await axios.get('/api/books/search/suggestions/', {
      params: { q: searchQuery.value }
    })
    suggestions.value = reorderSuggestions(resp.data, searchQuery.value)
  } catch (e) {
    suggestions.value = []
  }
}

function selectSuggestion(item) {
  searchQuery.value = item.text
  suggestions.value = []
  handleSearch()
}

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/books',
      query: { q: searchQuery.value }
    })
    suggestions.value = []
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
}

function onImgError(e) {
  if (e.target.src !== defaultProfile) {
    e.target.src = defaultProfile
  }
}

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}
function escapeHtml(str) {
  return str.replace(/[&<>"']/g, function(m) {
    return ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[m]
  })
}
function highlightMatch(text, query) {
  if (!query) return escapeHtml(text)
  const re = new RegExp(`(${escapeRegExp(query)})`, 'gi')
  return escapeHtml(text).replace(re, '<span class="blue">$1</span>')
}

onMounted(() => {
  authStore.initializeAuth()
})
</script>

<style scoped>
.navbar {
  height: var(--navbar-height);
  width: 100%;
  background: white;
}

.navbar-container {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1976d2;
  letter-spacing: -1px;
  text-decoration: none;
  margin-right: 2vw;
}
.main-menu {
  display: flex;
  gap: 1.5rem;
}
.menu-item {
  padding: 0.45rem 1.1rem;
  color: #222;
  text-decoration: none;
  border-radius: 7px;
  font-weight: 500;
  transition: background 0.18s, color 0.18s;
}
.menu-item:hover,
.menu-item:focus {
  background: #e3f2fd;
  color: #1976d2;
}
.search-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}
.search-input {
  padding: 0.5rem 1rem;
  border: 1.5px solid #d0d7de;
  border-radius: 8px;
  width: 220px;
  font-size: 1rem;
  background: #fafbfc;
  transition: border 0.18s;
}
.search-input:focus {
  border-color: #1976d2;
  outline: none;
}

.search-button {
  padding: 0.5rem 1rem;
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.18s;
}
.search-button:hover {
  background: #145a9e;
}
.suggestions-list {
  position: absolute;
  left: 0; right: 0; top: 100%;
  background: #fff;
  border: 1.5px solid #d0d7de;
  z-index: 100;
  max-height: 220px;
  overflow-y: auto;
  margin: 0; padding: 0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.suggestions-list li {
  padding: 0.55rem 1rem;
  cursor: pointer;
  display: flex;
  gap: 0.5rem;
  color: #444;
  font-size: 1rem;
  transition: background 0.15s;
}
.suggestions-list li:hover {
  background: #f2f7fd;
}
.label {
  font-weight: 500;
  margin-right: 0.5em;
  color: #888;
}
.blue {
  color: #1976d2;
  font-weight: bold;
}
.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  border-radius: 8px;
  padding: 0.3rem 0.8rem;
  transition: background 0.18s;
}
.user-profile:hover,
.user-profile:focus-within {
  background: #f2f7fd;
}
.profile-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background: #e0e0e0;
}
.username {
  font-weight: 600;
  color: #222;
  font-size: 1rem;
}
.dropdown-menu {
  position: absolute;
  top: 110%;
  right: 0;
  background: #fff;
  border: 1.5px solid #ececec;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  z-index: 1000;
  min-width: 170px;
}
.dropdown-item {
  display: block;
  padding: 0.7rem 1.1rem;
  color: #222;
  text-decoration: none;
  font-size: 1rem;
  border-radius: 8px;
  transition: background 0.18s, color 0.18s;
}
.dropdown-item:hover,
.dropdown-item:focus {
  background: #f2f7fd;
  color: #1976d2;
}
.auth-button {
  text-decoration: none;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  transition: background 0.18s, color 0.18s;
}
.auth-button.login {
  color: #1976d2;
  background: none;
}
.auth-button.signup {
  background: #1976d2;
  color: white;
  margin-left: 0.5rem;
}
.auth-button.signup:hover {
  background: #145a9e;
}
@media (max-width: 900px) {
  .navbar-container {
    flex-wrap: wrap;
    gap: 0.7rem;
  }
  .main-menu {
    gap: 1rem;
  }
  .search-input {
    width: 120px;
    font-size: 0.95rem;
  }
}
@media (max-width: 600px) {
  .navbar-container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
    padding: 0 0.5rem;
  }
  .main-menu {
    justify-content: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .search-container {
    width: 100%;
    margin-bottom: 0.5rem;
  }
  .user-menu {
    justify-content: flex-end;
    margin-top: 0.3rem;
  }
}
.navbar {
  background: #fff;
  border-bottom: 1.5px solid #ececec;
  padding: 0.7rem 0;
  font-size: 1.07rem;
  box-shadow: 0 2px 8px rgba(24,24,24,0.03);
}
.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  gap: 1.5rem;
}
.logo {
  font-size: 1.35rem;
  font-weight: 800;
  color: #181818;
  letter-spacing: -1px;
  text-decoration: none;
  margin-right: 2vw;
  font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
  transition: color 0.18s;
}
.logo:hover,
.logo:focus {
  color: #111;
}
.main-menu {
  display: flex;
  gap: 1.5rem;
}
.menu-item {
  padding: 0.45rem 1.1rem;
  color: #232323;
  background: none;
  text-decoration: none;
  border-radius: 7px;
  font-weight: 500;
  transition: background 0.18s, color 0.18s;
}
.menu-item:hover,
.menu-item:focus {
  background: #232323;
  color: #fff;
}
.search-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}
.search-input {
  padding: 0.5rem 1rem;
  border: 1.5px solid #c0c0c0;
  border-radius: 8px;
  width: 220px;
  font-size: 1rem;
  background: #f5f5f5;
  color: #232323;
  transition: border 0.18s, background 0.18s;
}
.search-input:focus {
  border-color: #181818;
  background: #fff;
  outline: none;
}
.search-button {
  padding: 0.5rem 1rem;
  background: #090909;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.18s;
}
.search-button:hover {
  background: #111;
}
.suggestions-list {
  position: absolute;
  left: 0; right: 0; top: 100%;
  background: #fff;
  border: 1.5px solid #ececec;
  z-index: 100;
  max-height: 220px;
  overflow-y: auto;
  margin: 0; padding: 0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(24,24,24,0.08);
}
.suggestions-list li {
  padding: 0.55rem 1rem;
  cursor: pointer;
  display: flex;
  gap: 0.5rem;
  color: #444;
  font-size: 1rem;
  transition: background 0.15s, color 0.15s;
}
.suggestions-list li:hover {
  background: #f5f5f5;
  color: #181818;
}
.label {
  font-weight: 500;
  margin-right: 0.5em;
  color: #888;
}
.blue {
  color: #232323;
  font-weight: bold;
}
.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  border-radius: 8px;
  padding: 0.3rem 0.8rem;
  transition: background 0.18s;
  background: none;
}
.user-profile:hover,
.user-profile:focus-within {
  background: #f5f5f5;
}
.profile-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background: #e0e0e0;
}
.username {
  font-weight: 600;
  color: #181818;
  font-size: 1rem;
}
.dropdown-menu {
  position: absolute;
  top: 110%;
  right: 0;
  background: #fff;
  border: 1.5px solid #ececec;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(24,24,24,0.08);
  z-index: 1000;
  min-width: 170px;
}
.dropdown-item {
  display: block;
  padding: 0.7rem 1.1rem;
  color: #232323;
  text-decoration: none;
  font-size: 1rem;
  border-radius: 8px;
  background: none;
  transition: background 0.18s, color 0.18s;
}
.dropdown-item:hover,
.dropdown-item:focus {
  background: #232323;
  color: #fff;
}
.auth-button {
  text-decoration: none;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  transition: background 0.18s, color 0.18s;
  background: none;
  color: #232323;
  border: 1.5px solid #232323;
  margin-left: 0.5rem;
}
.auth-button.login {
  background: #fff;
}
.auth-button.signup {
  background: #232323;
  color: #fff;
  border: 1.5px solid #232323;
}
.auth-button.signup:hover {
  background: #111;
  color: #fff;
}
.auth-button.login:hover {
  background: #f5f5f5;
  color: #181818;
}
@media (max-width: 900px) {
  .navbar-container {
    flex-wrap: wrap;
    gap: 0.7rem;
  }
  .main-menu {
    gap: 1rem;
  }
  .search-input {
    width: 120px;
    font-size: 0.95rem;
  }
}
@media (max-width: 600px) {
  .navbar-container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
    padding: 0 0.5rem;
  }
  .main-menu {
    justify-content: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .search-container {
    width: 100%;
    margin-bottom: 0.5rem;
  }
  .user-menu {
    justify-content: flex-end;
    margin-top: 0.3rem;
  }
}

</style>

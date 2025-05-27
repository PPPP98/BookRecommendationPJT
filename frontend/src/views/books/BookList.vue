<template>
  <div class="book-list-page">
    <Navbar />
    <main class="main-content">
      <div class="profile-section">
        <img
          class="profile-image"
          :src="userProfileImage"
          :alt="username ? username + '의 프로필' : '프로필'"
          @error="onImgError"
        />
        <div class="profile-info">
          <h2>{{ username ? username + '님' : '게스트' }}</h2>
          <p>당신이 좋아할 만한 도서를 AI가 추천해드릴 것입니다.</p>
        </div>
      </div>

      <!-- 필터 및 정렬 섹션 -->
      <div class="filter-section">
        <div class="category-buttons">
          <template v-if="!searchQuery">
            <button 
              class="category-button" 
              :class="{ active: selectedCategory === '' }"
              @click="selectedCategory = ''"
              :disabled="loading"
            >
              전체
            </button>
            <button 
              v-for="category in categories" 
              :key="category.id"
              class="category-button"
              :class="{ active: selectedCategory === category.name }"
              @click="selectedCategory = category.name"
              :disabled="loading"
            >
              {{ category.name }}
            </button>
          </template>
          <template v-else>
            <span class="search-result-label">검색결과</span>
          </template>
        </div>
        <select v-model="sortBy" class="filter-select" :disabled="loading">
          <option value="pub_date">최신순</option>
          <option value="-like_count">좋아요순</option>
          <option value="-thread_count">쓰레드순</option>
        </select>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="loading" class="loading-spinner">
        <div class="spinner"></div>
      </div>
      <!-- 에러 메시지 -->
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>
      <!-- 도서 그리드 -->
      <div v-else class="books-grid">
        <BookCard
          v-for="book in books"
          :key="book.id"
          :book="book"
          :like-count="book.like_count"
          :comment-count="book.thread_count"
          @click="navigateToDetail(book.id)"
        />
      </div>
      <!-- 페이지네이션 -->
      <div class="pagination" v-if="!loading && !error && totalPages > 1">
        <button 
          class="pagination-button" 
          :disabled="currentPage === 1"
          @click="handlePageChange(currentPage - 1)"
        >
          이전
        </button>
        <span class="pagination-info">
          {{ currentPage }} / {{ totalPages }}
        </span>
        <button 
          class="pagination-button"
          :disabled="currentPage === totalPages"
          @click="handlePageChange(currentPage + 1)"
        >
          다음
        </button>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import BookCard from '@/components/books/BookCard.vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const CDN_PROFILE = 'https://cdn-icons-png.flaticon.com/512/149/149071.png'
const BACKEND_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default {
  name: 'BookList',
  components: {
    Navbar,
    Footer,
    BookCard
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const books = ref([])
    const categories = ref([])
    const loading = ref(false)
    const error = ref(null)
    const totalBooks = ref(0)
    const currentPage = ref(1)
    const itemsPerPage = ref(25)
    const selectedCategory = ref('')
    const sortBy = ref('pub_date')
    const searchQuery = ref(route.query.q || '')

    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const username = computed(() =>
      user.value?.nickname ||
      user.value?.username ||
      user.value?.email ||
      ''
    )

    const userProfileImage = computed(() => {
      const img = user.value?.profile_image
      if (!img) return CDN_PROFILE
      if (img.startsWith('http')) return img
      return `${BACKEND_URL}${img}`
    })
    function onImgError(e) {
      if (e.target.src !== CDN_PROFILE) {
        e.target.src = CDN_PROFILE
      }
    }

    const totalPages = computed(() => Math.ceil(totalBooks.value / itemsPerPage.value))

    const fetchBooks = async () => {
      loading.value = true
      error.value = null
      try {
        const params = {
          page: currentPage.value,
          page_size: itemsPerPage.value,
          ordering: sortBy.value
        }
        if (selectedCategory.value !== '') {
          params.category = selectedCategory.value
        }
        let url = '/api/books/'
        if (searchQuery.value && searchQuery.value.trim()) {
          url = '/api/books/search/'
          params.q = searchQuery.value.trim()
        }
        const response = await axios.get(url, { params })
        books.value = response.data.results
        totalBooks.value = response.data.count
      } catch (err) {
        error.value = '도서 목록을 불러오는데 실패했습니다.'
        console.error('Error fetching books:', err)
      } finally {
        loading.value = false
      }
    }

    const fetchCategories = async () => {
      try {
        const response = await axios.get('/api/books/categories/')
        if (response.data && response.data.categories) {
          categories.value = response.data.categories
        } else {
          error.value = '카테고리 데이터를 불러오는데 실패했습니다.'
        }
      } catch (err) {
        console.error('Error fetching categories:', err)
        error.value = '카테고리 목록을 불러오는데 실패했습니다.'
      }
    }

    const handlePageChange = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
      }
    }

    const navigateToDetail = (bookId) => {
      router.push(`/books/${bookId}`)
    }

    watch([selectedCategory, sortBy], () => {
      currentPage.value = 1
      fetchBooks()
    })

    watch(currentPage, fetchBooks)

    watch(
      () => route.query.q,
      (newQ) => {
        searchQuery.value = newQ || ''
        currentPage.value = 1
        fetchBooks()
      }
    )

    watch([selectedCategory, sortBy, currentPage], () => {
      searchQuery.value = route.query.q || ''
    })

    onMounted(() => {
      fetchCategories()
      fetchBooks()
    })

    return {
      books,
      categories,
      loading,
      error,
      totalBooks,
      totalPages,
      currentPage,
      itemsPerPage,
      selectedCategory,
      sortBy,
      handlePageChange,
      navigateToDetail,
      username,
      searchQuery,
      user,
      userProfileImage,
      onImgError
    }
  }
}
</script>

<style scoped>
.book-list-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-section {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 1rem;
  background-color: #e9ecef;
  object-fit: cover;
}

.profile-info h2 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.profile-info p {
  color: #666;
  font-size: 0.9rem;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 2rem;
}

.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  flex: 1;
}

.category-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: white;
  color: #666;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}
.category-button:hover:not(:disabled) {
  background: #f0f0f0;
  border-color: #ccc;
}
.category-button.active {
  background: #0066cc;
  color: white;
  border-color: #0066cc;
}
.category-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.search-result-label {
  font-size: 1rem;
  font-weight: 600;
  color: #1976d2;
  padding: 0.5rem 1.2rem;
  background: #f3f7fa;
  border-radius: 20px;
  margin-right: 1rem;
  letter-spacing: 0.02em;
}
.filter-select {
  padding: 0.3rem 0.8rem;
  height: 32px;
  border: 1px solid #ddd;
  border-radius: 16px;
  background: white;
  font-size: 0.9rem;
  color: #666;
  cursor: pointer;
  min-width: 100px;
  max-width: 150px;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 1em;
  padding-right: 2rem;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin: 2rem 0;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  text-align: center;
  color: #dc3545;
  padding: 2rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
}

.pagination-button:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.9rem;
  color: #666;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1200px) {
  .main-content {
    padding: 1.5rem;
  }
  .books-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .profile-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .profile-image {
    width: 80px;
    height: 80px;
  }
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .profile-image {
    width: 60px;
    height: 60px;
  }
  .books-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}
</style>

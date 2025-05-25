<template>
  <div class="book-list-page">
    <Navbar />
    <main class="main-content">
      <div class="profile-section">
        <div class="profile-image"></div>
        <div class="profile-info">
          <h2><사용자명 추가할것></h2>
          <p>당신이 좋아할 만한 도서를 AI가 추천해드릴 것입니다.</p>
        </div>
      </div>

      <!-- 필터 및 정렬 섹션 -->
      <div class="filter-section">
        <div class="category-buttons">
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
            :class="{ active: selectedCategory === category.id }"
            @click="selectedCategory = category.id"
            :disabled="loading"
          >
            {{ category.name }}
          </button>
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
    // 검색창 제거, 대신 쿼리스트링 q만 사용
    const searchQuery = ref(route.query.q || '')

    const totalPages = computed(() => Math.ceil(totalBooks.value / itemsPerPage.value))

    // 도서 목록 조회
    const fetchBooks = async () => {
      loading.value = true
      error.value = null
      try {
        const params = {
          page: currentPage.value,
          page_size: itemsPerPage.value,
          ordering: sortBy.value
        }
        // 카테고리 필터
        if (selectedCategory.value !== '') {
          const selectedCategoryObj = categories.value.find(cat => cat.id === selectedCategory.value)
          if (selectedCategoryObj) {
            params.category = selectedCategoryObj.name
          }
        }
        // 검색어 연동 (Navbar에서 /books?q=검색어로 이동 시)
        if (searchQuery.value && searchQuery.value.trim()) {
          params.q = searchQuery.value.trim()
        }
        const response = await axios.get('/api/books/search/', { params })
        books.value = response.data.results
        totalBooks.value = response.data.count
      } catch (err) {
        error.value = '도서 목록을 불러오는데 실패했습니다.'
        console.error('Error fetching books:', err)
      } finally {
        loading.value = false
      }
    }

    // 카테고리 목록 조회
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

    // 페이지 변경 핸들러
    const handlePageChange = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
      }
    }

    // 상세 페이지 이동
    const navigateToDetail = (bookId) => {
      router.push(`/books/${bookId}`)
    }

    // 필터/정렬 변경시 첫 페이지로 이동 후 도서 목록 새로고침
    watch([selectedCategory, sortBy], () => {
      currentPage.value = 1
      fetchBooks()
    })

    // 페이지 변경시 도서 목록 새로고침
    watch(currentPage, fetchBooks)

    // 쿼리스트링(q) 변경 시 검색어와 도서 목록 동기화
    watch(
      () => route.query.q,
      (newQ) => {
        searchQuery.value = newQ || ''
        currentPage.value = 1
        fetchBooks()
      }
    )

    // 카테고리/정렬/페이지 변경 시에도 항상 최신 검색어를 반영
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
      navigateToDetail
    }
  }
}
</script>

<style scoped>
/* 기존 스타일 그대로 유지 */
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
  .books-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .books-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .books-grid {
    grid-template-columns: 1fr;
  }
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }
  .filter-select {
    max-width: none;
    width: 100%;
  }
}
</style>

<!-- 
  BookList 페이지
  역할: 도서 목록을 표시하고 필터링, 검색, 정렬 기능을 제공
  기능:
    - 도서 목록 표시 (그리드 형태)
    - 카테고리별 필터링
    - 검색
    - 정렬 (평점순, 최신순 등)
    - 무한스크롤/페이지네이션
  데이터 구조:
    - books: Array<{
        id: number,
        title: string,
        author: string,
        cover_image: string,
        rating: number,
        category: string
      }>
-->
<template>
  <div class="book-list-page">
    <Navbar />
    
    <main class="main-content">
      <div class="profile-section">
        <img src="@/assets/profile.png" alt="Profile" class="profile-image">
        <div class="profile-info">
          <h2>park heejae</h2>
          <p>당신이 좋아할 만한 도서를 AI가 추천해드릴 것입니다.</p>
        </div>
      </div>

      <!-- 필터 및 정렬 섹션 -->
      <div class="filter-section">
        <select v-model="selectedCategory" class="filter-select" :disabled="loading">
          <option value="">전체 카테고리</option>
          <option v-for="category in categories" 
                  :key="category.id" 
                  :value="category.id">
            {{ category.name }}
          </option>
        </select>

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
      <div class="pagination" v-if="!loading && !error">
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
import { useRouter } from 'vue-router'
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
    const books = ref([])
    const categories = ref([])
    const loading = ref(false)
    const error = ref(null)
    const totalBooks = ref(0)
    const currentPage = ref(1)
    const itemsPerPage = ref(25)
    const selectedCategory = ref('')
    const sortBy = ref('pub_date')

    const totalPages = computed(() => Math.ceil(totalBooks.value / itemsPerPage.value))

    // 도서 목록 조회
    const fetchBooks = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await axios.get('/api/books/', {
          params: {
            page: currentPage.value,
            page_size: itemsPerPage.value,
            category: selectedCategory.value,
            ordering: sortBy.value
          }
        })
        
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

    // 필터 변경시 첫 페이지로 이동 후 도서 목록 새로고침
    watch([selectedCategory, sortBy], () => {
      currentPage.value = 1
      fetchBooks()
    })

    // 페이지 변경시 도서 목록 새로고침
    watch(currentPage, fetchBooks)

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
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
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
  }
}
</style>
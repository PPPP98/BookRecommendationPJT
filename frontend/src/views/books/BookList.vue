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
      <h1>도서 목록</h1>
        <BookFilter
        :categories="categories"
        :selectedCategory="selectedCategory"
        @filter="handleFilterChange"
      />

      <div class="books-grid">
        <BookCard
          v-for="book in displayedBooks"
          :key="book.id"
          :book="book"
          @click="navigateToDetail(book.id)"
        />
      </div>

      <Pagination
        :totalItems="filteredBooks.length"
        :currentPage="currentPage"
        :itemsPerPage="itemsPerPage"
        :infiniteScroll="true"
        @load-more="loadMore"
      />
    </main>

    <Footer />
  </div>
</template>

<script>
import { books } from '@/mocks/books'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import BookFilter from '@/components/books/BookFilter.vue'
import BookCard from '@/components/books/BookCard.vue'
import Pagination from '@/components/common/Pagination.vue'

export default {
  name: 'BookList',
  components: {
    Navbar,
    Footer,
    BookFilter,
    BookCard,
    Pagination
  },
  data() {
    return {
      books: books,
      categories: ['소설', '에세이', '경제/경영', '자기계발'],
      sortOptions: [
        { label: '평점 높은순', value: 'rating-desc' },
        { label: '평점 낮은순', value: 'rating-asc' },
        { label: '최신순', value: 'date-desc' },
        { label: '오래된순', value: 'date-asc' }
      ],
      currentPage: 1,
      itemsPerPage: 12,
      searchQuery: '',
      selectedCategory: '',
      selectedSort: '',
    }
  },
  computed: {
    filteredBooks() {
      let result = [...this.books]

      // 검색어로 필터링
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(book => 
          book.title.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query)
        )
      }

      // 카테고리로 필터링
      if (this.selectedCategory) {
        result = result.filter(book => book.category === this.selectedCategory)
      }

      // 정렬
      if (this.selectedSort) {
        result.sort((a, b) => {
          switch (this.selectedSort) {
            case 'rating-desc':
              return b.rating - a.rating
            case 'rating-asc':
              return a.rating - b.rating
            case 'date-desc':
              return b.id - a.id // 임시로 id를 최신순으로 사용
            case 'date-asc':
              return a.id - b.id
            default:
              return 0
          }
        })
      }

      return result
    },
    displayedBooks() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredBooks.slice(start, end)
    }
  },
  methods: {    // 통합된 필터 처리
    handleFilterChange({ type, value }) {
      switch (type) {
        case 'search':
          this.searchQuery = value;
          break;
        case 'category':
          this.selectedCategory = value;
          break;
        case 'sort':
          this.selectedSort = value;
          break;
      }
      this.currentPage = 1;
    },

    // 무한 스크롤
    loadMore(nextPage) {
      if (nextPage <= Math.ceil(this.filteredBooks.length / this.itemsPerPage)) {
        this.currentPage = nextPage
      }
    },

    // 도서 상세 페이지로 이동
    navigateToDetail(bookId) {
      this.$router.push(`/books/${bookId}`)
    },

    // API 연동을 위한 데이터 fetch 함수
    async fetchBooks() {
      // TODO: API 연동 시 구현
      // try {
      //   const response = await api.get('/books', {
      //     params: {
      //       page: this.currentPage,
      //       category: this.selectedCategory,
      //       search: this.searchQuery,
      //       sort: this.selectedSort
      //     }
      //   })
      //   this.books = response.data
      // } catch (error) {
      //   console.error('Error fetching books:', error)
      // }
    }
  }
}
</script>

<style scoped>
.book-list-page {
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

h1 {
  margin-bottom: 2rem;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

@media (max-width: 768px) {
  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}
</style>
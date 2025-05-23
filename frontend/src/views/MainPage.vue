<!-- 
  MainPage 컴포넌트
  역할: 웹사이트의 메인 랜딩 페이지
  기능:
    - 추천 도서, 베스트셀러, 신작 도서 목록 표시
    - 인기 쓰레드, 팔로우 쓰레드 표시
    - 도서 검색 기능
    - 카테고리 바로가기
  데이터 구조:
    - books: Array - 도서 목록
    - threads: Array - 쓰레드 목록
    - categories: Array - 카테고리 목록
-->
<template>
  <div class="main-page">
    <Navbar />
    
    <main class="main-content">
      <SearchBar 
        @search="handleSearch"
        @filter="handleFilter"
      />

      <CategoryButtons 
        :categories="categories"
        @category-selected="handleCategorySelect"
      />

      <BookSection
        title="추천 도서"
        :books="recommendedBooks"
        type="recommended"
        @book-selected="navigateToBook"
      />

      <BookSection
        title="베스트셀러"
        :books="bestsellerBooks"
        type="bestseller"
        @book-selected="navigateToBook"
      />

      <BookSection
        title="신작 도서"
        :books="newBooks"
        type="new"
        @book-selected="navigateToBook"
      />

      <div class="thread-sections">
        <ThreadSection
          title="인기 쓰레드"
          :threads="popularThreads"
          type="popular"
        />
        <ThreadSection
          title="팔로우 쓰레드"
          :threads="followingThreads"
          type="following"
        />
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import { books } from '@/mocks/books'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import BookSection from '@/components/books/BookSection.vue'
import ThreadSection from '@/components/thread/ThreadSection.vue'
import CategoryButtons from '@/components/common/CategoryButtons.vue'

export default {
  name: 'MainPage',
  components: {
    Navbar,
    Footer,
    SearchBar,
    BookSection,
    ThreadSection,
    CategoryButtons
  },
  data() {
    return {
      categories: [
        { id: 1, name: '소설' },
        { id: 2, name: '에세이' },
        { id: 3, name: '경제/경영' },
        { id: 4, name: '자기계발' }
      ],
      // Mock 데이터로 초기화
      recommendedBooks: books,
      bestsellerBooks: books,
      newBooks: books,
      popularThreads: [
        {
          id: 1,
          title: '이번 달 추천 도서 목록',
          content: '여러분의 추천 도서를 공유해주세요',
          author: '사용자1',
          likes: 15,
          comments: 5
        }
      ],
      followingThreads: [
        {
          id: 2,
          title: '독서 모임 참여자 모집',
          content: '매주 토요일 독서 모임에 참여하실 분을 찾습니다',
          author: '사용자2',
          likes: 10,
          comments: 3
        }
      ]
    }
  },
  methods: {
    handleSearch(query) {
      console.log('Search query:', query)
      // TODO: API 연동 시 검색 기능 구현
    },
    handleFilter(category) {
      console.log('Filter category:', category)
      // TODO: API 연동 시 필터링 기능 구현
    },
    handleCategorySelect(category) {
      console.log('Selected category:', category)
      // TODO: API 연동 시 카테고리 이동 구현
    },
    navigateToBook(bookId) {
      // TODO: 도서 상세 페이지로 이동
      this.$router.push(`/books/${bookId}`)
    }
  }
}
</script>

<style scoped>
.main-page {
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

.thread-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .thread-sections {
    grid-template-columns: 1fr;
  }
}
</style>
<!-- 
  ThreadListPage(Community) 컴포넌트
  역할: 커뮤니티의 쓰레드 목록을 표시하고 필터링, 검색, 정렬 기능을 제공
  기능:
    - 쓰레드 목록 표시
    - 검색 및 필터링
    - 정렬 (최신순, 인기순 등)
    - 무한스크롤
  데이터 구조:
    - threads: Array<{
        id: Number,
        title: String,
        content: String,
        author: Object,
        likes: Number,
        comments: Array,
        ...
      }>
-->
<template>
  <div class="thread-list-page">
    <Navbar />
    
    <main class="main-content">
      <div class="page-header">
        <h1>커뮤니티</h1>
        <button @click="navigateToWrite" class="write-button">
          새 글 작성
        </button>
      </div>

      <ThreadFilter
        @search="handleSearch"
        @sort="handleSort"
        @filter="handleFilter"
      />

      <div class="threads-container">        <ThreadCard
          v-for="thread in displayedThreads"
          :key="thread.id"
          :thread="thread"
          @thread-click="navigateToThread"
        />
      </div>

      <Pagination
        :totalItems="filteredThreads.length"
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
import { threads } from '@/mocks/threads'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import ThreadFilter from '@/components/thread/ThreadFilter.vue'
import ThreadCard from '@/components/thread/ThreadCard.vue'
import Pagination from '@/components/common/Pagination.vue'

export default {
  name: 'Community',
  components: {
    Navbar,
    Footer,
    ThreadFilter,
    ThreadCard,
    Pagination
  },
  data() {
    return {
      threads: threads,
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: '',
      selectedFilter: '',
      selectedSort: ''
    }
  },
  computed: {
    filteredThreads() {
      let result = [...this.threads]

      // 검색어로 필터링
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(thread => 
          thread.title.toLowerCase().includes(query) ||
          thread.content.toLowerCase().includes(query) ||
          thread.author.username.toLowerCase().includes(query)
        )
      }

      // 필터 적용
      if (this.selectedFilter) {
        switch (this.selectedFilter) {
          case 'popular':
            result = result.filter(thread => thread.likes >= 10)
            break
          case 'following':
            // TODO: 실제 팔로우 목록과 비교하여 필터링
            break
          case 'ai':
            // TODO: AI 추천 로직 구현
            break
        }
      }

      // 정렬
      if (this.selectedSort) {
        result.sort((a, b) => {
          switch (this.selectedSort) {
            case 'date-desc':
              return new Date(b.createdAt) - new Date(a.createdAt)
            case 'date-asc':
              return new Date(a.createdAt) - new Date(b.createdAt)
            case 'likes':
              return b.likes - a.likes
            case 'comments':
              return b.comments.length - a.comments.length
            default:
              return 0
          }
        })
      }

      return result
    },
    displayedThreads() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredThreads.slice(start, end)
    }
  },
  methods: {
    handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1
    },
    handleSort(sortType) {
      this.selectedSort = sortType
      this.currentPage = 1
    },
    handleFilter(filterType) {
      this.selectedFilter = filterType
      this.currentPage = 1
    },
    loadMore(nextPage) {
      if (nextPage <= Math.ceil(this.filteredThreads.length / this.itemsPerPage)) {
        this.currentPage = nextPage
      }
    },    navigateToWrite() {
      this.$router.push('/threads/write')
    },
    navigateToThread(threadId) {
      this.$router.push(`/threads/${threadId}`)
    },
    // API 연동을 위한 데이터 fetch 함수
    async fetchThreads() {
      // TODO: API 연동 시 구현
      // try {
      //   const response = await api.get('/threads', {
      //     params: {
      //       page: this.currentPage,
      //       filter: this.selectedFilter,
      //       sort: this.selectedSort,
      //       search: this.searchQuery
      //     }
      //   })
      //   this.threads = response.data
      // } catch (error) {
      //   console.error('Error fetching threads:', error)
      // }
    }
  }
}
</script>

<style scoped>
.thread-list-page {
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.write-button {
  padding: 0.5rem 1rem;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.write-button:hover {
  background-color: #0052a3;
}

.threads-container {
  margin: 2rem 0;
}
</style>
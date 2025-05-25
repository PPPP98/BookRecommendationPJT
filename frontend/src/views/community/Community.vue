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

      <!-- 안내 메시지로 대체 -->
      <div class="info-state">
        현재 전체 쓰레드 목록은 제공되지 않습니다.
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import ThreadFilter from '@/components/thread/ThreadFilter.vue'
import { useAuthStore } from '@/stores/auth'
// import { useThreadsStore } from '@/stores/threads' // 제거

export default {
  name: 'Community',
  components: {
    Navbar,
    Footer,
    ThreadFilter,
    // ThreadCard, // 제거
    // Pagination, // 제거
  },
  setup() {
    const authStore = useAuthStore()
    // const threadsStore = useThreadsStore() // 제거

    return {
      authStore,
      // threadsStore, // 제거
      // threads: threadsStore.threads, // 제거
      // loading: threadsStore.loading, // 제거
      // error: threadsStore.error // 제거
    }
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: '',
      selectedFilter: '',
      selectedSort: ''
    }
  },
  // computed, mounted, methods 등 threads 관련 부분 모두 제거
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
    navigateToWrite() {
      if (!this.authStore.isAuthenticated) {
        this.$router.push('/auth/login')
        return
      }
      this.$router.push('/threads/write')
    }
    // 나머지 threads 관련 메서드 제거
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

.info-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}
</style>

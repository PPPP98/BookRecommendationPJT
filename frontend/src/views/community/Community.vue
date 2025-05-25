<template>
  <div class="thread-list-page">
    <Navbar />

    <main class="main-content">
      <div class="page-header">
        <h1>커뮤니티</h1>
      </div>

      <ThreadFilter
        @search="handleSearch"
        @sort="handleSort"
        @filter="handleFilter"
      />

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

export default {
  name: 'Community',
  components: {
    Navbar,
    Footer,
    ThreadFilter,
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
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 2rem;
}

.info-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}
</style>

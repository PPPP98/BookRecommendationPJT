<!-- 
  Pagination 컴포넌트
  역할: 페이지네이션 또는 무한스크롤 UI를 제공
  Props:
    - totalItems: Number - 전체 아이템 수
    - itemsPerPage: Number - 페이지당 아이템 수
    - currentPage: Number - 현재 페이지
  이벤트:
    - @page-change: 페이지 변경 시 발생
    - @load-more: 무한스크롤에서 추가 로딩 필요 시 발생
-->
<template>
  <div class="pagination" v-if="!infiniteScroll">
    <button 
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
      class="page-btn"
    >
      이전
    </button>
    
    <span class="page-info">
      {{ currentPage }} / {{ totalPages }}
    </span>
    
    <button 
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
      class="page-btn"
    >
      다음
    </button>
  </div>

  <div v-else class="infinite-scroll" ref="infiniteScroll">
    <div v-if="loading" class="loading">
      데이터를 불러오는 중...
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    totalItems: {
      type: Number,
      required: true
    },
    itemsPerPage: {
      type: Number,
      default: 12
    },
    currentPage: {
      type: Number,
      default: 1
    },
    infiniteScroll: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      loading: false,
      observer: null
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    }
  },
  mounted() {
    if (this.infiniteScroll) {
      this.setupInfiniteScroll()
    }
  },
  beforeUnmount() {
    if (this.observer) {
      this.observer.disconnect()
    }
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.$emit('page-change', page)
      }
    },
    setupInfiniteScroll() {
      const options = {
        root: null,
        rootMargin: '20px',
        threshold: 1.0
      }

      this.observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !this.loading) {
            this.loadMore()
          }
        })
      }, options)

      this.observer.observe(this.$refs.infiniteScroll)
    },
    loadMore() {
      if (this.loading || this.currentPage >= this.totalPages) return
      
      this.loading = true
      this.$emit('load-more', this.currentPage + 1)
      this.loading = false
    }
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.page-btn:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.page-info {
  min-width: 100px;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 1rem;
  color: #666;
}
</style>

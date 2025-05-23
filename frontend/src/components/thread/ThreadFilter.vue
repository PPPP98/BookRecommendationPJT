<!-- 
  ThreadFilter 컴포넌트
  역할: 쓰레드 목록의 필터링과 정렬 기능을 제공
  Props:
    - sortOptions: Array - 정렬 옵션 목록
    - filterOptions: Array - 필터 옵션 목록
  이벤트:
    - @search: 검색어 입력 시 발생
    - @sort: 정렬 옵션 변경 시 발생
    - @filter: 필터 옵션 변경 시 발생
-->
<template>
  <div class="thread-filter">
    <div class="search-section">
      <input 
        type="text" 
        v-model="searchQuery"
        @input="handleSearch"
        placeholder="제목, 내용, 작성자로 검색"
        class="search-input"
      />
    </div>

    <div class="filter-section">
      <select v-model="selectedFilter" @change="handleFilter" class="filter-select">
        <option value="">모든 글</option>
        <option v-for="filter in filterOptions" :key="filter.value" :value="filter.value">
          {{ filter.label }}
        </option>
      </select>

      <select v-model="selectedSort" @change="handleSort" class="sort-select">
        <option value="">정렬 방식</option>
        <option v-for="sort in sortOptions" :key="sort.value" :value="sort.value">
          {{ sort.label }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ThreadFilter',
  props: {
    filterOptions: {
      type: Array,
      default: () => [
        { label: '인기 글', value: 'popular' },
        { label: '팔로우 중', value: 'following' },
        { label: 'AI 추천', value: 'ai' }
      ]
    },
    sortOptions: {
      type: Array,
      default: () => [
        { label: '최신순', value: 'date-desc' },
        { label: '오래된순', value: 'date-asc' },
        { label: '좋아요순', value: 'likes' },
        { label: '댓글순', value: 'comments' }
      ]
    }
  },
  data() {
    return {
      searchQuery: '',
      selectedSort: '',
      selectedFilter: ''
    }
  },
  methods: {
    handleSearch() {
      this.$emit('search', this.searchQuery)
    },
    handleSort() {
      this.$emit('sort', this.selectedSort)
    },
    handleFilter() {
      this.$emit('filter', this.selectedFilter)
    }
  }
}
</script>

<style scoped>
.thread-filter {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.search-section {
  margin-bottom: 1rem;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-section {
  display: flex;
  gap: 1rem;
}

.filter-select, .sort-select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>

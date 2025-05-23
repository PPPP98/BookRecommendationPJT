<!-- 
  SearchBar 컴포넌트
  역할: 도서 검색을 위한 입력창 컴포넌트
  이벤트:
    - @search: 검색어가 입력되었을 때 발생하는 이벤트
    - @filter: 필터(카테고리 등)가 변경되었을 때 발생하는 이벤트
-->
<template>
  <div class="search-container">
    <input 
      type="text" 
      v-model="searchQuery"
      @input="handleSearch"
      placeholder="도서명, 저자, 키워드로 검색하세요"
      class="search-input"
    />
    <select v-model="selectedCategory" @change="handleFilter" class="category-select">
      <option value="">전체 카테고리</option>
      <option v-for="category in categories" :key="category" :value="category">
        {{ category }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      categories: ['소설', '에세이', '경제/경영', '자기계발']
    }
  },
  methods: {
    handleSearch() {
      this.$emit('search', this.searchQuery)
    },
    handleFilter() {
      this.$emit('filter', this.selectedCategory)
    }
  }
}
</script>

<style scoped>
.search-container {
  display: flex;
  gap: 1rem;
  padding: 1rem;
}

.search-input {
  flex: 1;
  padding: 0.5rem;
}

.category-select {
  padding: 0.5rem;
}
</style>

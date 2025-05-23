<!-- 
  BookFilter 컴포넌트
  역할: 도서 목록의 필터링 UI
  Props:
    - categories: Array<string> - 카테고리 목록
    - selectedCategory: string - 현재 선택된 카테고리
  Events:
    - @filter: 필터 변경 시 발생 (category, sort, search)
-->
<template>
  <div class="book-filter">
    <!-- 검색 영역 -->
    <div class="search-area">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="도서명 또는 저자를 입력하세요"
        @input="handleSearch"
      />
    </div>

    <!-- 필터 영역 -->
    <div class="filter-area">
      <!-- 카테고리 필터 -->
      <select v-model="selectedCategoryLocal" @change="handleCategoryChange">
        <option value="">전체 카테고리</option>
        <option 
          v-for="category in categories" 
          :key="category" 
          :value="category"
        >
          {{ category }}
        </option>
      </select>

      <!-- 정렬 옵션 -->
      <select v-model="sortBy" @change="handleSort">
        <option value="">정렬 방식</option>
        <option value="rating-desc">평점 높은순</option>
        <option value="rating-asc">평점 낮은순</option>
        <option value="title-asc">제목순</option>
        <option value="newest">최신순</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookFilter',
  props: {
    categories: {
      type: Array,
      required: true
    },
    selectedCategory: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      searchQuery: '',
      selectedCategoryLocal: this.selectedCategory,
      sortBy: ''
    }
  },
  watch: {
    selectedCategory(newValue) {
      this.selectedCategoryLocal = newValue
    }
  },
  methods: {
    handleSearch() {
      this.$emit('filter', {
        type: 'search',
        value: this.searchQuery
      })
    },
    handleCategoryChange() {
      this.$emit('filter', {
        type: 'category',
        value: this.selectedCategoryLocal
      })
    },
    handleSort() {
      this.$emit('filter', {
        type: 'sort',
        value: this.sortBy
      })
    }
  }
}
</script>

<style scoped>
.book-filter {
  margin: 1rem 0;
}

.search-area {
  margin-bottom: 1rem;
}

.filter-area {
  display: flex;
  gap: 1rem;
}

select {
  padding: 0.5rem;
}

input {
  padding: 0.5rem;
  width: 100%;
}
</style>

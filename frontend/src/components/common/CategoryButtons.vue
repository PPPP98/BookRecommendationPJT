<!-- 
  CategoryButtons 컴포넌트
  역할: 카테고리 바로가기 버튼 목록을 표시
  Props:
    - categories: Array - 카테고리 목록
  이벤트:
    - @category-selected: 카테고리가 선택되었을 때 발생
-->
<template>
  <div class="category-buttons">
    <button 
      v-for="category in categories" 
      :key="category.id"
      @click="selectCategory(category)"
      class="category-button"
    >
      {{ category.name }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'CategoryButtons',
  props: {
    categories: {
      type: Array,
      required: true
    }
  },
  methods: {
    selectCategory(category) {
      this.$emit('category-selected', category)
    }
  }
}
</script>

<style scoped>
.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem 0;
}

.category-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
}

.category-button:hover {
  background: #f5f5f5;
}
</style>

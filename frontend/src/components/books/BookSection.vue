<!-- 
  BookSection 컴포넌트
  역할: 도서 목록을 섹션 단위로 표시 (추천/베스트셀러/신작)
  Props:
    - title: String - 섹션 제목
    - books: Array - 도서 목록
    - type: String - 섹션 타입 ('recommended', 'bestseller', 'new')
-->
<template>
  <section class="book-section">
    <h2>{{ title }}</h2>
    <div class="books-container">      <BookCard
        v-for="book in books"
        :key="book.id"
        :book="book"
        @click="handleBookClick(book.id)"
      />
    </div>
  </section>
</template>

<script>
import BookCard from './BookCard.vue'

export default {
  name: 'BookSection',
  components: {
    BookCard
  },
  props: {
    title: {
      type: String,
      required: true
    },
    books: {
      type: Array,
      required: true
    },
    type: {
      type: String,
      required: true,
      validator: value => ['recommended', 'bestseller', 'new'].includes(value)
    }
  },
  methods: {
    handleBookClick(bookId) {
      this.$emit('book-selected', bookId)
    }
  }
}
</script>

<style scoped>
.book-section {
  margin: 2rem 0;
}

.books-container {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 1rem 0;
}
</style>

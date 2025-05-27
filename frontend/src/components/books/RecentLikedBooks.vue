<template>
  <div class="recent-liked-books-section">
    <div class="recent-liked-books-header">
      <h3>최근 찜한 도서</h3>
      <button class="summary-link" @click="$emit('more')">더보기</button>
    </div>
    <div class="books-container small horizontal-scroll">
      <BookCard
        v-for="book in books"
        :key="book.id"
        :book="book"
        @click="$emit('book-click', book.id)"
      />
    </div>
    <div v-if="!books || books.length === 0" class="empty-state">
      찜한 도서가 없습니다.
    </div>
  </div>
</template>
<script>
import BookCard from './BookCard.vue'
export default {
  props: { books: Array },
  components: { BookCard }
}
</script>

<template>
  <div class="book-like-list">
    <div class="books-container">
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
  props: { books: Array }
}
</script>

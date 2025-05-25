<template>
  <div class="book-like-list">
    <h2>찜한 도서</h2>
    <div class="books-container">
      <div
        v-for="book in books || []"
        :key="book.id"
        class="book-item"
      >
        <BookCard :book="book">
          <template #actions>
            <button
              v-if="editable"
              @click.stop="unlikeBook(book.id)"
              class="unlike-button"
            >
              찜 해제
            </button>
          </template>
        </BookCard>
      </div>
    </div>
    
    <div v-if="!books || books.length === 0" class="empty-state">
      찜한 도서가 없습니다.
    </div>
  </div>
</template>

<script>
import BookCard from './BookCard.vue'

export default {
  name: 'BookLikeList',
  components: {
    BookCard
  },
  props: {
    books: {
      type: Array,
      required: true,
      default: () => []
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    unlikeBook(bookId) {
      this.$emit('unlike', bookId)
    }
  }
}
</script>

<style scoped>
.book-like-list {
  margin: 2rem 0;
}

.books-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.book-item {
  position: relative;
}

.unlike-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: rgba(220, 53, 69, 0.9);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>

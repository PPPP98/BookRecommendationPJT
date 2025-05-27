<template>
  <div class="book-card">
    <div class="book-cover">
      <img :src="book.cover" :alt="book.title" />
    </div>

  </div>
</template>

<script setup>
defineProps({
  book: {
    type: Object,
    required: true,
    validator: (book) => {
      return book.id && book.title && book.author && book.cover;
    }
  }
})
</script>

<style scoped>
.book-card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  width: 150px;
  height: 210px; /* 1:1.4 비율 */
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.book-cover {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>

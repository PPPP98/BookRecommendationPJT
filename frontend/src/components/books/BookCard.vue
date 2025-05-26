<template>
  <div class="book-card" @click="$emit('click')">
    <div class="book-cover">
      <img 
        :src="book.cover_image || book.cover || defaultCover"
        :alt="book.title || '도서 이미지'"
        class="cover-image"
        @error="onImgError"
      >
    </div>
    <div class="book-info">
      <h3 class="title">{{ book.title || '제목 없음' }}</h3>
      <p class="author">{{ book.author || '저자 정보 없음' }}</p>
      <div class="metadata">
        <span class="category">{{ book.category_name || book.category || '카테고리 없음' }}</span>
        <div class="stats">
          <span class="likes">
            <i class="fas fa-heart"></i> {{ likeCount || 0 }}
          </span>
          <span class="comments">
            <i class="fas fa-comments"></i> {{ commentCount || 0 }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookCard',
  props: {
    book: {
      type: Object,
      required: true,
      validator(value) {
        // title만 필수, 나머지는 안전하게 처리
        return value && typeof value.title === 'string'
      }
    },
    likeCount: {
      type: Number,
      default: 0
    },
    commentCount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      defaultCover: 'https://cdn-icons-png.flaticon.com/512/29/29302.png'
    }
  },
  methods: {
    onImgError(e) {
      if (e.target.src !== this.defaultCover) {
        e.target.src = this.defaultCover
      }
    }
  }
}
</script>

<style scoped>
.book-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
  cursor: pointer;
}
.book-card:hover { transform: translateY(-5px); }
.book-cover { aspect-ratio: 3/4; overflow: hidden; }
.cover-image { width: 100%; height: 100%; object-fit: cover; }
.book-info { padding: 1rem; }
.title { font-size: 1rem; margin: 0 0 0.5rem; font-weight: 600; }
.author { font-size: 0.9rem; color: #666; margin-bottom: 1rem; }
.metadata { display: flex; justify-content: space-between; align-items: center; }
.category { background: #f8f9fa; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; }
.stats { display: flex; gap: 1rem; font-size: 0.8rem; color: #666; }
.stats i { margin-right: 0.3rem; }
.likes { color: #dc3545; }
.comments { color: #1976d2; }
</style>

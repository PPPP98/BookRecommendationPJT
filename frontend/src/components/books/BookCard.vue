<template>
  <div class="book-card" @click="$emit('click')">
    <!-- 도서 커버 이미지 -->
    <div class="book-cover">
      <img 
        :src="book.cover_image || book.cover || defaultCover"
        :alt="book.title"
        class="cover-image"
        @error="onImgError"
      >
    </div>
    
    <!-- 도서 정보 -->
    <div class="book-info">
      <h3 class="title">{{ book.title }}</h3>
      <p class="author">{{ book.author }}</p>
      <!-- 메타데이터: 카테고리, 좋아요 수, 댓글 수 -->
      <div class="metadata">
        <span class="category">{{ book.category_name || book.category }}</span>
        <div class="stats">
          <span class="likes">
            <i class="fas fa-heart"></i> {{ book.likes_count || 0 }}
          </span>
          <span class="threads">
            <i class="fas fa-comments"></i> {{ book.threads_count || 0 }}
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
        // 필수 필드 검증 - API 응답 구조에 맞게 수정
        const requiredFields = ['id', 'title', 'author'];
        const hasRequiredFields = requiredFields.every(prop => prop in value);
        // cover 또는 cover_image가 있는지 확인
        const hasCover = 'cover' in value || 'cover_image' in value;
        // category 또는 category_name이 있는지 확인
        const hasCategory = 'category' in value || 'category_name' in value;
        return hasRequiredFields && hasCover && hasCategory;
      }
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

.book-card:hover {
  transform: translateY(-5px);
}

.book-cover {
  aspect-ratio: 3/4;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-info {
  padding: 1rem;
}

.title {
  font-size: 1rem;
  margin: 0 0 0.5rem;
  font-weight: 600;
}

.author {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
}

.metadata {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  background: #f8f9fa;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.stats {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #666;
}

.stats i {
  margin-right: 0.3rem;
}

.likes {
  color: #dc3545;
}
</style>

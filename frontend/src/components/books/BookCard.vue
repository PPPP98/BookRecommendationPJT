<!-- 
  BookCard 컴포넌트
  역할: 도서 정보를 카드 형태로 표시하는 재사용 가능한 컴포넌트
  Props:
    - book: Object (필수) - 도서 정보
      {
        id: Number,
        title: String,
        author: String,
        cover_image: String,
        rating: Number,
        description: String,
        category: String,
        reviews: Array
      }
-->
<template>
  <div class="book-card" @click="$emit('click', book.id)">
    <!-- 도서 커버 이미지 -->
    <div class="book-cover">
      <img 
        :src="book.cover_image" 
        :alt="book.title"
        class="cover-image"
      >
    </div>

    <!-- 도서 정보 -->
    <div class="book-info">
      <h3 class="title">{{ book.title }}</h3>
      <p class="author">{{ book.author }}</p>
      
      <!-- 평점 정보 -->
      <div class="rating-info">
        <span class="rating">⭐ {{ book.rating }}</span>
        <span class="review-count" v-if="book.reviews">
          ({{ book.reviews.length }}개의 리뷰)
        </span>
      </div>

      <!-- 카테고리 표시 -->
      <span v-if="book.category" class="category">
        {{ book.category }}
      </span>
    </div>

    <!-- 슬롯: 추가 액션 버튼 등 -->
    <div class="actions">
      <slot name="actions"></slot>
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
        // 필수 필드 검증
        return value.id && 
               value.title && 
               value.author && 
               value.cover_image !== undefined
      }
    }
  }
}
</script>

<style scoped>
.book-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
}

.cover-image {
  width: 100%;
  height: auto;
  max-height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.book-info {
  margin-top: 1rem;
}

.title {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

.author {
  color: #666;
  font-size: 0.9rem;
}

.rating-info {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin: 0.5rem 0;
}

.review-count {
  color: #666;
  font-size: 0.9rem;
}

.category {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 0.8rem;
}

.actions {
  margin-top: 1rem;
}
</style>

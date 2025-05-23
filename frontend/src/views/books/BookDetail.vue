<!-- 
  BookDetail 컴포넌트
  역할: 개별 도서의 상세 정보를 표시하는 페이지
  기능:
    - 도서 상세 정보 표시
    - 좋아요 기능
    - 대출 정보
    - 리뷰 및 코멘트
-->
<template>
  <div class="book-detail-page">
    <div v-if="loading" class="loading">
      <p>도서 정보를 불러오는 중입니다...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchBookDetails">다시 시도</button>
    </div>
    <div v-else class="book-container">
      <!-- 도서 기본 정보 섹션 -->
      <section class="book-info-section">
        <div class="book-image">
          <img :src="book.coverImage" :alt="book.title" />
        </div>
        <div class="book-info">
          <h1 class="book-title">{{ book.title }}</h1>
          <div class="book-meta">
            <p class="author">작가: {{ book.author }}</p>
            <p class="publisher">출판사: {{ book.publisher }}</p>
            <p class="publication-date">출간일: {{ book.publicationDate }}</p>
            <p class="isbn">ISBN: {{ book.isbn }}</p>
          </div>
          <div class="book-actions">
            <button 
              class="like-button" 
              :class="{ active: book.isLiked }"
              @click="toggleLike"
            >
              {{ book.isLiked ? '❤️ 좋아요 취소' : '🤍 좋아요' }}
            </button>
            <button class="borrow-button" @click="checkAvailability">
              대출 가능 여부 확인
            </button>
          </div>
        </div>
      </section>

      <!-- 도서 상세 정보 섹션 -->
      <section class="book-description-section">
        <h2>도서 소개</h2>
        <p class="description">{{ book.description }}</p>
      </section>

      <!-- 대출 정보 섹션 -->
      <section class="availability-section" v-if="showAvailability">
        <h2>대출 가능 정보</h2>
        <div v-if="libraries.length > 0" class="library-list">
          <div 
            v-for="library in libraries" 
            :key="library.id" 
            class="library-item"
          >
            <h3>{{ library.name }}</h3>
            <p class="address">{{ library.address }}</p>
            <p class="status" :class="library.available ? 'available' : 'unavailable'">
              {{ library.available ? '대출 가능' : '대출 중' }}
            </p>
            <p v-if="!library.available" class="return-date">
              반납 예정일: {{ library.returnDate }}
            </p>
          </div>
        </div>
        <p v-else class="no-libraries">현재 등록된 도서관에 해당 도서가 없습니다.</p>
      </section>

      <!-- 유사 도서 추천 섹션 -->
      <section class="recommendations-section">
        <h2>이 도서와 유사한 도서</h2>
        <div class="similar-books">
          <div 
            v-for="similarBook in similarBooks" 
            :key="similarBook.id"
            class="similar-book-card"
            @click="navigateToBook(similarBook.id)"
          >
            <img :src="similarBook.coverImage" :alt="similarBook.title" />
            <h4>{{ similarBook.title }}</h4>
            <p>{{ similarBook.author }}</p>
          </div>
        </div>
      </section>

      <!-- 리뷰 섹션 -->
      <section class="reviews-section">
        <h2>리뷰 ({{ book.reviewCount }})</h2>
        <div class="review-form">
          <textarea 
            v-model="newReview" 
            placeholder="이 책에 대한 리뷰를 작성해주세요..."
            rows="3"
          ></textarea>
          <div class="rating-selector">
            <span>평점: </span>
            <span 
              v-for="star in 5" 
              :key="star"
              class="star"
              :class="{ active: star <= rating }"
              @click="rating = star"
            >★</span>
          </div>
          <button @click="submitReview">리뷰 작성</button>
        </div>

        <div class="reviews-list">
          <div v-if="book.reviews.length === 0" class="no-reviews">
            <p>아직 작성된 리뷰가 없습니다.</p>
          </div>
          <div v-else v-for="review in book.reviews" :key="review.id" class="review-item">
            <div class="review-header">
              <span class="reviewer-name">{{ review.userName }}</span>
              <span class="review-date">{{ review.date }}</span>
              <div class="review-rating">
                <span v-for="i in 5" :key="i" :class="{ active: i <= review.rating }">★</span>
              </div>
            </div>
            <p class="review-content">{{ review.content }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookDetail',
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      book: null,
      similarBooks: [],
      libraries: [],
      loading: true,
      error: null,
      showAvailability: false,
      newReview: '',
      rating: 0,
    }
  },
  mounted() {
    this.fetchBookDetails();
  },
  methods: {
    async fetchBookDetails() {
      this.loading = true;
      this.error = null;
      try {
        // 백엔드 API 구현 전 목업 데이터 사용
        // 실제로는 fetch 또는 axios로 API 호출
        setTimeout(() => {
          // 목업 데이터
          this.book = {
            id: this.id,
            title: '소설 제목',
            author: '홍길동',
            publisher: '출판사',
            publicationDate: '2023-01-01',
            isbn: '9788901234567',
            coverImage: 'https://via.placeholder.com/300x450',
            description: '이 소설은 현대 사회의 다양한 이슈를 다루고 있습니다. 작가의 섬세한 묘사와 깊이 있는 캐릭터 설정으로 독자들에게 깊은 인상을 남깁니다. 이 책을 통해 우리는 삶의 의미와 인간 관계의 중요성에 대해 다시 한번 생각해볼 수 있습니다.',
            isLiked: false,
            reviewCount: 2,
            reviews: [
              {
                id: 1,
                userName: '김독자',
                date: '2023-05-15',
                rating: 4,
                content: '흥미로운 내용과 캐릭터 설정이 좋았습니다. 다만 일부 장면에서는 전개가 조금 느린 감이 있어 아쉬웠습니다.'
              },
              {
                id: 2,
                userName: '이리뷰',
                date: '2023-06-20',
                rating: 5,
                content: '최근에 읽은 책 중 가장 인상적이었습니다. 작가의 문체와 이야기 전개 방식이 매우 독특하고 신선했습니다.'
              }
            ]
          };
          
          // 유사 도서 목업 데이터
          this.similarBooks = [
            {
              id: 101,
              title: '유사 도서 1',
              author: '작가 A',
              coverImage: 'https://via.placeholder.com/150x200'
            },
            {
              id: 102,
              title: '유사 도서 2',
              author: '작가 B',
              coverImage: 'https://via.placeholder.com/150x200'
            },
            {
              id: 103,
              title: '유사 도서 3',
              author: '작가 C',
              coverImage: 'https://via.placeholder.com/150x200'
            }
          ];
          
          this.loading = false;
        }, 500);
      } catch (err) {
        this.error = '도서 정보를 불러오는데 실패했습니다.';
        this.loading = false;
        console.error('Error fetching book details:', err);
      }
    },
    toggleLike() {
      // 백엔드 API 구현 전 클라이언트 상태만 변경
      if (this.book) {
        this.book.isLiked = !this.book.isLiked;
        // 실제로는 API 호출하여 서버에 상태 저장
      }
    },
    checkAvailability() {
      // 도서관별 대출 가능 여부 확인
      this.showAvailability = true;
      
      // 목업 데이터
      this.libraries = [
        {
          id: 1,
          name: '중앙 도서관',
          address: '서울시 강남구',
          available: true
        },
        {
          id: 2,
          name: '디지털 도서관',
          address: '서울시 서초구',
          available: false,
          returnDate: '2023-06-30'
        },
        {
          id: 3,
          name: '구립 도서관',
          address: '서울시 송파구',
          available: true
        }
      ];
    },
    submitReview() {
      if (!this.newReview.trim() || this.rating === 0) {
        alert('리뷰 내용과 평점을 모두 입력해주세요.');
        return;
      }
      
      // 새 리뷰 추가 (목업)
      const newReviewObj = {
        id: this.book.reviews.length + 1,
        userName: '사용자', // 실제로는 로그인된 사용자 이름
        date: new Date().toISOString().split('T')[0],
        rating: this.rating,
        content: this.newReview
      };
      
      this.book.reviews.push(newReviewObj);
      this.book.reviewCount += 1;
      this.newReview = '';
      this.rating = 0;
      
      // 실제로는 API 호출하여 리뷰 저장
    },
    navigateToBook(bookId) {
      this.$router.push({ name: 'BookDetail', params: { id: bookId } });
    }
  }
}
</script>

<style scoped>
.book-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.loading, .error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.book-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* 도서 기본 정보 스타일 */
.book-info-section {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.book-image img {
  width: 100%;
  max-width: 300px;
  height: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.book-title {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #333;
}

.book-meta {
  margin-bottom: 1.5rem;
}

.book-meta p {
  margin: 0.5rem 0;
  color: #555;
}

.book-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.like-button {
  background-color: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}

.like-button.active {
  background-color: #ffe0e0;
  color: #e74c3c;
}

.borrow-button {
  background-color: #4caf50;
  color: white;
}

button:hover {
  opacity: 0.9;
}

/* 도서 설명 스타일 */
.book-description-section {
  background-color: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
}

.description {
  line-height: 1.6;
  color: #333;
}

/* 대출 정보 섹션 */
.library-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.library-item {
  border: 1px solid #ddd;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: white;
}

.status.available {
  color: #4caf50;
  font-weight: bold;
}

.status.unavailable {
  color: #e74c3c;
  font-weight: bold;
}

.return-date {
  font-style: italic;
  font-size: 0.9rem;
  color: #666;
}

/* 유사 도서 추천 섹션 */
.similar-books {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 1rem 0;
}

.similar-book-card {
  min-width: 150px;
  cursor: pointer;
  transition: transform 0.3s;
}

.similar-book-card:hover {
  transform: translateY(-5px);
}

.similar-book-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.similar-book-card h4 {
  margin: 0.5rem 0 0.25rem;
  font-size: 1rem;
}

.similar-book-card p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

/* 리뷰 섹션 */
.review-form {
  margin-bottom: 2rem;
}

.review-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.rating-selector {
  margin-bottom: 1rem;
}

.star {
  font-size: 1.5rem;
  color: #ddd;
  cursor: pointer;
}

.star.active {
  color: #ffc107;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-item {
  border-bottom: 1px solid #eee;
  padding-bottom: 1.5rem;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.reviewer-name {
  font-weight: 600;
}

.review-date {
  color: #666;
  font-size: 0.9rem;
}

.review-rating {
  margin-left: auto;
}

.review-rating span {
  color: #ddd;
  font-size: 1rem;
}

.review-rating span.active {
  color: #ffc107;
}

.review-content {
  margin: 0;
  line-height: 1.6;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .book-info-section {
    grid-template-columns: 1fr;
  }
  
  .book-image {
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .book-image img {
    max-width: 200px;
  }
  
  .library-list {
    grid-template-columns: 1fr;
  }
}
</style>
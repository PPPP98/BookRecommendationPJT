<!-- 
  ThreadWrite 페이지
  역할: 새로운 쓰레드를 작성하는 페이지
  기능:
    - 제목, 내용 입력
    - 관련 도서 선택
    - 평점 입력
    - 태그 지정
  데이터 구조:
    - thread: {
        title: String,
        content: String,
        bookId: Number,
        rating: Number,
        tags: Array<String>
      }
-->
<template>
  <div class="thread-write-page">
    <Navbar />
    
    <main class="main-content">
      <h1>새 글 작성</h1>
      
      <form @submit.prevent="submitThread">
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            id="title" 
            v-model="thread.title" 
            type="text" 
            required 
            placeholder="제목을 입력하세요"
          >
        </div>
        
        <div class="form-group">
          <label for="book">관련 도서</label>
          <select 
            id="book" 
            v-model="thread.bookId" 
            required
          >
            <option value="" disabled>도서를 선택하세요</option>
            <option v-for="book in books" :key="book.id" :value="book.id">
              {{ book.title }} ({{ book.author }})
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="rating">평점</label>
          <div class="rating-selector">
            <div 
              v-for="score in 5" 
              :key="score" 
              class="star"
              :class="{ active: thread.rating >= score }"
              @click="thread.rating = score"
            >
              ⭐
            </div>
            <span class="rating-value">{{ thread.rating }}/5</span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content" 
            v-model="thread.content" 
            rows="10" 
            required 
            placeholder="내용을 입력하세요"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="tags">태그</label>
          <div class="tags-input">
            <input 
              id="tags" 
              v-model="tagInput" 
              type="text" 
              placeholder="태그를 입력하고 Enter를 누르세요"
              @keydown.enter.prevent="addTag"
            >
            <div class="tags-list">
              <span 
                v-for="(tag, index) in thread.tags" 
                :key="index" 
                class="tag"
              >
                #{{ tag }}
                <button type="button" @click="removeTag(index)" class="remove-tag">×</button>
              </span>
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="$router.back()" class="cancel-btn">취소</button>
          <button type="submit" class="submit-btn" :disabled="!isFormValid">등록</button>
        </div>
      </form>
    </main>
    
    <Footer />
  </div>
</template>

<script>
import { books } from '@/mocks/books'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'

export default {
  name: 'ThreadWrite',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      books: books,
      thread: {
        title: '',
        content: '',
        bookId: '',
        rating: 0,
        tags: []
      },
      tagInput: ''
    }
  },
  computed: {
    isFormValid() {
      return this.thread.title &&
             this.thread.bookId &&
             this.thread.rating > 0 &&
             this.thread.content
    }
  },
  methods: {
    addTag() {
      const tag = this.tagInput.trim()
      if (!tag) return
      
      if (!this.thread.tags.includes(tag)) {
        this.thread.tags.push(tag)
      }
      
      this.tagInput = ''
    },
    removeTag(index) {
      this.thread.tags.splice(index, 1)
    },
    async submitThread() {
      if (!this.isFormValid) return
      
      try {
        // API 연동 시 실제 API 호출로 변경
        console.log('작성된 쓰레드:', this.thread)
        
        // 성공적으로 작성되면 커뮤니티 페이지로 이동
        this.$router.push('/community')
      } catch (error) {
        console.error('글 작성 중 오류 발생:', error)
        // 오류 처리
      }
    }
  }
}
</script>

<style scoped>
.thread-write-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, select, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.rating-selector {
  display: flex;
  align-items: center;
}

.star {
  font-size: 1.5rem;
  color: #ccc;
  cursor: pointer;
}

.star.active {
  color: #f0ad4e;
}

.rating-value {
  margin-left: 1rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
}

.remove-tag {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  margin-left: 0.25rem;
  color: #666;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn {
  padding: 0.75rem 1.5rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>

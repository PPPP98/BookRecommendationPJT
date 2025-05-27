<template>
  <div class="page third-page">
    <div class="content">
      <h1>도서 카테고리</h1>
      <p class="subtitle">관심있는 도서 카테고리를 선택하세요</p>
      <div class="category-grid">
        <div 
          v-for="category in categories.categories" 
          :key="category.id"
          @click="handleCategoryClick(category.name)"
        >
          <h3 class="category-card" :class="{ active: selectedCategory === category.name }">
            {{ category.name }}
          </h3>
        </div>
      </div>
      <div class="hot-books">
        <h2>지금 인기 있는 도서</h2>
        <div class="books-grid">
          <router-link 
            v-for="book in hotBooks" 
            :key="book.id" 
            :to="`/books/${book.id}`"
            class="book-card-link"
          >
            <div class="book-card">
              <img :src="book.cover" :alt="book.title" class="book-cover">
              <h3 class="book-title">{{ truncateTitle(book.title) }}</h3>
              <p class="book-author">{{ truncateAuthor(book.author) }}</p>
              <p class="book-likes">❤️ {{ book.like_count }}</p>
            </div>
          </router-link>
        </div>
        <div class="more-books">
          <button @click="goToBooksList" class="more-books-btn">도서 더 보러가기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const categories = ref([])
const selectedCategory = ref('')
const hotBooks = ref([])

const truncateTitle = (title, maxLength = 20) => {
  if (title.length <= maxLength) return title
  return title.slice(0, maxLength) + '...'
}

const truncateAuthor = (author, maxLength = 15) => {
  if (author.length <= maxLength) return author
  return author.slice(0, maxLength) + '...'
}

const handleBookClick = (bookId) => {
  router.push(`/books/${bookId}`)
}

const goToBooksList = () => {
  router.push('/books')
}

const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/books/categories/')
    categories.value = response.data
    console.log('카테고리 목록:', categories.value)
    
    // 첫 번째 카테고리 선택 및 도서 로드
    if (categories.value.categories && categories.value.categories.length > 0) {
      selectedCategory.value = categories.value.categories[0].name
      await fetchBooks(selectedCategory.value)
    }
  } catch (error) {
    console.error('카테고리를 불러오는데 실패했습니다:', error)
  }
}

const fetchBooks = async (category) => {
  try {
    const response = await axios.get(`/api/books/?category=${category}&ordering=-like_count`)
    hotBooks.value = response.data.results.slice(0, 4) // 상위 5개만 선택
    console.log('인기 도서:', hotBooks.value)
  } catch (error) {
    console.error('도서를 불러오는데 실패했습니다:', error)
  }
}

const handleCategoryClick = async (categoryName) => {
  selectedCategory.value = categoryName
  await fetchBooks(categoryName)
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.page {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #ffffff;
  display: flex;
  /* align-items: center; */
  justify-content: center;
}

.content {
  padding: 2rem;
  text-align: center;
  max-width: 1200px;
  margin-top: 100px;
}

.category-grid {
  display: flex;
  /* grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); */
  gap: 2rem;
  margin-top: 2rem;
}

.category-card {
  color: white;
  background-color: #34495e;
  padding: 1rem;
  border-radius: 10px;
  width: 120px;
  transition: transform 0.3s ease;
  font-size: small;
}

.category-card:hover {
  background-color: #2c3e50;
  transform: translateY(-5px);
}

.category-card.active {
  background-color: #ffffff;
  border: #34495e 2px solid;
  color: #34495e;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .content {
    padding: 1rem;
  }
  
}

.hot-books {
  margin-top: 3rem;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  margin-top: 2rem;
  justify-items: center;
}

.book-card {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 1rem;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  cursor: pointer;
  width: 240px;
  height: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.book-card:hover {
  transform: translateY(-5px);
}

.book-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.book-cover {
  width: 150px;
  height: 210px;
  object-fit: cover;
  border-radius: 5px;
}

.book-title {
  margin: 1rem 0 0.5rem;
  font-size: 1.1rem;
  font-weight: bold;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  padding: 0 0.5rem;
  box-sizing: border-box;
}

.book-author {
  color: #666;
  margin-bottom: 0.5rem;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  padding: 0 0.5rem;
  box-sizing: border-box;
}

.book-likes {
  color: #e74c3c;
  font-weight: bold;
}

.more-books {
  margin-top: 2rem;
}

.more-books-btn {
  background-color: #34495e;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.more-books-btn:hover {
  background-color: #2c3e50;
}

@media (max-width: 1200px) {
  .books-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .books-grid {
    grid-template-columns: repeat(1, 1fr);
  }
  
  .book-card {
    width: 180px;
    height: 360px;
  }
}

</style>

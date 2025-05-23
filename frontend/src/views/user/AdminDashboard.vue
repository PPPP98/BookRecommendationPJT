<!-- 
  AdminDashboard 컴포넌트
  역할: 관리자 대시보드 페이지
  기능:
    - 사용자 관리
    - 도서 관리
    - 커뮤니티 관리
    - 통계 확인
-->
<template>
  <div class="admin-dashboard">
    <Navbar />
    
    <main class="main-content">
      <div class="dashboard-header">
        <h1>관리자 대시보드</h1>
      </div>

      <div class="dashboard-stats">
        <div class="stat-card">
          <h3>전체 사용자</h3>
          <p class="stat-number">{{ stats.totalUsers }}</p>
        </div>
        <div class="stat-card">
          <h3>전체 도서</h3>
          <p class="stat-number">{{ stats.totalBooks }}</p>
        </div>
        <div class="stat-card">
          <h3>오늘의 게시글</h3>
          <p class="stat-number">{{ stats.todayPosts }}</p>
        </div>
        <div class="stat-card">
          <h3>신규 가입자</h3>
          <p class="stat-number">{{ stats.newUsers }}</p>
        </div>
      </div>

      <div class="dashboard-sections">
        <!-- 사용자 관리 섹션 -->
        <section class="dashboard-section">
          <h2>사용자 관리</h2>
          <div class="section-content">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>이름</th>
                  <th>이메일</th>
                  <th>가입일</th>
                  <th>상태</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ formatDate(user.createdAt) }}</td>
                  <td>{{ user.status }}</td>
                  <td>
                    <button @click="toggleUserStatus(user.id)">
                      {{ user.status === 'active' ? '비활성화' : '활성화' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- 도서 관리 섹션 -->
        <section class="dashboard-section">
          <h2>도서 관리</h2>
          <div class="section-content">
            <div class="action-buttons">
              <button @click="openAddBookModal" class="add-button">새 도서 추가</button>
            </div>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>제목</th>
                  <th>저자</th>
                  <th>카테고리</th>
                  <th>평점</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="book in books" :key="book.id">
                  <td>{{ book.id }}</td>
                  <td>{{ book.title }}</td>
                  <td>{{ book.author }}</td>
                  <td>{{ book.category }}</td>
                  <td>{{ book.rating }}</td>
                  <td>
                    <button @click="editBook(book.id)">수정</button>
                    <button @click="deleteBook(book.id)">삭제</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import { computed } from 'vue'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import { books } from '@/mocks/books'
import { users } from '@/mocks/users'

export default {
  name: 'AdminDashboard',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      stats: {
        totalUsers: users.length,
        totalBooks: books.length,
        todayPosts: 5, // Mock data
        newUsers: 3 // Mock data
      },
      users: users.map(user => ({
        ...user,
        status: 'active',
        email: `${user.username}@example.com`,
        createdAt: new Date().toISOString()
      })),
      books: books
    }
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ko-KR')
    },
    toggleUserStatus(userId) {
      const user = this.users.find(u => u.id === userId)
      if (user) {
        user.status = user.status === 'active' ? 'inactive' : 'active'
      }
    },
    openAddBookModal() {
      // TODO: 도서 추가 모달 구현
      console.log('도서 추가 모달 열기')
    },
    editBook(bookId) {
      // TODO: 도서 수정 기능 구현
      console.log('도서 수정:', bookId)
    },
    deleteBook(bookId) {
      // TODO: 도서 삭제 기능 구현
      if (confirm('정말 삭제하시겠습니까?')) {
        console.log('도서 삭제:', bookId)
      }
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #0066cc;
  margin: 0;
}

.dashboard-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.dashboard-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-buttons {
  margin-bottom: 1rem;
}

.add-button {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

th {
  background: #f8f9fa;
  font-weight: 600;
}

button {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
  margin-right: 0.5rem;
  background: white;
}

button:hover {
  background: #f8f9fa;
}
</style>
<template>
  <div class="thread-list-page">
    <Navbar />

    <main class="main-content">
      <div class="page-header">
        <h1>커뮤니티</h1>
      </div>

      <div class="thread-container wide">
        <div class="divider"></div>

        <!-- 인기 쓰레드 슬라이드 -->
        <div v-if="popularThreads.length > 0" class="popular-thread-slide-section">
          <h2>🔥 인기 쓰레드</h2>
          <div class="popular-thread-slide"
               @mouseenter="showSlideButtons = true"
               @mouseleave="showSlideButtons = false">
            <ThreadCard
              v-if="popularThreads[currentPopularIndex]"
              :thread="popularThreads[currentPopularIndex]"
              :large="true"
              @thread-click="goToThread"
            />
            <button
              v-if="showSlideButtons"
              class="slide-btn prev"
              @click="prevPopularThread"
              aria-label="이전 인기 쓰레드"
            >&lt;</button>
            <button
              v-if="showSlideButtons"
              class="slide-btn next"
              @click="nextPopularThread"
              aria-label="다음 인기 쓰레드"
            >&gt;</button>
          </div>
        </div>

        <!-- 팔로잉 쓰레드 섹션 -->
        <div v-if="followingThreads.length > 0" class="following-thread-section">
          <h2>👥 팔로잉 쓰레드</h2>
          <div class="following-thread-list">
            <ThreadCard
              v-for="thread in followingThreads"
              :key="thread.id"
              :thread="thread"
              :large="true"
              @thread-click="goToThread"
            />
          </div>
        </div>

        <div class="divider"></div>

        <!-- 전체 쓰레드 목록 (세로 나열) -->
        <div v-if="loading" class="info-state">불러오는 중...</div>
        <div v-else-if="error" class="error-state">{{ error }}</div>
        <div v-else>
          <div v-if="threads.length === 0" class="info-state">게시글이 없습니다.</div>
          <div v-else>
            <div class="all-threads-list">
              <ThreadCard
                v-for="thread in threads"
                :key="thread.id"
                :thread="thread"
                :large="true"
                @thread-click="goToThread"
              />
            </div>
            <div class="pagination">
              <button v-if="prev" @click="goToPage(prev)">이전</button>
              <button v-if="next" @click="goToPage(next)">다음</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import ThreadCard from '@/components/thread/ThreadCard.vue'
import axios from 'axios'

function toRelativeUrl(url) {
  if (!url) return null
  try {
    const u = new URL(url)
    return u.pathname + u.search
  } catch {
    return url
  }
}

export default {
  name: 'Community',
  components: { Navbar, Footer, ThreadCard },
  data() {
    return {
      threads: [],
      next: null,
      prev: null,
      loading: false,
      error: null,
      currentPage: 1,
      itemsPerPage: 20,
      popularThreads: [],
      currentPopularIndex: 0,
      showSlideButtons: false,
      slideInterval: null,
      followingThreads: []
    }
  },
  mounted() {
    this.fetchPopularThreads()
    this.fetchThreads()
    this.fetchFollowingThreads()
    this.startSlideInterval()
  },
  beforeDestroy() {
    this.clearSlideInterval()
  },
  methods: {
    async fetchThreads(url) {
      this.loading = true
      this.error = null
      let apiUrl
      if (url) {
        apiUrl = toRelativeUrl(url)
        const match = apiUrl.match(/[?&]page=(\d+)/)
        if (match) this.currentPage = parseInt(match[1])
      } else {
        apiUrl = `/api/threads/?page=${this.currentPage}&page_size=${this.itemsPerPage}`
      }
      try {
        const { data } = await axios.get(apiUrl)
        this.threads = Array.isArray(data.results) ? data.results : []
        this.next = data.next
        this.prev = data.previous
      } catch (e) {
        if (e.response && e.response.status === 404) {
          this.error = '잘못된 페이지 번호입니다.'
        } else if (e.response && e.response.status === 400) {
          this.error = '잘못된 요청입니다.'
        } else {
          this.error = '목록을 불러올 수 없습니다.'
        }
        this.threads = []
      } finally {
        this.loading = false
      }
    },
    async fetchPopularThreads() {
      try {
        const { data } = await axios.get('/api/threads/popular/')
        this.popularThreads = Array.isArray(data) ? data : []
        this.currentPopularIndex = 0
      } catch {
        this.popularThreads = []
      }
    },
    // 팔로잉 쓰레드 불러오기 (최대 5개)
    async fetchFollowingThreads() {
      try {
        // 실제 API 엔드포인트에 맞게 수정
        const { data } = await axios.get('/api/threads/following/?limit=5')
        this.followingThreads = Array.isArray(data)
          ? data.slice(0, 5)
          : Array.isArray(data.results)
          ? data.results.slice(0, 5)
          : []
      } catch {
        this.followingThreads = []
      }
    },
    goToThread(threadId) {
      this.$router.push({ name: 'ThreadDetail', params: { id: threadId } })
    },
    prevPopularThread() {
      if (!this.popularThreads.length) return
      this.currentPopularIndex =
        (this.currentPopularIndex - 1 + this.popularThreads.length) % this.popularThreads.length
      this.restartSlideInterval()
    },
    nextPopularThread() {
      if (!this.popularThreads.length) return
      this.currentPopularIndex =
        (this.currentPopularIndex + 1) % this.popularThreads.length
      this.restartSlideInterval()
    },
    startSlideInterval() {
      this.clearSlideInterval()
      this.slideInterval = setInterval(() => {
        if (this.popularThreads.length > 0) {
          this.currentPopularIndex =
            (this.currentPopularIndex + 1) % this.popularThreads.length
        }
      }, 5000)
    },
    clearSlideInterval() {
      if (this.slideInterval) clearInterval(this.slideInterval)
    },
    restartSlideInterval() {
      this.clearSlideInterval()
      this.startSlideInterval()
    },
    goToPage(url) {
      this.fetchThreads(url)
    }
  }
}
</script>

<style scoped>
.thread-list-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
.page-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 2rem;
}
.thread-container.wide {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 2rem 2rem 2.5rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
.divider {
  border-bottom: 1.5px solid #e0e0e0;
  margin: 1.5rem 0 1.7rem 0;
}
.popular-thread-slide-section {
  margin-bottom: 2.5rem;
}
.popular-thread-slide-section h2 {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #1976d2;
}
.popular-thread-slide {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  margin-bottom: 1.2rem;
}
.popular-thread-slide .thread-card.large {
  min-width: 720px;
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
}
.slide-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: #fff;
  border: 1.5px solid #1976d2;
  color: #1976d2;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  font-size: 1.4rem;
  font-weight: bold;
  cursor: pointer;
  z-index: 2;
  opacity: 0.85;
  transition: background 0.2s, color 0.2s;
}
.slide-btn:hover {
  background: #1976d2;
  color: #fff;
}
.slide-btn.prev {
  left: 0;
}
.slide-btn.next {
  right: 0;
}

/* 팔로잉 쓰레드 섹션 */
.following-thread-section {
  margin-bottom: 2.5rem;
}
.following-thread-section h2 {
  font-size: 1.08rem;
  font-weight: 700;
  margin-bottom: 0.7rem;
  color: #1976d2;
}
/* 가로 스크롤 카드 리스트 */
.following-thread-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.2rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}
.following-thread-list .thread-card.large {
  min-width: 320px;
  max-width: 420px;
  width: 100%;
  margin: 0 auto;
}

@media (max-width: 1200px) {
  .thread-container.wide {
    max-width: 98vw;
    padding: 1rem 0.5rem 1.5rem 0.5rem;
  }
  .popular-thread-slide .thread-card.large,
  .all-threads-list .thread-card.large {
    min-width: 98vw;
    max-width: 98vw;
  }
  .following-thread-list {
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  }
}
@media (max-width: 600px) {
  .main-content { padding: 0.5rem; }
  .thread-container.wide { padding: 0.5rem 0.1rem 1rem 0.1rem; }
  .popular-thread-slide .thread-card.large,
  .all-threads-list .thread-card.large {
    min-width: 100vw;
    max-width: 100vw;
    border-radius: 0;
    padding: 0.8rem 0.4rem;
  }
  .following-thread-list {
    grid-template-columns: 1fr;
    gap: 0.7rem;
    padding-bottom: 0.2rem;
  }
  .following-thread-list .thread-card.large {
    min-width: 0;
    max-width: 100vw;
  }
}
.all-threads-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.all-threads-list .thread-card.large {
  min-width: 720px;
  max-width: 900px;
  margin: 0 auto 1.5rem auto;
}
.info-state, .error-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}
.error-state { color: #dc3545; }
.pagination {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 2rem 0;
}
</style>

<template>
  <div class="community-pinterest">
    <Navbar />

    <main class="main-content">
      <div class="page-header">
        <h1>커뮤니티</h1>
      </div>

      <!-- 상단 3개 카드 -->
      <section class="top-ideas">
        <PinterestCard
          v-if="popularThreads.length"
          :thread="popularThreads[currentPopularIndex]"
          label="인기 쓰레드"
        />
        <PinterestCard
          v-if="followingThreads.length"
          :thread="followingThreads[0]"
          label="팔로잉 쓰레드"
        />
        <PinterestCard
          :thread="{
            book: { cover: 'https://source.unsplash.com/220x300/?community,idea' },
            title: '임시 카드',
            user: { nickname: '임시' },
            like_count: 0,
            comment_count: 0
          }"
          label="임시 쓰레드"
        />
      </section>

      <div class="divider"></div>

      <!-- 전체 쓰레드 Masonry -->
      <section class="masonry-section">
        <h2 class="masonry-title">새로운 소식</h2>
        <div v-if="loading" class="info-state">불러오는 중...</div>
        <div v-else-if="error" class="error-state">{{ error }}</div>
        <div v-else>
          <div v-if="threads.length === 0" class="info-state">게시글이 없습니다.</div>
          <div v-else class="masonry-grid">
            <PinterestCard
              v-for="thread in threads"
              :key="thread.id"
              :thread="thread"
              @click.native="goToThread(thread.id)"
            />
          </div>
          <div class="pagination">
            <button v-if="prev" @click="goToPage(prev)">이전</button>
            <button v-if="next" @click="goToPage(next)">다음</button>
          </div>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import axios from 'axios'
import { h } from 'vue'

function toRelativeUrl(url) {
  if (!url) return null
  try {
    const u = new URL(url)
    return u.pathname + u.search
  } catch {
    return url
  }
}

// 커스텀 카드 컴포넌트 (렌더 함수)
const PinterestCard = {
  name: 'PinterestCard',
  props: {
    thread: { type: Object, required: true },
    label: { type: String, default: '' }
  },
  render() {
    const cover =
      this.thread.book && this.thread.book.cover
        ? this.thread.book.cover
        : (this.thread.image || 'https://source.unsplash.com/220x300/?book,community')
    const title = this.thread.title || ''
    const nickname =
      (this.thread.user && (this.thread.user.nickname || this.thread.user.username)) || '작성자 미상'
    const likeCount = this.thread.like_count || 0
    const commentCount = this.thread.comment_count || 0

    return h(
      'div',
      { class: 'custom-card', onClick: this.$attrs.onClick },
      [
        this.label
          ? h('div', { class: 'custom-label' }, this.label)
          : null,
        h('img', {
          class: 'custom-img',
          src: cover,
          alt: title
        }),
        h('div', { class: 'custom-title' }, title),
        h('div', { class: 'custom-meta' }, nickname),
        h('div', { class: 'custom-meta-counts' }, [
          h('span', { class: 'like' }, `❤️ ${likeCount}`),
          h('span', { class: 'comment' }, `💬 ${commentCount}`)
        ])
      ]
    )
  }
}

export default {
  name: 'CommunityPinterest',
  components: { Navbar, Footer, PinterestCard },
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
  beforeUnmount() {
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
    async fetchFollowingThreads() {
      try {
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
    goToPage(url) {
      this.fetchThreads(url)
    }
  }
}
</script>

<style scoped>
.community-pinterest {
  background: #faf8f6;
  min-height: 100vh;
  width: 100vw;
  overflow-x: hidden;
}
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.5rem 2vw 2rem 2vw;
}
.page-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 2rem;
}
.divider {
  border-bottom: 1.5px solid #e0e0e0;
  margin: 1.5rem 0 1.7rem 0;
}

/* 상단 3개 카드 */
.top-ideas {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  margin: 2.5rem 0 2.2rem 0;
  flex-wrap: wrap;
  width: 100%;
}

/* 커스텀 카드 스타일 (Pinterest 스타일 Masonry) */
.custom-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 210px;
  max-width: 100%;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.11s;
  break-inside: avoid;
  position: relative;
}
.custom-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  transform: translateY(-4px) scale(1.03);
}
.custom-label {
  position: absolute;
  top: 10px;
  left: 12px;
  background: #e60023;
  color: #fff;
  font-size: 0.93rem;
  font-weight: 600;
  border-radius: 12px;
  padding: 0.23em 0.9em;
  z-index: 2;
  opacity: 0.93;
}
.custom-img {
  width: 100%;
  height: 145px;
  max-width: 100%;
  object-fit: cover;
  background: #f8f8f8;
  display: block;
}
.custom-title {
  font-size: 1.01rem;
  font-weight: 600;
  margin: 0.7rem 0 0.15rem 0;
  padding: 0 0.6rem;
  text-align: left;
}
.custom-meta {
  font-size: 0.92rem;
  color: #888;
  margin-bottom: 0.2rem;
  padding: 0 0.6rem;
  text-align: left;
}
.custom-meta-counts {
  font-size: 0.89rem;
  color: #b70d1f;
  padding: 0 0.6rem 0.7rem 0.6rem;
  display: flex;
  gap: 1.1em;
}
.custom-meta-counts .like { color: #e60023; }
.custom-meta-counts .comment { color: #1976d2; }

/* Masonry 전체 쓰레드 */
.masonry-section {
  width: 100%;
  margin: 0 auto;
  background: #faf8f6;
  padding-bottom: 3rem;
}
.masonry-title {
  font-size: 1.22rem;
  font-weight: 700;
  margin: 2.5rem 0 1.5rem 0.5vw;
  text-align: left;
  color: #222;
}
.masonry-grid {
  max-width: 1200px;
  margin: 0 auto;
  column-count: 5;
  column-gap: 1.2rem;
  padding: 0 1vw;
}
.masonry-grid .custom-card {
  display: inline-block;
  width: 210px;
  max-width: 100%;
  margin: 0 0 1.2rem 0;
}

/* 반응형 */
@media (max-width: 1200px) {
  .main-content, .masonry-grid { max-width: 98vw; }
  .masonry-grid { column-count: 4; }
}
@media (max-width: 900px) {
  .main-content { padding: 1.2rem 0.5vw 1.2rem 0.5vw; }
  .masonry-grid { column-count: 3; }
}
@media (max-width: 700px) {
  .masonry-grid { column-count: 2; }
  .custom-card, .masonry-grid .custom-card { width: 95vw; max-width: 95vw; }
  .custom-img { height: 38vw; min-height: 120px; max-height: 180px; }
}
@media (max-width: 500px) {
  .masonry-grid { column-count: 1; }
  .custom-card, .masonry-grid .custom-card { width: 98vw; max-width: 98vw; }
  .custom-img { height: 46vw; min-height: 110px; max-height: 170px; }
}
.info-state, .error-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}
.error-state { color: #dc3545; }
.pagination {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 2rem 0;
}
</style>

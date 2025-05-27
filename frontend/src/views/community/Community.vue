<template>
  <div class="book-home">
    <!-- 메인 카드 그리드 -->
    <main class="main-grid">
      <!-- 인기 쓰레드 -->
      <section class="main-col">
        <h2 class="section-title"><span>🔥</span> 인기 쓰레드</h2>
        
        <div v-if="isPopularLoading" class="popular-loading">
          <div class="loading-spinner"></div>
          <p>인기 쓰레드를 불러오는 중...</p>
        </div>
        
        <div v-else-if="popularError" class="error-container">
          <p>{{ popularError }}</p>
          <button @click="fetchPopularThreads()" class="retry-btn">다시 시도</button>
        </div>
        
        <div v-else-if="popularThreads.length === 0" class="empty-container">
          <p>아직 인기 쓰레드가 없습니다.</p>
        </div>
        
        <div v-else class="popular-slider-container">
          <button class="slider-nav-btn prev-btn" @click="slidePrev" :disabled="isSliding">
            <span>◀</span>
          </button>
          
          <div class="popular-slider" :class="{ 'is-sliding': isSliding }">
            <!-- 이전 쓰레드 미리보기 -->
            <router-link
              v-if="displayIndexes.prev !== -1"
              :to="{ name: 'ThreadDetail', params: { id: popularThreads[displayIndexes.prev].id } }"
              class="slider-card prev-card"
              @click.native="slidePrev"
            >
              <div class="slider-card-content">
                <div class="thread-header">
                  <div class="thread-user-info">
                    <img
                      class="avatar"
                      :src="
                        popularThreads[displayIndexes.prev].user.profile_image || '/public/default-profile.png.jpg'
                      "
                      :alt="popularThreads[displayIndexes.prev].user.username"
                    />
                    <span class="user-name">{{
                      popularThreads[displayIndexes.prev].user.nickname || popularThreads[displayIndexes.prev].user.username
                    }}</span>
                  </div>
                </div>
                
                <img
                  v-if="popularThreads[displayIndexes.prev].book && popularThreads[displayIndexes.prev].book.cover"
                  class="card-img"
                  :src="popularThreads[displayIndexes.prev].book.cover"
                  :alt="popularThreads[displayIndexes.prev].book.title"
                />
                <div v-else class="card-img placeholder-img">
                  <span>📚</span>
                </div>
                
                <div class="card-title">{{ popularThreads[displayIndexes.prev].title }}</div>
              </div>
            </router-link>
            
            <!-- 현재 쓰레드 (가운데 큰 카드) -->
            <router-link
              :to="{ name: 'ThreadDetail', params: { id: popularThreads[displayIndexes.current].id } }"
              class="slider-card current-card"
            >
              <div class="slider-card-content">
                <div class="thread-header">
                  <div class="thread-user-info">
                    <img
                      class="avatar"
                      :src="
                        popularThreads[displayIndexes.current].user.profile_image || '/public/default-profile.png.jpg'
                      "
                      :alt="popularThreads[displayIndexes.current].user.username"
                    />
                    <span class="user-name">{{
                      popularThreads[displayIndexes.current].user.nickname || popularThreads[displayIndexes.current].user.username
                    }}</span>
                  </div>
                  <span class="thread-date">{{ formatDate(popularThreads[displayIndexes.current].created_at) }}</span>
                </div>
                
                <div class="current-card-main">
                  <img
                    v-if="popularThreads[displayIndexes.current].book && popularThreads[displayIndexes.current].book.cover"
                    class="card-img"
                    :src="popularThreads[displayIndexes.current].book.cover"
                    :alt="popularThreads[displayIndexes.current].book.title"
                  />
                  <div v-else class="card-img placeholder-img">
                    <span>📚</span>
                  </div>
                  
                  <div class="current-card-info">
                    <div v-if="popularThreads[displayIndexes.current].book" class="card-caption">
                      {{ popularThreads[displayIndexes.current].book.title }}
                    </div>
                    <div v-else class="card-caption">인기 쓰레드</div>
                    
                    <div class="card-title">{{ popularThreads[displayIndexes.current].title }}</div>
                    
                    <div class="card-footer">
                      <span class="like-count">❤️ {{ popularThreads[displayIndexes.current].like_count }}</span>
                      <span class="comment-count">💬 {{ popularThreads[displayIndexes.current].comment_count }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </router-link>
            
            <!-- 다음 쓰레드 미리보기 -->
            <router-link
              v-if="displayIndexes.next !== -1"
              :to="{ name: 'ThreadDetail', params: { id: popularThreads[displayIndexes.next].id } }"
              class="slider-card next-card"
              @click.native="slideNext"
            >
              <div class="slider-card-content">
                <div class="thread-header">
                  <div class="thread-user-info">
                    <img
                      class="avatar"
                      :src="
                        popularThreads[displayIndexes.next].user.profile_image || '/public/default-profile.png.jpg'
                      "
                      :alt="popularThreads[displayIndexes.next].user.username"
                    />
                    <span class="user-name">{{
                      popularThreads[displayIndexes.next].user.nickname || popularThreads[displayIndexes.next].user.username
                    }}</span>
                  </div>
                </div>
                
                <img
                  v-if="popularThreads[displayIndexes.next].book && popularThreads[displayIndexes.next].book.cover"
                  class="card-img"
                  :src="popularThreads[displayIndexes.next].book.cover"
                  :alt="popularThreads[displayIndexes.next].book.title"
                />
                <div v-else class="card-img placeholder-img">
                  <span>📚</span>
                </div>
                
                <div class="card-title">{{ popularThreads[displayIndexes.next].title }}</div>
              </div>
            </router-link>
          </div>
          
          <button class="slider-nav-btn next-btn" @click="slideNext" :disabled="isSliding">
            <span>▶</span>
          </button>
          
          <!-- 슬라이더 인디케이터 -->
          <div class="slider-indicators">
            <button
              v-for="(thread, index) in popularThreads"
              :key="index"
              class="indicator-dot"
              :class="{ active: index === currentPopularIndex }"
              @click="slideTo(index)"
            ></button>
          </div>
        </div>
      </section>
    </main>

    <!-- 전체 쓰레드 섹션 -->
    <section class="club-section">
      <div class="club-header">
        <h2>전체 쓰레드</h2>
        <div class="pagination-controls" v-if="totalCount > 0">
          <button
            class="pagination-btn"
            :disabled="!prevPage"
            @click="loadPrevPage"
            :class="{ disabled: !prevPage }"
          >
            이전
          </button>
          <span class="pagination-info"
            >{{ currentPage }} / {{ Math.ceil(totalCount / 20) }} 페이지</span
          >
          <button
            class="pagination-btn"
            :disabled="!nextPage"
            @click="loadNextPage"
            :class="{ disabled: !nextPage }"
          >
            다음
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>쓰레드를 불러오는 중...</p>
      </div>

      <div v-else-if="error" class="error-container">
        <p>{{ error }}</p>
        <button @click="fetchThreads()" class="retry-btn">다시 시도</button>
      </div>

      <div v-else-if="threads.length === 0" class="empty-container">
        <p>아직 쓰레드가 없습니다.</p>
      </div>

      <div v-else class="club-grid">
        <router-link
          v-for="thread in threads"
          :key="thread.id"
          :to="{ name: 'ThreadDetail', params: { id: thread.id } }"
          class="club-card thread-card"
        >
          <div class="thread-header">
            <div class="thread-user-info">
              <img
                class="avatar"
                :src="
                  thread.user.profile_image || '/public/default-profile.png.jpg'
                "
                :alt="thread.user.username"
              />
              <span class="user-name">{{
                thread.user.nickname || thread.user.username
              }}</span>
            </div>
            <span class="thread-date">{{ formatDate(thread.created_at) }}</span>
          </div>

          <img
            v-if="thread.book && thread.book.cover"
            class="card-img"
            :src="thread.book.cover"
            :alt="thread.book.title"
          />
          <div v-else class="card-img placeholder-img">
            <span>📚</span>
          </div>

          <div class="card-caption" v-if="thread.book">
            {{ thread.book.title }}
          </div>
          <div class="card-caption" v-else>쓰레드</div>

          <div class="card-title">{{ thread.title }}</div>

          <div class="card-footer">
            <span class="like-count">❤️ {{ thread.like_count }}</span>
            <span class="comment-count">💬 {{ thread.comment_count }}</span>
          </div>
        </router-link>
      </div>

      <div class="pagination-container" v-if="totalCount > 20">
        <button
          class="pagination-btn"
          :disabled="!prevPage"
          @click="loadPrevPage"
          :class="{ disabled: !prevPage }"
        >
          이전
        </button>
        <span class="pagination-info"
          >{{ currentPage }} / {{ Math.ceil(totalCount / 20) }} 페이지</span
        >
        <button
          class="pagination-btn"
          :disabled="!nextPage"
          @click="loadNextPage"
          :class="{ disabled: !nextPage }"
        >
          다음
        </button>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      threads: [],
      currentPage: 1,
      totalCount: 0,
      nextPage: null,
      prevPage: null,
      isLoading: false,
      error: null,
      // 인기 쓰레드 관련 데이터
      popularThreads: [],
      currentPopularIndex: 0,
      isPopularLoading: false,
      popularError: null,
      autoSlideInterval: null,
      isSliding: false
    };
  },
  created() {
    this.fetchThreads();
    this.fetchPopularThreads();
  },
  mounted() {
    // 자동 슬라이드 시작 (5초마다)
    this.startAutoSlide();
  },
  beforeUnmount() {
    // 컴포넌트 언마운트 시 자동 슬라이드 중지
    this.stopAutoSlide();
  },
  computed: {
    // 현재 표시할 쓰레드와 그 앞뒤의 쓰레드 인덱스를 계산
    displayIndexes() {
      if (this.popularThreads.length <= 1) return { prev: -1, current: 0, next: -1 };
      
      const current = this.currentPopularIndex;
      const max = this.popularThreads.length - 1;
      
      const prev = current === 0 ? max : current - 1;
      const next = current === max ? 0 : current + 1;
      
      return { prev, current, next };
    }
  },
  methods: {
    async fetchThreads(page = 1) {
      try {
        this.isLoading = true;
        const response = await axios.get(
          `/api/threads/?page=${page}&page_size=20`
        );
        this.threads = response.data.results;
        this.totalCount = response.data.count;
        this.nextPage = response.data.next;
        this.prevPage = response.data.previous;
        this.currentPage = page;
      } catch (error) {
        console.error("쓰레드를 불러오는 중 오류가 발생했습니다:", error);
        this.error = "쓰레드를 불러오는 중 오류가 발생했습니다.";
      } finally {
        this.isLoading = false;
      }
    },
    async fetchPopularThreads() {
      try {
        this.isPopularLoading = true;
        const response = await axios.get('/api/threads/popular/');
        this.popularThreads = response.data;
        this.popularError = null;
      } catch (error) {
        console.error("인기 쓰레드를 불러오는 중 오류가 발생했습니다:", error);
        this.popularError = "인기 쓰레드를 불러오는 중 오류가 발생했습니다.";
      } finally {
        this.isPopularLoading = false;
      }
    },
    // 슬라이드 이동 메서드
    slidePrev() {
      if (this.isSliding || this.popularThreads.length <= 1) return;
      this.isSliding = true;
      
      const max = this.popularThreads.length - 1;
      this.currentPopularIndex = this.currentPopularIndex === 0 ? max : this.currentPopularIndex - 1;
      
      // 슬라이드 애니메이션 시간 후 상태 초기화
      setTimeout(() => {
        this.isSliding = false;
      }, 500);
      
      // 자동 슬라이드 재설정
      this.resetAutoSlide();
    },
    slideNext() {
      if (this.isSliding || this.popularThreads.length <= 1) return;
      this.isSliding = true;
      
      const max = this.popularThreads.length - 1;
      this.currentPopularIndex = this.currentPopularIndex === max ? 0 : this.currentPopularIndex + 1;
      
      // 슬라이드 애니메이션 시간 후 상태 초기화
      setTimeout(() => {
        this.isSliding = false;
      }, 500);
      
      // 자동 슬라이드 재설정
      this.resetAutoSlide();
    },
    // 특정 인덱스로 이동
    slideTo(index) {
      if (this.isSliding || index === this.currentPopularIndex) return;
      this.isSliding = true;
      this.currentPopularIndex = index;
      
      setTimeout(() => {
        this.isSliding = false;
      }, 500);
      
      // 자동 슬라이드 재설정
      this.resetAutoSlide();
    },
    // 자동 슬라이드 시작
    startAutoSlide() {
      this.autoSlideInterval = setInterval(() => {
        if (!this.isSliding && this.popularThreads.length > 1) {
          this.slideNext();
        }
      }, 5000); // 5초마다 자동 슬라이드
    },
    // 자동 슬라이드 중지
    stopAutoSlide() {
      if (this.autoSlideInterval) {
        clearInterval(this.autoSlideInterval);
        this.autoSlideInterval = null;
      }
    },
    // 자동 슬라이드 재설정 (사용자가 수동으로 이동했을 때)
    resetAutoSlide() {
      this.stopAutoSlide();
      this.startAutoSlide();
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat("ko-KR", {
        year: "numeric",
        month: "long",
        day: "numeric",
      }).format(date);
    },
    loadNextPage() {
      if (this.nextPage) {
        this.fetchThreads(this.currentPage + 1);
      }
    },
    loadPrevPage() {
      if (this.prevPage) {
        this.fetchThreads(this.currentPage - 1);
      }
    },
  },
};
</script>

<style scoped>
.book-home {
  margin-top: 50px;
  background: #fff;
  color: #181818;
  min-height: 100vh;
  font-family: "Inter", "Segoe UI", Arial, sans-serif;
}
.main-header {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.7rem 2vw 0.8rem 2vw;
  text-align: center;
}
.header-row {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1.2rem;
  margin-bottom: 1.6rem;
}
.search-bar {
  flex: 1 1 350px;
  max-width: 350px;
  min-width: 180px;
  padding: 0.7rem 1.3rem;
  border: 1.5px solid #ececec;
  border-radius: 21px;
  font-size: 1.07rem;
  background: #fafafa;
  margin-right: auto;
}
.header-actions {
  display: flex;
  gap: 0.8rem;
}
.login-btn {
  background: none;
  border: 1.5px solid #888;
  color: #222;
  font-weight: 500;
  border-radius: 20px;
  padding: 0.45em 1.5em;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
}
.login-btn:hover {
  background: #f5f5f5;
}
.join-btn {
  background: #7c3aed;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 0.45em 1.5em;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.16s;
}
.join-btn:hover {
  background: #5b21b6;
}
.site-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1.7rem;
  letter-spacing: -1px;
  line-height: 1.2;
}
.tab-nav {
  display: flex;
  justify-content: center;
  gap: 1.2rem;
  margin-bottom: 2.5rem;
  border-bottom: 1.5px solid #ececec;
  padding-bottom: 0.7rem;
}
.tab-link {
  color: #222;
  font-size: 1.04rem;
  font-weight: 500;
  padding: 0.4em 1.2em;
  border-radius: 14px 14px 0 0;
  background: none;
  cursor: pointer;
  border: none;
  transition: background 0.16s, color 0.16s;
}
.tab-link.active,
.tab-link:hover {
  background: #f5f5f5;
  color: #7c3aed;
}

.main-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  gap: 2.2rem;
  margin-bottom: 2.7rem;
}
.main-col {
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}
.section-title {
  font-weight: 700;
  margin-bottom: 0.7rem;
  display: flex;
  align-items: center;
  gap: 0.5em;
}
.main-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  padding: 1.2rem 1.2rem 1rem 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
  min-height: 120px;
}
.card-img {
  width: 100%;
  max-width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 0.7rem;
  background: #f5f5f5;
}
.card-episode .card-row {
  display: flex;
  align-items: center;
  gap: 0.7em;
  margin-bottom: 0.6em;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background: #e0e0e0;
}
.card-label {
  font-size: 1.01rem;
  color: #7c3aed;
  font-weight: 600;
}
.card-caption {
  color: #888;
  font-size: 0.98rem;
  margin-bottom: 0.1rem;
  font-weight: 500;
}
.card-title {
  font-size: 1.13rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
  color: #181818;
}
.card-desc {
  font-size: 1.01rem;
  color: #444;
  margin-bottom: 0.5rem;
}
.card-footer {
  font-size: 0.93rem;
  color: #888;
  margin-top: 0.3rem;
}

.club-section {
  max-width: 1200px;
  margin: 0 auto 2.7rem auto;
  padding-top: 2.3rem;
  border-top: 1.5px solid #ececec;
}
.club-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.3rem;
  gap: 1.5rem;
}
.club-header h2 {
  font-size: 1.23rem;
  font-weight: 700;
}
.club-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.4rem;
  margin-bottom: 1.5rem;
}
.club-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
}
.club-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}
.club-card .card-img {
  width: 100%;
  height: 180px;
  margin-bottom: 0.6rem;
  object-fit: cover;
  border-radius: 12px;
  background: #f5f5f5;
}
.placeholder-img {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f0f0f0;
  font-size: 3rem;
  color: #999;
}
.club-card .card-caption {
  color: #888;
  font-size: 0.96rem;
  margin-bottom: 0.1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}
.club-card .card-title {
  font-size: 1.07rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
  color: #181818;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
  width: 100%;
}
.club-card .card-footer {
  font-size: 0.92rem;
  color: #888;
  margin-top: 0.5rem;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

/* 쓰레드 관련 추가 스타일 */
.thread-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 0.7rem;
}

.thread-user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
}

.thread-date {
  font-size: 0.8rem;
  color: #888;
}

.like-count,
.comment-count {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.9rem;
}

/* 인기 쓰레드 슬라이더 스타일 */
.popular-slider-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 1rem 0;
  min-height: 300px;
}

.popular-slider {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 100%;
  transition: transform 0.5s ease;
}

.slider-card {
  position: absolute;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  text-decoration: none;
  color: inherit;
  transition: all 0.4s ease;
  overflow: hidden;
}

.slider-card-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

.current-card {
  z-index: 10;
  width: 60%;
  transform: scale(1);
  opacity: 1;
}

.current-card-main {
  display: flex;
  gap: 1rem;
}

.current-card-main .card-img {
  width: 40%;
  height: 180px;
  flex-shrink: 0;
}

.current-card-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.prev-card, .next-card {
  width: 30%;
  transform: scale(0.8);
  opacity: 0.6;
  z-index: 5;
  pointer-events: auto;
}

.prev-card {
  left: 0;
  transform: translateX(-50%) scale(0.8);
}

.next-card {
  right: 0;
  transform: translateX(50%) scale(0.8);
}

.slider-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: #7c3aed;
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 20;
  transition: background 0.2s, opacity 0.2s;
}

.slider-nav-btn:hover {
  background: #6d28d9;
}

.slider-nav-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  opacity: 0.5;
}

.prev-btn {
  left: 10px;
}

.next-btn {
  right: 10px;
}

.slider-indicators {
  position: absolute;
  bottom: -10px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  z-index: 15;
}

.indicator-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}

.indicator-dot.active {
  background: #7c3aed;
  transform: scale(1.2);
}

.popular-loading, .popular-error {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 애니메이션 */
.is-sliding .slider-card {
  transition: all 0.5s ease;
}

/* 페이지네이션 스타일 */
.pagination-container,
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 1.5rem 0;
}

.pagination-btn {
  background: #7c3aed;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.4rem 1.2rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
}

.pagination-btn:hover {
  background: #6d28d9;
}

.pagination-btn.disabled {
  background: #ccc;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.9rem;
  color: #666;
}

/* 로딩 및 에러 상태 스타일 */
.loading-container,
.error-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  width: 100%;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #7c3aed;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.retry-btn {
  background: #7c3aed;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.4rem 1.2rem;
  font-size: 0.9rem;
  cursor: pointer;
  margin-top: 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 반응형 */
@media (max-width: 1100px) {
  .main-header,
  .main-grid,
  .club-section,
  .editor-section {
    max-width: 98vw;
  }
  .main-grid {
    gap: 1.2rem;
  }
  .club-grid,
  .editor-grid {
    gap: 1rem;
  }
  .current-card-main {
    flex-direction: column;
  }
  .current-card-main .card-img {
    width: 100%;
  }
}

@media (max-width: 900px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
  .main-col {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
  }
  .main-card,
  .club-card,
  .editor-card {
    width: 100%;
  }
  .club-grid,
  .editor-grid {
    grid-template-columns: 1fr 1fr;
  }
  .popular-slider-container {
    padding: 0;
  }
  .prev-card, .next-card {
    display: none;
  }
  .current-card {
    width: 90%;
  }
}

@media (max-width: 600px) {
  .main-header,
  .main-grid,
  .club-section,
  .editor-section {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  .site-title {
    font-size: 1.6rem;
  }
  .tab-nav {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  .club-grid,
  .editor-grid {
    grid-template-columns: 1fr;
  }
  .current-card {
    width: 100%;
  }
}
</style>

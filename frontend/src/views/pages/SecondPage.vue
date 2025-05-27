<template>
  <div class="page second-page">
    <div class="recommend-section">
      <!-- 상태에 따른 컴포넌트 전환 -->
      <Transition name="fade" mode="out-in">
        <!-- 비로그인 상태 -->
        <div v-if="!authStore.isAuthenticated" class="login-prompt" key="login">
          <div class="content-wrapper">
            <h2>로그인 하고<br />AI 추천 도서를 확인해보세요!</h2>
            <p class="subtitle">당신만을 위한 맞춤 도서 추천</p>
            <button
              @click="goToLogin"
              class="login-button"
              aria-label="로그인 페이지로 이동"
            >
              <span>로그인하기</span>
              <i class="arrow-icon" aria-hidden="true">↓</i>
            </button>
          </div>
        </div>

        <!-- 로그인 상태 -->
        <div v-else class="recommendations" key="recommendations">
          <Transition name="fade" mode="out-in">
            <!-- 로딩 상태 -->
            <div v-if="isLoading" class="loading-container" key="loading">
              <div class="books-grid">
                <div
                  v-for="i in 5"
                  :key="i"
                  class="book-card skeleton"
                  aria-hidden="true"
                >
                  <div class="skeleton-image"></div>
                  <div class="skeleton-content">
                    <div class="skeleton-title"></div>
                    <div class="skeleton-text"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 에러 상태 -->
            <div v-else-if="error" class="error" key="error" role="alert">
              <div class="error-content">
                <span class="error-icon" aria-hidden="true">⚠️</span>
                <h3>알림</h3>
                <p>{{ error }}</p>
                <button
                  v-if="error.includes('프로필')"
                  @click="goToProfile"
                  class="action-button"
                >
                  프로필 수정하기
                </button>
                <button
                  v-else
                  @click="fetchRecommendedBooks"
                  class="action-button"
                >
                  다시 시도하기
                </button>
              </div>
            </div>

            <!-- 콘텐츠 상태 -->
            <div v-else class="books-grid" key="content">
              <TransitionGroup
                name="book-list"
                tag="div"
                class="books-grid-inner"
                @after-enter="handleAfterEnter"
              >
                <RecommendBook
                  :book="book"
                  v-for="(book, index) in recommendedBooks"
                  :key="book.id"
                  class="book-card"
                  :style="{ animationDelay: `${index * 0.1}s` }"
                  @click="handleBookSelect(index)"
                />
              </TransitionGroup>
            </div>
          </Transition>
        </div>
      </Transition>
    </div>
    <div v-if="showNextDiv" class="next-show">
      <h1 class="tracking-in-expand recommend-title">내가 좋아할 만한 도서</h1>
      <div
        class="book-detail-container"
        :class="{ 'fade-in-fwd': true }"
        :key="animationKey"
        v-if="selectedBookDetail"
      >
        <div class="book-detail-content">
          <img
            :src="selectedBookDetail.cover"
            :alt="selectedBookDetail.title"
            class="book-cover"
          />          <div class="book-info">
            <h2 class="book-title">{{ selectedBookDetail.title }}</h2>
            <p class="book-author">저자: {{ selectedBookDetail.author }}</p>
          </div>
          <RouterLink
            :to="`/books/${selectedBookDetail.id}`"
            class="book-detail-link"
          >
            <span>도서 상세 정보</span>
            <i class="arrow-icon">→</i>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineAsyncComponent, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAuthStore } from "../../stores/auth";
import { RouterLink } from "vue-router";

// 상수 정의
const API_ENDPOINT = "http://127.0.0.1:8000/api/accounts/recommended-books/";
const ERROR_MESSAGES = {
  PROFILE_INCOMPLETE:
    "사용자 프로필 데이터가 부족합니다. 관심 카테고리나 자기소개를 추가해주세요.",
  FETCH_FAILED: "추천 도서를 불러오는데 실패했습니다.",
};

// 컴포넌트 지연 로딩
const RecommendBook = defineAsyncComponent(() =>
  import("../../components/books/RecommendBook.vue")
);

// props 정의
const props = defineProps({
  goToFirstPage: {
    type: Function,
    required: true,
  },
});

const router = useRouter();
const authStore = useAuthStore();

// 상태 변수들
const recommendedBooks = ref([]);
const isLoading = ref(false);
const error = ref(null);
const selectedBook = ref(-1); // 현재 선택된 도서

const showNextDiv = ref(false);

function handleAfterEnter() {
  // 모든 리스트 애니메이션이 끝난 뒤 호출됨
  showNextDiv.value = true;
}

// 네비게이션 함수
const goToLogin = () => {
  props.goToFirstPage();
};

const goToProfile = () => {
  router.push("/mypage");
};

// API 요청 함수
const fetchRecommendedBooks = async () => {
  if (!authStore.isAuthenticated) return;

  isLoading.value = true;
  error.value = null;

  try {
    const response = await axios.get(API_ENDPOINT, {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`,
      },
    });
    recommendedBooks.value = response.data.slice(0, 5); // 최대 5개만 표시
  } catch (err) {
    error.value =
      err.response?.status === 400
        ? ERROR_MESSAGES.PROFILE_INCOMPLETE
        : ERROR_MESSAGES.FETCH_FAILED;
    console.error("Error fetching recommended books:", err);
  } finally {
    isLoading.value = false;
  }
};

// 도서 선택 핸들러
const handleBookSelect = (book) => {
  selectedBook.value = book;
};

// computed 속성 추가
const selectedBookDetail = computed(() => {
  if (!recommendedBooks.value.length) return null;
  return recommendedBooks.value[selectedBook.value];
});

// 애니메이션 상태 관리
const animationKey = ref(0);

// selectedBook이 변경될 때마다 애니메이션 트리거
watch(selectedBook, () => {
  animationKey.value++;
});

// 라이프사이클 훅
onMounted(() => {
  if (authStore.isAuthenticated) {
    fetchRecommendedBooks().then(() => {
      if (recommendedBooks.value.length > 0) {
        selectedBook.value = recommendedBooks.value[0]; // 첫 번째 도서로 초기화
      }
    });
  }
});
</script>

<style scoped>
.page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background-color: #ffffff;
  padding-top: calc(var(--navbar-height) + 2rem);
  display: flex;
  /* justify-content: center; */
  align-items: flex-start;
  flex-direction: column;
}

.next-show {
  /* position: absolute; */
  top: 0px;
  left: 0;
  width: 100%;
  height: 100%;
  flex-direction: column;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 0;
  /* background-color: rgba(255, 255, 255, 0.8); */
}

.tracking-in-expand {
  -webkit-animation: tracking-in-expand 0.7s cubic-bezier(0.215, 0.61, 0.355, 1)
    both;
  animation: tracking-in-expand 0.7s cubic-bezier(0.215, 0.61, 0.355, 1) both;
}

/* ----------------------------------------------
 * Generated by Animista on 2025-5-27 16:47:18
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info. 
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation tracking-in-expand
 * ----------------------------------------
 */
@-webkit-keyframes tracking-in-expand {
  0% {
    letter-spacing: -0.5em;
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}
@keyframes tracking-in-expand {
  0% {
    letter-spacing: -0.5em;
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}

.recommend-title {
  position: absolute;
  top: 30rem;
}

.recommend-section {
  width: 90%;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  text-align: center;
}

.login-prompt {
  padding: 4rem;
  background: #ffffff;
  border-radius: 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  max-width: 600px;
  margin: 0 auto;
}

.login-prompt:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.login-prompt h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 600;
  line-height: 1.4;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.login-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 500;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.arrow-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.login-button:hover {
  background-color: #34495e;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.login-button:hover .arrow-icon {
  transform: translateY(4px);
}

.recommendations {
  width: 100%;
  /* 로그인 상태일 때 추천 도서 섹션 스타일 */
}

.books-grid {
  display: flex;
  /* grid-template-columns: repeat(5, 1fr); */
  gap: 2rem;
  padding: 2rem;
  background: #ffffff;
  border-radius: 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 400px;
  width: 100%;
}

/* 스켈레톤 로딩 스타일 */
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: #f0f0f0;
  border-radius: 1.5rem;
  overflow: hidden;
  position: relative;
}

.skeleton-image {
  width: 100%;
  height: 280px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e3e3e3 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2.5s infinite;
}

.skeleton-content {
  padding: 1rem;
}

.skeleton-title {
  height: 24px;
  margin-bottom: 0.8rem;
  background: linear-gradient(90deg, #f0f0f0 25%, #e3e3e3 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2.5s infinite;
  border-radius: 4px;
}

.skeleton-text {
  height: 16px;
  width: 60%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e3e3e3 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2.5s infinite;
  border-radius: 4px;
}

/* 에러 상태 스타일 */
.error {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-content {
  text-align: center;
  padding: 3rem;
  background: #ffffff;
  border-radius: 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  max-width: 500px;
}

.error-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: block;
}

.error-content h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.error-content p {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.action-button {
  padding: 0.8rem 2rem;
  font-size: 1rem;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #34495e;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* 페이드 애니메이션 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 책 리스트 애니메이션 */
.books-grid-inner {
  display: flex;
  gap: 2rem;
  width: 100%;
  justify-content: center;
  align-items: center;
}

.book-list-enter-active {
  transition: all 0.6s ease;
  animation: fadeInUp 0.6s ease forwards;
}

.book-list-leave-active {
  transition: all 0.6s ease;
  position: absolute;
}

.book-list-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.book-list-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 책 카드 호버 효과 */
.book-card {
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease forwards;
  animation-fill-mode: both;
  /* background-color: #2c3e50; */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.book-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.fade-in-fwd {
  -webkit-animation: fade-in-fwd 0.6s cubic-bezier(0.39, 0.575, 0.565, 1) both;
  animation: fade-in-fwd 0.6s cubic-bezier(0.39, 0.575, 0.565, 1) both;
}

/* ----------------------------------------------
 * Generated by Animista on 2025-5-27 17:40:5
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info. 
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation fade-in-fwd
 * ----------------------------------------
 */
@-webkit-keyframes fade-in-fwd {
  0% {
    -webkit-transform: translateZ(-80px);
    transform: translateZ(-80px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateZ(0);
    transform: translateZ(0);
    opacity: 1;
  }
}
@keyframes fade-in-fwd {
  0% {
    -webkit-transform: translateZ(-80px);
    transform: translateZ(-80px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateZ(0);
    transform: translateZ(0);
    opacity: 1;
  }
}

/* 도서 상세 정보 스타일 */
.book-detail-container {
  /* background: rgba(255, 255, 255, 0.95); */
  /* border-radius: 20px; */
  padding: 2rem;
  /* box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1); */
  width: 90%;
  max-width: 1000px;
  margin-top: 2rem;
  backdrop-filter: blur(10px);
  position: relative;
  min-height: 400px;
}

.book-detail-content {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.book-cover {
  width: 250px;
  height: 350px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.book-info {
  flex: 1;
  text-align: left;
}

.book-title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.book-author,
.book-publisher,
.book-published-date {
  color: #666;
  margin: 0.5rem 0;
}

.book-detail-link {
  position: absolute;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
  text-decoration: none;
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.book-detail-link:hover {
  background-color: #34495e;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.book-detail-link .arrow-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.book-detail-link:hover .arrow-icon {
  transform: translateX(4px);
}

@media (max-width: 1200px) {
  .recommend-section {
    width: 95%;
  }
}

@media (max-width: 768px) {
  .recommend-section {
    width: 100%;
    padding: 1rem;
  }

  .login-prompt h2 {
    font-size: 1.5rem;
  }

  .book-detail-content {
    flex-direction: column;
    align-items: center;
  }

  .book-cover {
    width: 200px;
  }

  .book-info {
    text-align: center;
  }
}
</style>

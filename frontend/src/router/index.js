import { createRouter, createWebHistory } from 'vue-router'

// 메인 페이지
import MainPage from '@/views/MainPage.vue'

// 인증 관련 페이지
import LoginPage from '@/views/auth/LoginPage.vue'
import SignupPage from '@/views/auth/SignupPage.vue'
import PasswordResetPage from '@/views/auth/PasswordResetPage.vue'

// 도서 관련 페이지
import BookList from '@/views/books/BookList.vue'
import BookDetail from '@/views/books/BookDetail.vue'

// 커뮤니티 관련 페이지
import Community from '@/views/community/Community.vue'

// 도서관 관련 페이지
import LibraryPage from '@/views/library/LibraryPage.vue'

// 사용자 관련 페이지
import MyPage from '@/views/user/MyPage.vue'
import AdminDashboard from '@/views/user/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage
  },
  // 인증 관련 라우트
  {
    path: '/auth/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/auth/signup',
    name: 'SignupPage',
    component: SignupPage
  },
  {
    path: '/auth/password-reset',
    name: 'PasswordResetPage',
    component: PasswordResetPage
  },
  // 도서 관련 라우트
  {
    path: '/books',
    name: 'BookList',
    component: BookList
  },
  {
    path: '/books/:id',
    name: 'BookDetail',
    component: BookDetail,
    props: true
  },
  // 커뮤니티 관련 라우트
  {
    path: '/community',
    name: 'Community',
    component: Community
  },
  {
    path: '/threads/:id',
    name: 'ThreadDetail',
    component: () => import('@/views/community/ThreadDetail.vue'),
    props: true
  },
  {
    path: '/threads/write',
    name: 'ThreadWrite',
    component: () => import('@/views/community/ThreadWrite.vue')
  },
  // 도서관 관련 라우트
  {
    path: '/library',
    name: 'LibraryPage',
    component: LibraryPage
  },
  // 사용자 관련 라우트
  {
    path: '/mypage',
    name: 'MyPage',
    component: MyPage
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  // 404 페이지
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 글로벌 네비게이션 가드 (인증 체크, 로그 등)
router.beforeEach((to, from, next) => {
  // TODO: 인증 체크 로직 구현
  next()
})

export default router

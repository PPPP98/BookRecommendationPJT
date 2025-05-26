import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: () => import('@/views/MainPage.vue')
  },
  // 인증 관련 라우트
  {
    path: '/auth/login',
    name: 'LoginPage',
    component: () => import('@/views/auth/LoginPage.vue')
  },
  {
    path: '/auth/signup',
    name: 'SignupPage',
    component: () => import('@/views/auth/SignupPage.vue')
  },
  {
    path: '/auth/password-reset',
    name: 'PasswordResetPage',
    component: () => import('@/views/auth/PasswordResetPage.vue')
  },
  // 도서 관련 라우트
  {
    path: '/books',
    name: 'BookList',
    component: () => import('@/views/books/BookList.vue')
  },
  {
    path: '/books/:id',
    name: 'BookDetail',
    component: () => import('@/views/books/BookDetail.vue'),
    props: true
  },
  // 커뮤니티 관련 라우트
  {
    path: '/community',
    name: 'Community',
    component: () => import('@/views/community/Community.vue')
  },
  {
    path: '/threads/:id',
    name: 'ThreadDetail',
    component: () => import('@/views/community/ThreadDetail.vue'),
    props: true
  },
  {
    path: '/threads/:id/edit',
    name: 'ThreadEdit',
    component: () => import('@/views/community/ThreadEdit.vue'),
    props: true
  },
  {
    path: '/threads/write/:bookId?',
    name: 'ThreadWrite',
    component: () => import('@/views/community/ThreadWrite.vue'),
    props: true
  },
  // 도서관 관련 라우트
  {
    path: '/library',
    name: 'LibraryPage',
    component: () => import('@/views/library/LibraryPage.vue')
  },
  // 내 마이페이지(내 정보)
  {
    path: '/mypage',
    name: 'MyPage',
    component: () => import('@/views/user/MyPage.vue')
  },
  // 👤 사용자 프로필(마이페이지) 라우트 (작성자 클릭 시 이동)
  {
    path: '/mypage/:id',
    name: 'UserProfile',
    component: () => import('@/views/user/MyPage.vue'),
    props: true
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('@/views/user/AdminDashboard.vue')
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

// 네비게이션 가드 추가
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token')

  if (to.name === 'AdminDashboard' && !isAuthenticated) {
    alert('관리자 권한이 필요합니다. 로그인해주세요.')
    return next({ name: 'LoginPage' })
  }

  next()
})

export default router

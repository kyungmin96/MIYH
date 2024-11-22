import MovieDetail from '@/components/MovieDetail.vue'
import ArticleView from '@/views/ArticleView.vue'
import CalenderView from '@/views/CalenderView.vue'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import Moviearticle from '@/views/Moviearticle.vue'
import MyPageView from '@/views/MyPageView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ArticleDetail from '@/components/ArticleDetail.vue'
import { createRouter, createWebHistory } from 'vue-router'
import ArticleCreate from '@/views/ArticleCreate.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/calender/:userName',
      name: 'calender',
      component: CalenderView,
      meta: { requiresAuth: true }
    },
    {
      path: '/mypage/:userName',
      name: 'mypage',
      component: MyPageView,
      meta: { requiresAuth: true }
    },
    {
      path: '/movie',
      name: 'movie',
      component: Moviearticle,
      meta: { requiresAuth: true }
    },
    {
      path: '/movie/:id',
      name: 'movie-detail',
      component: MovieDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/article',
      name: 'article',
      component: ArticleView,
      meta: { requiresAuth: true }
    },
    {
      path: '/article/:id',
      name: 'article-detail',
      component: ArticleDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/article/create',
      name: 'article-create',
      component: ArticleCreate,
      meta: { requiresAuth: true }
    },
    {
      path: '/article/edit/:id',
      name: 'article-edit',
      component: () => import('@/views/ArticleEdit.vue'),
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('counter')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  // 존재하지 않는 경로로 접근했을 때
  if (!to.matched.length) {
    // 세션 초기화
    sessionStorage.clear()
    // 로그인 페이지로 리다이렉트
    next('/login')
    return
  }

  // 인증이 필요한 페이지에 대한 처리
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
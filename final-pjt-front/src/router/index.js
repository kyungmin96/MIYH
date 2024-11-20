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
      component:SignUpView ,
    },
    {
      path: '/login',
      name: 'login',
      component:LoginView ,
    },
    {
      path: '/calender/:id',
      name: 'calender',
      component:CalenderView ,
    },
    {
      path: '/mypage/:name',
      name: 'mypage',
      component:MyPageView ,
    },
    {
      path: '/movie',
      name: 'movie',
      component:Moviearticle ,
    },
    {
      path: '/movie/:id',
      name: 'movie-detail',
      component:MovieDetail ,
    },
    {
      path: '/article',
      name: 'article',
      component:ArticleView ,
    },
    {
      path: '/article/:id',
      name: 'article-detail',
      component:ArticleDetail ,
    },
    {
      path: '/article/create',
      name: 'article-create',
      component:ArticleCreate ,
    },
    {
      path: '/article/edit/:id',
      name: 'article-edit',
      component: () => import('@/views/ArticleEdit.vue')
    },
  ],
})

export default router

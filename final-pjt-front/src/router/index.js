import CalenderView from '@/views/CalenderView.vue'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import Moviearticle from '@/views/Moviearticle.vue'
import MyPageView from '@/views/MyPageView.vue'
import SignUpView from '@/views/SignUpView.vue'
import { createRouter, createWebHistory } from 'vue-router'


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
      path: '/mypage/:id',
      name: 'mypage',
      component:MyPageView ,
    },
    {
      path: '/movie',
      name: 'movie',
      component:Moviearticle ,
    },
  ],
})

export default router

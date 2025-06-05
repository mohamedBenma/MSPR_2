import { createRouter, createWebHistory } from 'vue-router'
import AppHome from '@/components/AppHome.vue'
import LoginForm from '@/components/LoginForm.vue'
import RegisterForm from '@/components/RegisterForm.vue'
const routes = [
  
   {
    path: '/home',
    name: 'Home',
    component: AppHome
  },
  
  {
    path: '/register',
    name: 'Register',
    component: RegisterForm
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

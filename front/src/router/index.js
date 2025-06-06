import { createRouter, createWebHistory } from 'vue-router'
import AppHome from '@/components/AppHome.vue'
import LoginForm from '@/components/LoginForm.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import RenewForm from '@/components/RenewForm.vue'
import DashboardPage from'@/components/DashboardPage.vue'
const routes = [
  
   {
    path: '/',
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
  },
   {
    path: '/renew',
    name: 'Renew',
    component: RenewForm
  },
  { path: '/dashboard', name: 'Dashboard', component: DashboardPage }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

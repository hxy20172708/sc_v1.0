import Vue from 'vue'
import Router from 'vue-router'
import LoginPage from './views/LoginPage.vue'
import Home from './views/Home.vue'
import ServersPage from './views/ServersPage.vue'
import RoomsPage from './views/RoomsPage.vue'
import TasksPage from './views/TasksPage.vue'
import EnvironmentsPage from './views/EnvironmentsPage.vue'
import { getToken } from './utils/auth'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'servers',
          name: 'servers',
          component: ServersPage
        },
        {
          path: 'rooms',
          name: 'rooms',
          component: RoomsPage
        },
        {
          path: 'tasks',
          name: 'tasks',
          component: TasksPage
        },
        {
          path: 'environments',
          name: 'environments',
          component: EnvironmentsPage
        }
      ]
    }
  ]
})

// 路由守卫：验证登录状态
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!getToken()) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
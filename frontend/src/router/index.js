import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        redirect: '/upload',
        meta: {requiresAuth: true}
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/LoginPage.vue')
    },
    {
        path: '/upload',
        name: 'Upload',
        component: () => import('../views/UpLoad.vue'),
        meta: {requiresAuth: true}
    },
    {
        path: '/live',
        name: 'LiveMonitor',
        component: () => import('../views/LiveMonitor.vue'),
        meta: {requiresAuth: true}
    },
    {
        path: '/history',
        name: 'History',
        component: () => import('../views/HistoryPage.vue'),
        meta: {requiresAuth: true}
    },
    {
        path: '/settings',
        name: 'Settings',
        component: () => import('../views/SettingsPage.vue'),
        meta: {requiresAuth: true}
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token')
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else {
        next()
    }
})

export default router
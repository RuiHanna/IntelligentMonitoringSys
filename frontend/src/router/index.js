import {createRouter, createWebHistory} from 'vue-router'
import LoginPage from "@/views/LoginPage.vue";
import UpLoad from "@/views/UpLoad.vue";
import LiveMonitor from "@/views/LiveMonitor.vue";
import HistoryPage from "@/views/HistoryPage.vue";
import SettingsPage from "@/views/SettingsPage.vue";

const routes = [
    {path: '/', redirect: '/login',},
    {path: '/login', component: LoginPage},
    {path: '/upload',component: UpLoad},
    {path: '/live',component: LiveMonitor},
    {path: '/history',component: HistoryPage},
    {path: '/settings',component: SettingsPage},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
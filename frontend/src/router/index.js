import { createRouter, createWebHistory } from 'vue-router';
import Monitor from '../views/MonitorPage.vue';
import Analysis from '../views/AnalysisPage.vue';
import Settings from '../views/SettingsPage.vue';

const routes = [
  { path: '/', redirect: '/monitor' },
  { path: '/monitor', component: Monitor },
  { path: '/analysis', component: Analysis },
  { path: '/settings', component: Settings },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)

// 全局配置Axios
import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:5000/api'
app.config.globalProperties.$axios = axios

app.mount('#app')
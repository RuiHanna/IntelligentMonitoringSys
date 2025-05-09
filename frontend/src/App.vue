<template>
    <div id="app">
        <!-- 导航栏 -->
        <el-menu
            mode="horizontal"
            :router="true"
            active-text-color="#409EFF"
            v-if="$route.path !== '/login'"
            default-active="/upload"
        >
            <el-menu-item index="/upload">视频上传</el-menu-item>
            <el-menu-item index="/live">实时监控</el-menu-item>
            <el-menu-item index="/history">历史数据</el-menu-item>
            <el-menu-item index="/settings">系统设置</el-menu-item>
            <div class="logout-btn">
                <el-button @click="handleLogout">退出登录</el-button>
            </div>
        </el-menu>

        <!-- 页面内容 -->
        <router-view/>
    </div>
</template>

<script setup>
import router from "@/router";

function handleLogout(){
    localStorage.removeItem('token')
    router.push('/')
}
</script>

<style scoped>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}

.logout-btn {
    float: right;
    margin: 10px 20px;
}
</style>
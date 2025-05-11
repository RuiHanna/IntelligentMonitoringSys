<template>
    <el-container style="height: 100vh;">
        <el-header height="60px">
            <el-menu mode="horizontal" background-color="#545c64" text-color="#fff">
                <el-menu-item index="1">智能监控系统</el-menu-item>
            </el-menu>
        </el-header>
        <el-container>
            <el-aside width="200px">
                <el-menu
                    default-active="$route.path"
                    router
                    class="el-menu-vertical"
                >
                    <el-menu-item index="/monitor">视频监控</el-menu-item>
                    <el-menu-item index="/analysis">数据分析</el-menu-item>
                    <el-menu-item index="/settings">系统设置</el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view/>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
// import {useRoute} from 'vue-router'
//
// const route = useRoute()
</script>

<style scoped>
.el-header {
    line-height: 60px;
    font-size: 20px;
}
</style>

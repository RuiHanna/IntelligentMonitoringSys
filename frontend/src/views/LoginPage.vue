<template>
    <div class="login-container">
        <el-card class="login-box">
            <h2>智能监控系统登录</h2>
            <el-form @submit.prevent="handleLogin">
                <el-form-item label="用户名">
                    <el-input v-model="form.username" placeholder="请输入用户名"/>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input
                        v-model="form.password"
                        type="password"
                        placeholder="请输入密码"
                        show-password
                    />
                </el-form-item>
                <el-button type="primary" native-type="submit" :loading="loading">
                    登录
                </el-button>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import axios from 'axios'

const router = useRouter()
const form = ref({
    username: '',
    password: ''
})
const loading = ref(false)

const handleLogin = async () => {
    loading.value = true
    try {
        const response = await axios.post('/login', {
            username: form.value.username,
            password: form.value.password
        })
        const {token} = response.data
        localStorage.setItem('token', token)
        ElMessage.success('登录成功')
        await router.push('/upload')
    } catch (error) {
        ElMessage.error(error.response?.data?.message || '登录失败')
    } finally {
        loading.value = false
    }
}

</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #f5f7fa;
}

.login-box {
    width: 400px;
    padding: 20px;
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

.el-button {
    width: 100%;
}
</style>
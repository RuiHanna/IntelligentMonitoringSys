<template>
    <el-card class="task-card" shadow="hover">
        <template #header>
            <div class="card-header">
                <span>任务信息</span>
                <el-tag size="small" :type="taskStatusType">{{ taskStatusText }}</el-tag>
            </div>
        </template>

        <el-descriptions :column="1" border>
            <el-descriptions-item label="任务ID">{{ taskId }}</el-descriptions-item>
            <el-descriptions-item label="状态">{{ taskStatusText }}</el-descriptions-item>
            <el-descriptions-item label="进度">
                <el-progress :percentage="progress" :status="progressStatus"/>
            </el-descriptions-item>
            <el-descriptions-item label="开始时间">{{ startTime }}</el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue'
import {ElMessage} from 'element-plus'

// eslint-disable-next-line no-undef
const props = defineProps({
    taskId: {
        type: String,
        required: true
    }
})

// 模拟数据
const taskStatus = ref('pending') // 可选: 'pending', 'running', 'success', 'failed'
const progress = ref(0)
const startTime = ref(new Date().toLocaleString())

// 根据任务状态映射展示文本与颜色
const taskStatusText = computed(() => {
    switch (taskStatus.value) {
        case 'pending':
            return '等待中'
        case 'running':
            return '运行中'
        case 'success':
            return '已完成'
        case 'failed':
            return '失败'
        default:
            return '未知'
    }
})

const taskStatusType = computed(() => {
    switch (taskStatus.value) {
        case 'pending':
            return 'info'
        case 'running':
            return 'warning'
        case 'success':
            return 'success'
        case 'failed':
            return 'danger'
        default:
            return ''
    }
})

const progressStatus = computed(() => {
    if (taskStatus.value === 'failed') return 'exception'
    if (taskStatus.value === 'success') return 'success'
    return 'active'
})

// 模拟获取任务进度
const fetchTaskStatus = async () => {
    try {
        // 模拟任务进度轮询
        taskStatus.value = 'running'
        progress.value = 0
        const interval = setInterval(() => {
            progress.value += Math.floor(Math.random() * 10) + 5
            if (progress.value >= 100) {
                progress.value = 100
                taskStatus.value = 'success'
                clearInterval(interval)
            }
        }, 500)
    } catch (e) {
        taskStatus.value = 'failed'
        ElMessage.error('任务获取失败')
    }
}

onMounted(() => {
    if (props.taskId) {
        fetchTaskStatus()
    }
})
</script>

<style scoped>
.task-card {
    margin-top: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>

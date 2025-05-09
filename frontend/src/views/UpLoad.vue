<template>
    <div class="upload-container">
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>视频上传</span>
                </div>
            </template>

            <el-tabs v-model="activeTab">
                <el-tab-pane label="文件上传" name="file">
                    <el-upload
                        drag
                        :action="uploadUrl"
                        :headers="headers"
                        :on-success="handleSuccess"
                        :before-upload="beforeUpload"
                        accept=".mp4,.avi"
                    >
                        <el-icon :size="50">
                            <upload-filled/>
                        </el-icon>
                        <div class="el-upload__text">
                            拖拽视频文件到此处或 <em>点击上传</em>
                        </div>
                        <template #tip>
                            <div class="el-upload__tip">
                                支持MP4/AVI格式，不超过500MB
                            </div>
                        </template>
                    </el-upload>
                </el-tab-pane>

                <el-tab-pane label="RTSP流" name="rtsp">
                    <el-input
                        v-model="rtspUrl"
                        placeholder="rtsp://example.com/stream"
                        clearable
                    >
                        <template #append>
                            <el-button @click="connectStream" :loading="connecting">
                                连接
                            </el-button>
                        </template>
                    </el-input>
                </el-tab-pane>
            </el-tabs>
        </el-card>

        <!-- 内联任务列表 -->
        <el-card v-if="taskId" class="task-card">
            <template #header>
                <div class="card-header">
                    <span>任务进度 (ID: {{ taskId }})</span>
                    <el-button @click="refreshTask" :loading="refreshing">
                        <el-icon>
                            <refresh/>
                        </el-icon>
                    </el-button>
                </div>
            </template>

            <el-steps :active="taskStatus.activeStep" finish-status="success">
                <el-step title="上传完成" :description="formatTime(taskStatus.uploadTime)"/>
                <el-step title="视频解析" :description="taskStatus.parseProgress"/>
                <el-step title="目标跟踪" :description="taskStatus.trackProgress"/>
                <el-step title="分析完成" :description="formatTime(taskStatus.finishTime)"/>
            </el-steps>

            <div class="task-actions">
                <el-button
                    type="primary"
                    @click="viewResults"
                    :disabled="taskStatus.activeStep < 3"
                >
                    查看结果
                </el-button>
                <el-button @click="cancelTask" :disabled="taskStatus.activeStep >= 3">
                    取消任务
                </el-button>
            </div>

            <el-divider/>

            <el-collapse>
                <el-collapse-item title="详细日志">
                    <div v-for="(log, index) in taskLogs" :key="index" class="log-item">
                        [{{ log.time }}] {{ log.message }}
                    </div>
                </el-collapse-item>
            </el-collapse>
        </el-card>
    </div>
</template>

<script setup>
import {ref, computed, onUnmounted} from 'vue'
import {UploadFilled, Refresh} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'
import {useRouter} from 'vue-router'

const router = useRouter()
const activeTab = ref('file')
const rtspUrl = ref('')
const connecting = ref(false)
const taskId = ref(null)
const refreshing = ref(false)

// 任务状态相关
const taskStatus = ref({
    activeStep: 0,
    uploadTime: null,
    parseProgress: '0%',
    trackProgress: '0%',
    finishTime: null
})

const taskLogs = ref([
    {time: new Date().toLocaleTimeString(), message: '任务已创建'}
])

const uploadUrl = computed(() => `http://localhost:5000/api/upload`)
const headers = computed(() => ({
    Authorization: `Bearer ${localStorage.getItem('token')}`
}))

// 模拟任务进度更新
let progressInterval
const startProgressSimulation = () => {
    clearInterval(progressInterval)
    taskStatus.value = {
        activeStep: 0,
        uploadTime: new Date(),
        parseProgress: '0%',
        trackProgress: '0%',
        finishTime: null
    }

    progressInterval = setInterval(() => {
        if (taskStatus.value.activeStep < 3) {
            if (taskStatus.value.activeStep === 0) {
                taskStatus.value.activeStep = 1
                taskLogs.value.push({
                    time: new Date().toLocaleTimeString(),
                    message: '开始视频解析'
                })
            } else if (taskStatus.value.activeStep === 1) {
                const progress = parseInt(taskStatus.value.parseProgress)
                if (progress < 100) {
                    taskStatus.value.parseProgress = `${progress + 10}%`
                } else {
                    taskStatus.value.activeStep = 2
                    taskLogs.value.push({
                        time: new Date().toLocaleTimeString(),
                        message: '开始目标跟踪'
                    })
                }
            } else if (taskStatus.value.activeStep === 2) {
                const progress = parseInt(taskStatus.value.trackProgress)
                if (progress < 100) {
                    taskStatus.value.trackProgress = `${progress + 5}%`
                } else {
                    taskStatus.value.activeStep = 3
                    taskStatus.value.finishTime = new Date()
                    taskLogs.value.push({
                        time: new Date().toLocaleTimeString(),
                        message: '分析完成'
                    })
                    clearInterval(progressInterval)
                }
            }
        }
    }, 800)
}

const beforeUpload = (file) => {
    const isVideo = ['video/mp4', 'video/avi'].includes(file.type)
    const isLt500M = file.size / 1024 / 1024 < 500

    if (!isVideo) {
        ElMessage.error('只能上传视频文件!')
    }
    if (!isLt500M) {
        ElMessage.error('视频大小不能超过500MB!')
    }

    return isVideo && isLt500M
}

const handleSuccess = (res) => {
    taskId.value = res.task_id
    ElMessage.success(`任务创建成功: ${res.task_id}`)
    startProgressSimulation()
}

const connectStream = async () => {
    if (!rtspUrl.value) {
        ElMessage.warning('请输入RTSP流地址')
        return
    }

    connecting.value = true
    try {
        await new Promise(resolve => setTimeout(resolve, 800))
        taskId.value = 'rtsp-' + Date.now()
        ElMessage.success('流连接成功')
        startProgressSimulation()
    } finally {
        connecting.value = false
    }
}

const refreshTask = () => {
    refreshing.value = true
    setTimeout(() => {
        taskLogs.value.push({
            time: new Date().toLocaleTimeString(),
            message: '手动刷新任务状态'
        })
        refreshing.value = false
    }, 500)
}

const viewResults = () => {
    router.push(`/history/${taskId.value}`)
}

const cancelTask = () => {
    clearInterval(progressInterval)
    ElMessage.warning(`任务 ${taskId.value} 已取消`)
    taskId.value = null
}

const formatTime = (date) => {
    return date ? date.toLocaleTimeString() : '--'
}

onUnmounted(() => {
    clearInterval(progressInterval)
})
</script>

<style scoped>
.upload-container {
    padding: 20px;
}

.el-upload {
    width: 100%;
}

.el-upload-dragger {
    width: 100%;
    padding: 40px 0;
}

.el-input {
    margin-top: 20px;
}

.task-card {
    margin-top: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.task-actions {
    margin-top: 20px;
    display: flex;
    gap: 10px;
}

.log-item {
    font-family: monospace;
    font-size: 12px;
    padding: 2px 0;
    border-bottom: 1px solid #eee;
}
</style>
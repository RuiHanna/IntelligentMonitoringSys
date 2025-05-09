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

        <task-list v-if="taskId" :task-id="taskId"/>
    </div>
</template>

<script setup>
import {ref, computed} from 'vue'
import {UploadFilled} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'
import TaskList from '@/components/TaskList.vue'

const activeTab = ref('file')
const rtspUrl = ref('')
const connecting = ref(false)
const taskId = ref(null)

const uploadUrl = computed(() => `${import.meta.env.VITE_API_BASE}/upload`)
const headers = computed(() => ({
    Authorization: `Bearer ${localStorage.getItem('token')}`
}))

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
}

const connectStream = async () => {
    if (!rtspUrl.value) {
        ElMessage.warning('请输入RTSP流地址')
        return
    }

    connecting.value = true
    try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 800))
        ElMessage.success('流连接成功')
        taskId.value = 'rtsp-' + Date.now()
    } finally {
        connecting.value = false
    }
}
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
</style>
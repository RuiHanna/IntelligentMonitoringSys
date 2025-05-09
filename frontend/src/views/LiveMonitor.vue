<template>
    <div class="monitor-container">
        <el-row :gutter="20">
            <el-col :span="16">
                <!-- 视频播放器 -->
                <div class="video-wrapper">
                    <video
                        ref="videoPlayer"
                        class="video-js"
                        controls
                        autoplay
                        muted
                        :poster="posterUrl"
                    >
                        <source :src="videoUrl" type="video/mp4">
                    </video>
                    <canvas ref="trackingCanvas" class="tracking-overlay"></canvas>
                </div>

                <!-- 控制按钮 -->
                <div class="control-buttons">
                    <el-button-group>
                        <el-button @click="togglePlay" :icon="isPlaying ? 'VideoPause' : 'VideoPlay'">
                            {{ isPlaying ? '暂停' : '播放' }}
                        </el-button>
                        <el-button @click="skipBackward" icon="CaretLeft">
                            后退5秒
                        </el-button>
                        <el-button @click="skipForward" icon="CaretRight">
                            前进5秒
                        </el-button>
                        <el-button @click="toggleFullscreen" icon="FullScreen">
                            全屏
                        </el-button>
                    </el-button-group>
                </div>
            </el-col>

            <el-col :span="8">
                <!-- 统计面板 -->
                <el-card class="stats-card">
                    <template #header>
                        <div class="stats-header">
                            <span>实时统计</span>
                            <el-tag type="success">更新中</el-tag>
                        </div>
                    </template>

                    <div class="stat-item">
                        <span class="stat-label">目标数量:</span>
                        <el-statistic :value="stats.objectCount"/>
                    </div>

                    <div class="stat-item">
                        <span class="stat-label">平均速度:</span>
                        <el-statistic :value="stats.avgSpeed" suffix="px/s"/>
                    </div>

                    <el-divider/>

                    <div class="mini-chart">
                        <div class="chart-title">区域密度</div>
                        <div class="density-grid">
                            <div
                                v-for="(density, index) in zoneDensity"
                                :key="index"
                                class="density-cell"
                                :style="{ backgroundColor: getDensityColor(density) }"
                            >
                                {{ density }}
                            </div>
                        </div>
                    </div>
                </el-card>

                <!-- 报警列表 -->
                <el-card class="alerts-card">
                    <template #header>
                        <div class="alerts-header">
                            <span>异常报警</span>
                            <el-badge :value="alerts.length" :max="99"/>
                        </div>
                    </template>

                    <el-scrollbar height="200px">
                        <div
                            v-for="alert in alerts"
                            :key="alert.id"
                            class="alert-item"
                            :class="`alert-${alert.type}`"
                        >
                            <div class="alert-time">{{ alert.time }}</div>
                            <div class="alert-message">
                                <el-icon :size="16">
                                    <component :is="alertIcons[alert.type]"/>
                                </el-icon>
                                {{ alert.message }}
                            </div>
                        </div>
                    </el-scrollbar>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted} from 'vue'
import {ElMessage} from 'element-plus'
import {
    Warning,
    Bell,
    Position,
} from '@element-plus/icons-vue'

// 视频相关
const videoPlayer = ref(null)
const trackingCanvas = ref(null)
const videoUrl = ref('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4')
const posterUrl = ref('https://via.placeholder.com/1280x720.png?text=Video+Preview')
const isPlaying = ref(false)

// 统计与跟踪数据
const stats = ref({
    objectCount: 0,
    avgSpeed: 0
})

const zoneDensity = ref(Array(9).fill(0))
const alerts = ref([])

// 报警图标映射
const alertIcons = {
    warning: Warning,
    danger: Bell,
    normal: Position
}

// 模拟数据更新
let dataInterval
const updateTrackingData = () => {
    // 随机生成演示数据
    stats.value = {
        objectCount: Math.floor(Math.random() * 10),
        avgSpeed: (Math.random() * 5).toFixed(2)
    }

    zoneDensity.value = Array(9).fill(0).map(() => Math.floor(Math.random() * 10))

    // 随机生成报警
    if (Math.random() > 0.7) {
        const types = ['warning', 'danger', 'normal']
        alerts.value.unshift({
            id: Date.now(),
            type: types[Math.floor(Math.random() * 3)],
            message: ['逆行事件', '聚集警告', '异常停留'][Math.floor(Math.random() * 3)],
            time: new Date().toLocaleTimeString()
        })
    }

    // 绘制跟踪框（模拟）
    drawTrackingBoxes()
}

// 绘制跟踪框
const drawTrackingBoxes = () => {
    const canvas = trackingCanvas.value
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // 模拟绘制3个随机框
    for (let i = 0; i < 3; i++) {
        const x = Math.random() * canvas.width * 0.7
        const y = Math.random() * canvas.height * 0.7
        const width = 50 + Math.random() * 100
        const height = 50 + Math.random() * 100

        ctx.strokeStyle = `hsl(${Math.random() * 360}, 80%, 50%)`
        ctx.lineWidth = 2
        ctx.strokeRect(x, y, width, height)

        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)'
        ctx.fillRect(x, y - 20, 60, 20)

        ctx.fillStyle = 'white'
        ctx.font = '12px Arial'
        ctx.fillText(`ID: ${i + 1}`, x + 5, y - 5)
    }
}

// 控制方法
const togglePlay = () => {
    const video = videoPlayer.value
    if (!video) return

    if (video.paused) {
        video.play()
        isPlaying.value = true
    } else {
        video.pause()
        isPlaying.value = false
    }
}

const skipBackward = () => {
    if (videoPlayer.value) {
        videoPlayer.value.currentTime = Math.max(0, videoPlayer.value.currentTime - 5)
    }
}

const skipForward = () => {
    if (videoPlayer.value) {
        videoPlayer.value.currentTime = Math.min(
            videoPlayer.value.duration,
            videoPlayer.value.currentTime + 5
        )
    }
}

const toggleFullscreen = () => {
    const wrapper = document.querySelector('.video-wrapper')
    if (!wrapper) return

    if (!document.fullscreenElement) {
        wrapper.requestFullscreen().catch(err => {
            ElMessage.error(`全屏错误: ${err.message}`)
        })
    } else {
        document.exitFullscreen()
    }
}

// 密度颜色计算
const getDensityColor = (density) => {
    const hue = 120 - Math.min(density * 12, 120) // 从绿到红
    return `hsl(${hue}, 100%, 50%)`
}

// 初始化视频尺寸
const resizeCanvas = () => {
    if (trackingCanvas.value && videoPlayer.value) {
        trackingCanvas.value.width = videoPlayer.value.clientWidth
        trackingCanvas.value.height = videoPlayer.value.clientHeight
    }
}

// 生命周期
onMounted(() => {
    // 初始调整
    resizeCanvas()

    // 监听视频元素加载
    if (videoPlayer.value) {
        videoPlayer.value.addEventListener('loadedmetadata', resizeCanvas)
        videoPlayer.value.addEventListener('play', () => isPlaying.value = true)
        videoPlayer.value.addEventListener('pause', () => isPlaying.value = false)
    }

    // 监听窗口变化
    window.addEventListener('resize', resizeCanvas)

    // 启动数据更新
    dataInterval = setInterval(updateTrackingData, 1000)
})

onUnmounted(() => {
    clearInterval(dataInterval)
    window.removeEventListener('resize', resizeCanvas)
})
</script>

<style scoped>
.monitor-container {
    padding: 20px;
    height: calc(100vh - 60px);
    overflow: hidden;
}

.video-wrapper {
    position: relative;
    width: 100%;
    background: #000;
}

.video-js {
    width: 100%;
    max-height: 70vh;
}

.tracking-overlay {
    position: absolute;
    top: 0;
    left: 0;
    pointer-events: none;
}

.control-buttons {
    margin-top: 10px;
    display: flex;
    justify-content: center;
}

.stats-card, .alerts-card {
    margin-bottom: 20px;
}

.stats-header, .alerts-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 12px 0;
}

.stat-label {
    font-weight: bold;
}

.mini-chart {
    margin-top: 15px;
}

.chart-title {
    font-size: 14px;
    margin-bottom: 8px;
    color: #666;
}

.density-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
}

.density-cell {
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    border-radius: 4px;
}

.alert-item {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}

.alert-time {
    font-size: 12px;
    color: #999;
}

.alert-message {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 4px;
}

.alert-warning {
    border-left: 3px solid #e6a23c;
    padding-left: 5px;
}

.alert-danger {
    border-left: 3px solid #f56c6c;
    padding-left: 5px;
}

.alert-normal {
    border-left: 3px solid #67c23a;
    padding-left: 5px;
}

.el-col {
    height: 100%;
    display: flex;
    flex-direction: column;
}
</style>
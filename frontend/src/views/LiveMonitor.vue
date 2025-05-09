<template>
    <div class="monitor-container">
        <el-row :gutter="20">
            <el-col :span="16">
                <video-player :src="videoUrl" @frame="handleFrame"/>
                <track-controls
                    :playing="isPlaying"
                    @play="handlePlay"
                    @pause="handlePause"
                />
            </el-col>
            <el-col :span="8">
                <stats-panel :data="statsData"/>
                <alert-list :alerts="alerts"/>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
import StatsPanel from '@/components/StatsPanel.vue'
import AlertList from '@/components/AlertList.vue'
import TrackControls from '@/components/TrackControls.vue'
import {ElMessage} from "element-plus";

const videoUrl = ref('')
const isPlaying = ref(false)
const statsData = ref({
    objectCount: 0,
    avgSpeed: 0,
    density: {}
})
const alerts = ref([])

// 模拟从路由参数获取视频源
onMounted(() => {
    videoUrl.value = 'https://example.com/sample.mp4'
})

const handleFrame = () => {
    // 处理帧数据（实际应调用API）
    statsData.value = {
        objectCount: Math.floor(Math.random() * 10),
        avgSpeed: (Math.random() * 5).toFixed(2),
        density: {'x:100,y:200': 3}
    }

    if (Math.random() > 0.9) {
        alerts.value.unshift({
            id: Date.now(),
            type: ['逆行', '聚集', '滞留'][Math.floor(Math.random() * 3)],
            time: new Date().toLocaleTimeString()
        })
    }
}

const handlePlay = () => {
    isPlaying.value = true
    ElMessage.info('播放开始')
}

const handlePause = () => {
    isPlaying.value = false
}
</script>

<style scoped>
.monitor-container {
    padding: 20px;
    height: calc(100vh - 60px);
    overflow: hidden;
}

.el-col {
    height: 100%;
    display: flex;
    flex-direction: column;
}
</style>
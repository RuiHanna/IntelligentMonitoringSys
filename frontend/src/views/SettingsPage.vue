<template>
    <div class="settings-container">
        <el-tabs type="border-card">
            <el-tab-pane label="系统配置">
                <el-form :model="form" label-width="120px">
                    <el-form-item label="视频分辨率">
                        <el-select v-model="form.resolution">
                            <el-option label="640x480" value="640x480"/>
                            <el-option label="1280x720" value="1280x720"/>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="抽帧率(fps)">
                        <el-slider v-model="form.frameRate" :min="1" :max="30"/>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="saveConfig">保存配置</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>

            <el-tab-pane label="报警规则">
                <alert-rules :rules="rules" @add="handleAddRule"/>
            </el-tab-pane>

            <el-tab-pane label="系统日志">
                <log-viewer :logs="logs"/>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
import {ref} from 'vue'
import {ElMessage} from 'element-plus'
import AlertRules from '@/components/AlertRules.vue'
import LogViewer from '@/components/LogViewer.vue'

const form = ref({
    resolution: '640x480',
    frameRate: 10
})

const rules = ref([
    {id: 1, type: '逆行', threshold: 3, enabled: true},
    {id: 2, type: '聚集', threshold: 5, enabled: true}
])

const logs = ref([
    {time: '2023-01-01 10:00', level: 'INFO', message: '系统启动'},
    {time: '2023-01-01 10:05', level: 'WARN', message: '检测到低帧率'}
])

const saveConfig = () => {
    ElMessage.success('配置已保存')
    console.log('当前配置:', form.value)
}

const handleAddRule = (newRule) => {
    rules.value.push({
        id: Date.now(),
        ...newRule
    })
}
</script>

<style scoped>
.settings-container {
    padding: 20px;
}

.el-form {
    max-width: 600px;
}
</style>
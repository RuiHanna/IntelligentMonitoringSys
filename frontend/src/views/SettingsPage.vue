<template>
    <el-card>
        <el-form :model="settings" label-width="180px" style="max-width: 500px;">
            <el-form-item label="数据保留天数">
                <el-input-number v-model="settings.retain_days" :min="1"/>
            </el-form-item>
            <el-form-item label="最大跟踪目标数">
                <el-input-number v-model="settings.max_targets" :min="1"/>
            </el-form-item>
            <el-form-item label="检测置信度阈值">
                <el-slider v-model="settings.detection_thresh" :min="0.1" :max="1.0" step="0.05"/>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="saveSettings">保存设置</el-button>
            </el-form-item>
        </el-form>

        <h2 style="margin-top: 30px;">系统日志</h2>
        <el-table :data="logs" border>
            <el-table-column prop="log_time" label="时间"/>
            <el-table-column prop="level" label="级别"/>
            <el-table-column prop="message" label="信息"/>
        </el-table>
    </el-card>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import axios from 'axios';

const settings = ref({retain_days: 7, max_targets: 20, detection_thresh: 0.5});
const logs = ref([]);

onMounted(async () => {
    const res = await axios.get('http://localhost:5000/api/settings');
    settings.value = res.data;
    logs.value = (await axios.get('http://localhost:5000/api/logs')).data;
});

const saveSettings = async () => {
    await axios.post('http://localhost:5000/api/settings', settings.value);
};
</script>
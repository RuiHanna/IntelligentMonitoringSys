<template>
    <div>
        <el-button @click="startRealtime" :disabled="isTracking">启动摄像头</el-button>
        <el-button @click="stopRealtime" :disabled="!isTracking">关闭摄像头</el-button>
        <div v-if="isTracking" style="margin-top: 20px;">
            <img :src="streamUrl" style="max-width: 100%;" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const streamUrl = ref('');
const isTracking = ref(false);

const startRealtime = () => {
    streamUrl.value = 'http://localhost:5000/realtime-stream';
    isTracking.value = true;
};

const stopRealtime = () => {
    streamUrl.value = '';
    isTracking.value = false;
};
</script>

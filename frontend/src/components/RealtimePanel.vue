<template>
    <div>
        <el-button @click="startRealtime">启动摄像头</el-button>
        <video ref="videoRef" autoplay playsinline style="max-width: 100%; margin-top: 20px;"></video>
    </div>
</template>

<script setup>
import {ref} from 'vue';

const videoRef = ref(null);

const startRealtime = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        videoRef.value.srcObject = stream;
    } catch (err) {
        console.error('摄像头访问失败', err);
    }
};
</script>
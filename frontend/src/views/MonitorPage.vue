<template>
    <el-card>
        <el-tabs v-model="activeTab">
            <el-tab-pane label="上传视频" name="upload">
                <UploadPanel/>
            </el-tab-pane>
            <el-tab-pane label="实时监控" name="realtime">
                <RealtimePanel/>
            </el-tab-pane>
        </el-tabs>
    </el-card>
</template>

<script setup>
import {ref} from 'vue';
import UploadPanel from '../components/UploadPanel.vue';
import RealtimePanel from '../components/RealtimePanel.vue';

const activeTab = ref('upload');
</script>
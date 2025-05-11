<template>
    <el-upload
        class="upload-demo"
        drag
        action="http://127.0.0.1:5000/upload"
        accept="video/*"
        :on-success="handleSuccess"
        :on-error="handleError">
        <el-icon>
            <UploadFilled/>
        </el-icon>
        <div class="el-upload__text">拖拽或点击上传视频</div>
    </el-upload>
</template>

<script setup>
import {ElMessage} from 'element-plus';
import {UploadFilled} from '@element-plus/icons-vue';

const handleSuccess = () => {
    ElMessage.success('上传成功，后台开始处理');
};
const handleError = () => {
    ElMessage.error('上传失败');
};
</script>
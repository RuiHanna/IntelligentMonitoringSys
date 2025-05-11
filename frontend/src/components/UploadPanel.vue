<template>
    <div>
        <!-- 上传组件 -->
        <el-upload
            class="upload-demo"
            drag
            :http-request="customUpload"
            accept="video/*">
            <el-icon>
                <UploadFilled/>
            </el-icon>
            <div class="el-upload__text">拖拽或点击上传视频</div>
        </el-upload>

        <!-- 上传进度条 -->
        <el-progress
            v-if="uploading"
            :percentage="progress"
            status="active"
            style="margin-top: 20px;"
        />

        <!-- 上传成功按钮 -->
        <el-button
            v-if="videoUrl"
            type="primary"
            @click="showVideo = true"
            style="margin-top: 20px;"
        >
            查看上传视频结果
        </el-button>

        <video
            v-if="showVideo"
            :src="videoUrl"
            controls
            width="640"
            style="margin-top: 10px;"
        />

        <h3 style="margin-top: 30px;">历史跟踪结果视频：</h3>
        <el-table :data="videoList" border style="width: 100%; margin-top: 10px;">
            <el-table-column prop="name" label="视频文件名"/>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button size="small" type="success" @click="playExistingVideo(scope.row.name)">播放</el-button>
                </template>
            </el-table-column>
        </el-table>

        <video
            v-if="selectedVideo"
            :src="`http://127.0.0.1:5000/output/${selectedVideo}`"
            controls
            width="640"
            style="margin-top: 10px;"
        />
    </div>
</template>


<script setup>
import {ElMessage} from 'element-plus';
import {UploadFilled} from '@element-plus/icons-vue';
import axios from 'axios';
import {ref, onMounted} from 'vue';

const uploading = ref(false);
const progress = ref(0);
const videoUrl = ref('');
const showVideo = ref(false);
const videoList = ref([]);
const selectedVideo = ref('');

const customUpload = async ({file}) => {
    uploading.value = true;
    progress.value = 10;

    const formData = new FormData();
    formData.append('file', file);

    try {
        await axios.post('http://127.0.0.1:5000/upload', formData, {
            onUploadProgress: (e) => {
                progress.value = Math.round((e.loaded * 100) / e.total);
            }
        });

        progress.value = 100;
        ElMessage.success('上传成功，后台处理中');

        setTimeout(() => {
            videoUrl.value = `http://127.0.0.1:5000/output/${file.name.replace(/\.[^/.]+$/, '')}_tracked.mp4`;
            ElMessage.success('处理完成');
            loadVideoList();  // 重新加载视频列表
        }, 5000);
    } catch (error) {
        ElMessage.error('上传失败');
        console.error(error);
    } finally {
        uploading.value = false;
    }
};

// 加载 output 视频列表
const loadVideoList = async () => {
    try {
        const res = await axios.get('http://127.0.0.1:5000/api/output_videos');
        videoList.value = res.data.map(name => ({name}));
    } catch (err) {
        console.error('无法获取视频列表', err);
    }
};

const playExistingVideo = (filename) => {
    selectedVideo.value = filename;
    console.log(selectedVideo.value)
};

onMounted(() => {
    loadVideoList();
});
</script>


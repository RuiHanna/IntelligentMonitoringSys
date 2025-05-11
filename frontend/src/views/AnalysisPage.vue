<template>
    <el-card>
        <h2>热力图</h2>
        <div id="heatmap" style="height: 400px;"></div>

        <h2 style="margin-top: 20px;">目标统计</h2>
        <div id="barChart" style="height: 400px;"></div>

        <h2 style="margin-top: 20px;">跟踪数据表</h2>
        <el-table :data="tableData" border style="width: 100%;">
            <el-table-column prop="object_id" label="目标ID"/>
            <el-table-column prop="class_name" label="类型"/>
            <el-table-column prop="enter_time" label="进入时间"/>
            <el-table-column prop="exit_time" label="离开时间"/>
            <el-table-column prop="track_length" label="轨迹长度"/>
        </el-table>
    </el-card>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';

const tableData = ref([]);

onMounted(async () => {
    const heatmapChart = echarts.init(document.getElementById('heatmap'));
    const barChart = echarts.init(document.getElementById('barChart'));

    const heatData = (await axios.get('http://localhost:5000/api/heatmap')).data;
    const barData = (await axios.get('http://localhost:5000/api/stats')).data;
    const table = (await axios.get('http://localhost:5000/api/targets')).data;
    tableData.value = table;

    heatmapChart.setOption(heatData);
    barChart.setOption(barData);
});
</script>

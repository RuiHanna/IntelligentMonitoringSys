<template>
    <div class="history-container">
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>历史记录查询</span>
                    <div class="date-range-picker">
                        <el-date-picker
                            v-model="dateRange"
                            type="daterange"
                            range-separator="至"
                            start-placeholder="开始日期"
                            end-placeholder="结束日期"
                            @change="handleDateChange"
                        />
                    </div>
                </div>
            </template>

            <div class="history-content">
                <!-- 数据表格 -->
                <el-table
                    :data="filteredData"
                    style="width: 100%"
                    height="400"
                    @row-click="handleRowClick"
                >
                    <el-table-column prop="taskId" label="任务ID" width="180"/>
                    <el-table-column prop="startTime" label="开始时间" width="180"/>
                    <el-table-column prop="endTime" label="结束时间" width="180"/>
                    <el-table-column prop="objectCount" label="目标数量"/>
                    <el-table-column prop="status" label="状态">
                        <template #default="{ row }">
                            <el-tag :type="statusTagType(row.status)">
                                {{ row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="120">
                        <template #default="{ row }">
                            <el-button size="small" @click.stop="showDetail(row)">
                                详情
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>

                <!-- 分页 -->
                <div class="pagination-wrapper">
                    <el-pagination
                        v-model:current-page="currentPage"
                        v-model:page-size="pageSize"
                        :total="totalItems"
                        :page-sizes="[10, 20, 50, 100]"
                        layout="total, sizes, prev, pager, next, jumper"
                        @size-change="handleSizeChange"
                        @current-change="handlePageChange"
                    />
                </div>

                <!-- 详情对话框 -->
                <el-dialog v-model="detailVisible" title="任务详情" width="70%">
                    <div v-if="currentDetail" class="detail-content">
                        <el-descriptions :column="2" border>
                            <el-descriptions-item label="任务ID">{{ currentDetail.taskId }}</el-descriptions-item>
                            <el-descriptions-item label="持续时间">{{ currentDetail.duration }}秒</el-descriptions-item>
                            <el-descriptions-item label="开始时间">{{ currentDetail.startTime }}</el-descriptions-item>
                            <el-descriptions-item label="结束时间">{{ currentDetail.endTime }}</el-descriptions-item>
                            <el-descriptions-item label="目标数量">{{
                                    currentDetail.objectCount
                                }}
                            </el-descriptions-item>
                            <el-descriptions-item label="平均速度">{{ currentDetail.avgSpeed }} px/s
                            </el-descriptions-item>
                        </el-descriptions>

                        <div class="detail-charts">
                            <div class="chart-container">
                                <h3>目标数量变化</h3>
                                <div ref="countChart" class="chart"></div>
                            </div>
                            <div class="chart-container">
                                <h3>速度分布</h3>
                                <div ref="speedChart" class="chart"></div>
                            </div>
                        </div>

                        <el-divider/>

                        <h3>原始数据</h3>
                        <el-input
                            type="textarea"
                            :rows="5"
                            readonly
                            :value="JSON.stringify(currentDetail.rawData, null, 2)"
                        />
                    </div>
                </el-dialog>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import {ref, computed, onMounted, nextTick} from 'vue'
import * as echarts from 'echarts'

// 表格数据
const tableData = ref(generateMockData(50))
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = computed(() => tableData.value.length)

// 详情相关
const detailVisible = ref(false)
const currentDetail = ref(null)
const countChart = ref(null)
const speedChart = ref(null)

// 过滤后的数据
const filteredData = computed(() => {
    let data = [...tableData.value]

    // 日期过滤
    if (dateRange.value && dateRange.value.length === 2) {
        const [start, end] = dateRange.value
        data = data.filter(item => {
            const itemDate = new Date(item.startTime)
            return itemDate >= start && itemDate <= end
        })
    }

    // 分页
    const startIndex = (currentPage.value - 1) * pageSize.value
    return data.slice(startIndex, startIndex + pageSize.value)
})

// 生成模拟数据
function generateMockData(count) {
    const data = []
    const statuses = ['success', 'processing', 'failed']

    for (let i = 0; i < count; i++) {
        const start = new Date()
        start.setDate(start.getDate() - Math.floor(Math.random() * 30))

        const end = new Date(start)
        end.setMinutes(end.getMinutes() + Math.floor(Math.random() * 120))

        data.push({
            taskId: `TASK-${1000 + i}`,
            startTime: start.toLocaleString(),
            endTime: end.toLocaleString(),
            duration: Math.floor((end - start) / 1000),
            objectCount: Math.floor(Math.random() * 50),
            avgSpeed: (Math.random() * 10).toFixed(2),
            status: statuses[Math.floor(Math.random() * statuses.length)],
            rawData: {
                objects: Array(5).fill(0).map(() => ({
                    id: Math.floor(Math.random() * 1000),
                    type: ['person', 'vehicle', 'animal'][Math.floor(Math.random() * 3)],
                    speed: (Math.random() * 10).toFixed(2)
                }))
            }
        })
    }

    return data
}

// 状态标签类型
const statusTagType = (status) => {
    const map = {
        success: 'success',
        processing: 'warning',
        failed: 'danger'
    }
    return map[status] || ''
}

// 日期变化处理
const handleDateChange = () => {
    currentPage.value = 1
}

// 分页处理
const handleSizeChange = (val) => {
    pageSize.value = val
    currentPage.value = 1
}

const handlePageChange = (val) => {
    currentPage.value = val
}

// 行点击处理
const handleRowClick = (row) => {
    showDetail(row)
}

// 显示详情
const showDetail = (row) => {
    currentDetail.value = row
    detailVisible.value = true

    nextTick(() => {
        initCharts()
    })
}

// 初始化图表
const initCharts = () => {
    if (!currentDetail.value) return

    // 销毁旧图表
    if (countChart.value && countChart.value.dispose) {
        countChart.value.dispose()
    }
    if (speedChart.value && speedChart.value.dispose) {
        speedChart.value.dispose()
    }

    // 目标数量图表
    countChart.value = echarts.init(document.querySelector('.detail-charts .chart:first-child'))
    countChart.value.setOption({
        xAxis: {
            type: 'category',
            data: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00']
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: [3, 8, 12, 5, 18, 9, 15, 7],
            type: 'line',
            smooth: true
        }]
    })

    // 速度分布图表
    speedChart.value = echarts.init(document.querySelector('.detail-charts .chart:last-child'))
    speedChart.value.setOption({
        tooltip: {
            trigger: 'item'
        },
        series: [{
            name: '速度分布',
            type: 'pie',
            radius: '70%',
            data: [
                {value: 35, name: '0-2 px/s'},
                {value: 30, name: '2-4 px/s'},
                {value: 25, name: '4-6 px/s'},
                {value: 10, name: '6+ px/s'}
            ]
        }]
    })

    // 窗口大小变化时重绘图表
    window.addEventListener('resize', function () {
        countChart.value.resize()
        speedChart.value.resize()
    })
}

onMounted(() => {
    // 初始化时可以加载一些数据
})
</script>

<style scoped>
.history-container {
    padding: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.date-range-picker {
    width: 350px;
}

.history-content {
    margin-top: 20px;
}

.pagination-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}

.detail-content {
    padding: 10px;
}

.detail-charts {
    display: flex;
    margin-top: 20px;
    gap: 20px;
}

.chart-container {
    flex: 1;
    border: 1px solid #eee;
    padding: 10px;
    border-radius: 4px;
}

.chart-container h3 {
    margin: 0 0 10px 0;
    font-size: 16px;
    color: #666;
}

.chart {
    height: 300px;
    width: 100%;
}
</style>
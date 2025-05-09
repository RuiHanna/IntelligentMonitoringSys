<template>
    <div class="history-container">
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>历史数据查询</span>
                    <date-picker v-model="dateRange"/>
                </div>
            </template>

            <el-table :data="tableData" height="400" style="width: 100%">
                <el-table-column prop="id" label="任务ID" width="180"/>
                <el-table-column prop="start_time" label="开始时间"/>
                <el-table-column prop="end_time" label="结束时间"/>
                <el-table-column prop="object_count" label="目标数量"/>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button size="small" @click="handleDetail(scope.row)">
                            详情
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination
                v-model:current-page="currentPage"
                :page-size="pageSize"
                :total="total"
                layout="prev, pager, next"
            />
        </el-card>

        <history-chart :data="chartData"/>
    </div>
</template>

<script setup>
import {ref, watch} from 'vue'
import {useRouter} from 'vue-router'
import DatePicker from '@/components/DatePicker.vue'
import HistoryChart from '@/components/HistoryChart.vue'

const router = useRouter()
const dateRange = ref([new Date(), new Date()])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(50)

const tableData = ref(
    Array.from({length: 10}, (_, i) => ({
        id: `task-${i + 1}`,
        start_time: new Date(Date.now() - i * 3600000).toLocaleString(),
        end_time: new Date(Date.now() - i * 3600000 + 1800000).toLocaleString(),
        object_count: Math.floor(Math.random() * 20)
    }))
)

const chartData = ref({
    dates: ['1日', '2日', '3日', '4日', '5日'],
    counts: [12, 19, 3, 5, 8]
})

watch(dateRange, (newVal) => {
    console.log('日期范围变化:', newVal)
    // 实际应调用API获取数据
})

const handleDetail = (row) => {
    router.push(`/history/${row.id}`)
}
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

.el-pagination {
    margin-top: 20px;
    justify-content: center;
}
</style>
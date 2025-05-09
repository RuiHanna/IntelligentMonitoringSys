<template>
  <div class="settings-container">
    <el-tabs type="border-card" v-model="activeTab">
      <el-tab-pane label="系统设置" name="system">
        <el-form :model="systemForm" label-width="150px">
          <el-form-item label="视频处理分辨率">
            <el-select v-model="systemForm.resolution">
              <el-option label="640x480" value="640x480" />
              <el-option label="1280x720" value="1280x720" />
              <el-option label="1920x1080" value="1920x1080" />
            </el-select>
          </el-form-item>

          <el-form-item label="目标检测阈值">
            <el-slider
              v-model="systemForm.detectionThreshold"
              :min="0.1"
              :max="1"
              :step="0.05"
              show-input
            />
          </el-form-item>

          <el-form-item label="最大跟踪目标数">
            <el-input-number
              v-model="systemForm.maxObjects"
              :min="1"
              :max="100"
            />
          </el-form-item>

          <el-form-item label="数据保留天数">
            <el-input-number
              v-model="systemForm.retentionDays"
              :min="1"
              :max="365"
            />
          </el-form-item>

          <el-form-item label="启用实时报警">
            <el-switch v-model="systemForm.realtimeAlert" />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveSystemSettings">
              保存设置
            </el-button>
            <el-button @click="resetSystemSettings">
              恢复默认
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="报警规则" name="alerts">
        <div class="alert-rules-container">
          <div class="alert-rules-header">
            <el-button type="primary" @click="addAlertRule">
              <el-icon><plus /></el-icon>
              添加规则
            </el-button>

            <el-input
              v-model="alertSearch"
              placeholder="搜索规则..."
              clearable
              style="width: 200px; margin-left: 10px;"
            />
          </div>

          <el-table :data="filteredAlertRules" style="width: 100%">
            <el-table-column prop="name" label="规则名称" />
            <el-table-column prop="type" label="规则类型" />
            <el-table-column prop="threshold" label="阈值" />
            <el-table-column prop="enabled" label="状态">
              <template #default="{ row }">
                <el-switch
                  v-model="row.enabled"
                  @change="toggleAlertRule(row)"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="editAlertRule(row)">
                  编辑
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="deleteAlertRule(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 添加/编辑规则对话框 -->
        <el-dialog
          v-model="alertDialogVisible"
          :title="isEditingAlert ? '编辑规则' : '添加规则'"
          width="50%"
        >
          <el-form :model="currentAlertRule" label-width="100px">
            <el-form-item label="规则名称" required>
              <el-input v-model="currentAlertRule.name" />
            </el-form-item>

            <el-form-item label="规则类型" required>
              <el-select v-model="currentAlertRule.type">
                <el-option
                  v-for="type in alertTypes"
                  :key="type.value"
                  :label="type.label"
                  :value="type.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="阈值" required>
              <el-input-number
                v-model="currentAlertRule.threshold"
                :min="1"
                :max="100"
              />
            </el-form-item>

            <el-form-item label="启用规则">
              <el-switch v-model="currentAlertRule.enabled" />
            </el-form-item>

            <el-form-item label="规则描述">
              <el-input
                v-model="currentAlertRule.description"
                type="textarea"
                :rows="3"
              />
            </el-form-item>
          </el-form>

          <template #footer>
            <el-button @click="alertDialogVisible = false">
              取消
            </el-button>
            <el-button type="primary" @click="confirmAlertRule">
              确认
            </el-button>
          </template>
        </el-dialog>
      </el-tab-pane>

      <el-tab-pane label="系统日志" name="logs">
        <div class="log-container">
          <div class="log-toolbar">
            <el-button-group>
              <el-button @click="refreshLogs">
                <el-icon><refresh /></el-icon>
                刷新
              </el-button>
              <el-button @click="clearLogs">
                <el-icon><delete /></el-icon>
                清空
              </el-button>
              <el-button @click="exportLogs">
                <el-icon><download /></el-icon>
                导出
              </el-button>
            </el-button-group>

            <div style="margin-left: 20px;">
              <el-select
                v-model="logLevel"
                placeholder="日志级别"
                style="width: 120px;"
              >
                <el-option label="全部" value="all" />
                <el-option label="INFO" value="info" />
                <el-option label="WARN" value="warn" />
                <el-option label="ERROR" value="error" />
              </el-select>
            </div>
          </div>

          <div class="log-content">
            <el-scrollbar height="500px">
              <div
                v-for="(log, index) in filteredLogs"
                :key="index"
                class="log-item"
                :class="`log-${log.level}`"
              >
                <div class="log-time">{{ log.time }}</div>
                <div class="log-level">[{{ log.level }}]</div>
                <div class="log-message">{{ log.message }}</div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Refresh,
  Delete,
  Download
} from '@element-plus/icons-vue'

// 系统设置
const activeTab = ref('system')
const systemForm = ref({
  resolution: '1280x720',
  detectionThreshold: 0.5,
  maxObjects: 50,
  retentionDays: 30,
  realtimeAlert: true
})

// 报警规则
const alertSearch = ref('')
const alertRules = ref([
  { id: 1, name: '人群聚集', type: 'crowd', threshold: 5, enabled: true, description: '检测到5人以上聚集' },
  { id: 2, name: '异常停留', type: 'loitering', threshold: 30, enabled: true, description: '同一目标停留超过30秒' },
  { id: 3, name: '逆行检测', type: 'wrong-way', threshold: 1, enabled: false, description: '检测到逆行目标' }
])

const alertTypes = [
  { value: 'crowd', label: '人群聚集' },
  { value: 'loitering', label: '异常停留' },
  { value: 'wrong-way', label: '逆行检测' },
  { value: 'speed', label: '超速检测' },
  { value: 'area', label: '区域入侵' }
]

const alertDialogVisible = ref(false)
const isEditingAlert = ref(false)
const currentAlertRule = ref({
  id: 0,
  name: '',
  type: '',
  threshold: 1,
  enabled: true,
  description: ''
})

// 系统日志
const logLevel = ref('all')
const logs = ref([
  { time: '2023-07-01 09:00:00', level: 'info', message: '系统启动完成' },
  { time: '2023-07-01 09:05:23', level: 'info', message: '加载视频源 rtsp://example.com/stream1' },
  { time: '2023-07-01 09:12:45', level: 'warn', message: '检测到低帧率: 10fps' },
  { time: '2023-07-01 09:30:10', level: 'error', message: '无法连接到分析服务器' },
  { time: '2023-07-01 10:15:33', level: 'info', message: '服务器连接恢复' },
  { time: '2023-07-01 11:20:05', level: 'info', message: '检测到5个目标' },
  { time: '2023-07-01 12:45:18', level: 'warn', message: '高内存使用率: 85%' }
])

// 过滤后的报警规则
const filteredAlertRules = computed(() => {
  if (!alertSearch.value) return alertRules.value
  return alertRules.value.filter(rule =>
    rule.name.includes(alertSearch.value) ||
    rule.type.includes(alertSearch.value) ||
    rule.description.includes(alertSearch.value)
  )
})

// 过滤后的日志
const filteredLogs = computed(() => {
  if (logLevel.value === 'all') return logs.value
  return logs.value.filter(log => log.level === logLevel.value)
})

// 系统设置方法
const saveSystemSettings = () => {
  ElMessage.success('系统设置已保存')
  console.log('保存的设置:', systemForm.value)
}

const resetSystemSettings = () => {
  ElMessageBox.confirm('确定要恢复默认设置吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    systemForm.value = {
      resolution: '1280x720',
      detectionThreshold: 0.5,
      maxObjects: 50,
      retentionDays: 30,
      realtimeAlert: true
    }
    ElMessage.success('已恢复默认设置')
  })
}

// 报警规则方法
const addAlertRule = () => {
  currentAlertRule.value = {
    id: 0,
    name: '',
    type: '',
    threshold: 1,
    enabled: true,
    description: ''
  }
  isEditingAlert.value = false
  alertDialogVisible.value = true
}

const editAlertRule = (rule) => {
  currentAlertRule.value = { ...rule }
  isEditingAlert.value = true
  alertDialogVisible.value = true
}

const deleteAlertRule = (rule) => {
  ElMessageBox.confirm(`确定要删除规则 "${rule.name}" 吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    alertRules.value = alertRules.value.filter(r => r.id !== rule.id)
    ElMessage.success('规则已删除')
  })
}

const toggleAlertRule = (rule) => {
  ElMessage.info(`规则 "${rule.name}" 已${rule.enabled ? '启用' : '禁用'}`)
}

const confirmAlertRule = () => {
  if (!currentAlertRule.value.name || !currentAlertRule.value.type) {
    ElMessage.error('请填写完整的规则信息')
    return
  }

  if (isEditingAlert.value) {
    // 更新现有规则
    const index = alertRules.value.findIndex(r => r.id === currentAlertRule.value.id)
    if (index >= 0) {
      alertRules.value[index] = { ...currentAlertRule.value }
    }
    ElMessage.success('规则已更新')
  } else {
    // 添加新规则
    currentAlertRule.value.id = Math.max(...alertRules.value.map(r => r.id), 0) + 1
    alertRules.value.push({ ...currentAlertRule.value })
    ElMessage.success('规则已添加')
  }

  alertDialogVisible.value = false
}

// 日志方法
const refreshLogs = () => {
  // 模拟获取新日志
  const newLog = {
    time: new Date().toLocaleString(),
    level: 'info',
    message: '手动刷新日志'
  }
  logs.value.unshift(newLog)
  ElMessage.success('日志已刷新')
}

const clearLogs = () => {
  ElMessageBox.confirm('确定要清空所有日志吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    logs.value = []
    ElMessage.success('日志已清空')
  })
}

const exportLogs = () => {
  ElMessage.success('日志导出成功（模拟）')
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.alert-rules-container {
  padding: 10px;
}

.alert-rules-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
}

.log-container {
  padding: 10px;
}

.log-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.log-content {
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 10px;
}

.log-item {
  display: flex;
  padding: 5px 0;
  border-bottom: 1px solid #f0f0f0;
  font-family: monospace;
}

.log-time {
  width: 180px;
  color: #666;
}

.log-level {
  width: 80px;
}

.log-info .log-level {
  color: #67c23a;
}

.log-warn .log-level {
  color: #e6a23c;
}

.log-error .log-level {
  color: #f56c6c;
}

.log-message {
  flex: 1;
}
</style>
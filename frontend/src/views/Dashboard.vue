<template>
  <div>
    <div class="page-title">今日工作台</div>

    <el-row :gutter="24">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span style="font-size: 20px;">今日收购单数</span>
          </template>
          <div class="stat-value">{{ stats.today_purchases }}</div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span style="font-size: 20px;">今日收购金额</span>
          </template>
          <div class="stat-value">{{ stats.today_amount }} 元</div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span style="font-size: 20px;">累计农户数</span>
          </template>
          <div class="stat-value">{{ stats.total_farmers }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 24px;">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 20px;">今日收购记录</span>
          <el-button type="primary" @click="$router.push('/purchases/new')">
            新建收购
          </el-button>
        </div>
      </template>

      <el-table :data="todayList" stripe style="width: 100%">
        <el-table-column prop="id" label="单号" width="100" />
        <el-table-column prop="grain_type" label="粮食品种" width="120" />
        <el-table-column label="净重">
          <template #default="{ row }">
            {{ row.net_weight || '-' }} kg
          </template>
        </el-table-column>
        <el-table-column label="金额">
          <template #default="{ row }">
            {{ row.total_amount || '-' }} 元
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/purchases/${row.id}`)">
              详情
            </el-button>
            <el-button
              v-if="row.status === 'EMPTY_WEIGHTED'"
              size="small"
              type="primary"
              @click="handleComplete(row)"
            >
              完成
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import api from "@/api"
import { ElMessage } from "element-plus"

const stats = ref({
  today_purchases: 0,
  today_amount: "0.00",
  total_farmers: 0,
})

const todayList = ref<any[]>([])

function statusLabel(s: string) {
  const map: Record<string, string> = {
    CREATED: "已创建",
    GROSS_WEIGHTED: "已称毛重",
    PRICED: "已报价",
    UNLOADED: "已卸粮",
    EMPTY_WEIGHTED: "已称空车",
    COMPLETED: "已完成",
  }
  return map[s] || s
}

function statusTag(s: string) {
  if (s === "COMPLETED") return "success"
  if (s === "EMPTY_WEIGHTED") return "warning"
  return "info"
}

async function handleComplete(row: any) {
  await api.post(`/purchases/${row.id}/complete`)
  ElMessage.success("收购完成")
  loadData()
}

async function loadData() {
  const [statsRes, todayRes]: any = await Promise.all([
    api.get("/dashboard/stats"),
    api.get("/purchases/today"),
  ])
  stats.value = statsRes.data
  todayList.value = todayRes.data
}

onMounted(loadData)
</script>

<style scoped>
.stat-value {
  font-size: 48px;
  font-weight: bold;
  color: #1a1a2e;
  text-align: center;
  padding: 16px 0;
}
</style>

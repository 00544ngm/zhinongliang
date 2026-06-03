<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div class="page-title">收购记录</div>
      <el-button type="primary" @click="$router.push('/purchases/new')">
        新建收购
      </el-button>
    </div>

    <el-card>
      <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: center;">
        <el-date-picker
          v-model="startDate"
          type="date"
          placeholder="开始日期"
          value-format="YYYY-MM-DD"
        />
        <span>至</span>
        <el-date-picker
          v-model="endDate"
          type="date"
          placeholder="结束日期"
          value-format="YYYY-MM-DD"
        />
        <el-button type="primary" @click="searchByDate">查询</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </div>

      <el-table :data="list" stripe style="width: 100%">
        <el-table-column prop="id" label="单号" width="80" />
        <el-table-column label="农户" width="120">
          <template #default="{ row }">
            {{ row.farmer_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="grain_type" label="品种" width="100" />
        <el-table-column label="毛重">
          <template #default="{ row }">
            {{ row.gross_weight }} kg
          </template>
        </el-table-column>
        <el-table-column label="净重">
          <template #default="{ row }">
            {{ row.net_weight || '-' }} kg
          </template>
        </el-table-column>
        <el-table-column label="单价">
          <template #default="{ row }">
            {{ row.unit_price }} 元/斤
          </template>
        </el-table-column>
        <el-table-column label="金额">
          <template #default="{ row }">
            {{ row.total_amount || '-' }} 元
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="空车称重时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.empty_weighted_at) || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="结账时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.completed_at) || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/purchases/${row.id}`)">
              详情
            </el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(row)">
              删除
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
import { ElMessage, ElMessageBox } from "element-plus"

const list = ref<any[]>([])
const startDate = ref("")
const endDate = ref("")

function formatTime(t: string | null) {
  if (!t) return "-"
  return t.replace("T", " ").slice(0, 19)
}

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

async function searchByDate() {
  const res: any = await api.get("/purchases/range", {
    params: { start: startDate.value, end: endDate.value },
  })
  list.value = res.data
}

async function resetSearch() {
  startDate.value = ""
  endDate.value = ""
  loadToday()
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(
      `确认删除单号 #${row.id}（${row.farmer_name || "无农户"}）？此操作不可撤销。`,
      "删除确认",
      { confirmButtonText: "删除", cancelButtonText: "取消", type: "warning" },
    )
  } catch {
    return
  }
  try {
    await api.delete(`/purchases/${row.id}`)
    ElMessage.success("已删除")
    list.value = list.value.filter((item) => item.id !== row.id)
  } catch {
    // handled by interceptor
  }
}

async function loadToday() {
  const res: any = await api.get("/purchases/today")
  list.value = res.data
}

onMounted(loadToday)
</script>

<template>
  <div>
    <div class="page-title">库存查看</div>

    <el-card v-if="loading" style="text-align: center; padding: 40px;">
      加载中...
    </el-card>

    <template v-else v-for="grain in data.grain_types" :key="grain.grain_type">
      <el-card style="margin-top: 16px;">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 20px; font-weight: bold;">{{ grain.grain_type }}区</span>
            <span>
              库存总重：
              <strong style="font-size: 28px; color: #409eff;">{{ grain.total_weight }}</strong> kg
              &nbsp;（{{ (Number(grain.total_weight) * 2).toFixed(2) }} 斤）
            </span>
          </div>
        </template>

        <el-table :data="grain.daily" stripe style="width: 100%" v-if="grain.daily.length > 0">
          <el-table-column label="日期" width="140">
            <template #default="{ row }">
              {{ row.date }}
            </template>
          </el-table-column>
          <el-table-column label="当日收购重量">
            <template #default="{ row }">
              {{ row.total_weight }} kg
            </template>
          </el-table-column>
          <el-table-column label="当日最后一次收购时间">
            <template #default="{ row }">
              {{ formatTime(row.last_purchase_at) }}
            </template>
          </el-table-column>
        </el-table>

        <el-empty v-else description="暂无每日记录" />
      </el-card>
    </template>

    <div style="display: flex; justify-content: center; margin-top: 20px;">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="data.total_pages * pageSize"
        layout="prev, pager, next"
        @current-change="loadData"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue"
import api from "@/api"

const loading = ref(true)
const page = ref(1)
const pageSize = ref(10)
const data = reactive({
  grain_types: [] as any[],
  total_pages: 1,
})

function formatTime(t: string | null) {
  if (!t) return "-"
  return t.replace("T", " ").slice(0, 19)
}

async function loadData() {
  loading.value = true
  try {
    const res: any = await api.get("/inventory/daily", {
      params: { page: page.value, page_size: pageSize.value },
    })
    data.grain_types = res.data.grain_types
    data.total_pages = res.data.total_pages
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

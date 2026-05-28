<template>
  <div>
    <div class="page-title">库存查看</div>

    <el-card>
      <el-table :data="list" stripe style="width: 100%">
        <el-table-column prop="grain_type" label="粮食品种" />
        <el-table-column label="库存重量">
          <template #default="{ row }">
            <strong style="font-size: 22px;">{{ row.total_weight }}</strong> kg
          </template>
        </el-table-column>
        <el-table-column label="折合斤数">
          <template #default="{ row }">
            {{ (Number(row.total_weight) * 2).toFixed(2) }} 斤
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import api from "@/api"

const list = ref<any[]>([])

onMounted(async () => {
  const res: any = await api.get("/inventory")
  list.value = res.data
})
</script>

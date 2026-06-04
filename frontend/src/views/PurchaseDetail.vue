<template>
  <div>
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
      <el-button @click="$router.push('/purchases')">← 返回列表</el-button>
      <div class="page-title" style="margin-bottom: 0;">收购单 #{{ purchase?.id }}</div>
    </div>

    <el-card v-if="purchase" style="max-width: 600px;">
      <el-descriptions :column="1" border size="large">
        <el-descriptions-item label="单号">{{ purchase.id }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTag(purchase.status)">
            {{ statusLabel(purchase.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="农户">{{ purchase.farmer_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="品种">{{ purchase.grain_type }}</el-descriptions-item>
        <el-descriptions-item label="毛重">{{ purchase.gross_weight }} kg</el-descriptions-item>
        <el-descriptions-item label="皮重（空车）">
          {{ purchase.empty_weight || '-' }} kg
        </el-descriptions-item>
        <el-descriptions-item label="净重">
          {{ purchase.net_weight || '-' }} kg
        </el-descriptions-item>
        <el-descriptions-item label="单价">{{ purchase.unit_price }} 元/斤</el-descriptions-item>
        <el-descriptions-item label="金额">
          <strong style="font-size: 24px; color: #e6a23c;">
            {{ purchase.total_amount || '-' }} 元
          </strong>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatTime(purchase.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="空车称重时间">{{ formatTime(purchase.empty_weighted_at) || '-' }}</el-descriptions-item>
        <el-descriptions-item label="结账时间">{{ formatTime(purchase.completed_at) || '-' }}</el-descriptions-item>
      </el-descriptions>

      <div style="margin-top: 24px; display: flex; gap: 16px;">
        <template v-if="purchase.status === 'GROSS_WEIGHTED'">
          <el-button type="warning" size="large" @click="showWeightDialog = true">
            称空车
          </el-button>
        </template>

        <template v-if="purchase.status === 'EMPTY_WEIGHTED'">
          <el-button type="success" size="large" :loading="completing" @click="handleComplete">
            完成收购
          </el-button>
        </template>
        <el-button type="danger" size="large" plain :loading="deleting" @click="handleDelete" style="margin-left: auto;">
          删除
        </el-button>
      </div>
    </el-card>

    <el-dialog v-model="showWeightDialog" title="称空车" width="400px" top="5vh" :lock-scroll="false">
      <el-form>
        <el-form-item label="空车重量(KG)">
          <el-input-number
            v-model="emptyWeight"
            :min="0"
            :step="10"
            :precision="2"
            style="width: 100%;"
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showWeightDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSetWeight">
          确认
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "@/api"
import { ElMessage, ElMessageBox } from "element-plus"

const route = useRoute()
const router = useRouter()
const purchase = ref<any>(null)
const showWeightDialog = ref(false)
const emptyWeight = ref(0)
const submitting = ref(false)
const completing = ref(false)
const deleting = ref(false)

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

function formatTime(t: string | null) {
  if (!t) return "-"
  return t.replace("T", " ").slice(0, 19)
}

function statusTag(s: string) {
  if (s === "COMPLETED") return "success"
  if (s === "EMPTY_WEIGHTED") return "warning"
  return "info"
}

async function handleSetWeight() {
  submitting.value = true
  try {
    const res: any = await api.post(`/purchases/${purchase.value.id}/set-empty-weight`, {
      empty_weight: emptyWeight.value,
    })
    purchase.value = res.data
    showWeightDialog.value = false
    ElMessage.success("空车重量已记录")
  } catch {
    // handled
  } finally {
    submitting.value = false
  }
}

async function handleComplete() {
  completing.value = true
  try {
    const res: any = await api.post(`/purchases/${purchase.value.id}/complete`)
    purchase.value = res.data
    ElMessage.success("收购完成")
  } catch {
    // handled
  } finally {
    completing.value = false
  }
}

async function handleDelete() {
  try {
    await ElMessageBox.confirm(
      `确认删除收购单 #${purchase.value.id}？此操作不可撤销。`,
      "删除确认",
      { confirmButtonText: "删除", cancelButtonText: "取消", type: "warning" },
    )
  } catch {
    return
  }
  deleting.value = true
  try {
    await api.delete(`/purchases/${purchase.value.id}`)
    ElMessage.success("收购单已删除")
    router.push("/purchases")
  } catch {
    // handled by interceptor
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  const res: any = await api.get(`/purchases/${route.params.id}`)
  purchase.value = res.data
})
</script>

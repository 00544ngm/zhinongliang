<template>
  <div>
    <div class="page-title">农户管理</div>

    <el-card>
      <div style="margin-bottom: 16px; display: flex; gap: 12px; flex-wrap: wrap;">
        <el-input
          v-model="keyword"
          placeholder="搜索农户姓名"
          style="width: 300px;"
          clearable
          @input="handleSearch"
        />
        <el-button type="primary" @click="showAddDialog = true">新增农户</el-button>
        <el-button @click="handleExportAll">导出全部</el-button>
        <el-button
          type="success"
          :disabled="selectedIds.length === 0"
          @click="handleExportSelected"
        >
          导出选中 ({{ selectedIds.length }})
        </el-button>
      </div>

      <el-table
        ref="tableRef"
        :data="list"
        stripe
        style="width: 100%"
        @selection-change="onSelectionChange"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="id_card" label="身份证号" />
        <el-table-column label="累计售粮重量">
          <template #default="{ row }">
            {{ row.total_weight }} kg
          </template>
        </el-table-column>
        <el-table-column label="累计金额">
          <template #default="{ row }">
            {{ row.total_amount }} 元
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="showDetail(row)">详情</el-button>
            <el-button size="small" type="default" link @click="editFarmer(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showAddDialog" title="新增农户" width="400px">
      <el-form ref="addFormRef" :model="addForm" :rules="addRules">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="addForm.name" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="addForm.phone" />
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="addForm.id_card" maxlength="18" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" :loading="adding" @click="handleAdd">确认</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditDialog" title="编辑农户" width="400px">
      <el-form ref="editFormRef" :model="editForm">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="editForm.phone" />
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="editForm.id_card" maxlength="18" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="editing" @click="handleEdit">确认</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showDetailDialog" :title="detailTitle" width="80%" top="5vh">
      <template v-if="detailFarmer">
        <el-descriptions :column="3" border size="small" style="margin-bottom: 16px;">
          <el-descriptions-item label="姓名">{{ detailFarmer.name }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ detailFarmer.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ detailFarmer.id_card || '-' }}</el-descriptions-item>
          <el-descriptions-item label="累计重量">{{ detailFarmer.total_weight }} kg</el-descriptions-item>
          <el-descriptions-item label="累计金额">{{ detailFarmer.total_amount }} 元</el-descriptions-item>
          <el-descriptions-item label="收购次数">{{ detailPurchases.length }} 次</el-descriptions-item>
        </el-descriptions>

        <el-table :data="detailPurchases" stripe style="width: 100%" v-loading="detailLoading">
          <el-table-column prop="id" label="单号" width="80" />
          <el-table-column prop="grain_type" label="品种" width="80" />
          <el-table-column label="毛重">
            <template #default="{ row }">{{ row.gross_weight }} kg</template>
          </el-table-column>
          <el-table-column label="皮重">
            <template #default="{ row }">{{ row.empty_weight || '-' }} kg</template>
          </el-table-column>
          <el-table-column label="净重">
            <template #default="{ row }">{{ row.net_weight || '-' }} kg</template>
          </el-table-column>
          <el-table-column label="单价">
            <template #default="{ row }">{{ row.unit_price }} 元/斤</template>
          </el-table-column>
          <el-table-column label="金额">
            <template #default="{ row }">{{ row.total_amount || '-' }} 元</template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="statusTag(row.status)">{{ statusLabel(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="创建时间" width="150">
            <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="结账时间" width="150">
            <template #default="{ row }">{{ formatTime(row.completed_at) || '-' }}</template>
          </el-table-column>
        </el-table>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import api from "@/api"
import { ElMessage } from "element-plus"
import type { ElTable } from "element-plus"

const list = ref<any[]>([])
const keyword = ref("")
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const adding = ref(false)
const editing = ref(false)
const addFormRef = ref()
const editFormRef = ref()
const tableRef = ref<InstanceType<typeof ElTable>>()
const selectedIds = ref<number[]>([])

const showDetailDialog = ref(false)
const detailFarmer = ref<any>(null)
const detailPurchases = ref<any[]>([])
const detailLoading = ref(false)
const detailTitle = ref("")

type FarmerForm = {
  _id?: number
  name: string
  phone: string
  id_card: string
}

const addForm = ref<FarmerForm>({ name: "", phone: "", id_card: "" })
const editForm = ref<FarmerForm>({ name: "", phone: "", id_card: "" })

const addRules = {
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
}

let searchTimer: ReturnType<typeof setTimeout>

function onSelectionChange(rows: any[]) {
  selectedIds.value = rows.map(r => r.id)
}

function handleSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(loadList, 300)
}

async function loadList() {
  const params: any = {}
  if (keyword.value) params.keyword = keyword.value
  const res: any = await api.get("/farmers", { params })
  list.value = res.data
}

async function handleAdd() {
  await addFormRef.value?.validate()
  adding.value = true
  try {
    await api.post("/farmers", addForm.value)
    ElMessage.success("农户添加成功")
    showAddDialog.value = false
    addForm.value = { name: "", phone: "", id_card: "" }
    loadList()
  } finally {
    adding.value = false
  }
}

function editFarmer(row: any) {
  editForm.value = { name: row.name, phone: row.phone || "", id_card: row.id_card || "" }
  editForm.value._id = row.id
  showEditDialog.value = true
}

async function handleEdit() {
  editing.value = true
  try {
    await api.put(`/farmers/${editForm.value._id}`, {
      name: editForm.value.name,
      phone: editForm.value.phone || null,
      id_card: editForm.value.id_card || null,
    })
    ElMessage.success("农户信息已更新")
    showEditDialog.value = false
    loadList()
  } finally {
    editing.value = false
  }
}

function statusLabel(s: string) {
  const map: Record<string, string> = {
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

function formatTime(t: string | null) {
  if (!t) return "-"
  return t.replace("T", " ").slice(0, 19)
}

async function showDetail(row: any) {
  detailFarmer.value = row
  detailTitle.value = `农户详情 - ${row.name}`
  detailLoading.value = true
  showDetailDialog.value = true
  try {
    const res: any = await api.get(`/purchases/by-farmer/${row.id}`)
    detailPurchases.value = res.data
  } catch {
    detailPurchases.value = []
  } finally {
    detailLoading.value = false
  }
}

async function handleExportAll() {
  await doExport(null)
}

async function handleExportSelected() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning("请先选择要导出的农户")
    return
  }
  await doExport(selectedIds.value)
}

async function doExport(farmerIds: number[] | null) {
  const loading = ElMessage({
    message: "正在生成导出文件...",
    icon: "el-icon-loading",
    duration: 0,
  })
  try {
    const res = await api.post("/farmers/export",
      { farmer_ids: farmerIds },
      { responseType: "blob" }
    )
    const url = window.URL.createObjectURL(new Blob([res as any]))
    const link = document.createElement("a")
    link.href = url
    const filename = `农户记录_${new Date().toISOString().slice(0, 10)}.xlsx`
    link.setAttribute("download", filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } finally {
    loading.close()
  }
}

onMounted(loadList)
</script>

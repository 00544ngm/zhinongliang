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
            <el-button size="small" @click="editFarmer(row)">编辑</el-button>
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

const addForm = ref({ name: "", phone: "", id_card: "" })
const editForm = ref({ name: "", phone: "", id_card: "" })

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

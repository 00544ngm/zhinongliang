<template>
  <div>
    <div class="page-title">农户管理</div>

    <el-card>
      <div style="margin-bottom: 16px; display: flex; gap: 12px;">
        <el-input
          v-model="keyword"
          placeholder="搜索农户姓名"
          style="width: 300px;"
          clearable
          @input="handleSearch"
        />
        <el-button type="primary" @click="showAddDialog = true">新增农户</el-button>
      </div>

      <el-table :data="list" stripe style="width: 100%">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="car_number" label="车牌号" />
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
        <el-form-item label="车牌号" prop="car_number">
          <el-input v-model="addForm.car_number" />
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
        <el-form-item label="车牌号" prop="car_number">
          <el-input v-model="editForm.car_number" />
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

const list = ref<any[]>([])
const keyword = ref("")
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const adding = ref(false)
const editing = ref(false)
const addFormRef = ref()
const editFormRef = ref()

const addForm = ref({ name: "", phone: "", car_number: "" })
const editForm = ref({ name: "", phone: "", car_number: "" })

const addRules = {
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
}

let searchTimer: ReturnType<typeof setTimeout>

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
    addForm.value = { name: "", phone: "", car_number: "" }
    loadList()
  } finally {
    adding.value = false
  }
}

function editFarmer(row: any) {
  editForm.value = { name: row.name, phone: row.phone || "", car_number: row.car_number || "" }
  editForm.value._id = row.id
  showEditDialog.value = true
}

async function handleEdit() {
  editing.value = true
  try {
    await api.put(`/farmers/${editForm.value._id}`, {
      name: editForm.value.name,
      phone: editForm.value.phone || null,
      car_number: editForm.value.car_number || null,
    })
    ElMessage.success("农户信息已更新")
    showEditDialog.value = false
    loadList()
  } finally {
    editing.value = false
  }
}

onMounted(loadList)
</script>

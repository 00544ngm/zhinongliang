<template>
  <div>
    <div class="page-title">新建收购</div>

    <el-card style="max-width: 600px;">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        size="large"
      >
        <el-form-item label="农户姓名" prop="farmer_name">
          <el-input v-model="form.farmer_name" placeholder="输入农户姓名" />
        </el-form-item>

        <el-form-item label="粮食品种" prop="grain_type">
          <el-select v-model="form.grain_type" placeholder="选择品种" style="width: 100%;">
            <el-option label="小麦" value="小麦" />
            <el-option label="玉米" value="玉米" />
            <el-option label="水稻" value="水稻" />
            <el-option label="大豆" value="大豆" />
            <el-option label="高粱" value="高粱" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>

        <el-form-item label="毛重(KG)" prop="gross_weight">
          <el-input-number
            v-model="form.gross_weight"
            :min="0"
            :step="10"
            :precision="2"
            style="width: 100%;"
          />
        </el-form-item>

        <el-form-item label="单价(元/斤)" prop="unit_price">
          <el-input-number
            v-model="form.unit_price"
            :min="0"
            :step="0.01"
            :precision="3"
            style="width: 100%;"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit" style="width: 100%;">
            创建收购单
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue"
import { useRouter } from "vue-router"
import api from "@/api"
import { ElMessage } from "element-plus"

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  farmer_name: "",
  grain_type: "",
  gross_weight: 0,
  unit_price: 0,
})

const rules = {
  farmer_name: [{ required: true, message: "请输入农户姓名", trigger: "blur" }],
  grain_type: [{ required: true, message: "请选择品种", trigger: "change" }],
  gross_weight: [{ required: true, message: "请输入毛重", trigger: "blur" }],
  unit_price: [{ required: true, message: "请输入单价", trigger: "blur" }],
}

async function handleSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res: any = await api.post("/purchases", form)
    ElMessage.success("收购单创建成功")
    router.push(`/purchases/${res.data.id}`)
  } catch {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>

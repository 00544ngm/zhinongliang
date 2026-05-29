<template>
  <div class="login-container" :style="{ '--login-bg-image': backgroundImage }">
    <div class="login-card">
      <h1 class="login-title">智农粮</h1>
      <p class="login-subtitle">粮食收购管理系统</p>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        @keyup.enter="handleLogin"
        size="large"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            style="width: 100%; height: 52px; font-size: 22px;"
            @click="handleLogin"
          >
            登 录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue"
import { useRouter } from "vue-router"
import { User, Lock } from "@element-plus/icons-vue"
import { useAuthStore } from "@/stores/auth"
import { useBackground } from "@/composables/useBackground"
import { ElMessage } from "element-plus"

const router = useRouter()
const auth = useAuthStore()
const { backgroundImage } = useBackground()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: "",
  password: "",
})

const rules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    await auth.login(form.username, form.password)
    ElMessage.success("登录成功")
    router.push("/dashboard")
  } catch {
    // error handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-image: var(--login-bg-image);
  background-position: center;
  background-size: cover;
}

.login-container::before {
  position: absolute;
  inset: 0;
  content: "";
  background:
    radial-gradient(circle at 22% 18%, rgba(255, 255, 255, 0.72), transparent 28%),
    linear-gradient(135deg, rgba(221, 247, 255, 0.68), rgba(179, 223, 248, 0.42));
}

.login-card {
  position: relative;
  z-index: 1;
  width: 420px;
  padding: 48px 40px;
  background: rgba(248, 253, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.72);
  border-radius: 20px;
  box-shadow: 0 24px 70px rgba(36, 111, 155, 0.2);
  backdrop-filter: blur(24px) saturate(1.2);
}

.login-title {
  text-align: center;
  font-size: 40px;
  color: #123246;
  margin-bottom: 8px;
  letter-spacing: 0;
}

.login-subtitle {
  text-align: center;
  font-size: 18px;
  color: #5f7e8f;
  margin-bottom: 36px;
}
</style>

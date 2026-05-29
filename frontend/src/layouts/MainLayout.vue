<template>
  <el-container style="min-height: 100vh">
    <el-aside width="260px" style="background: #1a1a2e">
      <div class="logo">马西军粮食收购站系统</div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#1a1a2e"
        text-color="#fff"
        active-text-color="#ffd700"
        style="border-right: none"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <span>工作台</span>
        </el-menu-item>
        <el-menu-item index="/purchases">
          <el-icon><Document /></el-icon>
          <span>收购管理</span>
        </el-menu-item>
        <el-menu-item index="/purchases/new">
          <el-icon><Plus /></el-icon>
          <span>新建收购</span>
        </el-menu-item>
        <el-menu-item index="/inventory">
          <el-icon><Box /></el-icon>
          <span>库存查看</span>
        </el-menu-item>
        <el-menu-item index="/farmers">
          <el-icon><User /></el-icon>
          <span>农户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="background: #fff; border-bottom: 2px solid #e0e0e0; display: flex; align-items: center; justify-content: space-between; height: 72px;">
        <h2 style="font-size: 24px; color: #1a1a2e;">{{ route.meta?.title || '智农粮' }}</h2>
        <div style="display: flex; align-items: center; gap: 16px;">
          <span style="font-size: 18px;">{{ auth.user?.username }}</span>
          <el-button type="danger" plain @click="handleLogout">退出</el-button>
        </div>
      </el-header>

      <el-main style="background: #f5f7fa; padding: 24px;">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
  auth.logout()
  router.push("/login")
}
</script>

<style scoped>
.logo {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: bold;
  color: #ffd700;
  letter-spacing: 2px;
  white-space: nowrap;
}

.el-menu-item {
  font-size: 18px !important;
  height: 56px !important;
}
</style>

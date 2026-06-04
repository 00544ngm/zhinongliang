<template>
  <el-container class="app-shell" :style="{ '--app-bg-image': backgroundImage, '--app-overlay-opacity': overlayOpacity }">
    <el-aside width="260px" class="app-aside">
      <div class="logo">马西军粮食收购站系统</div>
      <el-menu
        :default-active="route.path"
        router
        class="app-menu"
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
      <el-header class="app-header">
        <h2>{{ route.meta?.title || '智农粮' }}</h2>
        <div class="header-actions">
          <el-button plain class="background-button" @click="openBackgroundDialog">
            <el-icon><Picture /></el-icon>
            背景
          </el-button>
          <span class="user-name">{{ auth.user?.username }}</span>
          <el-button type="danger" plain @click="handleLogout">退出</el-button>
        </div>
      </el-header>

      <el-main class="app-main">
        <div class="glass-content">
          <router-view />
        </div>
      </el-main>
    </el-container>

    <el-dialog v-model="backgroundDialogVisible" title="更换背景" width="620px" top="5vh" :lock-scroll="false">
      <el-form label-position="top">
        <el-form-item>
          <template #label>
            <div class="photo-section-title">
              <span>项目照片</span>
              <el-button text size="small" :loading="backgroundPhotosLoading" @click="loadBackgroundPhotos">
                刷新
              </el-button>
            </div>
          </template>
          <div class="photo-picker">
            <button
              v-for="photo in backgroundPhotos"
              :key="photo.url"
              type="button"
              class="photo-option"
              :class="{ active: draftBackgroundUrl === photo.url }"
              @click="selectBackgroundPhoto(photo.url)"
            >
              <img :src="photo.url" :alt="photo.name" />
              <span>{{ photo.name }}</span>
            </button>
            <el-empty
              v-if="!backgroundPhotosLoading && backgroundPhotos.length === 0"
              description="photos/backgrounds 文件夹中暂无图片"
              :image-size="72"
            />
          </div>
        </el-form-item>
        <el-form-item label="遮罩透明度">
          <el-slider
            v-model="draftOpacity"
            :min="0"
            :max="1"
            :step="0.05"
            show-input
            :format-tooltip="(v: number) => `${Math.round(v * 100)}%`"
          />
          <span class="opacity-hint">降低透明度让背景图片更清晰，提高让文字更易读</span>
        </el-form-item>
        <el-form-item label="图片地址">
          <el-input
            v-model="draftBackgroundUrl"
            clearable
            placeholder="https://example.com/background.jpg 或 /photos/backgrounds/bg.jpg"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button plain @click="resetBackgroundUrl">
          <el-icon><RefreshLeft /></el-icon>
          默认
        </el-button>
        <el-button @click="backgroundDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveBackgroundUrl">
          <el-icon><Check /></el-icon>
          保存
        </el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { ElMessage } from "element-plus"
import api from "@/api"
import { useAuthStore } from "@/stores/auth"
import { useBackground } from "@/composables/useBackground"
import { useRoute, useRouter } from "vue-router"

interface BackgroundPhoto {
  name: string
  filename: string
  url: string
}

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const { backgroundUrl, backgroundImage, overlayOpacity, setBackgroundUrl, resetBackground, setOverlayOpacity } =
  useBackground()

const backgroundDialogVisible = ref(false)
const draftBackgroundUrl = ref("")
const draftOpacity = ref(0.6)
const backgroundPhotos = ref<BackgroundPhoto[]>([])
const backgroundPhotosLoading = ref(false)

function handleLogout() {
  auth.logout()
  router.push("/login")
}

function openBackgroundDialog() {
  draftBackgroundUrl.value = backgroundUrl.value
  draftOpacity.value = overlayOpacity.value
  backgroundDialogVisible.value = true
  loadBackgroundPhotos()
}

async function loadBackgroundPhotos() {
  backgroundPhotosLoading.value = true
  try {
    const res: any = await api.get("/background-photos")
    backgroundPhotos.value = res.data || []
  } catch {
    ElMessage.error("背景照片读取失败")
  } finally {
    backgroundPhotosLoading.value = false
  }
}

function selectBackgroundPhoto(url: string) {
  draftBackgroundUrl.value = url
}

function saveBackgroundUrl() {
  setBackgroundUrl(draftBackgroundUrl.value)
  setOverlayOpacity(draftOpacity.value)
  backgroundDialogVisible.value = false
}

function resetBackgroundUrl() {
  resetBackground()
  draftBackgroundUrl.value = ""
}
</script>

<style scoped>
.app-shell {
  position: relative;
  min-height: 100vh;
  background-image: var(--app-bg-image);
  background-position: center;
  background-size: cover;
  background-attachment: fixed;
}

.app-shell::before {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  content: "";
  opacity: var(--app-overlay-opacity, 0.6);
  background:
    linear-gradient(120deg, rgba(237, 252, 255, 0.7), rgba(209, 239, 255, 0.34)),
    radial-gradient(circle at 74% 18%, rgba(255, 255, 255, 0.58), transparent 26%);
}

.app-shell > .el-aside,
.app-shell > .el-container {
  position: relative;
  z-index: 1;
}

.app-aside {
  background: linear-gradient(
    180deg,
    rgba(231, 250, 255, 0.72),
    rgba(190, 230, 249, 0.46)
  );
  border-right: 1px solid rgba(255, 255, 255, 0.62);
  box-shadow: 12px 0 36px rgba(46, 123, 166, 0.13);
  backdrop-filter: blur(24px) saturate(1.25);
}

.logo {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 18px;
  font-size: 20px;
  font-weight: 900;
  color: #135476;
  letter-spacing: 0;
  white-space: nowrap;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8);
}

.app-menu {
  border-right: none !important;
  background: transparent !important;
}

.el-menu-item {
  margin: 6px 14px;
  border-radius: 14px;
  font-size: 18px !important;
  height: 56px !important;
  color: #24536a !important;
}

.el-menu-item:hover {
  background: rgba(255, 255, 255, 0.42) !important;
  color: #106592 !important;
}

.el-menu-item.is-active {
  color: #0f628f !important;
  background: rgba(255, 255, 255, 0.72) !important;
  box-shadow: inset 0 0 0 1px rgba(118, 194, 232, 0.42),
    0 12px 24px rgba(57, 140, 190, 0.12);
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  margin: 16px 20px 0;
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 18px;
  background: rgba(247, 253, 255, 0.62);
  box-shadow: 0 16px 40px rgba(46, 123, 166, 0.13);
  backdrop-filter: blur(22px) saturate(1.2);
}

.app-header h2 {
  font-size: 24px;
  color: #123246;
  letter-spacing: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.background-button {
  color: #176b95;
  border-color: rgba(124, 197, 232, 0.56);
  background: rgba(255, 255, 255, 0.46);
}

.user-name {
  font-size: 18px;
  color: #315c72;
}

.app-main {
  min-height: calc(100vh - 88px);
  padding: 24px 20px;
  background: transparent;
}

.glass-content {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.72), rgba(244, 252, 255, 0.42));
  border: 1px solid var(--znl-glass-border);
  border-radius: 18px;
  box-shadow: var(--znl-shadow);
  backdrop-filter: blur(24px) saturate(1.25);
  padding: 28px;
  min-height: calc(100vh - 136px);
}

.opacity-hint {
  display: block;
  margin-top: 6px;
  font-size: 13px;
  color: #8492a6;
  line-height: 1.4;
}

.photo-section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.photo-picker {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(132px, 1fr));
  gap: 12px;
  width: 100%;
  min-height: 96px;
}

.photo-option {
  display: grid;
  gap: 8px;
  padding: 8px;
  overflow: hidden;
  color: #315c72;
  text-align: left;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(124, 197, 232, 0.34);
  border-radius: 8px;
}

.photo-option:hover,
.photo-option.active {
  border-color: #4fa8f5;
  box-shadow: 0 8px 18px rgba(57, 140, 190, 0.16);
}

.photo-option img {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: 6px;
}

.photo-option span {
  overflow: hidden;
  font-size: 13px;
  line-height: 18px;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>

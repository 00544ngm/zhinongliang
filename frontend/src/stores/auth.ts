import { defineStore } from "pinia"
import { ref } from "vue"
import api from "@/api"

interface User {
  id: number
  username: string
  role: string
}

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null)
  const token = ref(localStorage.getItem("token") || "")

  async function login(username: string, password: string) {
    const res: any = await api.post("/auth/login", { username, password })
    token.value = res.access_token
    localStorage.setItem("token", res.access_token)
    await fetchUser()
  }

  async function fetchUser() {
    const res: any = await api.get("/auth/me")
    user.value = res
  }

  function logout() {
    user.value = null
    token.value = ""
    localStorage.removeItem("token")
  }

  return { user, token, login, fetchUser, logout }
})

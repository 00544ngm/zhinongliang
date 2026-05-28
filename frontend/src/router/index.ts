import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "Login",
      component: () => import("@/views/Login.vue"),
    },
    {
      path: "",
      component: () => import("@/layouts/MainLayout.vue"),
      redirect: "/dashboard",
      children: [
        {
          path: "dashboard",
          name: "Dashboard",
          component: () => import("@/views/Dashboard.vue"),
        },
        {
          path: "purchases",
          name: "Purchases",
          component: () => import("@/views/PurchaseList.vue"),
        },
        {
          path: "purchases/new",
          name: "NewPurchase",
          component: () => import("@/views/PurchaseNew.vue"),
        },
        {
          path: "purchases/:id",
          name: "PurchaseDetail",
          component: () => import("@/views/PurchaseDetail.vue"),
        },
        {
          path: "inventory",
          name: "Inventory",
          component: () => import("@/views/Inventory.vue"),
        },
        {
          path: "farmers",
          name: "Farmers",
          component: () => import("@/views/FarmerList.vue"),
        },
      ],
    },
  ],
})

router.beforeEach((to, _from) => {
  const token = localStorage.getItem("token")
  if (to.name !== "Login" && !token) {
    return { name: "Login" }
  }
})

export default router

import { createApp } from "vue"
import { createPinia } from "pinia"
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import * as ElementPlusIcons from "@element-plus/icons-vue"
import App from "./App.vue"
import router from "./router"
import "./style.css"

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus, { size: "large" })

for (const [key, component] of Object.entries(ElementPlusIcons)) {
  app.component(key, component)
}

app.mount("#app")

import { computed, ref, watch } from "vue"

const STORAGE_KEY = "znl-background-url"
const OPACITY_KEY = "znl-overlay-opacity"

const defaultBackground =
  "linear-gradient(135deg, rgba(216, 244, 255, 0.92), rgba(238, 252, 255, 0.78) 38%, rgba(196, 231, 255, 0.86)), radial-gradient(circle at 20% 18%, rgba(255, 255, 255, 0.95), transparent 28%), radial-gradient(circle at 78% 12%, rgba(151, 213, 255, 0.5), transparent 30%), linear-gradient(160deg, #d6f2ff 0%, #f6fdff 52%, #cfefff 100%)"

const backgroundUrl = ref(localStorage.getItem(STORAGE_KEY) || "")
const overlayOpacity = ref(Number(localStorage.getItem(OPACITY_KEY)) || 0.6)

watch(overlayOpacity, (val) => {
  localStorage.setItem(OPACITY_KEY, String(val))
})

function normalizeUrl(value: string) {
  return value.trim()
}

export function useBackground() {
  const backgroundImage = computed(() => {
    const url = normalizeUrl(backgroundUrl.value)
    return url ? `url("${url}")` : defaultBackground
  })

  function setBackgroundUrl(value: string) {
    const next = normalizeUrl(value)
    backgroundUrl.value = next
    if (next) {
      localStorage.setItem(STORAGE_KEY, next)
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  function resetBackground() {
    setBackgroundUrl("")
  }

  function setOverlayOpacity(val: number) {
    overlayOpacity.value = Math.max(0, Math.min(1, val))
  }

  return {
    backgroundUrl,
    backgroundImage,
    overlayOpacity,
    setBackgroundUrl,
    resetBackground,
    setOverlayOpacity,
  }
}

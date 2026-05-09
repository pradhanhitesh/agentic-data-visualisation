<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue"
import { useRoute, useRouter } from "vue-router"
import { marked } from "marked"

const route = useRoute()
const router = useRouter()
const sessionId = route.params.id

const insight = ref("")
const plots = ref([])
const loading = ref(true)

const goBack = () => {
  router.push('/upload')
}

// viewer state
const showViewer = ref(false)
const activeImage = ref("")
const activeIndex = ref(0)

const openViewer = (img, index) => {
  activeImage.value = img
  activeIndex.value = index
  showViewer.value = true
}

const closeViewer = () => {
  showViewer.value = false
}

// keyboard support
const handleKey = (e) => {
  if (!showViewer.value) return

  if (e.key === "Escape") closeViewer()

  if (e.key === "ArrowRight") nextImage()
  if (e.key === "ArrowLeft") prevImage()
}

const nextImage = () => {
  activeIndex.value = (activeIndex.value + 1) % plots.value.length
  activeImage.value = plots.value[activeIndex.value]
}

const prevImage = () => {
  activeIndex.value =
    (activeIndex.value - 1 + plots.value.length) % plots.value.length
  activeImage.value = plots.value[activeIndex.value]
}

const downloadReport = () => {
  // Directly point to the download API
  window.location.href = `/api/v1/assets/download/${sessionId}`
}

onMounted(async () => {
  window.addEventListener("keydown", handleKey)

  const res = await fetch(`/api/v1/assets/${sessionId}`)
  const data = await res.json()

  insight.value = marked.parse(data.insight || "")
  plots.value = data.plots || []
  loading.value = false
})

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleKey)
})
</script>

<template>
  <div class="page">
    <!-- GO BACK BUTTON -->
    <button class="back-btn" @click="goBack" title="Go back to upload">
      <i class="bi bi-arrow-left"></i>
    </button>

    <!-- DOWNLOAD BUTTON -->
    <button class="download-btn" @click="downloadReport" title="Download PDF Report">
      <i class="bi bi-download"></i>
    </button>

    <div v-if="loading"></div>
    <div v-else class="container">

      <!-- INSIGHTS -->
      <div class="insights" v-html="insight"></div>

      <!-- PLOTS -->
      <div class="plots">
        <img
          v-for="(p, i) in plots"
          :key="i"
          :src="p"
          class="plot"
          @click="openViewer(p, i)"
        />
      </div>

    </div>

    <!-- IMAGE VIEWER -->
    <div v-if="showViewer" class="viewer" @click.self="closeViewer">

      <button class="close" @click="closeViewer">✕</button>

      <button class="nav left" @click.stop="prevImage">‹</button>

      <img :src="activeImage" class="viewer-img" />

      <button class="nav right" @click.stop="nextImage">›</button>

    </div>
  </div>
</template>

<style scoped>
.back-btn {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 110;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #475569;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  transition: background 0.2s, color 0.2s;
}

.back-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.container {
  max-width: 900px;
  margin: auto;
  padding: 40px 20px;
}

.insights {
  margin-bottom: 40px;
  line-height: 1.6;
}

.plots {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.plot {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.viewer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.viewer-img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 8px;
}

.close {
  position: absolute;
  top: 20px;
  right: 30px;
  font-size: 24px;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}

.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 40px;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}

.nav.left {
  left: 30px;
}

.nav.right {
  right: 30px;
}

.plot {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.plot:hover {
  transform: scale(1.02);
}

@media (max-width: 600px) {
  .container {
    padding: 80px 20px 40px;
  }
  
  .plots {
    grid-template-columns: 1fr;
  }

  .download-btn {
    bottom: 16px;
    right: 16px;
    width: 44px;
    height: 44px;
    font-size: 18px;
  }
}

.download-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 110;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: none;
  background: #3b82f6;
  color: white;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transition: all 0.2s ease;
}

.download-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

</style>
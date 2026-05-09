<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useToast } from "vue-toastification"

const router = useRouter()
const toast = useToast()

const file = ref(null)
const fileName = ref("")
const loading = ref(false)

// Allowed file extensions
const ALLOWED_EXTENSIONS = [".csv", ".xlsx"]

// Sidebar state
const sidebarOpen = ref(false)
const recentSearches = ref([])

const STORAGE_KEY = "recentSearches"

// Modal state
const showDeleteModal = ref(false)
const deleteIndex = ref(null)

const showRenameModal = ref(false)
const renameIndex = ref(null)
const newSessionName = ref("")



// Load recent searches from localStorage
const loadSearches = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    recentSearches.value = raw ? JSON.parse(raw) : []
  } catch {
    recentSearches.value = []
  }
}

// Save a new search to localStorage
const saveSearch = (name, sessionId) => {
  const entry = { name, path: `/results/${sessionId}` }

  // Avoid duplicates (same name + path)
  recentSearches.value = recentSearches.value.filter(
    (s) => !(s.name === entry.name && s.path === entry.path)
  )

  // Prepend newest
  recentSearches.value.unshift(entry)

  localStorage.setItem(STORAGE_KEY, JSON.stringify(recentSearches.value))
}

// Navigate to a previous search
const goToSearch = (path) => {
  router.push(path)
}

// Toggle sidebar
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const deleteSearch = (index, event) => {
  event.stopPropagation()
  deleteIndex.value = index
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  deleteIndex.value = null
}

const confirmDelete = async () => {
  if (deleteIndex.value === null) return
  
  const index = deleteIndex.value
  const session = recentSearches.value[index]
  const sessionId = session.path.split("/").pop()

  try {
    // 1. Delete from local storage
    recentSearches.value.splice(index, 1)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(recentSearches.value))

    // 2. Delete from server
    await fetch(`/api/v1/assets/delete/${sessionId}`)
    toast.success("Analysis deleted")
  } catch (err) {
    console.error(err)
    toast.error("Failed to delete from server")
  } finally {
    cancelDelete()
  }
}

const openRenameModal = (index, event) => {
  event.stopPropagation()
  renameIndex.value = index
  newSessionName.value = recentSearches.value[index].name
  showRenameModal.value = true
}

const cancelRename = () => {
  showRenameModal.value = false
  renameIndex.value = null
  newSessionName.value = ""
}

const confirmRename = () => {
  if (renameIndex.value === null || !newSessionName.value.trim()) return

  recentSearches.value[renameIndex.value].name = newSessionName.value.trim()
  localStorage.setItem(STORAGE_KEY, JSON.stringify(recentSearches.value))
  
  toast.success("Session renamed")
  cancelRename()
}



const handleFile = async (e) => {
  if (loading.value) return

  const f = e.target.files[0]
  if (!f) return

  // Validate file extension
  const ext = f.name.substring(f.name.lastIndexOf(".")).toLowerCase()
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    toast.error("Only .csv and .xlsx files are allowed.")
    e.target.value = ""
    return
  }

  file.value = f
  fileName.value = f.name

  await upload()
}

const upload = async () => {
  if (loading.value) return

  loading.value = true

  const formData = new FormData()
  formData.append("file", file.value)

  try {
    const res = await fetch("/api/v1/assets/upload", {
      method: "POST",
      body: formData
    })

    const data = await res.json()

    if (!res.ok) {
      toast.error(data.error || "Upload failed")
      return
    }

    // Strip extension for the display name
    const displayName = fileName.value.replace(/\.[^/.]+$/, "")
    saveSearch(displayName, data.session_id)

    router.push(`/results/${data.session_id}`)

  } catch (e) {
    console.error(e)
    toast.error("Something went wrong. Please try again.")
  } finally {
    loading.value = false
  }
}

const goHome = () => {
  router.push("/")
}

onMounted(() => {
  loadSearches()
})
</script>

<template>
  <div class="page">

    <!-- HOME BUTTON -->
    <button class="home-btn" @click="goHome" title="Go to Home">
      <i class="bi bi-house"></i>
    </button>

    <!-- SIDEBAR TOGGLE -->
    <button class="sidebar-toggle" @click="toggleSidebar">
      <i :class="sidebarOpen ? 'bi bi-x-lg' : 'bi bi-clock-history'"></i>
    </button>

    <!-- COLLAPSIBLE SIDEBAR -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <h3 class="sidebar-title">Recent</h3>

      <div v-if="recentSearches.length === 0" class="sidebar-empty">
        No recent searches
      </div>

      <ul v-else class="sidebar-list">
        <li
          v-for="(s, i) in recentSearches"
          :key="i"
          class="sidebar-item"
          @click="goToSearch(s.path)"
        >
          <div class="item-info">
            <i class="bi bi-file-earmark-bar-graph item-icon"></i>
            <span class="item-name">{{ s.name }}</span>
          </div>
          <div class="item-actions">
            <button class="rename-btn" @click="openRenameModal(i, $event)" title="Rename analysis">
              <i class="bi bi-pencil"></i>
            </button>
            <button class="delete-btn" @click="deleteSearch(i, $event)" title="Delete analysis">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </li>
      </ul>

    </aside>

    <!-- MAIN CONTENT -->
    <div class="main-content">
      <div class="search-bar">

        <!-- CLICKABLE AREA -->
        <label class="file-trigger" :class="{ disabled: loading }">
          <input type="file" accept=".csv,.xlsx" @change="handleFile" :disabled="loading" hidden />
          <i class="bi bi-upload icon"></i>
          <span class="text">
            {{ loading ? "Analysing..." : (fileName || "Upload dataset...") }}
          </span>
        </label>

        <!-- ACTION BUTTON -->
        <div class="action">
          <i v-if="!loading" class="bi bi-arrow-up"></i>
          <i v-else class="bi bi-arrow-repeat spin"></i>
        </div>

      </div>
      <p class="limit-info">Note: Only five uploads per hour is allowed.</p>
    </div>

    <!-- DELETE CONFIRMATION MODAL -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showDeleteModal" class="modal-overlay" @click.self="cancelDelete">
          <div class="modal-content">
            <div class="modal-header">
              <p>This action cannot be undone. All data for "{{ recentSearches[deleteIndex]?.name }}" will be permanently removed.</p>
            </div>
            <div class="modal-actions">
              <button class="btn-cancel" @click="cancelDelete">Cancel</button>
              <button class="btn-delete" @click="confirmDelete">Delete</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- RENAME MODAL -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showRenameModal" class="modal-overlay" @click.self="cancelRename">
          <div class="modal-content">
            <div class="modal-header">
              <p>Enter a new name for this analysis.</p>
            </div>
            <div class="modal-body">
              <input 
                v-model="newSessionName" 
                type="text" 
                placeholder="Session name"
                class="modal-input"
                @keyup.enter="confirmRename"
                ref="renameInput"
              />
            </div>
            <div class="modal-actions">
              <button class="btn-cancel" @click="cancelRename">Cancel</button>
              <button class="btn-save" @click="confirmRename">Save</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>



<style scoped>
.page {
  height: 100vh;
  display: flex;
  background: #f8fafc;
  position: relative;
  overflow: hidden;
}

/* ── Sidebar toggle button ── */
.sidebar-toggle {
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

.sidebar-toggle:hover {
  background: #f1f5f9;
  color: #1e293b;
}

/* ── Sidebar ── */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 260px;
  height: 100vh;
  background: white;
  border-right: 1px solid #e2e8f0;
  padding: 64px 16px 24px;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 100;
  overflow-y: auto;
}

.sidebar.open {
  transform: translateX(0);
}

.sidebar-title {
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 16px;
  padding: 0 4px;
}

.sidebar-empty {
  font-size: 13px;
  color: #94a3b8;
  padding: 8px 4px;
}

.sidebar-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #334155;
  transition: background 0.15s;
}

.sidebar-item:hover {
  background: #f1f5f9;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow: hidden;
}

.item-icon {
  font-size: 16px;
  color: #64748b;
  flex-shrink: 0;
}

.item-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-btn:hover {
  color: #ef4444;
  background: #fee2e2;
}

.item-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

.sidebar-item:hover .item-actions {
  opacity: 1;
}

.rename-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.rename-btn:hover {
  color: #3b82f6;
  background: #eff6ff;
}


/* ── Main content ── */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.limit-info {
  font-size: 13px;
  color: #a9b1bb;
  font-weight: 500;
}

.search-bar {
  display: flex;
  align-items: center;
  width: 90%;
  max-width: 520px;
  padding: 14px 18px;
  border-radius: 999px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

.search-bar:hover {
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

.file-trigger {
  display: flex;
  align-items: center;
  flex: 1;
  cursor: pointer;
}

.icon {
  font-size: 18px;
  margin-right: 10px;
  color: #666;
}

.text {
  flex: 1;
  text-align: left;
  color: #555;
  font-size: 14px;
}

/* BUTTON */
.action {
  border: none;
  background: #3b82f6;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
}

.action:hover {
  background: #2563eb;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.disabled {
  pointer-events: none;
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive Styles */
@media (max-width: 600px) {
  .sidebar {
    width: 80%;
  }
  
  .search-bar {
    width: 95%;
    padding: 10px 14px;
  }
  
  .icon {
    font-size: 16px;
    margin-right: 8px;
  }
  
  .text {
    font-size: 13px;
  }
  
  .action {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }

  .home-btn {
    bottom: 16px;
    right: 16px;
    width: 44px;
    height: 44px;
    font-size: 18px;
  }
}

.home-btn {
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

.home-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

/* ── Modal Styles ── */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 400px;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  text-align: center;
  animation: modal-pop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modal-pop {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-header {
  margin-bottom: 28px;
}

.alert-icon {
  width: 56px;
  height: 56px;
  background: #fee2e2;
  color: #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin: 0 auto 20px;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.modal-header p {
  font-size: 15px;
  color: #64748b;
  line-height: 1.5;
}

.modal-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.modal-actions button {
  padding: 12px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-cancel {
  background: #f1f5f9;
  color: #475569;
}

.btn-cancel:hover {
  background: #e2e8f0;
}

.btn-delete {
  background: #ef4444;
  color: white;
}

.btn-delete:hover {
  background: #dc2626;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-save {
  background: #3b82f6;
  color: white;
}

.btn-save:hover {
  background: #2563eb;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.modal-input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  font-size: 15px;
  margin-bottom: 24px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.modal-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}


/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
// Import dependencies
import { createRouter, createWebHistory } from 'vue-router'

// Import vue-components
import HomePage from '@/components/HomePage.vue'
import UploadData from '@/components/UploadData.vue'
import ResultsPage from '@/components/ResultsPage.vue'

// Define routes
const routes = [
    { path: '/', component: HomePage },
    { path: '/upload', component: UploadData },
    { path: '/results/:id', component: ResultsPage }
]

// Define router
const router = createRouter({
    history: createWebHistory(),
    routes
})

// Export router
export default router
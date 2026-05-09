// main.css
import './assets/main.css'

// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import Bootstrap CSS & JS
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import Toast, { POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App)
app.use(router)
app.use(Toast, {
  position: POSITION.TOP_RIGHT,
  timeout: 2000,
  closeOnClick: true,
  pauseOnHover: true,
});
app.mount('#app')
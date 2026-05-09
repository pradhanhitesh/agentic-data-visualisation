<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const timeline = [
  {
    version: 'V0.0 - April 15, 2026',
    title: 'Ideation & Planning',
    description: 'Taking part in Kaggle Playground Competititions - I thought why not use AI for data visualization (yet again another ChatGPT wrapper, heavy sigh). ',
    status: 'completed'
  },
  {
    version: 'V1.0 - May 04, 2026',
    title: 'Core Engine Release',
    description: 'Initial launch featuring automated data profiling, CSV processing, and AI-driven static plot generation.',
    status: 'latest'
  },
  {
    version: 'V2.0 - TBD',
    title: 'Multi-Agent Reasoning',
    description: 'Planned integration of collaborative agent swarms for deep analytical reasoning and interactive 3D charts.',
    status: 'planned'
  }
]

const features = [
  {
    title: "AI Insights & Plots",
    description: "Automatically generates deep analytical insights and professional-grade visualizations from your raw data.",
    icon: "bi-magic"
  },
  {
    title: "Local Privacy",
    description: "Your data stays yours. History is stored locally in your browser with full control to delete anytime.",
    icon: "bi-shield-lock"
  },
  {
    title: "Zero Friction",
    description: "No sign-up or accounts required. Just upload your file and start getting answers immediately.",
    icon: "bi-lightning-charge"
  },
  {
    title: "PDF Reports",
    description: "Export your entire analysis, including all insights and charts, into a beautifully formatted PDF report.",
    icon: "bi-file-earmark-pdf"
  },
  {
    title: "Zero Cost",
    description: "Enjoy full access to all features completely free of charge, with no hidden fees or subscriptions.",
    icon: "bi-cash-coin"
  },
  {
    title: "Multi-format Support",
    description: "Seamlessly process and analyze both .csv and .xlsx files with a single click.",
    icon: "bi-file-earmark-spreadsheet"
  }
]

const navigateToUpload = () => {
  router.push('/upload')
}

const scrollToFeatures = () => {
  const el = document.getElementById('features')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <header class="hero">
      <div class="hero-content">
        <h1>Transform Data into <span>Insights</span></h1>
        <p class="description">
          Agentic Data Visualization is an intelligent platform designed to transform raw datasets into meaningful visual stories. 
          Leveraging advanced agents, it automatically analyzes, profiles, and visualizes data to uncover hidden patterns with zero friction.
        </p>
        <div class="hero-actions">
          <button @click="navigateToUpload" class="cta-btn">Start Visualizing</button>
          <button @click="scrollToFeatures" class="cta-btn secondary">Explore Features</button>
        </div>
      </div>
    </header>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="features-grid">
        <div v-for="(f, i) in features" :key="i" class="feature-card">
          <div class="feature-icon">
            <i :class="['bi', f.icon]"></i>
          </div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.description }}</p>
        </div>
      </div>
    </section>

    <!-- Timeline Section -->
    <section class="timeline-section">
      <div class="timeline">
        <div 
          v-for="(item, index) in timeline" 
          :key="index" 
          class="timeline-item"
          :class="item.status"
        >
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="version-tag">{{ item.version }}</div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
            <span class="status-badge">{{ item.status }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2026 Hitesh Pradhan</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.home-page {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #1e293b;
  background: #f8fafc;
  min-height: 100vh;
}

/* Navbar Styles */
.navbar {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  border-bottom: 1px solid #e2e8f0;
}

.nav-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #0f172a;
}

.logo span {
  color: #3b82f6;
}

.nav-btn {
  text-decoration: none;
  background: #3b82f6;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

/* Hero Section */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  background: radial-gradient(circle at top right, #eff6ff 0%, #f8fafc 100%);
}

.hero-content {
  max-width: 800px;
}

/* Features Section */
.features-section {
  padding: 6rem 2rem;
  background: white;
}

.features-grid {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2.5rem;
}

.feature-card {
  padding: 2.5rem;
  border-radius: 24px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  background: white;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
  border-color: #e2e8f0;
}

.feature-icon {
  width: 50px;
  height: 50px;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #0f172a;
}

.feature-card p {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
}

h1 {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: #0f172a;
  letter-spacing: -0.05em;
}

h1 span {
  background: linear-gradient(135deg, #3b82f6 0%, #2dd4bf 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.description {
  font-size: 1.25rem;
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  gap: 1.25rem;
  justify-content: center;
  align-items: center;
}

.cta-btn {
  background: #0f172a;
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.cta-btn:hover {
  background: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
}

.cta-btn.secondary {
  background: transparent;
  color: #0f172a;
  border: 2px solid #e2e8f0;
}

.cta-btn.secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Timeline Section */
.timeline-section {
  max-width: 900px;
  margin: 0 auto;
  padding: 6rem 2rem;
}

h2 {
  text-align: center;
  font-size: 2.25rem;
  font-weight: 800;
  margin-bottom: 4rem;
  color: #0f172a;
}

.timeline {
  position: relative;
  border-left: 2px solid #e2e8f0;
  margin-left: 20px;
  padding-left: 40px;
}

.timeline-item {
  position: relative;
  margin-bottom: 3rem;
}

.timeline-dot {
  position: absolute;
  left: -49px;
  top: 4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #e2e8f0;
  border: 4px solid #f8fafc;
  z-index: 10;
}

.timeline-item.completed .timeline-dot {
  background: #10b981;
}

.timeline-item.latest .timeline-dot {
  background: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.timeline-content {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.timeline-content:hover {
  transform: translateX(8px);
}

.version-tag {
  font-size: 0.75rem;
  font-weight: 700;
  color: #3b82f6;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

p {
  color: #64748b;
  line-height: 1.6;
}

.status-badge {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  border-radius: 999px;
  background: #f1f5f9;
}

.completed .status-badge {
  background: #ecfdf5;
  color: #059669;
}

.latest .status-badge {
  background: #eff6ff;
  color: #2563eb;
}

/* Footer */
.footer {
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  background: white;
}

.footer-content {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #94a3b8;
  font-size: 0.9rem;
}

.footer-content p {
  margin: 0;
}

.footer-github {
  color: #94a3b8;
  font-size: 1.4rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}

.footer-github:hover {
  color: #0f172a;
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>

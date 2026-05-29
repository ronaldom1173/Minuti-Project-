<template>
  <div class="dashboard-container">
    <!-- Sidebar navigation -->
    <aside class="sidebar">
      <nav class="sidebar-nav">
        <div class="user-info">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-details">
            <span class="user-role">{{ userRole }}</span>
          </div>
        </div>
        
        <ul class="nav-list">
          <li 
            @click="showComponent('home')" 
            :class="['nav-item', currentComponent === 'home' ? 'active' : '']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="nav-icon"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            <span>Dashboard</span>
          </li>
          <li 
            @click="showComponent('foodLog')" 
            :class="['nav-item', currentComponent === 'foodLog' ? 'active' : '']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="nav-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            <span>Products</span>
          </li>
          <li 
            @click="showComponent('reports')" 
            :class="['nav-item', currentComponent === 'reports' ? 'active' : '']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="nav-icon"><path d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2z"></path><line x1="7" y1="7" x2="7" y2="7"></line><line x1="17" y1="7" x2="17" y2="7"></line><line x1="7" y1="12" x2="17" y2="12"></line><line x1="7" y1="17" x2="17" y2="17"></line></svg>
            <span>Waste Logs</span>
          </li>
          
          <li class="nav-divider"></li>
          
          <li 
            @click="showComponent('Analytics'); analyticsTab = 'overview'" 
            :class="['nav-item', currentComponent === 'Analytics' ? 'active' : '']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="nav-icon"><path d="M18 20V10M12 20V4M6 20v-6"></path></svg>
            <span>Analytics</span>
          </li>
          
          <!-- Analytics subitems -->
          <li 
            v-if="currentComponent === 'Analytics'"
            @click="showComponent('Analytics'); analyticsTab = 'overview'" 
            :class="['nav-subitem', analyticsTab === 'overview' ? 'active' : '']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="nav-icon-small"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            <span>Overview</span>
          </li>
          <li 
            v-if="currentComponent === 'Analytics'"
            @click="showComponent('Analytics'); analyticsTab = 'report'" 
            :class="['nav-subitem', analyticsTab === 'report' ? 'active' : '']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="nav-icon-small"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            <span>Reports</span>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- Main content area -->
    <main class="main-area">
      <!-- Display different components based on selection -->
      <div v-if="currentComponent === 'home'" class="dashboard-content">
        <div class="page-header">
          <h1>Dashboard</h1>
          <div class="page-subtitle">Welcome to Minuti Waste Management</div>
        </div>
        <Home />
      </div>
      
      <div v-if="currentComponent === 'foodLog'" class="dashboard-content">
        <div class="page-header">
          <h1>Product Management</h1>
          <div class="page-subtitle">Manage your inventory items</div>
        </div>
        <FoodLog />
      </div>
      
      <div v-if="currentComponent === 'reports'" class="dashboard-content">
        <div class="page-header">
          <h1>Waste Reports</h1>
          <div class="page-subtitle">Record and view waste data</div>
        </div>
        <reports />
      </div>
      
      <div v-if="currentComponent === 'Analytics'" class="dashboard-content">
        <div class="page-header">
          <h1>Analytics</h1>
          <div class="page-subtitle">
            {{ analyticsTab === 'overview' ? 'Data overview and insights' : 'Generate detailed reports' }}
          </div>
        </div>
        <Analytics :tab="analyticsTab" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import Home from './Home.vue';
import FoodLog from './foodLog.vue';
import reports from './reports.vue';
import Analytics from './analytics.vue';

const currentComponent = ref('home');
const analyticsTab = ref('overview');
const userName = ref('');
const userRole = ref('');

const userInitials = computed(() => {
  if (userName.value) {
    return userName.value.split(' ').map(name => name[0]).join('');
  }
  return userRole.value ? userRole.value[0].toUpperCase() : 'U';
});

const showComponent = (component) => {
  currentComponent.value = component;
  if (component !== 'Analytics') {
    analyticsTab.value = 'overview'; 
  }
};

onMounted(() => {
  const storedRole = localStorage.getItem('userRole');
  userRole.value = storedRole ? storedRole.charAt(0).toUpperCase() + storedRole.slice(1) : 'User';
  userName.value = localStorage.getItem('username') || '';
});
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: calc(100vh - 138px); /* Account for header and footer */
}

/* Sidebar styling */
.sidebar {
  width: 250px;
  background: var(--surface);
  box-shadow: 1px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 10;
}

.sidebar-nav {
  padding: var(--space-md);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: var(--space-xl);
  padding: var(--space-md);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: var(--space-md);
}

.user-details {
  flex: 1;
}

.user-role {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  font-weight: 500;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: var(--space-md);
  border-radius: 6px;
  margin-bottom: var(--space-xs);
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
}

.nav-item:hover {
  background-color: rgba(111, 78, 55, 0.1);
  color: var(--primary);
}

.nav-item.active {
  background-color: rgba(111, 78, 55, 0.15);
  color: var(--primary);
  font-weight: 500;
}

.nav-subitem {
  display: flex;
  align-items: center;
  padding: var(--space-sm) var(--space-md);
  padding-left: var(--space-xl);
  border-radius: 6px;
  margin-bottom: var(--space-xs);
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.nav-subitem:hover {
  background-color: rgba(111, 78, 55, 0.05);
  color: var(--primary);
}

.nav-subitem.active {
  background-color: rgba(111, 78, 55, 0.1);
  color: var(--primary);
  font-weight: 500;
}

.nav-icon {
  width: 18px;
  height: 18px;
  margin-right: var(--space-md);
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.nav-icon-small {
  width: 14px;
  height: 14px;
  margin-right: var(--space-md);
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.nav-divider {
  height: 1px;
  background-color: rgba(0, 0, 0, 0.1);
  margin: var(--space-md) 0;
}

/* Main content area */
.main-area {
  flex: 1;
  overflow-y: auto;
  background-color: var(--background);
}

.dashboard-content {
  padding: var(--space-lg);
}

.page-header {
  margin-bottom: var(--space-xl);
}

.page-header h1 {
  font-size: var(--text-heading);
  margin-bottom: var(--space-xs);
  color: var(--primary-dark);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: var(--text-md);
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    position: relative;
  }
  
  .main-area {
    width: 100%;
  }
}
</style>
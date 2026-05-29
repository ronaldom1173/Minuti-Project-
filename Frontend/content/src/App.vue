<script setup>
import Login from './components/Login.vue';
import TheWelcome from './components/TheWelcome.vue';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoggedIn = ref(false);

onMounted(() => {
  const userRole = localStorage.getItem('userRole');
  isLoggedIn.value = !!userRole;
  
  // Redirect if needed
  if (!isLoggedIn.value && router.currentRoute.value.path !== '/') {
    router.push('/');
  }
});
</script>

<template>
  <div class="app-container">
    <!-- Header with logo -->
    <header class="app-header">
      <div class="header-content">
        <!-- Coffee Mug SVG Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M160-120v-80h640v80H160Zm160-160q-66 0-113-47t-47-113v-400h640q33 0 56.5 23.5T880-760v120q0 33-23.5 56.5T800-560h-80v120q0 66-47 113t-113 47H320Zm0-80h240q33 0 56.5-23.5T640-440v-320H240v320q0 33 23.5 56.5T320-360Zm400-280h80v-120h-80v120ZM320-360h-80 400-320Z"/></svg>
        <h1 class="app-title">Minuti Coffee Waste Manager</h1>
      </div>
      
      <div v-if="isLoggedIn" class="user-controls">
        <button @click="router.push('/')" class="logout-btn">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18"><path d="M19 21h-9a2 2 0 0 1-2-2v-4h2v4h9V5h-9v4H8V5a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2z"></path><path d="M13 10V8l-5 4 5 4v-2H3v-4h10z"></path></svg>
          Logout
        </button>
      </div>
    </header>

    <!-- Main content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="app-footer">
      <p>&copy; Code Catalyst <span id="current-year">{{ new Date().getFullYear() }}</span></p>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
  /* Modern coffee-themed color palette */
  --primary: #6F4E37; /* Coffee brown */
  --primary-light: #A67C52; /* Lighter coffee brown */
  --primary-dark: #422D1C; /* Darker coffee brown */
  --accent: #D4A373; /* Caramel */
  --secondary: #E9DAC1; /* Coffee cream */
  --background: #F9F5EB; /* Light cream background */
  --surface: #FFFFFF; /* White surface */
  --text-primary: #1A1A1A; /* Almost black */
  --text-secondary: #5F5F5F; /* Medium gray */
  --text-tertiary: #8A8A8A; /* Light gray */
  --danger: #D32F2F; /* Red */
  --success: #388E3C; /* Green */
  --warning: #F57C00; /* Orange */
  
  /* Spacing system */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-xxl: 3rem;

  /* Font sizes */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-md: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-xxl: 1.5rem;
  --text-heading: 2rem;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--background);
  color: var(--text-primary);
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  background-color: var(--surface);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.logo-icon {
  width: 2.5rem;
  height: 2.5rem;
  fill: var(--primary);
}

.app-title {
  font-size: var(--text-xl);
  color: var(--primary);
  margin: 0;
  font-weight: 600;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--text-tertiary);
  border-radius: 4px;
  padding: var(--space-xs) var(--space-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: var(--primary);
  color: var(--surface);
  border-color: var(--primary);
}

.logout-btn svg {
  fill: currentColor;
}

.main-content {
  flex: 1;
  padding: 0;
  background-color: var(--background);
}

.app-footer {
  background-color: var(--primary-dark);
  color: var(--surface);
  text-align: center;
  padding: var(--space-md);
  font-size: var(--text-sm);
}

/* Utility classes */
.card {
  background-color: var(--surface);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
}

.btn {
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 4px;
  padding: var(--space-sm) var(--space-lg);
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn:hover {
  background-color: var(--primary-light);
}

.btn-secondary {
  background-color: var(--secondary);
  color: var(--primary-dark);
}

.btn-secondary:hover {
  background-color: var(--accent);
}

.btn-danger {
  background-color: var(--danger);
}

.btn-danger:hover {
  background-color: #B71C1C;
}

.text-danger {
  color: var(--danger);
}

.text-success {
  color: var(--success);
}

</style>
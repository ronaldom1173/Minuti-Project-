import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import TheWelcome from '../components/TheWelcome.vue';

const routes = [
  { path: '/', name: 'Login', component: Login },         // Default route: Login (disabled)
  { path: '/Home', name: 'Home', component: TheWelcome }    // Welcome page after login
];

const router = createRouter({
  history: createWebHistory('/'),
  routes,
});

export default router;

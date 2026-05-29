import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // This imports your router/index.js

const app = createApp(App);
app.use(router);  // Registers Vue Router globally
app.mount('#app');
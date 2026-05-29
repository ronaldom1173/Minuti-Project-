<template>
  <div class="login-wrapper">
    <div class="login-card">
      
      <h1>Minuti Coffee</h1>
      <h2>Waste Management System</h2>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-field">
          <label for="username">Username</label>
          <input 
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter your username"
            required
          />
        </div>
        
        <div class="form-field">
          <label for="password">Password</label>
          <div class="password-field">
            <input 
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
            <button 
              type="button" 
              class="toggle-password" 
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? 'Hide' : 'Show' }}
            </button>
          </div>
        </div>
        
        <div v-if="errorMessage" class="error">
          {{ errorMessage }}
        </div>
        
        <button type="submit" class="login-button">Log In</button>
      </form>
      
      <p class="login-hint">Staff access only | Contact admin for support</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '@/api';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const showPassword = ref(false);
const router = useRouter();

const handleLogin = async () => {
  try {
    errorMessage.value = '';
    
    if (!username.value || !password.value) {
      errorMessage.value = 'Please enter both username and password';
      return;
    }
    
    const user = await login(username.value, password.value);
    
    if (user && user.role) {
      localStorage.setItem('userRole', user.role);
      localStorage.setItem('username', username.value);
      router.push('/Home');
    } else {
      errorMessage.value = 'Invalid credentials';
    }
  } catch (error) {
    console.error('Login error:', error);
    errorMessage.value = error.message || 'Login failed. Please try again.';
  }
};
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f4e9;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
  text-align: center;
}

.logo {
  margin-bottom: 20px;
}

.logo-image {
  width: 80px;
  height: 80px;
}

h1 {
  color: #6F4E37;
  font-size: 24px;
  margin: 0 0 8px 0;
}

h2 {
  color: #A67C52;
  font-size: 16px;
  font-weight: normal;
  margin: 0 0 30px 0;
}

.login-form {
  text-align: left;
}

.form-field {
  margin-bottom: 20px;
}

label {
  display: block;
  color: #555;
  font-size: 14px;
  margin-bottom: 6px;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box;
}

input:focus {
  border-color: #A67C52;
  outline: none;
  box-shadow: 0 0 0 3px rgba(166, 124, 82, 0.2);
}

.password-field {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #A67C52;
  cursor: pointer;
  font-size: 14px;
}

.login-button {
  width: 100%;
  background-color: #6F4E37;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #5d4230;
}

.error {
  background-color: #fdeaea;
  color: #d32f2f;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 14px;
}

.login-hint {
  margin-top: 25px;
  font-size: 12px;
  color: #888;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
}
</style>
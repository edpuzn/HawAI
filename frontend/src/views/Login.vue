<template>
  <div class="card" style="max-width:380px;margin:80px auto;">
    <h2>Giriş</h2>
    <form @submit.prevent="onSubmit">
      <div>
        <label>Email</label>
        <input v-model="email" type="email" required style="width:100%" />
      </div>
      <div style="margin-top:8px">
        <label>Şifre</label>
        <input v-model="password" type="password" required style="width:100%" />
      </div>
      <button style="margin-top:12px" :disabled="loading">Giriş yap</button>
      <p style="margin-top:8px">Hesabın yok mu? <router-link to="/register">Kayıt ol</router-link></p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from '../utils/axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const loading = ref(false)
const router = useRouter()

async function onSubmit() {
  loading.value = true
  try {
    await axios.post('/auth/login', { email: email.value, password: password.value })
    router.push('/chat')
  } finally {
    loading.value = false
  }
}
</script>



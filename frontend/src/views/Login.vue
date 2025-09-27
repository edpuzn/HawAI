<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>Giriş</h2>
        <p class="login-subtitle">Hesabınıza giriş yapın</p>
      </div>
      <form @submit.prevent="onSubmit" class="login-form">
        <div class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="form-input"
            placeholder="email@example.com"
          />
        </div>
        <div class="form-group">
          <label class="form-label">Şifre</label>
          <input
            v-model="password"
            type="password"
            required
            class="form-input"
            placeholder="••••••••"
          />
        </div>
        <button type="submit" class="btn-primary login-btn" :disabled="loading">
          <span v-if="loading">Giriş yapılıyor...</span>
          <span v-else>Giriş yap</span>
        </button>
        <p class="login-footer">
          Hesabın yok mu?
          <router-link to="/register" class="login-link">Kayıt ol</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "../utils/axios";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const loading = ref(false);
const router = useRouter();

async function onSubmit() {
  loading.value = true;
  try {
    await axios.post("/auth/login", {
      email: email.value,
      password: password.value,
    });
    router.push("/chat");
  } catch (err: any) {
    const status = err?.response?.status;
    if (status === 401) {
      try {
        // Otomatik kayıt dene, ardından tekrar login dene
        await axios.post("/auth/register", {
          email: email.value,
          password: password.value,
        });
        await axios.post("/auth/login", {
          email: email.value,
          password: password.value,
        });
        router.push("/chat");
        return;
      } catch (e: any) {
        const detail = e?.response?.data?.detail || "Giriş başarısız. Lütfen bilgileri kontrol edin.";
        window.alert(detail);
      }
    } else {
      const detail = err?.response?.data?.detail || "Giriş başarısız. Lütfen bilgileri kontrol edin.";
      window.alert(detail);
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 128px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-900);
}

.login-subtitle {
  margin: 0;
  color: var(--text-600);
  font-size: 16px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 600;
  color: var(--text-900);
  font-size: 14px;
}

.form-input {
  padding: 12px 16px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--input-bg);
  color: var(--text-900);
  font-size: 16px;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--brand-500);
  box-shadow: 0 0 0 3px var(--ring);
}

.form-input::placeholder {
  color: var(--input-placeholder);
}

.login-btn {
  width: 100%;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 600;
  margin-top: 8px;
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.login-footer {
  text-align: center;
  margin: 24px 0 0 0;
  color: var(--text-600);
  font-size: 14px;
}

.login-link {
  color: var(--brand-600);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: var(--brand-700);
  text-decoration: underline;
}
</style>

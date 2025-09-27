<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>Kayıt Ol</h2>
        <p class="register-subtitle">Yeni hesap oluşturun</p>
      </div>
      <form @submit.prevent="onSubmit" class="register-form">
        <div class="form-group">
          <label class="form-label">Kullanıcı Adı</label>
          <input
            v-model="username"
            type="text"
            required
            class="form-input"
            placeholder="Kullanıcı adınızı girin"
          />
        </div>
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
        <button
          type="submit"
          class="btn-primary register-btn"
          :disabled="loading"
        >
          <span v-if="loading">Kayıt oluşturuluyor...</span>
          <span v-else>Kayıt ol</span>
        </button>
        <p class="register-footer">
          Hesabın var mı?
          <router-link to="/login" class="register-link">Giriş yap</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "../utils/axios";
import { useRouter } from "vue-router";

const username = ref("");
const email = ref("");
const password = ref("");
const loading = ref(false);
const router = useRouter();

async function onSubmit() {
  loading.value = true;
  try {
    // Backend yalnızca email ve password bekliyor
    await axios.post("/auth/register", {
      email: email.value,
      password: password.value,
    });
    await axios.post("/auth/login", {
      email: email.value,
      password: password.value,
    });
    router.push("/chat");
  } catch (err: any) {
    const status = err?.response?.status;
    const detail = err?.response?.data?.detail;
    if (status === 400 && String(detail).includes("email exists")) {
      window.alert("Bu e‑posta zaten kayıtlı. Lütfen giriş yapın.");
      router.push("/login");
    } else {
      window.alert(detail || "Kayıt başarısız. Lütfen bilgileri kontrol edin.");
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.register-container {
  min-height: calc(100vh - 128px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.register-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-header h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-900);
}

.register-subtitle {
  margin: 0;
  color: var(--text-600);
  font-size: 16px;
}

.register-form {
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

.register-btn {
  width: 100%;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 600;
  margin-top: 8px;
}

.register-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.register-footer {
  text-align: center;
  margin: 24px 0 0 0;
  color: var(--text-600);
  font-size: 14px;
}

.register-link {
  color: var(--brand-600);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.register-link:hover {
  color: var(--brand-700);
  text-decoration: underline;
}
</style>

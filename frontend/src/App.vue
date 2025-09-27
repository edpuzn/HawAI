<template>
  <div class="app-shell">
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg nav-glass">
      <div class="container-fluid nav-inner">
        <!-- Marka (sol) -->
        <router-link class="navbar-brand brand" to="/" aria-label="HawAI Home">
          <span class="logo">Haw<span class="accent">AI</span></span>
        </router-link>

        <!-- Mobil menü toggler -->
        <button
          ref="togglerEl"
          class="navbar-toggler"
          type="button"
          :aria-expanded="isNavOpen ? 'true' : 'false'"
          aria-label="Toggle navigation"
          @click="toggleNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Çöken menü -->
        <div
          class="collapse navbar-collapse"
          id="navbarsExampleDefault"
          ref="collapseEl"
        >
          <ul class="navbar-nav ms-auto me-3 mb-2 mb-lg-0 links">
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{
                  active: $route.path === '/chat' || $route.path === '/',
                }"
                to="/chat"
              >
                Sohbet
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path === '/about' }"
                to="/about"
              >
                Hakkında
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path === '/ilkyardim' }"
                to="/ilkyardim"
              >
                İlk Yardım
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path === '/developers' }"
                to="/developers"
              >
                Geliştiriciler
              </router-link>
            </li>
          </ul>

          <div class="d-flex align-items-center gap-2 right">
            <!-- Auth controls (koşullu) -->
            <div class="me-2 d-flex align-items-center gap-2">
              <template v-if="isAuthed">
                <span class="user-pill" title="Oturum açık">
                  <span class="dot ok"></span>{{ shortUserId }}
                </span>
                <button
                  class="btn btn-sm btn-outline-danger"
                  type="button"
                  @click="logout"
                >
                  Çıkış
                </button>
              </template>
              <template v-else>
                <router-link
                  class="nav-auth-btn nav-auth-btn--secondary"
                  to="/login"
                  >Giriş</router-link
                >
                <router-link
                  class="nav-auth-btn nav-auth-btn--primary"
                  to="/register"
                  >Kayıt ol</router-link
                >
              </template>
            </div>
            <button
              class="theme-toggle"
              @click="toggleTheme"
              :aria-label="
                theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'
              "
            >
              <svg
                v-if="theme === 'dark'"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden="true"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="5"
                  stroke="currentColor"
                  stroke-width="2"
                />
                <path
                  d="M12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
              <svg
                v-else
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"
                  stroke="currentColor"
                  stroke-width="2"
                  fill="none"
                />
              </svg>
            </button>

            <span
              v-if="isBooleanHealth"
              class="status-pill"
              :class="statusClass"
            >
              <span class="dot"></span>{{ statusText }}
            </span>
            <span class="badge beta">Beta</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- SAYFA -->
    <main class="app-main">
      <div class="container py-3">
        <router-view v-if="!bootLoading" />
        <LoadingScreen v-else />
      </div>
    </main>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="container foot-inner">
        <span
          >© {{ year }} HawAI • Bilgi amaçlıdır; acil durumda
          <strong>112</strong>'yi arayın.</span
        >
      </div>
    </footer>

    <!-- TOAST -->
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1080">
      <div
        ref="toastEl"
        class="toast align-items-center text-white bg-danger border-0"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
      >
        <div class="d-flex">
          <div class="toast-body">
            Çok fazla istek gönderdiniz. Lütfen kısa bir süre sonra tekrar
            deneyin.
          </div>
          <button
            type="button"
            class="btn-close btn-close-white me-2 m-auto"
            data-bs-dismiss="toast"
            aria-label="Close"
          ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui;
  background: var(--bg);
  color: var(--text-900);
}
a {
  color: #22c55e;
}
input,
button,
textarea {
  font: inherit;
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
}
</style>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from "vue";
import store from "./store";
import { useRoute, useRouter } from "vue-router";
import axios from "./utils/axios";
import LoadingScreen from "./components/LoadingScreen.vue";

const route = useRoute();
const router = useRouter();

/* ---- Vuex ---- */
const health = computed(() => store.state.health.reachable);
const rateLimited = computed(() => store.state.rateLimited);

/* ---- Health UI türevleri ---- */
const isBooleanHealth = computed(() => typeof health.value === "boolean");
const statusClass = computed(() => (health.value ? "ok" : "bad"));
const statusText = computed(() => (health.value ? "Online" : "Offline"));

/* ---- Bootstrap Collapse ---- */
const collapseEl = ref<HTMLDivElement | null>(null);
const togglerEl = ref<HTMLButtonElement | null>(null);
let collapseInstance: any = null;
const isNavOpen = ref(false);

/* ---- Toast ---- */
const toastEl = ref<HTMLDivElement | null>(null);
let toastInstance: any = null;

/* ---- Tema ---- */
const theme = ref<"light" | "dark">("light");
/* ---- Auth durumu ---- */
const isAuthed = ref(false);
const bootLoading = ref(true);
const userId = ref<string | null>(null);
const shortUserId = computed(() =>
  userId.value ? userId.value.slice(-6) : ""
);

async function refreshAuth() {
  try {
    const r = await axios.get("/auth/me");
    userId.value = r.data?.id || null;
    isAuthed.value = !!userId.value;
  } catch {
    userId.value = null;
    isAuthed.value = false;
  }
  bootLoading.value = false;
}
function applyTheme(t: "light" | "dark") {
  document.documentElement.setAttribute("data-theme", t);
  localStorage.setItem("theme", t);
}
function toggleTheme() {
  theme.value = theme.value === "dark" ? "light" : "dark";
  applyTheme(theme.value);
}

async function logout() {
  try {
    await axios.post("/auth/logout");
  } catch {}
  try {
    router.push("/login");
  } catch {}
  await refreshAuth();
}

/* ---- NAV: toggle (Bootstrap varsa onunla, yoksa fallback) ---- */
function toggleNav() {
  if (collapseInstance) {
    collapseInstance.toggle();
  } else if (collapseEl.value) {
    // Fallback: .show sınıfını kendimiz yönetelim
    isNavOpen.value = !collapseEl.value.classList.contains("show");
    collapseEl.value.classList.toggle("show", isNavOpen.value);
  }
}

/* Dışarı tıklayınca kapat (iki modda da çalışsın) */
function hideNav() {
  if (collapseInstance) {
    collapseInstance.hide();
  } else if (collapseEl.value) {
    collapseEl.value.classList.remove("show");
    isNavOpen.value = false;
  }
}

let onDocClick: ((e: MouseEvent) => void) | null = null;

onMounted(() => {
  // @ts-ignore
  const bootstrap = (window as any).bootstrap;

  // Toast
  if (toastEl.value && bootstrap?.Toast) {
    toastInstance = new bootstrap.Toast(toastEl.value, {
      autohide: true,
      delay: 3000,
    });
  }

  // Collapse (varsa)
  if (collapseEl.value && bootstrap?.Collapse) {
    collapseInstance = new bootstrap.Collapse(collapseEl.value, {
      toggle: false,
    });
    collapseEl.value.addEventListener("shown.bs.collapse", () => {
      isNavOpen.value = true;
    });
    collapseEl.value.addEventListener("hidden.bs.collapse", () => {
      isNavOpen.value = false;
    });
  }

  // Dışarı tıklama
  onDocClick = (e: MouseEvent) => {
    const target = e.target as Node;
    const openNow =
      isNavOpen.value || collapseEl.value?.classList.contains("show");
    if (!openNow) return;
    const insideMenu = collapseEl.value?.contains(target);
    const onToggler = togglerEl.value?.contains(target);
    if (!insideMenu && !onToggler) hideNav();
  };
  document.addEventListener("click", onDocClick, { passive: true });

  // Tema başlangıcı
  const saved = localStorage.getItem("theme") as "light" | "dark" | null;
  if (saved) {
    theme.value = saved;
  } else {
    const prefersDark = window.matchMedia?.(
      "(prefers-color-scheme: dark)"
    )?.matches;
    theme.value = prefersDark ? "dark" : "light";
  }
  applyTheme(theme.value);
  // İlk yüklemede auth durumunu kontrol et
  refreshAuth();
});

onUnmounted(() => {
  if (onDocClick) document.removeEventListener("click", onDocClick);
});

/* ---- Reaksiyonlar ---- */
watch(rateLimited, (val) => {
  if (val && toastInstance) toastInstance.show();
});
watch(
  () => route.fullPath,
  () => {
    hideNav();
    // Rota değişiminde auth durumunu yinele (özellikle login/register sonrası)
    refreshAuth();
  }
);

/* ---- Statik ---- */
const year = new Date().getFullYear();
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-main {
  flex: 1;
}

/* NAVBAR (glass) */
.nav-glass {
  position: sticky;
  top: 0;
  z-index: 1030;
  background: var(--navbar-bg);
  backdrop-filter: saturate(140%) blur(8px);
  -webkit-backdrop-filter: saturate(140%) blur(8px);
  border-bottom: 1px solid var(--border);
}
.nav-inner {
  height: 64px;
  gap: 16px;
}

/* Logo */
.brand {
  text-decoration: none;
}
.logo {
  font-weight: 800;
  font-size: 20px;
  letter-spacing: 0.2px;
  color: var(--text-900);
}
.accent {
  color: var(--brand-600);
  position: relative;
}
.accent::after {
  content: "";
  position: absolute;
  right: -8px;
  top: -6px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--brand-500);
  box-shadow: 0 0 0 6px var(--brand-100);
  animation: pulse 2.2s infinite ease-in-out;
}
@keyframes pulse {
  0% {
    transform: scale(0.9);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(0.9);
    opacity: 0.8;
  }
}

/* Links */
.links .nav-link {
  font-weight: 600;
  color: var(--text-900);
  border-radius: 10px;
  padding: 8px 10px;
  transition: background 0.2s, color 0.2s;
}
.links .nav-link:hover {
  background: var(--brand-50);
}
.links .nav-link.active {
  color: var(--brand-700) !important;
  background: var(--brand-100);
}
.links .router-link-exact-active {
  color: var(--brand-700) !important;
  background: var(--brand-100);
}

/* Mobile navigation */
@media (max-width: 768px) {
  .nav-inner {
    height: 56px;
    padding: 0 16px;
  }

  .links {
    flex-direction: column;
    gap: 8px;
    margin-top: 16px;
  }

  .links .nav-link {
    padding: 12px 16px;
    text-align: center;
  }

  .right {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .nav-auth-btn {
    justify-content: center;
    padding: 12px 16px;
  }

  .theme-toggle {
    width: 100%;
    height: 44px;
  }

  .status-pill {
    justify-content: center;
  }
}

/* Toggler */
.nav-glass .navbar-toggler {
  border-color: rgba(22, 163, 74, 0.35);
}
.nav-glass .navbar-toggler:focus {
  box-shadow: 0 0 0 0.2rem rgba(34, 197, 94, 0.25);
}
.nav-glass .navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(22,163,74,1)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

/* Theme toggle */
.theme-toggle {
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-900);
  transition: background 0.2s ease, transform 0.12s ease;
}
.theme-toggle:hover {
  background: var(--brand-50);
}
.theme-toggle:active {
  transform: translateY(1px);
}

/* Status pill */
.right .beta {
  background: var(--brand-200);
  border: 1px solid var(--brand-300);
  color: #065f46;
}
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 999px;
  font-weight: 600;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-900);
}
.status-pill .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  box-shadow: 0 0 0 4px var(--brand-100);
}
.status-pill.ok {
  border-color: rgba(16, 185, 129, 0.25);
  background: var(--brand-50);
  color: #065f46;
}
.status-pill.ok .dot {
  background: var(--brand-600);
}
.status-pill.bad {
  border-color: rgba(239, 68, 68, 0.25);
  background: #fef2f2;
  color: #7f1d1d;
}
.status-pill.bad .dot {
  background: #ef4444;
  box-shadow: 0 0 0 4px #fee2e2;
}

/* Footer */
.footer {
  border-top: 1px solid var(--border);
  background: var(--surface);
}
.foot-inner {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-600);
}

/* Navigation auth buttons */
.nav-auth-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.nav-auth-btn--secondary {
  color: var(--text-900);
  background: var(--surface);
  border-color: var(--border);
}

.nav-auth-btn--secondary:hover {
  background: var(--brand-50);
  transform: translateY(-1px);
}

.nav-auth-btn--primary {
  color: white;
  background: var(--brand-600);
  border-color: var(--brand-600);
}

.nav-auth-btn--primary:hover {
  background: var(--brand-700);
  border-color: var(--brand-700);
  transform: translateY(-1px);
}

/* Font smoothing */
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-900);
}
</style>

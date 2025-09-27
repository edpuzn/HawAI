<template>
  <div class="chat-container">
    <!-- Warning Popup -->
    <div v-if="showWarning" class="warning-popup" @click="closeWarning">
      <div class="warning-content" @click.stop>
        <div class="warning-header">
          <h3>⚠️ Önemli Uyarı</h3>
          <button class="warning-close" @click="closeWarning">×</button>
        </div>
        <div class="warning-body">
          <p><strong>Bu sistem doktor değildir!</strong></p>
          <p>
            Sadece bilgilendirme amaçlıdır ve tıbbi tavsiye niteliği taşımaz.
          </p>
          <p><strong>Özel bilgilerinizi paylaşmayınız.</strong></p>
          <p>Acil durumlarda 112'yi arayın.</p>
        </div>
        <div class="warning-footer">
          <button class="warning-ok" @click="closeWarning">Anladım</button>
        </div>
      </div>
    </div>

    <!-- Mobile sidebar toggle -->
    <button
      v-if="isMobile"
      class="sidebar-toggle"
      @click="toggleSidebar"
      :aria-label="sidebarOpen ? 'Sidebarı kapat' : 'Sidebarı aç'"
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>

    <!-- Mobile sidebar overlay -->
    <div
      v-if="isMobile && sidebarOpen"
      class="sidebar-overlay"
      @click="closeSidebar"
    ></div>

    <!-- Sidebar -->
    <aside
      class="sidebar"
      :class="{ 'sidebar-open': sidebarOpen, 'sidebar-mobile': isMobile }"
    >
      <!-- New Chat Button -->
      <div class="new-chat-section">
        <button class="new-chat-btn" @click="createThread">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
            ></path>
          </svg>
          Yeni sohbet
        </button>
        <button v-if="isMobile" class="close-sidebar" @click="closeSidebar">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Search Section -->
      <div class="search-section">
        <div class="search-container">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
          <input
            type="text"
            placeholder="Sohbetleri ara..."
            class="search-input"
          />
        </div>
      </div>

      <!-- Chats Section -->
      <div class="chats-section">
        <div class="section-header">
          <span class="section-title">Sohbetler</span>
          <span class="thread-count">{{ threads.length }}</span>
        </div>

        <div class="threads-container">
          <div v-if="threads.length === 0" class="empty-threads">
            <div class="empty-icon">
              <svg
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
              >
                <path
                  d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                ></path>
              </svg>
            </div>
            <p>Henüz sohbet yok</p>
            <span>Yeni bir sohbet başlatın</span>
          </div>
          <ul v-else class="threads">
            <li
              v-for="t in threads"
              :key="t.id"
              :class="['thread-item', t.id === threadId ? 'active' : '']"
            >
              <button
                class="thread-content"
                type="button"
                @click="openThread(t.id)"
              >
                <div class="thread-icon">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                    ></path>
                  </svg>
                </div>
                <div class="thread-info">
                  <span class="thread-title">{{ t.title }}</span>
                  <span class="thread-time">{{ formatTime(t.createdAt) }}</span>
                </div>
              </button>
              <button
                class="thread-delete"
                type="button"
                title="Sil"
                aria-label="Sil"
                @click="removeThread(t.id)"
              >
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <polyline points="3,6 5,6 21,6"></polyline>
                  <path
                    d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"
                  ></path>
                </svg>
              </button>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Actions -->
      <div class="bottom-actions">
        <button
          class="action-btn"
          @click="clearAllThreads"
          title="Tüm sohbetleri sil"
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="3,6 5,6 21,6"></polyline>
            <path
              d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"
            ></path>
          </svg>
          Tümünü Sil
        </button>
      </div>

      <!-- User Profile -->
      <div class="user-profile">
        <div class="user-avatar">
          <span>{{ userInitials }}</span>
        </div>
        <div class="user-info">
          <span class="user-name">{{ username }}</span>
          <span class="user-status">Çevrimiçi</span>
        </div>
      </div>
    </aside>

    <!-- Main chat area -->
    <main class="main">
      <!-- Messages area -->
      <div ref="messagesEl" class="messages">
        <!-- Empty state with centered input -->
        <div v-if="messages.length === 0" class="empty-state">
          <div class="empty-content">
            <h1 class="empty-title">HawAI</h1>
            <p class="empty-subtitle">Sana nasıl yardımcı olabilirim?</p>
            <div class="centered-composer">
              <ChatBox
                :thinking="isThinking"
                :placeholder="'Herhangi bir şey sorun...'"
                @send="handleSendWithImage"
              />
            </div>
          </div>
        </div>

        <!-- Messages when there are conversations -->
        <div v-else class="messages-container">
          <div
            v-for="m in messages"
            :key="m.id"
            class="msg-row"
            :class="m.role === 'user' ? 'to-right' : 'to-left'"
          >
            <div v-if="editId === m.id && m.role === 'user'" class="edit-wrap">
              <textarea
                v-model="editText"
                class="edit-textarea"
                rows="3"
                placeholder="Mesajınızı düzenleyin..."
              />
              <div class="edit-actions">
                <button class="btn-save" @click="saveEdit">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <polyline points="20,6 9,17 4,12"></polyline>
                  </svg>
                  Kaydet
                </button>
                <button class="btn-cancel" @click="cancelEdit">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                  Vazgeç
                </button>
              </div>
            </div>
            <template v-else>
              <MessageBubble
                :text="m.content"
                :from="m.role"
                :image_preview_src="firstImage(m)"
              />
              <div v-if="m.images?.length > 1" class="img-grid">
                <img
                  v-for="(im, i) in m.images.slice(1)"
                  :key="i"
                  :src="previewSrc(im)"
                  class="thumb"
                />
              </div>
              <div v-if="m.role === 'user'" class="meta">
                <button class="edit-btn" @click="startEdit(m)">
                  <svg
                    width="12"
                    height="12"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                    ></path>
                    <path
                      d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                    ></path>
                  </svg>
                  Düzenle
                </button>
              </div>
            </template>
          </div>

          <div v-if="isThinking" class="thinking">
            <div class="thinking-avatar">
              <div class="ai-avatar">AI</div>
            </div>
            <div class="thinking-content">
              <div class="dots"><span></span><span></span><span></span></div>
              <div class="thinking-text">HawAI düşünüyor…</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom composer (only when there are messages) -->
      <div v-if="messages.length > 0" class="composer">
        <ChatBox
          :thinking="isThinking"
          :placeholder="'Mesajınızı yazın…'"
          @send="handleSendWithImage"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "../utils/axios";
import MessageBubble from "@/components/MessageBubble.vue";
import ChatBox from "@/components/ChatBox.vue";

const router = useRouter();
const threads = ref<any[]>([]);
const messages = ref<any[]>([]);
const threadId = ref<string>("");
const isThinking = ref(false);
const messagesEl = ref<HTMLDivElement | null>(null);

const editId = ref<string>("");
const editText = ref("");

// Mobile responsiveness
const isMobile = ref(false);
const sidebarOpen = ref(false);

// Warning popup
const showWarning = ref(true);

// User info
const username = ref<string>("");

const userInitials = computed(() => {
  if (!username.value) return "U";
  return username.value
    .split(" ")
    .map((name) => name.charAt(0))
    .join("")
    .toUpperCase()
    .slice(0, 2);
});

function checkMobile() {
  isMobile.value = window.innerWidth < 768;
  if (!isMobile.value) {
    sidebarOpen.value = false;
  }
}

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value;
}

function closeSidebar() {
  sidebarOpen.value = false;
}

function closeWarning() {
  showWarning.value = false;
}

function previewSrc(im: string) {
  if (im?.startsWith("data:image")) return im;
  return im;
}

function firstImage(m: any) {
  const im = (m?.images || [])[0];
  return im ? previewSrc(im) : undefined;
}

async function ensureAuth() {
  try {
    const response = await axios.get("/auth/me");
    username.value =
      response.data?.username || response.data?.email || "Kullanıcı";
  } catch {
    // Otomatik yönlendirme kaldırıldı
    username.value = "Misafir Kullanıcı";
  }
}

async function loadThreads() {
  threads.value = (await axios.get("/chat/threads")).data;
  if (!threads.value.length) await createThread();
}

async function createThread() {
  const res = await axios.post("/chat/threads", { title: "Yeni Sohbet" });
  threadId.value = res.data.id;
  await openThread(threadId.value);
}

async function openThread(id: string) {
  threadId.value = id;
  if (isMobile.value) {
    closeSidebar();
  }
  messages.value = (await axios.get(`/chat/messages/${id}`)).data;
  await nextTick();
  scrollToBottom(false);
}

async function removeThread(id: string) {
  try {
    await axios.delete(`/chat/threads/${id}`);
    // listeden çıkar
    threads.value = threads.value.filter((t) => t.id !== id);
    if (threadId.value === id) {
      // mevcut silindiyse: varsa ilkine geç, yoksa sıfırla
      if (threads.value.length) {
        await openThread(threads.value[0].id);
      } else {
        threadId.value = "";
        messages.value = [];
      }
    }
  } catch (e) {
    /* sessizce geç */
  }
}

function scrollToBottom(smooth = true) {
  const el = messagesEl.value;
  if (!el) return;
  el.scrollTo({ top: el.scrollHeight, behavior: smooth ? "smooth" : "auto" });
}

async function handleSendWithImage(
  text: string,
  image_base64?: string,
  image_preview_src?: string
) {
  if (!text && !image_preview_src) return;
  if (!threadId.value) {
    await createThread();
  }
  isThinking.value = true;
  try {
    const images = image_preview_src ? [image_preview_src] : [];
    await axios.post("/chat/send", {
      thread_id: threadId.value,
      content: text,
      images,
    });
    await openThread(threadId.value);
  } finally {
    isThinking.value = false;
    await nextTick();
    scrollToBottom(true);
  }
}

function startEdit(m: any) {
  editId.value = m.id;
  editText.value = m.content;
}

async function saveEdit() {
  await axios.post(`/chat/edit/${editId.value}`, { content: editText.value });
  editId.value = "";
  await openThread(threadId.value);
}

function cancelEdit() {
  editId.value = "";
}

// New functions for enhanced UI
function getCurrentThreadTitle() {
  const currentThread = threads.value.find((t) => t.id === threadId.value);
  return currentThread ? currentThread.title : "Yeni Sohbet";
}

function formatTime(timestamp: string | number) {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  const now = new Date();
  const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

  if (diffInHours < 1) return "Az önce";
  if (diffInHours < 24) return `${Math.floor(diffInHours)} saat önce`;
  if (diffInHours < 168) return `${Math.floor(diffInHours / 24)} gün önce`;
  return date.toLocaleDateString("tr-TR");
}

async function clearAllThreads() {
  if (threads.value.length === 0) return;

  if (
    confirm(
      "Tüm sohbetleri silmek istediğinizden emin misiniz? Bu işlem geri alınamaz."
    )
  ) {
    try {
      // Tüm thread'leri sil
      for (const thread of threads.value) {
        await axios.delete(`/chat/threads/${thread.id}`);
      }

      // Local state'i temizle
      threads.value = [];
      messages.value = [];
      threadId.value = "";
    } catch (e) {
      console.error("Sohbetler silinirken hata oluştu:", e);
    }
  }
}

onMounted(async () => {
  checkMobile();
  window.addEventListener("resize", checkMobile);
  await ensureAuth();
  await loadThreads();
  await nextTick();
  scrollToBottom(false);
});

onUnmounted(() => {
  window.removeEventListener("resize", checkMobile);
});
</script>

<style scoped>
/* ===== CONTAINER ===== */
.chat-container {
  display: flex;
  height: calc(100vh - 64px);
  position: relative;
  background: var(--page-bg);
  overflow: hidden;
}

/* ===== WARNING POPUP ===== */
.warning-popup {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.warning-content {
  background: var(--surface);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  border: 1px solid var(--border);
}

.warning-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid var(--border);
}

.warning-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-900);
}

.warning-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--text-100);
  color: var(--text-600);
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.warning-close:hover {
  background: var(--text-200);
  color: var(--text-900);
}

.warning-body {
  padding: 20px 24px;
}

.warning-body p {
  margin: 0 0 12px;
  font-size: 15px;
  line-height: 1.5;
  color: var(--text-700);
}

.warning-body p:last-child {
  margin-bottom: 0;
}

.warning-body strong {
  color: var(--text-900);
  font-weight: 600;
}

.warning-footer {
  padding: 16px 24px 20px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
}

.warning-ok {
  background: var(--brand-600);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.warning-ok:hover {
  background: var(--brand-700);
  transform: translateY(-1px);
}

/* ===== MOBILE SIDEBAR TOGGLE ===== */
.sidebar-toggle {
  position: fixed;
  top: 80px;
  left: 16px;
  z-index: 1001;
  width: 44px;
  height: 44px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-900);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  cursor: pointer;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

.sidebar-toggle:hover {
  background: var(--brand-50);
  border-color: var(--brand-300);
}

.sidebar-toggle:active {
  transform: scale(0.95);
  background: var(--brand-100);
}

/* ===== SIDEBAR OVERLAY ===== */
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  backdrop-filter: blur(4px);
}

/* ===== SIDEBAR ===== */
.sidebar {
  width: 240px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
  z-index: 1000;
  position: fixed;
  left: 0;
  top: 64px;
  height: calc(100vh - 64px);
  flex-shrink: 0;
}

.sidebar-mobile {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  transform: translateX(-100%);
}

.sidebar-mobile.sidebar-open {
  transform: translateX(0);
}

/* ===== NEW CHAT SECTION ===== */
.new-chat-section {
  padding: 12px;
  border-bottom: 1px solid var(--border);
  text-align: left;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.close-sidebar {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--brand-50);
  color: var(--text-900);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.close-sidebar:hover {
  background: var(--brand-100);
  border-color: var(--brand-300);
}

.new-chat-btn {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid var(--brand-300);
  background: var(--brand-100);
  color: var(--brand-800);
  font-weight: 600;
  font-size: 13px;
  transition: all 0.2s ease;
  cursor: pointer;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  min-height: 44px;
}

.new-chat-btn:hover {
  background: var(--brand-200);
  border-color: var(--brand-400);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
}

.new-chat-btn:active {
  transform: scale(0.98);
  background: var(--brand-300);
}

/* ===== SEARCH SECTION ===== */
.search-section {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--brand-50);
  border: 1px solid var(--border);
}

.search-input {
  flex: 1;
  background: none;
  border: none;
  color: var(--text-900);
  font-size: 13px;
  outline: none;
}

.search-input::placeholder {
  color: var(--text-600);
}

/* ===== CHATS SECTION ===== */
.chats-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  text-align: left;
}

.section-header {
  padding: 10px 12px 6px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-600);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.thread-count {
  font-size: 10px;
  color: var(--text-600);
  background: var(--brand-100);
  padding: 2px 5px;
  border-radius: 8px;
}

.threads-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 6px 6px;
}

.threads-container::-webkit-scrollbar {
  width: 4px;
}

.threads-container::-webkit-scrollbar-track {
  background: transparent;
}

.threads-container::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 2px;
}

/* ===== EMPTY THREADS ===== */
.empty-threads {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 40px 20px;
  text-align: left;
  color: var(--text-600);
}

.empty-icon {
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-threads p {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-900);
}

.empty-threads span {
  font-size: 12px;
  opacity: 0.8;
}

/* ===== THREADS LIST ===== */
.threads {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.thread-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
}

.thread-item:hover {
  background: var(--brand-50);
}

.thread-item.active {
  background: var(--brand-100);
  border: 1px solid var(--brand-300);
}

.thread-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: inherit;
  padding: 0;
  cursor: pointer;
  text-align: left;
}

.thread-icon {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: var(--brand-100);
  color: var(--brand-600);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.thread-info {
  flex: 1;
  min-width: 0;
}

.thread-title {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}

.thread-time {
  font-size: 12px;
  color: var(--text-600);
}

.thread-delete {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: none;
  background: transparent;
  color: var(--text-600);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
  opacity: 0;
}

.thread-item:hover .thread-delete {
  opacity: 1;
}

.thread-delete:hover {
  background: var(--brand-100);
  color: var(--brand-700);
}

/* ===== BOTTOM ACTIONS ===== */
.bottom-actions {
  padding: 10px 12px;
  border-top: 1px solid var(--border);
  text-align: left;
}

.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--brand-50);
  color: var(--brand-700);
  font-weight: 500;
  font-size: 13px;
  transition: all 0.2s ease;
  cursor: pointer;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  min-height: 44px;
}

.action-btn:hover {
  background: var(--brand-100);
  border-color: var(--brand-300);
}

.action-btn:active {
  transform: scale(0.98);
  background: var(--brand-200);
}

/* ===== USER PROFILE ===== */
.user-profile {
  padding: 10px 12px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
  text-align: left;
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: var(--brand-600);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 11px;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}

.user-status {
  font-size: 11px;
  color: var(--brand-600);
}

/* ===== MAIN CHAT AREA ===== */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: var(--page-bg);
  margin-left: 240px;
}

/* ===== MESSAGES AREA ===== */
.messages {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.messages::-webkit-scrollbar {
  width: 6px;
}

.messages::-webkit-scrollbar-track {
  background: transparent;
}

.messages::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 3px;
}

/* ===== EMPTY STATE ===== */
.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.empty-content {
  text-align: center;
  max-width: 600px;
  width: 100%;
}

.empty-title {
  font-size: 48px;
  font-weight: 700;
  margin: 0 0 16px 0;
  background: linear-gradient(135deg, var(--brand-600), var(--brand-500));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.empty-subtitle {
  font-size: 20px;
  color: var(--text-600);
  margin: 0 0 40px 0;
  font-weight: 400;
}

.centered-composer {
  max-width: 600px;
  margin: 0 auto;
}

/* ===== MESSAGES CONTAINER ===== */
.messages-container {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ===== MESSAGE ROWS ===== */
.msg-row {
  display: flex;
  margin-bottom: 8px;
}

.msg-row.to-right {
  justify-content: flex-end;
}

.msg-row.to-left {
  justify-content: flex-start;
}

/* ===== EDIT WRAPPER ===== */
.edit-wrap {
  max-width: min(600px, 90vw);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.edit-textarea {
  width: 100%;
  min-height: 100px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--input-bg);
  color: var(--text-900);
  font-family: inherit;
  resize: vertical;
  font-size: 14px;
  line-height: 1.5;
}

.edit-textarea:focus {
  outline: none;
  border-color: var(--brand-500);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.edit-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-save {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  border: 1px solid var(--brand-300);
  background: var(--brand-600);
  color: white;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
}

.btn-save:hover {
  background: var(--brand-700);
  transform: translateY(-1px);
}

.btn-cancel {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-900);
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: var(--brand-50);
  border-color: var(--brand-300);
}

/* ===== IMAGE GRID ===== */
.img-grid {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.thumb {
  max-width: 180px;
  border-radius: 12px;
  border: 1px solid var(--border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* ===== META ACTIONS ===== */
.meta {
  margin-top: 8px;
  text-align: right;
}

.edit-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: var(--text-600);
  font-size: 12px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.edit-btn:hover {
  background: var(--brand-50);
  color: var(--brand-700);
}

/* ===== COMPOSER ===== */
.composer {
  padding: 20px 24px;
  border-top: 1px solid var(--border);
  background: var(--surface);
}

/* ===== THINKING INDICATOR ===== */
.thinking {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 0;
}

.thinking-avatar {
  flex-shrink: 0;
}

.ai-avatar {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--brand-200), var(--brand-300));
  color: var(--brand-800);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.thinking-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.thinking-text {
  color: var(--text-600);
  font-size: 14px;
  font-weight: 500;
}

.dots {
  display: flex;
  gap: 6px;
}

.dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand-600);
  animation: bounce 1.2s infinite ease-in-out;
}

.dots span:nth-child(2) {
  animation-delay: 0.15s;
}

.dots span:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  40% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

/* ===== RESPONSIVE DESIGN ===== */

/* Large tablets and small desktops */
@media (max-width: 992px) {
  .chat-container {
    height: calc(100vh - 64px);
  }

  .sidebar {
    width: 240px;
  }

  .main {
    margin-left: 240px;
  }

  .messages-container {
    padding: clamp(16px, 3vw, 24px);
  }

  .composer {
    padding: clamp(16px, 3vw, 24px);
  }

  .empty-state {
    padding: clamp(20px, 4vw, 32px);
  }

  .empty-title {
    font-size: clamp(32px, 6vw, 48px);
  }

  .empty-subtitle {
    font-size: clamp(16px, 3vw, 20px);
  }
}

/* Tablets */
@media (max-width: 768px) {
  .chat-container {
    height: calc(100vh - 64px);
    flex-direction: column;
  }

  .sidebar {
    width: 280px;
    position: fixed;
    top: 64px;
    left: 0;
    height: calc(100vh - 64px);
    transform: translateX(-100%);
    z-index: 1000;
    transition: transform 0.3s ease;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }

  .sidebar.sidebar-open {
    transform: translateX(0);
  }

  .main {
    width: 100%;
    height: 100%;
    margin-left: 0;
  }

  .messages-container {
    padding: clamp(12px, 2.5vw, 20px);
  }

  .composer {
    padding: clamp(12px, 2.5vw, 20px);
  }

  .empty-state {
    padding: clamp(16px, 3vw, 24px);
  }

  .empty-title {
    font-size: clamp(28px, 8vw, 40px);
  }

  .empty-subtitle {
    font-size: clamp(14px, 4vw, 18px);
  }

  .edit-wrap {
    max-width: calc(100vw - 32px);
  }

  .warning-content {
    margin: 16px;
    max-width: calc(100vw - 32px);
  }

  .warning-header {
    padding: 16px 20px 12px;
  }

  .warning-header h3 {
    font-size: 16px;
  }

  .warning-body {
    padding: 16px 20px;
  }

  .warning-body p {
    font-size: 14px;
  }

  .warning-footer {
    padding: 12px 20px 16px;
  }

  .warning-ok {
    padding: 8px 20px;
    font-size: 13px;
  }

  /* Sidebar içeriği mobile optimizasyonu */
  .new-chat-section {
    padding: 12px;
  }

  .new-chat-btn {
    padding: 12px 16px;
    font-size: 14px;
  }

  .search-section {
    padding: 12px;
  }

  .search-input {
    font-size: 14px;
  }

  .section-header {
    padding: 12px;
  }

  .section-title {
    font-size: 13px;
  }

  .threads-container {
    padding: 0 8px 8px;
  }

  .bottom-actions {
    padding: 12px;
  }

  .action-btn {
    padding: 10px 12px;
    font-size: 14px;
  }

  .user-profile {
    padding: 12px;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
  }

  .user-name {
    font-size: 14px;
  }

  .user-status {
    font-size: 12px;
  }
}

/* Mobile phones */
@media (max-width: 640px) {
  .sidebar {
    width: 260px;
    top: 64px;
    height: calc(100vh - 64px);
    box-shadow: 2px 0 15px rgba(0, 0, 0, 0.15);
  }

  .messages-container {
    padding: clamp(8px, 2vw, 12px);
  }

  .composer {
    padding: clamp(8px, 2vw, 12px);
  }

  .sidebar-toggle {
    left: 12px;
    top: 76px;
    width: 38px;
    height: 38px;
    font-size: 12px;
  }

  .empty-state {
    padding: clamp(12px, 3vw, 16px);
  }

  .empty-title {
    font-size: clamp(24px, 9vw, 32px);
  }

  .empty-subtitle {
    font-size: clamp(13px, 4vw, 16px);
  }

  .edit-wrap {
    max-width: calc(100vw - 24px);
  }

  /* Sidebar mobile optimizasyonu */
  .new-chat-section {
    padding: 10px;
  }

  .new-chat-btn {
    padding: 10px 12px;
    font-size: 13px;
  }

  .search-section {
    padding: 10px;
  }

  .search-input {
    font-size: 13px;
  }

  .section-header {
    padding: 10px;
  }

  .section-title {
    font-size: 12px;
  }

  .threads-container {
    padding: 0 6px 6px;
  }

  .bottom-actions {
    padding: 10px;
  }

  .action-btn {
    padding: 8px 10px;
    font-size: 13px;
  }

  .user-profile {
    padding: 10px;
  }

  .user-avatar {
    width: 28px;
    height: 28px;
  }

  .user-name {
    font-size: 13px;
  }

  .user-status {
    font-size: 11px;
  }

  /* Warning popup mobile */
  .warning-content {
    margin: 12px;
    max-width: calc(100vw - 24px);
  }

  .warning-header {
    padding: 12px 16px 8px;
  }

  .warning-header h3 {
    font-size: 15px;
  }

  .warning-body {
    padding: 12px 16px;
  }

  .warning-body p {
    font-size: 13px;
  }

  .warning-footer {
    padding: 8px 16px 12px;
  }

  .warning-ok {
    padding: 6px 16px;
    font-size: 12px;
  }
}

/* Small mobile phones */
@media (max-width: 480px) {
  .sidebar {
    width: 240px;
    top: 64px;
    height: calc(100vh - 64px);
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.2);
  }

  .messages-container {
    padding: 8px;
  }

  .composer {
    padding: 8px;
  }

  .sidebar-toggle {
    left: 8px;
    top: 72px;
    width: 36px;
    height: 36px;
    font-size: 12px;
  }

  .empty-state {
    padding: 12px;
  }

  .empty-title {
    font-size: clamp(20px, 10vw, 28px);
  }

  .empty-subtitle {
    font-size: clamp(12px, 4.5vw, 14px);
  }

  .edit-wrap {
    max-width: calc(100vw - 16px);
  }

  /* Sidebar küçük mobile optimizasyonu */
  .new-chat-section {
    padding: 8px;
  }

  .new-chat-btn {
    padding: 8px 10px;
    font-size: 12px;
  }

  .search-section {
    padding: 8px;
  }

  .search-input {
    font-size: 12px;
  }

  .section-header {
    padding: 8px;
  }

  .section-title {
    font-size: 11px;
  }

  .threads-container {
    padding: 0 4px 4px;
  }

  .bottom-actions {
    padding: 8px;
  }

  .action-btn {
    padding: 6px 8px;
    font-size: 12px;
  }

  .user-profile {
    padding: 8px;
  }

  .user-avatar {
    width: 24px;
    height: 24px;
  }

  .user-name {
    font-size: 12px;
  }

  .user-status {
    font-size: 10px;
  }

  /* Warning popup küçük mobile */
  .warning-content {
    margin: 8px;
    max-width: calc(100vw - 16px);
  }

  .warning-header {
    padding: 10px 12px 6px;
  }

  .warning-header h3 {
    font-size: 14px;
  }

  .warning-body {
    padding: 10px 12px;
  }

  .warning-body p {
    font-size: 12px;
  }

  .warning-footer {
    padding: 6px 12px 10px;
  }

  .warning-ok {
    padding: 5px 12px;
    font-size: 11px;
  }
}
</style>

<template>
  <div class="home-landing" :class="{ empty: isEmpty }">
    <div class="inner">
      <!-- ===== İlk açılış (orta prompt) ===== -->
      <div v-if="isEmpty" class="empty-hero">
        <h1 class="hero-title">Nasıl yardımcı olabilirim?</h1>
        <div class="hero-prompt">
          <!-- ÖRNEKLERİ GEÇİRDİK -->
          <ChatBox
            :thinking="isThinking"
            :examples="EXAMPLES"
            :placeholder="rotatingExample"
            @send="handleSendWithImage"
          />
        </div>
      </div>

      <!-- ===== Sohbet düzeni ===== -->
      <div v-else ref="chatCardEl" class="chat-surface">
        <div class="messages" ref="messagesEl">
          <template v-for="(it, i) in renderItems" :key="itemKey(it, i)">
            <div v-if="it.type === 'sep'" class="day-sep">
              <span class="day-chip">{{ it.label }}</span>
            </div>
            <div
              v-else
              class="msg-wrap fade-in"
              :class="it.m?.from === 'user' ? 'to-right' : 'to-left'"
              :style="{ animationDelay: it.msgIndex * 50 + 'ms' }"
            >
              <MessageBubble
                :text="it.m.text"
                :from="it.m.from"
                :tags="it.m.tags"
                :sources="it.m.sources"
                :image_preview_src="it.m.image_preview_src"
              />
            </div>
          </template>

          <div v-if="isThinking" class="thinking-overlay">
            <div class="dots"><span></span><span></span><span></span></div>
            <div class="thinking-text">Düşünüyor…</div>
          </div>
        </div>

        <button
          v-show="showJump"
          class="jump-bottom"
          type="button"
          @click="scrollToBottom(true)"
          aria-label="Sona atla"
          title="Sona atla"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path
              d="M12 4v12m0 0l-6-6m6 6l6-6M5 20h14"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              fill="none"
            />
          </svg>
        </button>
      </div>

      <!-- Composer (sohbette altta; ilk ekranda ortada zaten var) -->
      <div v-if="!isEmpty" class="composer">
        <!-- ÖRNEKLERİ GEÇİRDİK -->
        <ChatBox
          :thinking="isThinking"
          :examples="EXAMPLES"
          :placeholder="rotatingExample"
            @send="handleSendWithImage"
        />
      </div>

      <!-- Ekranı temizle FAB -->
      <button
        class="clear-fab"
        @click="clearChat"
        title="Ekranı temizle"
        aria-label="Ekranı temizle"
      >
        <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
          <path
            d="M6 7h12m-9-3h6m-7 3 1 12m6-12-1 12"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            fill="none"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  onMounted,
  onBeforeUnmount,
  computed,
  ref,
  watch,
  nextTick,
} from "vue";
import { useStore } from "vuex";
import MessageBubble from "@/components/MessageBubble.vue";
import ChatBox from "@/components/ChatBox.vue";

const store = useStore();

/* Vuex */
const messages = computed(() => store.state.messages);
const isThinking = computed<boolean>(
  () => (store.state as any).loading ?? (store.state as any).thinking ?? false
);

/* Sağlık temalı örnek sorular (placeholder rotasyonu için) */
const EXAMPLES = [
  "Günlük su hedefim kaç olmalı?",
  "Akşam baş ağrısına ne iyi gelir?",
  "Uykuya dalmakta zorlanıyorum, ne yapabilirim?",
  "Stresi azaltmak için kısa bir nefes egzersizi önerir misin?",
];

/* Placeholder rotasyonu */
const exampleIndex = ref(0);
const rotatingExample = computed(
  () => EXAMPLES[exampleIndex.value] || "Mesajınızı yazın…"
);
let rotateTimer: number | undefined;

function startPlaceholderRotation() {
  stopPlaceholderRotation();
  rotateTimer = window.setInterval(() => {
    exampleIndex.value = (exampleIndex.value + 1) % EXAMPLES.length;
  }, 2800); // ~2.8sn’de bir değiştir
}
function stopPlaceholderRotation() {
  if (rotateTimer) {
    clearInterval(rotateTimer);
    rotateTimer = undefined;
  }
}

/* Boş mu? (ilk ekran) */
const isEmpty = computed(() => (messages.value?.length ?? 0) === 0);

/* Gün ayraçları */
const stamps = ref<number[]>([]);
function ensureStamps() {
  const len = messages.value?.length ?? 0;
  while (stamps.value.length < len) {
    const idx = stamps.value.length;
    const m: any = messages.value[idx];
    const ts = m?.createdAt || m?.time || Date.now();
    stamps.value.push(typeof ts === "number" ? ts : Date.now());
  }
}
type RenderItem =
  | { type: "sep"; label: string }
  | { type: "msg"; m: any; msgIndex: number };

const renderItems = computed<RenderItem[]>(() => {
  const out: RenderItem[] = [];
  const arr: any[] = messages.value || [];
  if (!arr.length) return out;
  ensureStamps();

  let lastDayKey = "";
  arr.forEach((m, i) => {
    const d = new Date(stamps.value[i]);
    const key = d.toDateString();
    if (key !== lastDayKey) {
      out.push({ type: "sep", label: dayLabel(d) });
      lastDayKey = key;
    }
    out.push({ type: "msg", m, msgIndex: i });
  });
  return out;
});
function itemKey(it: RenderItem, i: number) {
  return it.type === "sep" ? `sep-${i}` : `msg-${i}`;
}
function dayLabel(d: Date) {
  const today = new Date();
  const yd = new Date();
  yd.setDate(today.getDate() - 1);
  const same = (a: Date, b: Date) =>
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate();
  if (same(d, today)) return "Bugün";
  if (same(d, yd)) return "Dün";
  return d.toLocaleDateString();
}

/* Gönderim */
const justSent = ref(false);
function handleSendWithImage(msg: string, image_base64?: string, image_preview_src?: string) {
  store.dispatch("sendMessage", { text: msg, image_base64, image_preview_src });
  justSent.value = true;
  setTimeout(() => (justSent.value = false), 360);
}

/* Sona atla */
const messagesEl = ref<HTMLDivElement | null>(null);
const showJump = ref(false);
function updateJump() {
  const el = messagesEl.value;
  if (!el) return;
  const atBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - 60;
  showJump.value = !atBottom;
}
async function scrollToBottom(smooth = true) {
  await nextTick();
  const el = messagesEl.value;
  if (el)
    el.scrollTo({ top: el.scrollHeight, behavior: smooth ? "smooth" : "auto" });
}
watch(
  () => messages.value?.length,
  () => {
    ensureStamps();
    scrollToBottom(true);
    showJump.value = false;
  }
);
function onScroll() {
  updateJump();
}

/* Temizle (ekranı komple boşalt) */
function clearChat() {
  try {
    store.commit("clearMessages");
  } catch {
    store.dispatch?.("clearMessages");
  }
  stamps.value = [];
}

/* Mount */
onMounted(() => {
  scrollToBottom(false);
  messagesEl.value?.addEventListener("scroll", onScroll, { passive: true });
  updateJump();
  ensureStamps();
  startPlaceholderRotation();
});
onBeforeUnmount(() => {
  messagesEl.value?.removeEventListener("scroll", onScroll as any);
  stopPlaceholderRotation();
});
</script>

<style scoped>
/* global: yatay scrollbar’ı kökten kapat */
:global(html, body, #app) {
  max-width: 100%;
  overflow-x: hidden;
}

/* ===== Kök ===== */
.home-landing {
  --nav-gap-fix: 10px;
  color: var(--text-900);
  background: var(--page-bg);
  width: 100%;
  margin: 0 auto;
  padding: clamp(12px, 3.6vw, 24px);
  margin-top: calc(-1 * var(--nav-gap-fix));
  background-image: radial-gradient(
      760px 420px at 12% 14%,
      rgba(16, 185, 129, 0.1),
      transparent 60%
    ),
    var(--page-bg);
  overflow-x: clip;
}
.inner {
  width: 100%;
  display: grid;
  gap: 12px;
}

/* ===== İlk açılış ortadaki prompt ===== */
.empty-hero {
  min-height: calc(100vh - 180px);
  display: grid;
  align-content: center;
  justify-items: center;
  gap: 18px;
  text-align: center;
}
.hero-title {
  font-weight: 900;
  font-size: clamp(28px, 5.4vw, 44px);
  color: var(--text-900);
}
.hero-prompt {
  width: min(1100px, 92vw);
}
.empty .hero-prompt :deep(textarea),
.empty .hero-prompt :deep(input[type="text"]) {
  min-height: 56px;
  font-size: clamp(16px, 1.4vw, 18px);
}

/* ===== Sohbet düzeni ===== */
.chat-surface {
  position: relative;
  border: 0;
  border-radius: 0;
  background: transparent;
  min-height: calc(100vh - 210px);
}
.messages {
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: clamp(8px, 2.2vw, 14px);
  word-break: break-word;
  overflow-wrap: anywhere;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge legacy */
}
.messages::-webkit-scrollbar {
  width: 0;
  height: 0;
}

.msg-wrap {
  display: flex;
  padding: 2px 0;
}
.msg-wrap.to-left {
  justify-content: flex-start;
}
.msg-wrap.to-right {
  justify-content: flex-end;
}
.msg-wrap > * {
  max-width: min(820px, 84vw);
}

/* Gün ayırıcı */
.day-sep {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 6px 0;
}
.day-sep::before,
.day-sep::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--border);
}
.day-chip {
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid var(--brand-200);
  background: var(--brand-50);
  color: #065f46;
  font-weight: 700;
  font-size: 0.9rem;
}

/* Düşünme overlay */
.thinking-overlay {
  position: sticky;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 10px 0 2px;
  backdrop-filter: blur(2px);
}
.thinking-text {
  color: var(--text-700);
  font-size: 0.92rem;
}
.dots {
  display: inline-flex;
  gap: 6px;
}
.dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand-600);
  animation: bounce 1s infinite ease-in-out;
}
.dots span:nth-child(2) {
  animation-delay: 0.12s;
}
.dots span:nth-child(3) {
  animation-delay: 0.24s;
}
@keyframes bounce {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  40% {
    transform: translateY(-5px);
    opacity: 1;
  }
}

/* Sona atla FAB */
.jump-bottom {
  position: absolute;
  right: 12px;
  bottom: 12px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--brand-300);
  background: var(--brand-50);
  color: #065f46;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.12);
  transition: transform 0.12s ease, background 0.15s ease,
    border-color 0.15s ease;
}
.jump-bottom:hover {
  transform: translateY(-1px);
  background: var(--brand-100);
  border-color: var(--brand-400);
}

/* Composer (sohbette altta) */
.composer {
  position: sticky;
  bottom: 10px;
  z-index: 5;
  padding: 0;
}

/* Form alanları – iç scrollbar yok */
:deep(textarea),
:deep(input[type="text"]) {
  border-radius: 12px !important;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text-900);
  resize: none;
  overflow: hidden !important;
  scrollbar-width: none;
}
:deep(textarea::-webkit-scrollbar) {
  width: 0;
  height: 0;
}

/* Clear FAB (sağ altta) */
.clear-fab {
  position: fixed;
  right: 14px;
  bottom: 14px;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  border: 1px solid var(--brand-300);
  background: var(--brand-50);
  color: #065f46;
  display: grid;
  place-items: center;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.18);
}
.clear-fab:hover {
  background: var(--brand-100);
  border-color: var(--brand-400);
}

/* Mobil */
@media (max-width: 576px) {
  .messages {
    padding: 10px;
  }
}
</style>

<template>
  <div class="chatbox">
    <!-- Yazıyor göstergesi (opsiyonel) -->
    <div v-if="thinking" class="typing card border-0 shadow-sm">
      <div class="typing-inner">
        <span class="avatar">AI</span>
        <span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>
        <span class="typing-label">HawAI yazıyor…</span>
      </div>
    </div>

    <!-- Kompozitör -->
    <form class="composer" @submit.prevent="handleSend">
      <textarea
        ref="inputEl"
        v-model="message"
        class="form-control input"
        :placeholder="placeholder"
        rows="1"
        @input="autoResize"
        @keydown="onKeydown"
        :disabled="disabled || isSending"
      ></textarea>

      <!-- Görsel önizleme (varsa) -->
      <div v-if="imagePreviewSrc" class="image-preview card">
        <img :src="imagePreviewSrc" alt="seçilen görsel" />
        <button
          class="btn btn-sm btn-link remove"
          type="button"
          @click="clearImage"
          aria-label="Görseli kaldır"
        >
          ✕
        </button>
      </div>

      <input
        ref="fileEl"
        type="file"
        accept="image/*"
        class="d-none"
        @change="onPick"
      />

      <button
        type="button"
        class="btn camera-btn"
        :disabled="disabled || isSending"
        @click="pick"
        title="Görsel ekle"
        aria-label="Görsel ekle"
      >
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M5 7h2.2l1.2-2h7.2l1.2 2H19a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2Z"
            stroke="currentColor"
            stroke-width="2"
            stroke-linejoin="round"
          />
          <circle
            cx="12"
            cy="13"
            r="3.5"
            stroke="currentColor"
            stroke-width="2"
          />
        </svg>
      </button>

      <button
        type="submit"
        class="btn btn-success send-btn"
        :disabled="!canSend || disabled || isSending"
        @click="nudge"
      >
        <svg
          class="send-icon"
          :class="{ fly }"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M22 2L11 13"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
          <path
            d="M22 2L14.5 22l-3.5-8-8-3.5L22 2z"
            stroke="currentColor"
            stroke-width="2"
            stroke-linejoin="round"
            fill="none"
          />
        </svg>
        <span class="visually-hidden">Gönder</span>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from "vue";

const props = withDefaults(
  defineProps<{
    placeholder?: string;
    thinking?: boolean; // HawAI yazıyor… göstergesi
    disabled?: boolean; // Dışarıdan kilitlemek istersen
  }>(),
  {
    placeholder: "Mesajınızı yazın…",
    thinking: false,
    disabled: false,
  }
);

const emit = defineEmits<{
  (
    e: "send",
    message: string,
    image_base64?: string,
    image_preview_src?: string
  ): void;
}>();

const message = ref<string>("");
const inputEl = ref<HTMLTextAreaElement | null>(null);
const fileEl = ref<HTMLInputElement | null>(null);
const imageBase64 = ref<string | undefined>(undefined);
const imagePreviewSrc = ref<string | undefined>(undefined);
const isSending = ref(false);
const fly = ref(false);

const canSend = computed(
  () => message.value.trim().length > 0 && !isSending.value
);

function autoResize() {
  const el = inputEl.value;
  if (!el) return;
  el.style.height = "auto";
  const max = 180; // px
  el.style.height = Math.min(el.scrollHeight, max) + "px";
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
}

async function handleSend() {
  const text = message.value.trim();
  if (!text) return;
  isSending.value = true;
  emit("send", text, imageBase64.value, imagePreviewSrc.value);
  message.value = "";
  imageBase64.value = undefined;
  imagePreviewSrc.value = undefined;
  fly.value = true;
  await nextTick();
  autoResize();
  inputEl.value?.focus();
  setTimeout(() => (fly.value = false), 320);
  isSending.value = false;
}

function nudge() {
  // küçük bir mikro-animasyon tetiklemesi
  fly.value = true;
  setTimeout(() => (fly.value = false), 260);
}

function pick() {
  fileEl.value?.click();
}

function onPick(e: Event) {
  const input = e.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    const result = reader.result as string;
    // result e.g. data:image/png;base64,xxxx
    const b64 = result.split(",")[1] || result;
    imageBase64.value = b64;
    imagePreviewSrc.value = result; // tam data URL önizleme için
  };
  reader.readAsDataURL(file);
}

function clearImage() {
  imageBase64.value = undefined;
  imagePreviewSrc.value = undefined;
  if (fileEl.value) fileEl.value.value = "";
}

onMounted(() => autoResize());
</script>

<style scoped>
.chatbox {
  display: grid;
  gap: 10px;
}

/* Yazıyor… kartı */
.typing {
  background: var(--brand-50);
}
.typing-inner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid var(--brand-100);
  border-radius: 14px;
}
.typing .avatar {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--brand-200);
  color: #065f46;
  border: 1px solid var(--brand-300);
}
.typing .typing-label {
  font-weight: 600;
  color: var(--brand-700);
}

.dots {
  display: inline-flex;
  gap: 4px;
}
.dots i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--brand-600);
  opacity: 0.4;
  animation: blink 1.2s infinite ease-in-out;
}
.dots i:nth-child(2) {
  animation-delay: 0.2s;
}
.dots i:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes blink {
  0%,
  80%,
  100% {
    opacity: 0.2;
    transform: translateY(0);
  }
  40% {
    opacity: 1;
    transform: translateY(-2px);
  }
}

/* Kompozitör */
.composer {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 8px;
  align-items: end;
}

@media (max-width: 480px) {
  .composer {
    gap: 6px;
  }
}
.input {
  line-height: 1.55;
  border-radius: 14px;
  padding: 10px 12px;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.06),
    rgba(255, 255, 255, 0.02)
  );
  color: var(--text-900);
  border: 1px solid var(--input-border);
  box-shadow: 0 8px 30px rgba(2, 6, 23, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  resize: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease,
    background 0.15s ease, color 0.15s ease;
}
.input::placeholder {
  color: var(--input-placeholder);
  opacity: 1;
}
.input:focus {
  border-color: rgba(34, 197, 94, 0.6);
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.18),
    0 10px 30px rgba(34, 197, 94, 0.12);
}
.send-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 12px 28px rgba(34, 197, 94, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.12);
  background: linear-gradient(180deg, #22c55e, #16a34a);
  color: #fff;
  transition: transform 0.12s ease;
}
.send-btn:active {
  transform: translateY(1px);
}

.send-icon {
  transition: transform 0.25s ease;
}
.send-icon.fly {
  transform: translateX(2px) translateY(-2px) rotate(18deg);
}

/* Görsel önizleme */
.image-preview {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  display: inline-block;
  max-width: 160px;
  border: 1px solid var(--border);
  box-shadow: 0 10px 26px rgba(2, 6, 23, 0.22);
}
.image-preview img {
  display: block;
  width: 100%;
  height: auto;
}
.image-preview .remove {
  position: absolute;
  top: 2px;
  right: 2px;
  color: #ef4444;
}

.camera-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--text-900);
  border: 1px solid var(--border);
  background: var(--surface);
}
.camera-btn:hover {
  border-color: var(--brand-300);
}
</style>

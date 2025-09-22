<template>
  <div class="row" :class="roleClass">
    <!-- SADECE ASİSTAN İÇİN AVATAR (istersen prop ile kapatabilirsin) -->
    <div
      v-if="showAssistantAvatar && isAssistant"
      class="avatar"
      aria-hidden="true"
    >
      AI
    </div>

    <!-- Balon -->
    <div class="bubble">
      <div class="text" v-html="safeText"></div>

      <!-- Kullanıcının yüklediği görselin minisi -->
      <div v-if="image_preview_src" class="mini-image">
        <img :src="image_preview_src" alt="yüklenen görsel" />
      </div>

      <div v-if="hasTags" class="tags">
        <span v-for="(t, i) in tags" :key="i" class="tag-pill">{{
          String(t)
        }}</span>
      </div>

      <details v-if="hasSources" class="sources">
        <summary>Kaynaklar</summary>
        <ul>
          <li v-for="(s, i) in normalizedSources" :key="i">
            <a :href="s.url" target="_blank" rel="noopener">{{ s.title }}</a>
          </li>
        </ul>
      </details>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

type SourceLike = string | { title?: string; url?: string };

const props = withDefaults(
  defineProps<{
    text: string;
    from?: string;
    tags?: (string | number)[];
    sources?: SourceLike[];
    showAssistantAvatar?: boolean;
    image_preview_src?: string;
  }>(),
  {
    showAssistantAvatar: true,
  }
);

/** Sağ/sol tarafı güçlü eşleştirme ile belirle */
const rawFrom = computed(() =>
  (props.from ?? "").toString().toLowerCase().trim()
);

const userKeys = [
  "user",
  "me",
  "self",
  "sender",
  "human",
  "client",
  "you",
  "u",
  "s",
  "ben",
  "kullanıcı",
];
const aiKeys = [
  "assistant",
  "ai",
  "asistan",
  "bot",
  "system",
  "sys",
  "hawai",
  "hawai",
  "server",
];

const isAssistant = computed(() => {
  const f = rawFrom.value;
  if (aiKeys.includes(f)) return true;
  if (userKeys.includes(f)) return false;
  // eşleşmezse: girişsiz chatbot → varsayılan KULLANICI (sağ)
  return false;
});
const roleClass = computed(() => (isAssistant.value ? "assistant" : "user"));

// Basit XSS koruması + satır sonu
function escapeHtml(s: string) {
  return s.replace(
    /[&<>"']/g,
    (m) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[
        m
      ]!)
  );
}
const safeText = computed(() =>
  escapeHtml(props.text || "").replace(/\n/g, "<br>")
);

const hasTags = computed(
  () => Array.isArray(props.tags) && props.tags.length > 0
);

const normalizedSources = computed(() => {
  if (!Array.isArray(props.sources)) return [];
  return props.sources.map((s) => {
    if (typeof s === "string") return { title: s, url: s };
    return { title: s.title || s.url || "Kaynak", url: s.url || "#" };
  });
});
const hasSources = computed(() => normalizedSources.value.length > 0);
</script>

<style scoped>
.row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: flex-start;
  will-change: opacity, transform;
  animation: fadeIn 0.25s ease-out both;
}
/* Kullanıcı (sağ) */
.row.user {
  flex-direction: row-reverse;
}

/* Avatar sadece asistanda görünür */
.avatar {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  background: var(--brand-200);
  color: #065f46;
  border: 1px solid var(--brand-300);
  box-shadow: 0 4px 10px rgba(2, 6, 23, 0.06);
}

/* Balonlar (artık değişkenleri kullanıyor) */
.bubble {
  max-width: 100%;
  border-radius: 16px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  background: var(--surface);
  position: relative;
}
.row.assistant .bubble {
  background: var(--bubble-ai-bg);
  border-color: var(--bubble-ai-border);
}
.row.user .bubble {
  background: var(--bubble-user-bg);
  border-color: var(--bubble-user-border);
}

/* Kuyruklar */
.row.assistant .bubble::before,
.row.user .bubble::before {
  content: "";
  position: absolute;
  width: 10px;
  height: 10px;
  top: 12px;
  transform: rotate(45deg);
}
.row.assistant .bubble::before {
  left: -5px;
  background: var(--bubble-ai-bg);
  border-left: 1px solid var(--bubble-ai-border);
  border-top: 1px solid var(--bubble-ai-border);
}
.row.user .bubble::before {
  right: -5px;
  background: var(--bubble-user-bg);
  border-right: 1px solid var(--bubble-user-border);
  border-top: 1px solid var(--bubble-user-border);
}

/* Metin her temada okunaklı */
.text {
  white-space: pre-wrap;
  line-height: 1.5;
  color: var(--text-900);
}

/* Etiketler */
.tags {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.tag-pill {
  background: var(--brand-200);
  border: 1px solid var(--brand-300);
  color: #065f46;
  border-radius: 999px;
  padding: 4px 8px;
  font-weight: 600;
  font-size: 12px;
}

/* Kaynaklar */
.sources {
  margin-top: 8px;
}
.sources summary {
  cursor: pointer;
  user-select: none;
  font-weight: 600;
  color: var(--brand-700);
}
.sources ul {
  margin: 8px 0 0 16px;
  padding: 0;
}
.sources a {
  color: var(--brand-700);
  text-decoration: underline;
}

/* Mini görsel */
.mini-image {
  margin-top: 8px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  max-width: 220px;
  box-shadow: 0 6px 18px rgba(2,6,23,.18);
}
.mini-image img {
  display: block;
  width: 100%;
  height: auto;
}

/* Animasyon */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}
</style>

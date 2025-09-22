<!-- src/views/AboutView.vue -->
<template>
  <div class="about-landing">
    <!-- ===== HERO ===== -->
    <section
      class="hero"
      ref="heroEl"
      role="application"
      aria-label="Sohbet arayüzü"
    >
      <p class="welcome">HawAI’ye hoş geldiniz</p>
      <h1 class="question">Nasıl yardımcı olabilirim?</h1>

      <form
        class="prompt"
        :class="{ shake: justShook }"
        @submit.prevent="submit"
      >
        <input
          ref="inputRef"
          v-model="query"
          class="prompt-input"
          type="text"
          :placeholder="placeholder"
          autocomplete="off"
          spellcheck="false"
          aria-label="Soru yazın"
          @keydown.enter.exact.prevent="submit"
        />
        <button
          class="send"
          type="submit"
          :disabled="!canSend"
          :aria-disabled="!canSend"
          aria-label="Gönder"
          title="Gönder"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path fill="currentColor" d="M2 21l21-9L2 3v7l15 2-15 2z" />
          </svg>
        </button>
      </form>
    </section>

    <!-- ===== HABER DECK ===== -->
    <section class="news-deck" aria-label="Sağlık haberleri" ref="deckEl">
      <div class="news-grid">
        <div class="lead-carousel">
          <article
            class="lead-frame active"
            :style="{ '--bg': `url('${heroA}')` }"
          >
            <div class="lead-overlay"></div>
            <div class="lead-cap">
              <span class="kicker pill">GÜNCEL</span>
              <h2 class="lead-title">HawAI</h2>
              <p class="lead-desc">
                Anlık sağlık önerileri ve güvenli bilgi — tanı koymaz, acil
                durum 112.
              </p>
            </div>
          </article>
        </div>

        <div
          class="side-rail"
          aria-label="Öne çıkan kısa haberler"
          ref="railEl"
        >
          <article
            v-for="(c, k) in sideCards"
            :key="'side-' + k"
            class="side-card"
            :style="{ '--bg': `url('${c.img}')` }"
          >
            <div class="side-overlay"></div>
            <div class="side-cap">
              <span class="kicker">{{ c.tag }}</span>
              <h3 class="side-title">{{ c.title }}</h3>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ===== SDG TICKER (2 sıra, modal ile) ===== -->
    <section class="sdg-ticker" aria-label="Sağlık Hedefleri (SDG 3)">
      <div v-for="(lane, li) in lanes" :key="'lane-' + li" class="sdg-lane">
        <div class="sdg-track" :style="{ '--dur': laneDurations[li] + 's' }">
          <!-- sonsuz akış için iki kez -->
          <button
            class="sdg-chip"
            v-for="(g, i) in lane"
            :key="'a-' + li + '-' + i"
            type="button"
            @click="openModal(g)"
            :aria-label="`${g.code} ${g.title}`"
          >
            <span class="sdg-title">{{ g.code }} — {{ g.short }}</span>
          </button>
          <button
            class="sdg-chip"
            v-for="(g, i) in lane"
            :key="'b-' + li + '-' + i"
            type="button"
            @click="openModal(g)"
            :aria-label="`${g.code} ${g.title}`"
          >
            <span class="sdg-title">{{ g.code }} — {{ g.short }}</span>
          </button>
        </div>
      </div>
    </section>

    <!-- ===== MODAL (popup) ===== -->
    <teleport to="body">
      <div
        v-if="activeGoal"
        class="modal-backdrop"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="`goal-${activeGoal.code}`"
        @click.self="closeModal"
      >
        <div class="modal-card" ref="modalCardRef">
          <div class="modal-head">
            <h3 class="modal-title" :id="`goal-${activeGoal.code}`">
              {{ activeGoal.code }} — {{ activeGoal.title }}
            </h3>
            <button
              class="modal-x"
              type="button"
              aria-label="Kapat"
              title="Kapat"
              @click="closeModal"
            >
              ×
            </button>
          </div>
          <ul class="modal-list">
            <li v-for="(p, i) in activeGoal.detail" :key="i">{{ p }}</li>
          </ul>
          <div class="modal-foot">
            <button class="modal-ok" type="button" @click="closeModal">
              Tamam
            </button>
          </div>
        </div>
      </div>
    </teleport>

    <!-- ===== YOL HARİTASI ===== -->
    <section class="roadmap" ref="roadmapEl" aria-label="Yol Haritası">
      <div class="container">
        <h2 class="section-title">Yol Haritası</h2>
        <ol class="steps">
          <li>
            <h3>Güvenli Sohbet</h3>
            <p>Bilgilendirme amaçlı, acil durum yönlendirmeleriyle birlikte.</p>
          </li>
          <li>
            <h3>Kişisel Hedefler</h3>
            <p>Su, uyku ve adım hedeflerini takip et.</p>
          </li>
          <li>
            <h3>Okul Modülü</h3>
            <p>Afişler, mini içerikler ve etkinlik fikirleri.</p>
          </li>
          <li>
            <h3>Partner API</h3>
            <p>Kurumsal entegrasyonlar ve denetimli kullanım.</p>
          </li>
        </ol>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  watch,
  onMounted,
  onBeforeUnmount,
  nextTick,
} from "vue";
import { useRouter } from "vue-router";

/* Görseller */
import heroA from "@/assets/sembol.jpg";
import img1 from "@/assets/healt1.jpg";
import img2 from "@/assets/healt2.jpg";
import img3 from "@/assets/healt3.jpg";
import img4 from "@/assets/healt4.jpg";

/* --------- Chat hero state --------- */
const router = useRouter();
const query = ref("");
const canSend = computed(() => query.value.trim().length > 0);

const EXAMPLES = [
  "Günlük su hedefimi nasıl belirlerim?",
  "Baş ağrısı için evde neler yapabilirim?",
  "Uyku kalitesini artırmak için öneriler?",
];
const exIndex = ref(0);
const placeholder = computed(() => EXAMPLES[exIndex.value]);
let rotator: number | null = null;
function startRotate() {
  stopRotate();
  rotator = window.setInterval(() => {
    if (!query.value.trim())
      exIndex.value = (exIndex.value + 1) % EXAMPLES.length;
  }, 2800);
}
function stopRotate() {
  if (rotator) {
    clearInterval(rotator);
    rotator = null;
  }
}
watch(
  () => query.value,
  (v) => (v.trim() ? stopRotate() : startRotate()),
  { immediate: true }
);

const justShook = ref(false);
function shakeOnce() {
  justShook.value = false;
  requestAnimationFrame(() => (justShook.value = true));
  setTimeout(() => (justShook.value = false), 350);
}
function submit() {
  const text = query.value.trim();
  if (!text) {
    shakeOnce();
    return;
  }
  router.push({ path: "/", query: { q: text, from: "about" } });
}

/* --------- Sağ sütun: healt1–4 --------- */
const sideCards = [
  {
    img: img1,
    tag: "BİLGİLENDİRME",
    title: "Evde nabız/oksijen ölçümünde doğru teknik",
  },
  { img: img2, tag: "YAŞAM", title: "Basit esneme ile bel ağrısını azaltma" },
  { img: img3, tag: "GÜNCEL", title: "Günde kaç adım gerçekten yeterli?" },
  {
    img: img4,
    tag: "İPUCU",
    title: "3 dakikalık nefes egzersiziyle odaklanma",
  },
];

/* --------- Scroll yönlendirme + snap --------- */
const heroEl = ref<HTMLElement | null>(null);
const deckEl = ref<HTMLElement | null>(null);
const railEl = ref<HTMLElement | null>(null);
const roadmapEl = ref<HTMLElement | null>(null);

const CLAMP_MAX = 140;
const SENS = 0.85;
const DEADZONE = 1.5;
const SNAP_LOCK = 500;

let lockedToDeck = false;
let snapping = false;

function deckInView() {
  const el = deckEl.value;
  if (!el) return false;
  const r = el.getBoundingClientRect();
  return r.top < window.innerHeight * 0.9 && r.bottom > 0;
}
function scrollToEl(el: HTMLElement | null) {
  if (!el) return;
  snapping = true;
  const y = window.scrollY + el.getBoundingClientRect().top - 8;
  window.scrollTo({ top: y, behavior: "smooth" });
  setTimeout(() => (snapping = false), SNAP_LOCK);
}
function lockDeckOnTop() {
  if (lockedToDeck || snapping) return;
  const el = deckEl.value;
  if (!el) return;
  const y = window.scrollY + el.getBoundingClientRect().top - 8;
  window.scrollTo({ top: y, behavior: "smooth" });
  lockedToDeck = true;
}

function onWheel(e: WheelEvent) {
  if (snapping) {
    e.preventDefault();
    return;
  }
  const rail = railEl.value;
  if (!rail || !deckInView()) {
    lockedToDeck = false;
    return;
  }
  const canScroll = rail.scrollHeight > rail.clientHeight;
  if (!canScroll) {
    lockedToDeck = false;
    return;
  }
  const dyRaw = e.deltaY;
  if (Math.abs(dyRaw) < DEADZONE) return;

  const atTop = rail.scrollTop <= 0;
  const atBottom = rail.scrollTop + rail.clientHeight >= rail.scrollHeight - 1;

  if (dyRaw > 0) {
    if (!atBottom) {
      e.preventDefault();
      if (!lockedToDeck) lockDeckOnTop();
      rail.scrollBy({
        top: Math.min(Math.abs(dyRaw), CLAMP_MAX) * SENS,
        behavior: "auto",
      });
    } else {
      e.preventDefault();
      lockedToDeck = false;
      scrollToEl(roadmapEl.value);
    }
  } else {
    if (!atTop) {
      e.preventDefault();
      if (!lockedToDeck) lockDeckOnTop();
      rail.scrollBy({
        top: -Math.min(Math.abs(dyRaw), CLAMP_MAX) * SENS,
        behavior: "auto",
      });
    } else {
      e.preventDefault();
      lockedToDeck = false;
      scrollToEl(heroEl.value);
    }
  }
}

/* Mount / Unmount */
onMounted(() => {
  window.addEventListener("wheel", onWheel, { passive: false });
  startRotate();
  document.addEventListener("keydown", onKey);
});
onBeforeUnmount(() => {
  window.removeEventListener("wheel", onWheel as any);
  stopRotate();
  document.removeEventListener("keydown", onKey);
});

/* --------- SDG 3 içerik + 2 şerit --------- */
type Goal = { code: string; short: string; title: string; detail: string[] };

const GOALS: Goal[] = [
  {
    code: "3.1",
    short: "Anne ölümleri",
    title:
      "2030’a kadar anne ölüm oranının 100.000’de 70’in altına indirilmesi",
    detail: [
      "3.1.1 Anne ölüm oranı",
      "3.1.2 Uzman sağlık personeli ile doğum oranı",
    ],
  },
  {
    code: "3.2",
    short: "Yenidoğan/5 yaş altı",
    title:
      "Yenidoğan ve 5 yaş altı çocukların önlenebilir ölümlerinin sona erdirilmesi",
    detail: ["3.2.1 5 yaş altı ölüm hızı", "3.2.2 Neonatal ölüm hızı"],
  },
  {
    code: "3.3",
    short: "Bulaşıcı hastalıklar",
    title: "AIDS, tüberküloz, sıtma ve ihmal edilen hastalıklarla mücadele",
    detail: [
      "HIV, TB, sıtma insidansı",
      "Hepatit B",
      "İhmal edilen tropikal hastalıklar",
    ],
  },
  {
    code: "3.4",
    short: "Bulaşıcı olmayan",
    title: "Erken ölümler %33 azaltılsın; akıl/ruh sağlığı desteklensin",
    detail: ["KKH/kanser/diyabet/KOAH", "İntihar ölüm hızı"],
  },
  {
    code: "3.5",
    short: "Madde bağımlılığı",
    title: "Uyuşturucu ve alkol bağımlılığının önlenmesi/tedavisi",
    detail: ["Tedavi kapsamı", "Zararlı alkol kullanımı"],
  },
  {
    code: "3.6",
    short: "Trafik kazaları",
    title: "Karayolu ölümleri ve yaralanmaları yarıya indirilsin",
    detail: ["Trafik kazası ölüm oranı"],
  },
  {
    code: "3.7",
    short: "Üreme/cinsel sağlık",
    title: "Hizmet/eğitime evrensel erişim; ulusal stratejilere entegrasyon",
    detail: ["Aile planlaması", "Adölesan doğurganlık hızı"],
  },
  {
    code: "3.8",
    short: "Sağlık güvencesi",
    title: "Finansal koruma ve temel hizmet/ilaç/aşı erişimi",
    detail: ["Hizmet kapsam endeksi", "Kişi başı güvenceden yararlanan sayısı"],
  },
  {
    code: "3.9",
    short: "Çevresel riskler",
    title: "Hava/su/toprak kirliliğine bağlı hastalık ve ölümler azaltılsın",
    detail: [
      "Hava kirliliği",
      "Güvenilir olmayan su/sağlık/hijyen",
      "Kasıtsız zehirlenmeler",
    ],
  },
  {
    code: "3.a",
    short: "Tütün kontrolü",
    title: "TKÇS’nin uygulanması güçlendirilsin",
    detail: ["15+ tütün kullanım yaygınlığı"],
  },
  {
    code: "3.b",
    short: "Aşı/ilaç erişimi",
    title: "AR-GE ve TRIPS/Doha ile uygun fiyatlı ilaç/aşı erişimi",
    detail: ["Erişimi olan nüfus", "Resmi kalkınma yardımı"],
  },
  {
    code: "3.c",
    short: "Sağlık işgücü",
    title: "Sağlık finansmanı ve işgücü kapasitesi artırılsın",
    detail: ["Çalışan yoğunluğu ve dağılımı"],
  },
  {
    code: "3.d",
    short: "Erken uyarı",
    title: "Sağlık risklerine karşı erken uyarı ve kriz yönetimi",
    detail: ["IHR kapasitesi ve acil durum hazırlığı"],
  },
];

const lanes = computed(() => {
  // *** 2 ŞERİT ***
  const a: Goal[][] = [[], []];
  GOALS.forEach((g, i) => a[i % 2].push(g));
  return a;
});

// iki şeride hızlar
const laneDurations = [36, 42];

/* --------- Modal --------- */
const activeGoal = ref<Goal | null>(null);
const modalCardRef = ref<HTMLElement | null>(null);

function openModal(goal: Goal) {
  activeGoal.value = goal;
  // modal açıldığında OK butonuna odaklan
  nextTick(() =>
    modalCardRef.value?.querySelector<HTMLButtonElement>(".modal-ok")?.focus()
  );
}
function closeModal() {
  activeGoal.value = null;
}
function onKey(e: KeyboardEvent) {
  if (e.key === "Escape" && activeGoal.value) closeModal();
}
</script>

<style scoped>
/* ===== Genel ===== */
.about-landing {
  color: var(--text-900);
  background: var(--page-bg);
}

/* ===== HERO ===== */
.hero {
  width: 100vw;
  margin-left: 50%;
  transform: translateX(-50%);
  margin-top: -1px;
  min-height: calc(100vh - 84px);
  padding: clamp(24px, 5vw, 60px) clamp(12px, 6vw, 72px);
  display: grid;
  place-items: center;
  gap: clamp(10px, 2.4vw, 18px);
  background: radial-gradient(
      760px 420px at 12% 14%,
      rgba(16, 185, 129, 0.1),
      transparent 60%
    ),
    var(--surface);
}
.welcome {
  margin: 0;
  font-weight: 800;
  letter-spacing: 0.2px;
  opacity: 0.92;
  font-size: clamp(18px, 2.3vw, 32px);
  text-align: center;
}
.question {
  margin: 0 0 10px;
  font-weight: 900;
  line-height: 1.05;
  text-align: center;
  font-size: clamp(32px, 6.8vw, 64px);
}

.prompt {
  width: min(1600px, 92vw);
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  background: color-mix(in oklab, var(--surface), black 8%);
  border: 1px solid var(--border);
  border-radius: 26px;
  padding: 10px;
  gap: 10px;
  box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--surface), white 6%),
    0 6px 24px rgba(2, 6, 23, 0.08);
}
.prompt-input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text-900);
  padding: 18px 16px 18px 18px;
  font-size: clamp(16px, 1.7vw, 22px);
}
.prompt-input::placeholder {
  color: color-mix(in oklab, var(--text-900), transparent 45%);
}
.send {
  width: 54px;
  height: 54px;
  border-radius: 999px;
  border: 1px solid var(--border);
  display: grid;
  place-items: center;
  background: linear-gradient(180deg, var(--brand-400), var(--brand-600));
  color: #fff;
  transition: transform 0.12s ease, filter 0.12s ease, opacity 0.12s ease,
    box-shadow 0.12s ease;
  box-shadow: 0 4px 18px rgba(16, 185, 129, 0.35);
}
.send:hover {
  transform: scale(1.04);
  filter: saturate(110%);
}
.send:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  filter: grayscale(0.15);
  box-shadow: none;
}

@keyframes k-shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20% {
    transform: translateX(-5px);
  }
  40% {
    transform: translateX(5px);
  }
  60% {
    transform: translateX(-3px);
  }
  80% {
    transform: translateX(3px);
  }
}
.prompt.shake {
  animation: k-shake 0.32s ease;
}

/* ===== NEWS DECK ===== */
.news-deck {
  width: 100vw;
  margin-left: 50%;
  transform: translateX(-50%);
  padding: clamp(16px, 4vw, 28px);
  padding-top: 0;
}
.news-grid {
  display: grid;
  grid-template-columns: minmax(0, 2.2fr) minmax(0, 1fr);
  gap: clamp(14px, 2.4vw, 20px);
}
.lead-carousel {
  position: relative;
  border: 1px solid var(--border);
  border-radius: 18px;
  overflow: hidden;
  height: clamp(280px, 42vw, 520px);
  background: var(--surface);
}
.lead-frame {
  position: absolute;
  inset: 0;
  background: var(--bg) center/cover no-repeat;
  opacity: 1;
}
.lead-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(
      1200px 700px at 10% 10%,
      rgba(16, 185, 129, 0.22),
      transparent 60%
    ),
    linear-gradient(180deg, rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.55));
  pointer-events: none;
}
.lead-cap {
  position: absolute;
  left: clamp(14px, 3vw, 28px);
  right: clamp(14px, 6vw, 240px);
  bottom: clamp(14px, 4vw, 36px);
  color: #fff;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.35);
  max-width: 960px;
}
.kicker {
  display: inline-block;
  font-weight: 800;
  letter-spacing: 0.2px;
  padding: 8px 10px;
  border-radius: 999px;
  background: color-mix(in oklab, white, transparent 75%);
  color: #065f46;
}
.kicker.pill {
  border: 1px solid var(--brand-200);
  background: var(--brand-50);
}
.lead-title {
  margin: 10px 0 4px;
  font-weight: 900;
  line-height: 1.02;
  font-size: clamp(28px, 5.4vw, 62px);
}
.lead-desc {
  opacity: 0.95;
  font-size: clamp(14px, 1.8vw, 18px);
}

.side-rail {
  position: sticky;
  top: clamp(70px, 9vh, 110px);
  max-height: calc(100vh - 120px);
  overflow: auto;
  scroll-snap-type: y proximity;
  display: grid;
  gap: clamp(14px, 2.2vw, 20px);
  padding-right: 2px;
  scrollbar-width: none;
}
.side-rail::-webkit-scrollbar {
  width: 0;
  height: 0;
}
.side-card {
  position: relative;
  min-height: clamp(180px, 44vh, 360px);
  border: 1px solid var(--border);
  border-radius: 18px;
  overflow: hidden;
  background: var(--bg) center/cover no-repeat;
  scroll-snap-align: start;
}
.side-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.55));
}
.side-cap {
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 14px;
  color: #fff;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.35);
}
.side-title {
  margin: 6px 0 0;
  font-size: clamp(16px, 2vw, 20px);
  font-weight: 800;
}

/* ===== SDG TICKER: 2 şerit ===== */
.sdg-ticker {
  width: 100vw;
  margin-left: 50%;
  transform: translateX(-50%);
  padding: clamp(8px, 2.2vw, 14px) clamp(12px, 6vw, 72px);
  display: grid;
  gap: 10px;
  background: transparent;
  border: 0;
}
.sdg-lane {
  overflow: hidden;
  mask-image: linear-gradient(
    90deg,
    transparent,
    #000 8%,
    #000 92%,
    transparent
  );
}
.sdg-track {
  display: inline-flex;
  gap: 10px;
  white-space: nowrap;
  will-change: transform;
  animation: sdg-marquee var(--dur, 40s) linear infinite;
}
.sdg-lane:hover .sdg-track {
  animation-play-state: paused;
}
@keyframes sdg-marquee {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

.sdg-chip {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: color-mix(in oklab, var(--surface), black 3%);
  color: var(--text-900);
  box-shadow: 0 1px 0 color-mix(in oklab, var(--surface), white 8%) inset,
    0 6px 18px rgba(2, 6, 23, 0.06);
  cursor: pointer;
  transition: transform 0.08s ease;
}
.sdg-chip:active {
  transform: scale(0.98);
}
.sdg-title {
  font-weight: 800;
  font-size: 14px;
  letter-spacing: 0.2px;
}

/* ===== MODAL ===== */
.modal-backdrop {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  background: color-mix(in oklab, var(--page-bg), black 60% / 40%);
  backdrop-filter: saturate(130%) blur(2px);
  z-index: 999;
}
.modal-card {
  width: min(640px, 92vw);
  background: var(--surface);
  color: var(--text-900);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: 0 24px 64px rgba(2, 6, 23, 0.28);
  padding: 14px;
}
.modal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.modal-title {
  margin: 0;
  font-weight: 900;
  font-size: 18px;
}
.modal-x {
  border: 1px solid var(--border);
  background: color-mix(in oklab, var(--surface), black 3%);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 20px;
  line-height: 1;
  display: grid;
  place-items: center;
}
.modal-list {
  margin: 10px 0 0;
  padding-left: 18px;
}
.modal-list li {
  margin: 4px 0;
  color: var(--text-800);
  font-size: 14px;
}
.modal-foot {
  display: flex;
  justify-content: flex-end;
  margin-top: 14px;
}
.modal-ok {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid var(--brand-300);
  background: linear-gradient(180deg, var(--brand-100), var(--brand-300));
  color: #065f46;
  font-weight: 800;
  cursor: pointer;
}

/* ===== ROADMAP ===== */
.roadmap {
  padding: 40px 0 80px;
  border-top: 1px solid var(--border);
  background: linear-gradient(
    180deg,
    var(--surface),
    color-mix(in oklab, var(--page-bg), white 3%)
  );
}
.container {
  width: min(1200px, 92vw);
  margin: 0 auto;
}
.section-title {
  font-weight: 900;
  margin-bottom: 16px;
}
.steps {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  counter-reset: s;
}
.steps li {
  position: relative;
  border: 1px solid var(--border);
  background: var(--surface);
  border-radius: 16px;
  padding: 14px;
}
.steps li::before {
  counter-increment: s;
  content: counter(s);
  position: absolute;
  top: -10px;
  left: -10px;
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  font-weight: 900;
  background: var(--brand-50);
  border: 1px solid var(--brand-200);
  color: #065f46;
}
.steps h3 {
  margin: 2px 0 6px;
  font-weight: 800;
}
.steps p {
  margin: 0;
  color: var(--text-700);
}

@media (max-width: 992px) {
  .news-grid {
    grid-template-columns: 1fr;
  }
  .side-rail {
    position: static;
    max-height: none;
  }
  .steps {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 640px) {
  .steps {
    grid-template-columns: 1fr;
  }
  .send {
    width: 48px;
    height: 48px;
  }
  .prompt-input {
    padding: 14px 12px 14px 14px;
  }
}
:root {
  color-scheme: light dark;
}
</style>

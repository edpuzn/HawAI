<template>
  <div class="container py-5 devs-root">
    <h1 class="page-title text-center mb-5">Developers</h1>

    <!-- Timeline / Alternating Cards -->
    <div class="dev-timeline">
      <section
        v-for="(dev, idx) in devs"
        :key="dev.id"
        class="dev-item"
        :class="idx % 2 === 0 ? 'left' : 'right'"
      >
        <div class="dev-card glass hover-rise">
          <div class="d-flex align-items-center gap-3 flex-wrap">
            <img
              :src="dev.photo"
              :alt="dev.name"
              class="avatar-xl shadow-sm"
              loading="lazy"
              decoding="async"
            />

            <div class="flex-grow-1">
              <h2 class="dev-name mb-1">{{ dev.name }}</h2>
              <div class="role-badge">{{ dev.role }}</div>

              <div class="d-flex align-items-center gap-2 mt-3">
                <a
                  class="btn-linkedin"
                  :href="dev.linkedin"
                  target="_blank"
                  rel="noopener"
                  aria-label="LinkedIn"
                  title="LinkedIn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      d="M4.98 3.5C4.98 4.88 3.86 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM0 8h5v16H0zM8 8h4.8v2.2h.07c.67-1.2 2.3-2.47 4.73-2.47C22.6 7.73 24 10.3 24 14.2V24h-5v-8.4c0-2-.04-4.57-2.78-4.57-2.78 0-3.2 2.17-3.2 4.42V24H8z"
                    />
                  </svg>
                  <span>LinkedIn</span>
                </a>

                <button
                  class="btn btn-success btn-sm px-3"
                  type="button"
                  data-bs-toggle="modal"
                  data-bs-target="#devModal"
                  @click="selected = dev"
                >
                  Hakkında
                </button>
              </div>
            </div>
          </div>

          <!-- alt özet/chips -->
          <ul class="dev-highlights">
            <li v-for="(h, i) in dev.highlights" :key="i">{{ h }}</li>
          </ul>
        </div>
      </section>
    </div>

    <!-- Modal body'e taşındı -->
    <teleport to="body">
      <div
        class="modal fade"
        id="devModal"
        tabindex="-1"
        aria-labelledby="devModalTitle"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content modal-surface rounded-4 shadow-lg">
            <div class="modal-gradient" aria-hidden="true"></div>

            <div class="modal-header border-0 pb-0">
              <h2
                class="modal-title w-100 text-center dev-name fs-2"
                id="devModalTitle"
              >
                {{ selected?.name }}
                <div class="role-badge mt-2">{{ selected?.role }}</div>
              </h2>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>

            <div class="modal-body pt-2">
              <div class="d-flex flex-column align-items-center text-center">
                <img
                  :src="selected?.photo"
                  :alt="selected?.name"
                  class="avatar-lg shadow mb-3"
                  loading="lazy"
                  decoding="async"
                />

                <p class="dev-body mb-3">{{ selected?.bio }}</p>

                <div class="d-flex flex-wrap justify-content-center gap-2 mb-1">
                  <span
                    v-for="(h, i) in selected?.highlights || []"
                    :key="i"
                    class="chip"
                  >
                    {{ h }}
                  </span>
                </div>

                <a
                  v-if="selected"
                  :href="selected.linkedin"
                  target="_blank"
                  class="btn-linkedin mt-2"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M4.98 3.5C4.98 4.88 3.86 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM0 8h5v16H0zM8 8h4.8v2.2h.07c.67-1.2 2.3-2.47 4.73-2.47C22.6 7.73 24 10.3 24 14.2V24h-5v-8.4c0-2-.04-4.57-2.78-4.57-2.78 0-3.2 2.17-3.2 4.42V24H8z"
                    />
                  </svg>
                  <span>LinkedIn</span>
                </a>
              </div>
            </div>
            <!-- footer yok; sadece çarpı -->
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

// Bootstrap removed - using custom responsive design

import edip from "@/assets/team/edip.jpeg";
import nurgul from "@/assets/team/nurgul.jpeg";
import bartu from "@/assets/team/bartu.jpeg";

type Dev = {
  id: string;
  name: string;
  role: string;
  photo: string;
  linkedin: string;
  bio: string;
  highlights: string[];
};

const devs: Dev[] = [
  {
    id: "edip",
    name: "Mustafa Edip Uzan",
    role: "Project Manager",
    photo: edip,
    linkedin: "https://www.linkedin.com/in/edipuzan",
    bio: "Proje planlama, süreç koordinasyonu ve ürün vizyonuna liderlik.",
    highlights: [
      "Scrum & roadmapping",
      "Risk & KPI takibi",
      "Paydaş iletişimi",
    ],
  },
  {
    id: "nurgul",
    name: "Nurgül Yalman",
    role: "Researcher",
    photo: nurgul,
    linkedin: "https://www.linkedin.com/in/nurgul-yalman",
    bio: "Literatür analizi, deney tasarımı ve raporlama.",
    highlights: [
      "Benchmark & POC",
      "Akademik araştırma",
      "Sunum & dokümantasyon",
    ],
  },
  {
    id: "bartu",
    name: "Bartu Dönmez",
    role: "Developer",
    photo: bartu,
    linkedin: "https://www.linkedin.com/in/bartu-donmez",
    bio: "Vue + TypeScript ile modern arayüz ve servis entegrasyonları.",
    highlights: ["Vite + Vue 3", "API entegrasyon", "Performans & test"],
  },
];

const selected = ref<Dev | null>(devs[0]);
</script>

<style scoped>
/* ===== Title ===== */
.page-title {
  font-weight: 900;
  letter-spacing: 0.2px;
  color: var(--text-900);
}

/* ===== Timeline ===== */
.dev-timeline {
  position: relative;
  display: grid;
  gap: 28px;
}
.dev-timeline::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  transform: translateX(-50%);
  background: var(--border);
  opacity: 0.35;
}
.dev-item {
  display: grid;
  grid-template-columns: 1fr minmax(0, 560px) 1fr;
  align-items: center;
}
.dev-item.left .dev-card {
  grid-column: 1 / 3;
  justify-self: end;
}
.dev-item.right .dev-card {
  grid-column: 2 / 4;
  justify-self: start;
}

@media (max-width: 992px) {
  .dev-timeline::before {
    display: none;
  }
  .dev-item {
    grid-template-columns: 1fr;
  }
  .dev-item.left .dev-card,
  .dev-item.right .dev-card {
    grid-column: 1;
    justify-self: stretch;
  }
}

@media (max-width: 768px) {
  .dev-card {
    padding: 16px;
  }

  .dev-card .d-flex {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }

  .avatar-xl {
    width: 80px;
    height: 80px;
    align-self: center;
  }

  .dev-name {
    font-size: 20px;
  }

  .dev-highlights {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .dev-card {
    padding: 12px;
  }

  .avatar-xl {
    width: 64px;
    height: 64px;
  }

  .dev-name {
    font-size: 18px;
  }

  .role-badge {
    font-size: 0.85rem;
    padding: 3px 8px;
  }

  .dev-highlights li {
    font-size: 0.8rem;
    padding: 3px 8px;
  }
}

/* ===== Cards ===== */
.dev-card {
  width: min(640px, 100%);
  padding: 18px;
  border-radius: 18px;
  border: 1px solid var(--border);
  position: relative;
}
.glass {
  background: linear-gradient(
        180deg,
        rgba(255, 255, 255, 0.06),
        rgba(255, 255, 255, 0)
      )
      /* light overlay */,
    var(--surface);
  backdrop-filter: saturate(140%) blur(8px);
}
.hover-rise {
  transition: transform 0.18s ease, box-shadow 0.18s ease,
    border-color 0.18s ease;
}
.hover-rise:hover {
  transform: translateY(-2px);
  border-color: rgba(34, 197, 94, 0.35);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.dev-name {
  font-weight: 800;
  color: var(--text-900);
  margin: 0;
}
.role-badge {
  display: inline-block;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 4px 10px;
  border-radius: 999px;
  color: #065f46;
  background: var(--brand-50);
  border: 1px solid var(--brand-200);
}

/* quick chips */
.dev-highlights {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 14px 0 0 0;
  padding: 0;
  list-style: none;
}
.dev-highlights li {
  font-size: 0.9rem;
  color: var(--text-700);
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--surface);
  border: 1px solid var(--border);
}

/* ===== Avatars ===== */
.avatar-xl {
  width: 96px;
  height: 96px;
  border-radius: 16px;
  object-fit: cover;
  border: 1px solid var(--border);
}
.avatar-lg {
  width: 220px;
  height: 220px;
  border-radius: 18px;
  object-fit: cover;
  border: 2px solid var(--border);
}

/* ===== LinkedIn button ===== */
.btn-linkedin {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1px solid var(--brand-200);
  background: var(--brand-50);
  color: #065f46;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.15s ease, border-color 0.15s ease,
    transform 0.12s ease;
}
.btn-linkedin:hover {
  background: var(--brand-100);
  border-color: var(--brand-300);
  transform: translateY(-1px);
}

/* ===== Modal ===== */
.modal-surface {
  background: var(--surface);
  color: var(--text-900);
  border: 1px solid var(--border);
}
.modal-gradient {
  position: absolute;
  inset: 0 0 auto 0;
  height: 6px;
  border-radius: 16px 16px 0 0;
  background: linear-gradient(90deg, var(--brand-400), var(--brand-600));
  opacity: 0.85;
}
.dev-body {
  color: var(--text-700);
}

/* small pill chips in modal */
.chip {
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-700);
  font-size: 0.92rem;
}

/* Backdrop blur */
.modal-backdrop.show {
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(6px);
  z-index: 1990;
}
.modal {
  z-index: 2000;
}
</style>

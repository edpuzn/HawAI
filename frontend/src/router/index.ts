import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { title: "HawAI — Home" },
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/AboutView.vue"),
    meta: { title: "HawAI — About" },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("../views/NotFoundView.vue"),
    meta: { title: "Sayfa bulunamadı — HawAI" },
  },
  {
    path: "/developers",
    name: "Developers",
    component: () => import("../views/DevelopersView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // TS için vite/client türleri şart
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    return { top: 0 };
  },
});

// İsteğe bağlı: sekme başlığını rotaya göre ayarla
router.beforeEach((to) => {
  const base = "HawAI";
  if (to.meta?.title) document.title = String(to.meta.title);
  else if (typeof to.name === "string") document.title = `${base} — ${to.name}`;
  else document.title = base;
});

export default router;

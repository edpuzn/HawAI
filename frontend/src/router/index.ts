import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/chat",
  },
  {
    path: "/chat",
    name: "chat",
    component: () => import("../views/Chat.vue"),
    meta: { title: "HawAI — Sohbet" },
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/AboutView.vue"),
    meta: { title: "HawAI — Hakkında" },
  },
  {
    path: "/ilkyardim",
    name: "ilkyardim",
    component: () => import("../views/IlkyardimView.vue"),
    meta: { title: "HawAI — İlkyardım" },
  },
  {
    path: "/developers",
    name: "developers",
    component: () => import("../views/DevelopersView.vue"),
    meta: { title: "HawAI — Geliştiriciler" },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login.vue"),
    meta: { title: "HawAI — Giriş" },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Register.vue"),
    meta: { title: "HawAI — Kayıt" },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("../views/NotFoundView.vue"),
    meta: { title: "Sayfa bulunamadı — HawAI" },
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

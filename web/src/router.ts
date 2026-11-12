import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView, meta: { title: "Accueil" } },
    // The other pages are loaded on demand (one JS chunk each).
    {
      path: "/joueur",
      name: "player",
      component: () => import("./views/PlayerView.vue"),
      meta: { title: "Fiche joueur" },
    },
    {
      path: "/comparer",
      name: "compare",
      component: () => import("./views/CompareView.vue"),
      meta: { title: "Comparaison de joueurs" },
    },
    {
      path: "/match",
      name: "match",
      component: () => import("./views/MatchView.vue"),
      meta: { title: "Détail de match" },
    },
  ],
  // Scroll to an anchor (/#pipeline) or back to the top on page change.
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition;
    if (to.hash) return { el: to.hash };
    return { top: 0 };
  },
});

router.afterEach((to) => {
  document.title = `${String(to.meta.title)} — D-Foot`;
});

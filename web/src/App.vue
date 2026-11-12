<script setup lang="ts">
// Layout shared by every page: header with navigation, page content, footer.
const SOURCE_URL = "https://github.com/MirijaMarc/d-foot";
</script>

<template>
  <header class="site-header">
    <nav
      aria-label="Navigation principale"
      class="container nav"
    >
      <RouterLink
        to="/"
        class="brand"
      >
        <svg
          width="28"
          height="28"
          viewBox="0 0 28 28"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          aria-hidden="true"
        >
          <rect
            x="2"
            y="5"
            width="24"
            height="18"
            rx="2"
          />
          <line
            x1="14"
            y1="5"
            x2="14"
            y2="23"
          />
          <circle
            cx="14"
            cy="14"
            r="3.5"
          />
        </svg>
        <span>D-Foot</span>
      </RouterLink>
      <div class="nav-links">
        <!-- RouterLink adds aria-current="page" to the link of the current page. -->
        <RouterLink
          to="/joueur"
          class="nav-link"
        >Joueurs</RouterLink>
        <RouterLink
          to="/match"
          class="nav-link"
        >Matchs</RouterLink>
        <RouterLink
          to="/comparer"
          class="nav-link"
        >Comparer</RouterLink>
        <!-- "custom": a plain <a>, so this link to a home section is never marked current. -->
        <RouterLink
          v-slot="{ href, navigate }"
          :to="{ path: '/', hash: '#pipeline' }"
          custom
        >
          <a
            :href="href"
            class="nav-link"
            @click="navigate"
          >Pipeline</a>
        </RouterLink>
      </div>
      <a
        :href="SOURCE_URL"
        class="source-link"
      >Code source</a>
    </nav>
  </header>

  <RouterView />

  <footer class="site-footer">
    <div class="container footer-inner">
      <span>
        Données :
        <a href="https://github.com/statsbomb/open-data">StatsBomb Open Data</a>
      </span>
      <span>Projet personnel de Mirija</span>
    </div>
  </footer>
</template>

<style scoped>
.site-header {
  border-bottom: 1px solid var(--border);
}

.nav {
  padding-top: 16px;
  padding-bottom: 16px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 18px;
}

.brand svg {
  color: var(--accent);
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  flex: 1 1 auto;
}

.nav-link {
  padding: 10px 14px;
  border-radius: 8px;
  color: var(--text-2);
  text-decoration: none;
  font-size: 15px;
}

.nav-link:hover {
  color: var(--text);
}

.nav-link[aria-current="page"] {
  background: var(--surface-2);
  color: var(--text);
}

.source-link {
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  text-decoration: none;
  font-size: 14px;
}

.site-footer {
  border-top: 1px solid var(--border);
}

.footer-inner {
  padding-top: 28px;
  padding-bottom: 28px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 16px;
  font-size: 14px;
  color: var(--muted);
}
</style>

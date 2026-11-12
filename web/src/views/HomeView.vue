<script setup lang="ts">
import { ref } from "vue";
import { competitions, pipelineSteps } from "../data/demo";

const query = ref("");

// Search isn't wired yet: it will call the API once players/matches are served.
function search(): void {}

// Data volume figures: will come from the API (pipeline run metadata).
const volume = [
  { label: "matchs ingérés" },
  { label: "événements traités" },
  { label: "compétitions couvertes" },
  { label: "durée du dernier run complet" },
];
</script>

<template>
  <main class="container">
    <section class="hero">
      <p class="eyebrow mono">
        StatsBomb Open Data · pipeline open source
      </p>
      <h1>Chaque tir, chaque passe, transformés en analyses.</h1>
      <p class="lead">
        Fiches joueurs, comparaisons et détails de match calculés à partir des données
        événementielles StatsBomb, avec un modèle xG maison entraîné sur les données 360.
      </p>
      <form
        role="search"
        class="search"
        @submit.prevent="search"
      >
        <label
          for="recherche"
          class="visually-hidden"
        >
          Rechercher un joueur, une équipe ou un match
        </label>
        <input
          id="recherche"
          v-model="query"
          type="search"
          placeholder="Rechercher un joueur, une équipe, un match…"
        >
        <button type="submit">
          Rechercher
        </button>
      </form>
    </section>

    <section
      aria-label="Volume de données"
      class="volume"
    >
      <div
        v-for="item in volume"
        :key="item.label"
        class="volume-item"
      >
        <!-- "—" until the API provides the figure. -->
        <span class="volume-value">—</span>
        <span class="muted">{{ item.label }}</span>
      </div>
    </section>

    <section class="block">
      <h2>Compétitions</h2>
      <div class="competitions">
        <RouterLink
          v-for="c in competitions"
          :key="c.name"
          to="/match"
          class="card competition"
        >
          <span class="chip mono">{{ c.tag }}</span>
          <span class="competition-name">{{ c.name }}</span>
          <span class="muted small">{{ c.period }}</span>
        </RouterLink>
      </div>
    </section>

    <section class="block">
      <h2>À explorer</h2>
      <RouterLink
        to="/match"
        class="card feature"
      >
        <div class="feature-text">
          <span class="muted xsmall">Finale · Coupe du monde 2022 · 18 déc. 2022</span>
          <span class="feature-title">Argentine 3 – 3 France</span>
          <span class="muted small">Argentine victorieuse aux tirs au but (4–2)</span>
        </div>
        <span class="feature-cta">Voir le match →</span>
      </RouterLink>
      <RouterLink
        to="/comparer"
        class="card feature"
      >
        <div class="feature-text">
          <span class="muted xsmall">Comparaison · Coupe du monde 2022</span>
          <span class="feature-title">Messi vs Mbappé</span>
          <span class="muted small">Statistiques par 90 minutes sur le tournoi</span>
        </div>
        <span class="feature-cta">Comparer →</span>
      </RouterLink>
    </section>

    <section
      id="pipeline"
      class="block"
    >
      <h2>Le pipeline derrière les chiffres</h2>
      <ol class="steps">
        <li
          v-for="s in pipelineSteps"
          :key="s.n"
          class="step"
        >
          <span class="step-n mono">{{ s.n }}</span>
          <span class="step-title">{{ s.title }}</span>
          <span class="muted step-text">{{ s.text }}</span>
        </li>
      </ol>
      <p class="muted small">
        Dernier run Airflow : — · statut : — · tests dbt : —
      </p>
    </section>
  </main>
</template>

<style scoped>
main {
  padding-bottom: 88px;
}

h2 {
  font-size: 28px;
}

.small {
  font-size: 14px;
}

.xsmall {
  font-size: 13px;
}

.hero {
  padding: 88px 0 56px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 820px;
}

.eyebrow {
  font-size: 13px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
}

.hero h1 {
  /* 56px on desktop, shrinks on phones. */
  font-size: clamp(36px, 7vw, 56px);
  line-height: 1.05;
}

.lead {
  font-size: 19px;
  line-height: 1.55;
  color: var(--muted);
}

.search {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
}

.search input {
  flex: 1 1 360px;
  min-width: 0;
  height: 52px;
  padding: 0 18px;
  border-radius: 10px;
  border: 1px solid var(--border-strong);
  background: var(--surface);
  color: var(--text);
  font-size: 16px;
}

.search button {
  height: 52px;
  padding: 0 26px;
  border: 0;
  border-radius: 10px;
  background: var(--accent);
  color: var(--bg);
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
}

.search button:hover {
  background: var(--accent-hover);
}

/* 1px gaps over a border-coloured background draw the separators. */
.volume {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}

.volume-item {
  background: var(--surface);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
}

.volume-value {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 600;
}

.block {
  padding-top: 72px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.competitions {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.competition {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 22px;
  text-decoration: none;
  color: var(--text);
}

.competition:hover,
.feature:hover {
  border-color: var(--border-strong);
  color: var(--text);
}

.chip {
  align-self: flex-start;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--surface-2);
  color: var(--text-2);
  font-size: 12px;
}

.competition-name {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
}

.feature {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 24px;
  padding: 24px 28px;
  text-decoration: none;
  color: var(--text);
}

.feature-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1 1 280px;
}

.feature-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
}

.feature-cta {
  font-size: 15px;
  font-weight: 600;
  color: var(--accent);
}

.steps {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
}

.step {
  padding: 18px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-n {
  font-size: 12px;
  color: var(--accent);
}

.step-title {
  font-weight: 600;
}

.step-text {
  font-size: 14px;
  line-height: 1.45;
}
</style>

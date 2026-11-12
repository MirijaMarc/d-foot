<script setup lang="ts">
import { computed, ref } from "vue";
import { comparison } from "../data/demo";
import { fmt } from "../format";

type Mode = "per90" | "total";
const mode = ref<Mode>("per90");

// Editable, but not looked up yet: the API will provide player search.
const playerA = ref(comparison.a.name);
const playerB = ref(comparison.b.name);

const caption = computed(() =>
  mode.value === "per90"
    ? "Statistiques ramenées à 90 minutes jouées"
    : "Totaux sur l’ensemble du tournoi",
);

// Each bar is a share of the larger of the two values (the larger one = 100%).
const rows = computed(() =>
  comparison.metrics.map((m) => {
    const [a, b] = mode.value === "per90" ? m.per90 : m.total;
    const max = Math.max(a, b) || 1;
    return {
      label: m.label,
      a: fmt(a),
      b: fmt(b),
      widthA: Math.round((a / max) * 100),
      widthB: Math.round((b / max) * 100),
    };
  }),
);
</script>

<template>
  <main class="container page">
    <h1>Comparer deux joueurs</h1>

    <section
      aria-label="Choix des joueurs"
      class="pickers"
    >
      <div class="card picker picker-a">
        <label for="joueurA">Joueur A</label>
        <input
          id="joueurA"
          v-model="playerA"
          type="text"
        >
        <span class="muted small">{{ comparison.a.info }}</span>
      </div>
      <div
        class="versus"
        aria-hidden="true"
      >
        vs
      </div>
      <div class="card picker picker-b">
        <label for="joueurB">Joueur B</label>
        <input
          id="joueurB"
          v-model="playerB"
          type="text"
        >
        <span class="muted small">{{ comparison.b.info }}</span>
      </div>
    </section>

    <section class="card chart">
      <div class="chart-head">
        <div class="chart-title">
          <h2>{{ comparison.competition }}</h2>
          <span class="muted xsmall">{{ caption }}</span>
        </div>
        <div
          role="group"
          aria-label="Unité des statistiques"
          class="toggle"
        >
          <button
            type="button"
            :aria-pressed="mode === 'per90'"
            @click="mode = 'per90'"
          >
            Par 90 min
          </button>
          <button
            type="button"
            :aria-pressed="mode === 'total'"
            @click="mode = 'total'"
          >
            Totaux
          </button>
        </div>
      </div>

      <div class="names">
        <span class="name-a">{{ comparison.a.short }}</span>
        <span class="name-b">{{ comparison.b.short }}</span>
      </div>

      <div
        v-for="r in rows"
        :key="r.label"
        class="row"
      >
        <div class="side side-a">
          <span class="mono value">{{ r.a }}</span>
          <div class="track track-a">
            <div
              class="bar bar-a"
              :style="{ width: `${r.widthA}%` }"
            />
          </div>
        </div>
        <span class="row-label">{{ r.label }}</span>
        <div class="side">
          <div class="track">
            <div
              class="bar bar-b"
              :style="{ width: `${r.widthB}%` }"
            />
          </div>
          <span class="mono value">{{ r.b }}</span>
        </div>
      </div>
    </section>

    <section class="strengths">
      <div class="card strength">
        <span class="strength-title name-a">Points forts de {{ comparison.a.short }}</span>
        <p>{{ comparison.strengths.a }}</p>
      </div>
      <div class="card strength">
        <span class="strength-title name-b">Points forts de {{ comparison.b.short }}</span>
        <p>{{ comparison.strengths.b }}</p>
      </div>
    </section>

    <p class="note">
      Chiffres illustratifs dans cette maquette : remplacés par les tables gold du pipeline.
    </p>
  </main>
</template>

<style scoped>
.page {
  padding-top: 40px;
}

h1 {
  font-size: 40px;
}

.small {
  font-size: 14px;
}

.xsmall {
  font-size: 13px;
}

.pickers {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 16px;
}

.picker {
  flex: 1 1 320px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.picker-a {
  border-top: 4px solid var(--team-a);
}

.picker-b {
  border-top: 4px solid var(--team-b);
}

.picker label {
  font-size: 13px;
  color: var(--muted);
}

.picker input {
  height: 48px;
  padding: 0 14px;
  border-radius: 10px;
  border: 1px solid var(--border-strong);
  background: var(--bg);
  color: var(--text);
  font-size: 17px;
  font-weight: 600;
}

.versus {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--muted);
}

.chart {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.chart-head {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.chart-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toggle {
  display: flex;
  padding: 4px;
  gap: 4px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 10px;
}

.toggle button {
  min-height: 40px;
  padding: 0 16px;
  border: 0;
  border-radius: 7px;
  background: transparent;
  color: var(--text-2);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.toggle button[aria-pressed="true"] {
  background: var(--accent);
  color: var(--bg);
  font-weight: 600;
}

.names {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  font-weight: 600;
}

.name-a {
  color: var(--team-a);
}

.name-b {
  color: var(--team-b);
}

/* Butterfly chart: A's bar grows leftwards, B's rightwards, label in the middle. */
.row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 150px minmax(0, 1fr);
  align-items: center;
  gap: 16px;
}

.side {
  display: flex;
  align-items: center;
  gap: 10px;
}

.side-a {
  justify-content: flex-end;
}

.value {
  font-size: 14px;
}

.track {
  flex: 1 1 auto;
  height: 14px;
  display: flex;
}

.track-a {
  justify-content: flex-end;
}

.bar {
  height: 100%;
}

.bar-a {
  border-radius: 4px 0 0 4px;
  background: var(--team-a);
}

.bar-b {
  border-radius: 0 4px 4px 0;
  background: var(--team-b);
}

.row-label {
  text-align: center;
  font-size: 14px;
  color: var(--text-2);
}

.strengths {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.strength {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.strength-title {
  font-size: 13px;
  font-weight: 600;
}

.strength p {
  font-size: 15px;
  line-height: 1.5;
  color: var(--text-2);
}

/* Phones: narrower label column so the bars keep some room. */
@media (max-width: 600px) {
  .chart {
    padding: 20px;
  }

  .row {
    grid-template-columns: minmax(0, 1fr) 88px minmax(0, 1fr);
    gap: 8px;
  }

  .row-label {
    font-size: 12px;
  }
}
</style>

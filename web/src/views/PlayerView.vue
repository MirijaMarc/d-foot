<script setup lang="ts">
import { ref } from "vue";
import { player } from "../data/demo";
import { fmt } from "../format";

// Selected scope. Not applied yet: the API will filter the stats by scope.
const scope = ref(player.scopes[0]);

// Marker diameter grows with the shot's xG (12px for 0, 46px for 1).
function shotSize(xg: number): number {
  return Math.round(12 + xg * 34);
}
</script>

<template>
  <main class="container page">
    <p class="breadcrumb">
      <RouterLink to="/">Accueil</RouterLink> / Joueurs / {{ player.name }}
    </p>

    <section class="identity">
      <div
        class="avatar"
        aria-hidden="true"
      >
        {{ player.initials }}
      </div>
      <div class="identity-text">
        <h1>{{ player.name }}</h1>
        <p class="muted">
          {{ player.subtitle }}
        </p>
      </div>
      <div class="scope">
        <label for="perimetre">Périmètre</label>
        <select
          id="perimetre"
          v-model="scope"
        >
          <option
            v-for="s in player.scopes"
            :key="s"
          >
            {{ s }}
          </option>
        </select>
      </div>
      <RouterLink
        to="/comparer"
        class="compare-button"
      >Comparer</RouterLink>
    </section>

    <section
      aria-label="Chiffres clés"
      class="kpis"
    >
      <div
        v-for="k in player.kpis"
        :key="k.label"
        class="card kpi"
      >
        <span class="muted small">{{ k.label }}</span>
        <span class="kpi-value">{{ k.value }}</span>
        <span class="muted small">{{ k.sub }}</span>
      </div>
    </section>

    <div class="columns">
      <section class="card panel shots-panel">
        <div class="panel-head">
          <h2>Carte des tirs</h2>
          <span class="muted small">Taille = xG du tir</span>
        </div>
        <div
          class="pitch"
          role="img"
          aria-label="Carte des tirs sur une moitié de terrain, but en haut"
        >
          <!-- Pitch markings: penalty area, six-yard box, goal, halfway line, centre circle. -->
          <div class="line penalty-area" />
          <div class="line six-yard-box" />
          <div class="goal" />
          <div class="halfway" />
          <div class="line centre-circle" />
          <span
            v-for="(s, i) in player.shots"
            :key="i"
            class="shot"
            :class="{ goal: s.goal }"
            :style="{
              left: `${s.x}%`,
              top: `${s.y}%`,
              width: `${shotSize(s.xg)}px`,
              height: `${shotSize(s.xg)}px`,
            }"
          />
        </div>
        <div class="legend">
          <span><span class="dot legend-goal" />But</span>
          <span><span class="dot legend-miss" />Tir non marqué</span>
        </div>
      </section>

      <section class="card panel profile-panel">
        <div class="panel-title">
          <h2>Profil par 90 minutes</h2>
          <span class="muted small">Percentile parmi les attaquants du tournoi</span>
        </div>
        <div
          v-for="p in player.percentiles"
          :key="p.label"
          class="percentile"
        >
          <div class="percentile-head">
            <span>{{ p.label }}</span>
            <span class="mono percentile-value">{{ fmt(p.value, 1) }} · {{ p.pct }}e</span>
          </div>
          <div class="bar-track">
            <div
              class="bar"
              :style="{ width: `${p.pct}%` }"
            />
          </div>
        </div>
      </section>
    </div>

    <section class="card panel">
      <h2>Matchs du tournoi</h2>
      <!-- Wide table: scrolls horizontally inside its box on small screens. -->
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th scope="col">
                Match
              </th>
              <th scope="col">
                Phase
              </th>
              <th
                scope="col"
                class="num"
              >
                Min.
              </th>
              <th
                scope="col"
                class="num"
              >
                Buts
              </th>
              <th
                scope="col"
                class="num"
              >
                xG
              </th>
              <th
                scope="col"
                class="num"
              >
                Passes clés
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="m in player.matches"
              :key="m.name"
            >
              <td>
                <RouterLink
                  to="/match"
                  class="match-link"
                >{{ m.name }}</RouterLink>
              </td>
              <td class="muted">
                {{ m.phase }}
              </td>
              <td class="num mono">
                {{ m.minutes }}
              </td>
              <td class="num mono">
                {{ m.goals }}
              </td>
              <td class="num mono">
                {{ fmt(m.xg, 1) }}
              </td>
              <td class="num mono">
                {{ m.keyPasses }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="note">
        Chiffres illustratifs dans cette maquette : remplacés par les tables gold du pipeline.
      </p>
    </section>
  </main>
</template>

<style scoped>
.small {
  font-size: 13px;
}

.identity {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 24px;
}

.avatar {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: var(--surface-2);
  border: 2px solid var(--team-a);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 700;
  color: var(--team-a);
}

.identity-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1 1 300px;
}

.identity h1 {
  font-size: 44px;
}

.scope {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.scope label {
  font-size: 13px;
  color: var(--muted);
}

.scope select {
  height: 46px;
  min-width: 240px;
  padding: 0 14px;
  border-radius: 10px;
  border: 1px solid var(--border-strong);
  background: var(--surface);
  color: var(--text);
  font-size: 15px;
}

.compare-button {
  height: 46px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  align-self: flex-end;
  border-radius: 10px;
  background: var(--accent);
  color: var(--bg);
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
}

.compare-button:hover {
  background: var(--accent-hover);
  color: var(--bg);
}

.kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
}

.kpi {
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.kpi-value {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 600;
}

.columns {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.panel {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.shots-panel {
  flex: 1 1 460px;
}

.profile-panel {
  flex: 1 1 380px;
  gap: 18px;
}

.panel-head {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: baseline;
  gap: 8px;
}

.panel-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pitch {
  position: relative;
  height: 380px;
  border-radius: 10px;
  background: var(--pitch);
  overflow: hidden;
}

.pitch > div {
  position: absolute;
}

.line {
  border: 2px solid rgb(255 255 255 / 35%);
}

.penalty-area {
  left: 20%;
  right: 20%;
  top: 0;
  height: 30%;
  border-top: 0;
}

.six-yard-box {
  left: 37%;
  right: 37%;
  top: 0;
  height: 10%;
  border-top: 0;
}

.goal {
  left: 44%;
  right: 44%;
  top: 0;
  height: 4px;
  background: rgb(255 255 255 / 70%);
}

.halfway {
  left: 0;
  right: 0;
  bottom: 0;
  height: 2px;
  background: rgb(255 255 255 / 35%);
}

.centre-circle {
  left: 50%;
  bottom: -60px;
  width: 120px;
  height: 120px;
  margin-left: -60px;
  border-radius: 50%;
}

/* Centred on its (x, y) position whatever its size. */
.shot {
  position: absolute;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  box-sizing: border-box;
  border: 2px solid var(--text);
  background: rgb(232 238 234 / 12%);
}

.shot.goal {
  border: 0;
  background: var(--accent);
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  font-size: 13px;
  color: var(--text-2);
}

.legend > span {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend .dot {
  width: 12px;
  height: 12px;
  box-sizing: border-box;
}

.legend-goal {
  background: var(--accent);
}

.legend-miss {
  border: 2px solid var(--text);
}

.percentile {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.percentile-head {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.percentile-value {
  color: var(--text-2);
}

.bar-track {
  height: 8px;
  border-radius: 999px;
  background: var(--border);
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 999px;
  background: var(--team-a);
}

.table-scroll {
  overflow-x: auto;
}

table {
  width: 100%;
  min-width: 640px;
  border-collapse: collapse;
  font-size: 15px;
}

th {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  text-align: left;
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
}

td {
  padding: 12px;
  border-bottom: 1px solid var(--surface-2);
}

.num {
  text-align: right;
}

.match-link {
  color: var(--text);
}
</style>

<script setup lang="ts">
import { type Side, match } from "../data/demo";
import { fmt } from "../format";

const teamColor = (side: Side): string => (side === "a" ? "var(--team-a)" : "var(--team-b)");

// Timeline: position in % of the match duration (capped so labels stay inside).
// Team A's goals sit above the axis; team B's below, alternating between two
// rows so labels of goals a minute apart don't overlap (as in the design).
let bGoals = 0;
const goals = match.goals.map((g) => {
  const top = g.side === "a" ? 30 : bGoals++ % 2 === 0 ? 96 : 132;
  return {
    ...g,
    left: Math.min((g.minute / match.duration) * 100, 94),
    top,
  };
});

// Share of team A in each stat, for the two-colour bar.
const stats = match.stats.map((s) => ({
  ...s,
  shareA: Math.round((s.a / (s.a + s.b)) * 100),
  labelA: fmt(s.a) + (s.unit ?? ""),
  labelB: fmt(s.b) + (s.unit ?? ""),
}));
</script>

<template>
  <main class="container page">
    <p class="breadcrumb">
      <RouterLink to="/">Accueil</RouterLink> /
      {{ match.breadcrumb.join(" / ") }}
    </p>

    <section class="card scoreboard">
      <span class="muted small">{{ match.context }}</span>
      <div class="score-line">
        <div class="team">
          <span
            class="dot team-dot"
            :style="{ background: teamColor('a') }"
          />
          <span class="team-name">{{ match.teamA }}</span>
        </div>
        <span class="score">{{ match.score[0] }} – {{ match.score[1] }}</span>
        <div class="team">
          <span
            class="dot team-dot"
            :style="{ background: teamColor('b') }"
          />
          <span class="team-name">{{ match.teamB }}</span>
        </div>
      </div>
      <span class="outcome">{{ match.outcome }}</span>
    </section>

    <section class="card panel">
      <h2>Chronologie des buts</h2>
      <!-- Below 640px the labels would overlap: the timeline scrolls instead. -->
      <div class="timeline-scroll">
        <div
          class="timeline"
          role="img"
          :aria-label="`Frise des buts de 0 à 120 minutes : ${match.teamA} au-dessus, ${match.teamB} en dessous`"
        >
          <div class="axis" />
          <div
            class="tick"
            style="left: 37.5%"
          />
          <div
            class="tick"
            style="left: 75%"
          />
          <span
            class="minute"
            style="left: 0"
          >0'</span>
          <span
            class="minute centred"
            style="left: 37.5%"
          >45'</span>
          <span
            class="minute centred"
            style="left: 75%"
          >90'</span>
          <span
            class="minute"
            style="right: 0"
          >120'</span>
          <div
            v-for="g in goals"
            :key="g.label"
            class="goal"
            :style="{ left: `${g.left}%`, top: `${g.top}px` }"
          >
            <span
              class="dot goal-dot"
              :style="{ background: teamColor(g.side) }"
            />
            <span class="goal-label">{{ g.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <div class="columns">
      <section class="card panel stats-panel">
        <h2>Statistiques du match</h2>
        <div
          v-for="s in stats"
          :key="s.label"
          class="stat"
        >
          <div class="stat-head">
            <span class="mono">{{ s.labelA }}</span>
            <span class="stat-label">{{ s.label }}</span>
            <span class="mono">{{ s.labelB }}</span>
          </div>
          <div class="stat-bar">
            <div
              class="stat-a"
              :style="{ width: `${s.shareA}%` }"
            />
            <div class="stat-b" />
          </div>
        </div>
      </section>

      <section class="card panel players-panel">
        <h2>Joueurs du match</h2>
        <ul class="players">
          <li
            v-for="p in match.players"
            :key="p.name"
          >
            <RouterLink
              to="/joueur"
              class="player"
            >
              <span
                class="dot player-dot"
                :style="{ background: teamColor(p.side) }"
              />
              <span class="player-name">{{ p.name }}</span>
              <span class="mono muted player-line">{{ p.line }}</span>
            </RouterLink>
          </li>
        </ul>
        <RouterLink
          to="/comparer"
          class="compare-link"
        >Comparer Messi et Mbappé →</RouterLink>
      </section>
    </div>

    <p class="note">
      Score, buteurs et minutes réels. Statistiques et xG illustratifs dans cette maquette :
      remplacés par les tables gold du pipeline.
    </p>
  </main>
</template>

<style scoped>
.small {
  font-size: 14px;
}

.scoreboard {
  padding: 36px 28px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  text-align: center;
}

.score-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 32px;
}

.team {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 160px;
}

.team-dot {
  width: 14px;
  height: 14px;
}

.team-name {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 600;
}

.score {
  font-family: var(--font-display);
  font-size: 72px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.outcome {
  padding: 6px 14px;
  border-radius: 999px;
  background: var(--surface-2);
  font-size: 14px;
  color: var(--text-2);
}

.panel {
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

.timeline-scroll {
  overflow-x: auto;
}

.timeline {
  position: relative;
  height: 200px;
  min-width: 640px;
}

.timeline > * {
  position: absolute;
}

.axis {
  left: 0;
  right: 0;
  top: 80px;
  height: 2px;
  background: var(--border-strong);
}

.tick {
  top: 70px;
  width: 2px;
  height: 22px;
  background: var(--border-strong);
}

.minute {
  top: 180px;
  font-size: 12px;
  color: var(--muted);
}

.minute.centred {
  margin-left: -10px;
}

.goal {
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.goal-dot {
  width: 14px;
  height: 14px;
}

.goal-label {
  font-size: 12px;
  white-space: nowrap;
}

.columns {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.stats-panel {
  flex: 1 1 520px;
  gap: 18px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-head {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.stat-label {
  color: var(--text-2);
}

.stat-bar {
  display: flex;
  height: 8px;
  gap: 3px;
}

.stat-a {
  background: var(--team-a);
  border-radius: 999px 0 0 999px;
}

.stat-b {
  flex: 1 1 auto;
  background: var(--team-b);
  border-radius: 0 999px 999px 0;
}

.players-panel {
  flex: 1 1 340px;
  gap: 16px;
}

.players {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.player {
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 52px;
  padding: 6px 10px;
  border-radius: 10px;
  text-decoration: none;
  color: var(--text);
}

.player:hover {
  background: var(--surface-2);
  color: var(--text);
}

.player-dot {
  width: 10px;
  height: 10px;
}

.player-name {
  flex: 1 1 auto;
  font-weight: 500;
}

.player-line {
  font-size: 13px;
}

.compare-link {
  font-size: 15px;
  font-weight: 600;
}

/* Phones: smaller score so both teams fit. */
@media (max-width: 600px) {
  .score {
    font-size: 56px;
  }

  .team {
    min-width: 0;
  }
}
</style>

// Demonstration data for the screens, taken from the design mock-ups.
//
// The score, scorers and minutes of the 2022 World Cup final are real; every
// other figure is ILLUSTRATIVE. These objects will be replaced by responses
// from the API (gold tables built by dbt in DuckDB) once the pipeline exists.

export interface Competition {
  tag: string;
  name: string;
  period: string;
}

export interface PipelineStep {
  n: string;
  title: string;
  text: string;
}

export const competitions: Competition[] = [
  { tag: "Sélections", name: "Coupe du monde 2022", period: "Qatar · 64 matchs" },
  { tag: "Sélections", name: "Euro 2024", period: "Allemagne" },
  { tag: "Club", name: "La Liga", period: "Saisons de l’ère Messi" },
  { tag: "Féminin", name: "Coupe du monde féminine 2023", period: "Australie et Nouvelle-Zélande" },
];

export const pipelineSteps: PipelineStep[] = [
  { n: "01 · Extract", title: "Ingestion", text: "Airflow récupère les JSON bruts, de façon incrémentale." },
  { n: "02 · Bronze", title: "Stockage brut", text: "Fichiers conservés tels quels dans Cloudflare R2." },
  { n: "03 · Silver", title: "Parquet", text: "Événements typés, partitionnés par compétition et saison." },
  { n: "04 · Gold", title: "dbt + DuckDB", text: "Modèles testés : stats joueurs, matchs, features xG." },
  { n: "05 · Serve", title: "API FastAPI", text: "Les écrans de cette application." },
];

// ---- Player page --------------------------------------------------------

export interface Kpi {
  label: string;
  value: string;
  sub: string;
}

export interface Percentile {
  label: string;
  value: number; // per 90 minutes
  pct: number; // percentile, 0-100
}

/** A shot on a half pitch, goal at the top. x, y in % of the pitch. */
export interface Shot {
  x: number;
  y: number;
  xg: number;
  goal: boolean;
}

export interface PlayerMatch {
  name: string;
  phase: string;
  minutes: number;
  goals: number;
  xg: number;
  keyPasses: number;
}

export const player = {
  name: "Lionel Messi",
  initials: "LM",
  subtitle: "Argentine · Attaquant · Coupe du monde 2022",
  scopes: ["Coupe du monde 2022", "La Liga 2020/21", "Toutes compétitions"],
  kpis: [
    { label: "Matchs", value: "7", sub: "690 minutes jouées" },
    { label: "Buts", value: "7", sub: "dont 4 penalties" },
    { label: "xG (modèle maison)", value: "5,9", sub: "xG StatsBomb : 6,1" },
    { label: "Passes clés", value: "21", sub: "2,7 par 90 min" },
    { label: "Dribbles réussis", value: "15", sub: "56 % de réussite" },
  ] satisfies Kpi[],
  percentiles: [
    { label: "Buts hors penalty", value: 0.39, pct: 88 },
    { label: "npxG", value: 0.31, pct: 81 },
    { label: "Tirs", value: 3.4, pct: 92 },
    { label: "Passes clés", value: 2.7, pct: 97 },
    { label: "Passes progressives", value: 6.1, pct: 95 },
    { label: "Dribbles réussis", value: 1.9, pct: 84 },
    { label: "Pressions", value: 6.0, pct: 18 },
  ] satisfies Percentile[],
  shots: (
    [
      [50, 13, 0.78, 1], [46, 12, 0.76, 1], [55, 22, 0.32, 1], [38, 26, 0.12, 0],
      [62, 30, 0.09, 0], [30, 34, 0.06, 0], [52, 18, 0.21, 1], [70, 24, 0.07, 0],
      [44, 40, 0.04, 0], [58, 36, 0.05, 0], [48, 28, 0.15, 0], [35, 20, 0.11, 0],
      [66, 16, 0.18, 0], [50, 45, 0.03, 0], [42, 31, 0.08, 1],
    ] as const
  ).map(([x, y, xg, goal]): Shot => ({ x, y, xg, goal: goal === 1 })),
  matches: [
    { name: "Argentine – Arabie saoudite", phase: "Groupe C", minutes: 90, goals: 1, xg: 0.9, keyPasses: 2 },
    { name: "Argentine – Mexique", phase: "Groupe C", minutes: 90, goals: 1, xg: 0.4, keyPasses: 3 },
    { name: "Argentine – Croatie", phase: "Demi-finale", minutes: 90, goals: 1, xg: 1.0, keyPasses: 4 },
    { name: "Argentine – France", phase: "Finale", minutes: 120, goals: 2, xg: 1.4, keyPasses: 3 },
  ] satisfies PlayerMatch[],
};

// ---- Comparison page ----------------------------------------------------

export interface ComparedMetric {
  label: string;
  per90: [number, number]; // [player A, player B]
  total: [number, number];
}

export const comparison = {
  competition: "Coupe du monde 2022",
  a: { name: "Lionel Messi", short: "Messi", info: "Argentine · Attaquant · 690 min" },
  b: { name: "Kylian Mbappé", short: "Mbappé", info: "France · Attaquant · 598 min" },
  metrics: [
    { label: "Buts", per90: [0.91, 1.2], total: [7, 8] },
    { label: "Buts hors pen.", per90: [0.39, 0.9], total: [3, 6] },
    { label: "xG", per90: [0.77, 0.95], total: [5.9, 6.3] },
    { label: "Tirs", per90: [3.4, 4.2], total: [26, 28] },
    { label: "Passes clés", per90: [2.7, 1.5], total: [21, 10] },
    { label: "Dribbles réussis", per90: [1.9, 2.4], total: [15, 16] },
    { label: "Pressions", per90: [6.0, 8.3], total: [46, 55] },
  ] satisfies ComparedMetric[],
  strengths: {
    a: "Création : plus de passes clés et de passes progressives, rôle de meneur autant que de finisseur.",
    b: "Finition : plus de buts hors penalty et un volume de tirs supérieur par 90 minutes.",
  },
};

// ---- Match page ---------------------------------------------------------

export type Side = "a" | "b"; // a = first-named team, b = second

export interface Goal {
  minute: number;
  side: Side;
  label: string;
}

export interface MatchStat {
  label: string;
  a: number;
  b: number;
  unit?: string; // e.g. " %" for possession
}

export const match = {
  breadcrumb: ["Coupe du monde 2022", "Finale"],
  context: "Finale · 18 décembre 2022 · Stade de Lusail",
  teamA: "Argentine",
  teamB: "France",
  score: [3, 3] as [number, number],
  outcome: "Après prolongation · Argentine victorieuse aux tirs au but (4–2)",
  duration: 120, // minutes, extra time included
  goals: [
    { minute: 23, side: "a", label: "Messi (pen.) 23′" },
    { minute: 36, side: "a", label: "Di María 36′" },
    { minute: 80, side: "b", label: "Mbappé (pen.) 80′" },
    { minute: 81, side: "b", label: "Mbappé 81′" },
    { minute: 108, side: "a", label: "Messi 108′" },
    { minute: 118, side: "b", label: "Mbappé (pen.) 118′" },
  ] satisfies Goal[],
  stats: [
    { label: "Possession", a: 54, b: 46, unit: " %" },
    { label: "xG (modèle maison)", a: 3.1, b: 2.4 },
    { label: "Tirs", a: 20, b: 10 },
    { label: "Tirs cadrés", a: 10, b: 5 },
    { label: "Passes réussies", a: 590, b: 420 },
    { label: "Pressions", a: 140, b: 160 },
  ] satisfies MatchStat[],
  players: [
    { name: "Lionel Messi", line: "2 buts · xG 1,4", side: "a" },
    { name: "Kylian Mbappé", line: "3 buts · xG 1,6", side: "b" },
    { name: "Ángel Di María", line: "1 but · xG 0,4", side: "a" },
    { name: "Emiliano Martínez", line: "Gardien", side: "a" },
  ] satisfies { name: string; line: string; side: Side }[],
};

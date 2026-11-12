# Décisions d'architecture (ADR)

Chaque décision structurante est consignée ici, avec son contexte, pour qu'on puisse comprendre plus tard *pourquoi* le projet est ainsi fait. Une décision n'est jamais effacée : si elle change, on en rédige une nouvelle qui la remplace.

---

## ADR 001 — Cloudflare R2 plutôt que MinIO

- **Statut** : acceptée
- **Date** : 2026-11-12

### Contexte

Les couches bronze (JSON) et silver (Parquet) ont besoin d'un stockage objet compatible S3 : DuckDB, boto3 et l'écosystème de données savent tous lire et écrire en S3, et le projet doit pouvoir tourner sur un petit VPS.

### Option écartée : MinIO auto-hébergé

MinIO était le choix habituel pour un S3 auto-hébergé. Son édition communautaire est passée en mode maintenance fin 2025 et n'est plus distribuée en images Docker officielles. Le dépôt a ensuite été archivé. Bâtir un projet neuf dessus, c'était dépendre d'un logiciel qui ne reçoit plus de correctifs.

### Décision

Utiliser **Cloudflare R2** en production :

- l'offre gratuite suffit pour le volume de StatsBomb Open Data ;
- pas de frais de sortie (egress), contrairement à S3 ;
- API compatible S3, lisible directement par DuckDB (`r2://`).

Le code passe par une **abstraction de stockage** (`dfoot_core.storage`) avec deux implémentations : `local` (système de fichiers) et `r2`. On peut ainsi développer, tester et faire tourner la CI sans compte Cloudflare (`STORAGE_BACKEND=local`).

### Conséquences

- **Dépendance à un service externe** : une panne ou un changement d'offre de Cloudflare touche la production. Les données bronze restent reconstructibles depuis StatsBomb.
- Le code ne dépend que de l'interface de `dfoot_core.storage`. Changer de fournisseur (S3, autre service compatible) revient à écrire une nouvelle implémentation, sans toucher à l'ingestion ni aux transformations.
- Les secrets R2 n'existent qu'en production, dans `.env`. Aucun test ne les utilise.

---

## Gabarit pour les prochaines décisions

```markdown
## ADR NNN — Titre court, sous forme de choix

- **Statut** : proposée | acceptée | remplacée par ADR NNN
- **Date** : AAAA-MM-JJ

### Contexte

Le problème à résoudre et les contraintes.

### Options considérées

- Option A : avantages, inconvénients.
- Option B : avantages, inconvénients.

### Décision

Ce qui est retenu, et pourquoi.

### Conséquences

Ce que la décision implique, en bien comme en mal.
```

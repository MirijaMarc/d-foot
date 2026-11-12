# D-Foot — football analytics

D-Foot ingère les données ouvertes de StatsBomb, les transforme en couches bronze / silver / gold, entraîne un modèle d'expected goals (xG) et expose le résultat via une API et une application web.

- [Architecture](docs/architecture.md) : couches de données, composants, réseau
- [Déploiement](docs/deploiement.md) : Cloudflare R2, les deux modes nginx, Certbot
- [Décisions d'architecture](docs/decisions.md) : ADR

**Stack** : Python 3.12 (uv), Airflow, Cloudflare R2, Parquet, DuckDB, dbt, FastAPI, scikit-learn / LightGBM / MLflow, Vue 3 + Vite + TypeScript (pnpm), Docker Compose, nginx.

## Organisation du dépôt

```
packages/    code Python : dfoot-core, dfoot-ingestion, dfoot-ml, dfoot-api (workspace uv)
transform/   projet dbt (gold, DuckDB)
dags/        DAG Airflow
web/         application Vue
infra/       Docker Compose, template nginx, .env.example
docs/        documentation
benchmarks/  mesures de performance
data/        stockage local en développement (ignoré par git)
```

## Lancer en local

Aucun compte Cloudflare n'est nécessaire : avec `STORAGE_BACKEND=local` (la valeur par défaut), les données sont stockées dans `data/`.

Prérequis : [uv](https://docs.astral.sh/uv/), [pnpm](https://pnpm.io/) avec Node 24, Docker.

```bash
cp infra/.env.example .env      # puis remplir POSTGRES_PASSWORD et les clés Airflow
uv sync                         # environnement Python (.venv) depuis uv.lock
(cd web && pnpm install)        # dépendances du front
docker compose -f infra/docker-compose.yml --env-file .env up -d --build
```

- API : http://127.0.0.1:8000/health
- Web : http://127.0.0.1:8080

Vérifications de qualité :

```bash
uv run pre-commit install       # une fois : hooks exécutés à chaque commit
uv run pytest
uv run ruff check . && uv run mypy packages
(cd transform && uv run dbt parse)
```

## Données

Ce projet utilise les données de **[StatsBomb Open Data](https://github.com/statsbomb/open-data)**. Merci à StatsBomb (Hudl) de les mettre à disposition.

Ces données sont soumises à leurs propres conditions d'utilisation, indépendantes de la licence de ce dépôt : toute utilisation doit citer StatsBomb comme source. Aucune donnée StatsBomb n'est stockée dans ce dépôt : elles sont téléchargées à l'exécution.

## Feuille de route

- [ ] **Fondations** : structure du dépôt, outillage, abstraction de stockage, CI
- [ ] **Pipeline orchestré** : ingestion bronze → silver, modèles dbt gold, DAG Airflow
- [ ] **Produit en ligne** : API, application web, déploiement HTTPS
- [ ] **Différenciation** : modèle xG enrichi par les données 360, benchmark

## Licence

Code sous licence [MIT](LICENSE). Les données StatsBomb suivent leurs propres conditions (voir ci-dessus).

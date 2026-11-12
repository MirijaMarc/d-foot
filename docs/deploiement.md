# Déploiement

Le déploiement cible un VPS avec Docker. Toutes les commandes sont lancées depuis la racine du dépôt, cloné sur le serveur.

Raccourci utilisé ci-dessous :

```bash
alias dc='docker compose -f infra/docker-compose.yml --env-file .env'
```

## 1. Préparer Cloudflare R2

### Créer le bucket

Dans le tableau de bord Cloudflare : **R2 Object Storage → Create bucket**. Donne-lui un nom (par exemple `dfoot`) et laisse l'emplacement sur *Automatic*. Le bucket reste **privé** : n'active ni l'accès public ni de domaine personnalisé.

### Créer un jeton d'accès limité

**R2 Object Storage → Manage API tokens → Create API token** :

- **Permissions** : *Object Read & Write*. Ce jeton n'a pas besoin des droits *Admin*, qui permettent de créer ou supprimer des buckets.
- **Specify bucket(s)** : *Apply to specific buckets only* → uniquement le bucket D-Foot.
- **TTL** : selon ta politique de rotation.

Cloudflare affiche alors l'**Access Key ID** et le **Secret Access Key**, ce dernier **une seule fois**. L'**Account ID** apparaît sur la page d'accueil de R2.

Si le jeton fuit, il ne donne accès qu'à ce bucket, en lecture/écriture d'objets.

### Renseigner `.env`

```bash
cp infra/.env.example .env
chmod 600 .env
```

```dotenv
STORAGE_BACKEND=r2
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET=dfoot
```

Remplis aussi `POSTGRES_PASSWORD`, `AIRFLOW__CORE__FERNET_KEY`, `AIRFLOW__API_AUTH__JWT_SECRET` (les commandes de génération sont dans `.env.example`), `DFOOT_DOMAIN` et `LETSENCRYPT_EMAIL`.

Le DNS du domaine (enregistrement A/AAAA) doit pointer vers le VPS avant de demander un certificat.

## 2. Choisir le mode nginx

| | Mode 1 : nginx en conteneur | Mode 2 : nginx de l'hôte |
|---|---|---|
| Quand | VPS dédié à D-Foot | nginx déjà installé (autres sites) |
| Démarrage | `dc --profile proxy up -d` | `dc up -d` |
| Configuration | rendue automatiquement depuis le template | template rendu à la main dans le nginx de l'hôte |
| Certificats | service `certbot` du profil `proxy` | Certbot de l'hôte |

Dans les deux cas, `api` et `web` n'écoutent que sur `127.0.0.1`. C'est important car Docker contourne les règles de pare-feu de type `ufw` pour les ports qu'il publie.

### Mode 1 : nginx en conteneur

**Premier certificat.** nginx ne peut pas démarrer sans certificat, donc on obtient le premier avec le serveur web intégré de Certbot (mode *standalone*), avant de lancer nginx :

```bash
set -a; . ./.env; set +a     # charge DFOOT_DOMAIN et LETSENCRYPT_EMAIL dans le shell
dc --profile proxy run --rm -p 80:80 --entrypoint certbot certbot \
  certonly --standalone -d "$DFOOT_DOMAIN" \
  --email "$LETSENCRYPT_EMAIL" --agree-tos --no-eff-email
```

**Démarrage :**

```bash
dc --profile proxy up -d --build
```

**Renouvellement** : automatique. Le service `certbot` lance `certbot renew --webroot` toutes les 12 h, via le challenge HTTP servi par nginx sur `/.well-known/acme-challenge/`. nginx se recharge lui aussi toutes les 12 h pour prendre en compte les nouveaux certificats.

Test du renouvellement à blanc :

```bash
dc --profile proxy exec certbot certbot renew --webroot -w /var/www/certbot --dry-run
```

### Mode 2 : nginx déjà installé sur le VPS

**Démarrage des services**, sans le profil `proxy` (ni nginx ni certbot dans Docker) :

```bash
dc up -d --build
```

**Premier certificat**, avec le plugin nginx de Certbot. Il ajoute temporairement le challenge, sans modifier durablement la configuration :

```bash
sudo certbot certonly --nginx -d dfoot.example.org \
  --deploy-hook "systemctl reload nginx"
```

Le renouvellement est géré par le timer systemd installé avec Certbot. Le *deploy hook* recharge nginx après chaque renouvellement.

**Configuration nginx.** On rend le template avec les valeurs de l'hôte. Les upstreams sont les ports publiés sur `127.0.0.1` (`API_PORT`, `WEB_PORT` du `.env`). La liste explicite de variables passée à `envsubst` évite d'effacer les variables propres à nginx comme `$host` :

```bash
set -a; . ./.env; set +a
export API_UPSTREAM="127.0.0.1:${API_PORT}" WEB_UPSTREAM="127.0.0.1:${WEB_PORT}"
envsubst '${DFOOT_DOMAIN} ${API_UPSTREAM} ${WEB_UPSTREAM}' \
  < infra/nginx/d-foot.conf.template | sudo tee /etc/nginx/sites-available/d-foot.conf
sudo ln -s /etc/nginx/sites-available/d-foot.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

À adapter selon l'hôte :

- nginx < 1.25.1 ne connaît pas `http2 on;` : supprime la ligne et écris `listen 443 ssl http2;`.
- Si le fichier `access.log` est partagé avec d'autres sites, choisis un fichier dédié (`/var/log/nginx/d-foot.access.log`).
- Le bloc `/.well-known/acme-challenge/` pointe sur `/var/www/certbot`. Il ne sert qu'avec `certbot --webroot` : tu peux le garder ou le retirer.

## 3. Accéder aux consoles (Airflow, MLflow)

Postgres, Airflow et MLflow ne publient aucun port, même sur `127.0.0.1`. On y accède par un tunnel SSH vers l'IP du conteneur dans le réseau Docker :

```bash
# Sur le VPS : IP des conteneurs
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dfoot-airflow-1 dfoot-mlflow-1

# Sur ton poste : tunnels (remplace les IP)
ssh -N -L 8081:<ip-airflow>:8080 -L 5001:<ip-mlflow>:5000 utilisateur@vps
```

Ensuite, ouvre `http://localhost:8081` pour Airflow et `http://localhost:5001` pour MLflow.

Au premier démarrage, Airflow (mode *standalone*) génère le mot de passe de l'utilisateur `admin` et l'écrit dans ses logs :

```bash
dc logs airflow | grep -i password
```

## 4. Vérifications

```bash
dc ps                                        # tous les services "Up"
curl -fsS https://dfoot.example.org/api/health   # {"status":"ok"}
```

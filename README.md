# Site BDE (Django)

Application Django du BDE, avec :
- front public (`showcase`)
- espace membres (`members`)
- administration Django (URL configurable)
- authentification OIDC (`mozilla-django-oidc`)
- base de données MySQL/MariaDB

## Stack technique

- Python 3.12
- Django 5.2
- MySQL/MariaDB (`mysqlclient`)
- Gunicorn
- Docker + Docker Compose

## Prérequis

### Pour un lancement local (sans Docker)

- Python 3.12+
- MySQL ou MariaDB en local
- Outils de compilation (Linux) : `build-essential`, `pkg-config`, `default-libmysqlclient-dev`

### Pour un lancement Docker

- Docker
- Docker Compose (plugin `docker compose`)
- Une base MySQL/MariaDB accessible depuis le conteneur web

> Important : le `docker-compose.yaml` actuel **ne démarre que le service web**.
> La base est attendue sur l'hôte via `host.docker.internal:3306`.

## Configuration `.env`

Copier l'exemple :

```bash
cp .env.example .env
```

Variables principales :

```dotenv
DEBUG=True
DEV_MODE=True

SECRET_KEY=change-me
ADMIN_URL=admin/

ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False

DB_NAME=bde
DB_USER=bdeuser
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306

# OIDC (optionnel en local selon votre besoin)
OIDC_OP_AUTHORIZATION_ENDPOINT=
OIDC_OP_TOKEN_ENDPOINT=
OIDC_OP_USER_ENDPOINT=
OIDC_OP_JWKS_ENDPOINT=
OIDC_RP_CLIENT_ID=
OIDC_RP_CLIENT_SECRET=
OIDC_RP_SIGN_ALGO=RS256
OIDC_RP_SCOPES=openid email profile
```

## Démarrage en local (sans Docker)

### 1) Créer l'environnement Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Créer la base MySQL

```sql
CREATE DATABASE bde CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bdeuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON bde.* TO 'bdeuser'@'localhost';
FLUSH PRIVILEGES;
```

### 3) Initialiser Django

```bash
python manage.py migrate
python -m bde.generate_robots
python manage.py createsuperuser
python manage.py runserver
```

Application disponible sur `http://127.0.0.1:8000`.

## Démarrage avec Docker Compose

### 1) Préparer `.env`

Pour la stack Docker actuelle, la base doit être joignable depuis le conteneur sur l'hôte :

```dotenv
DB_HOST=host.docker.internal
DB_PORT=3306
```

### 2) Lancer

```bash
docker compose up --build
```

Le conteneur exécute automatiquement :
- `python manage.py migrate`
- `python -m bde.generate_robots`
- `gunicorn bde.wsgi:application --bind 0.0.0.0:8000`

### 3) Arrêter

```bash
docker compose down
```

## Démarrage avec `docker run` (manuel)

```bash
docker build -t bde-app:0.1 .
docker run -p 8000:8000 --env-file .env --add-host=host.docker.internal:host-gateway bde-app:0.1
```

## Commandes utiles

```bash
# tests
python manage.py test

# lint/type-check
pylint bde members showcase auth utils
mypy .

# logs Docker
docker compose logs -f web
```

## Arborescence principale

- `bde/` : configuration Django (settings, urls, env)
- `showcase/` : pages publiques
- `members/` : pages et données membres
- `auth/` : backend OIDC personnalisé
- `templates/`, `static/`, `uploads/` : assets et médias

## Notes de fonctionnement

- `ADMIN_URL` est configurable via `.env` (ex: `admin/`, `secret-admin/`).
- Le fichier `robots.txt` est généré automatiquement au démarrage (`bde.generate_robots`).
- En `DEBUG=True`, les médias (`/uploads/`) sont servis par Django.
**« Ajoute aussi les commandes pour tester, lancer le projet, démarrer Docker, et tout le nécessaire. »**

Oui. Pour un README vraiment utilisable, ajoute une section **Installation & Commandes** avec tout le workflow : installation, `.env`, Docker, Airflow, tests, PostgreSQL et arrêt.

Tu peux remplacer les sections correspondantes de ton README par celles-ci :

````markdown
# YouTube Data Pipeline

Pipeline ETL/ELT permettant d'extraire les données d'une chaîne YouTube via la **YouTube Data API v3**, de les sauvegarder en JSON, de les charger dans PostgreSQL, puis de les transformer et synchroniser dans un Data Warehouse organisé en couches **Staging / Core**.

Le pipeline est orchestré avec **Apache Airflow** et l'infrastructure est exécutée avec **Docker Compose**.

---

## 1. Objectif du projet

Le projet permet de :

- récupérer les informations d'une chaîne YouTube ;
- récupérer les vidéos de la chaîne ;
- gérer la pagination de l'API ;
- récupérer les détails des vidéos ;
- sauvegarder les données brutes au format JSON ;
- charger les données dans PostgreSQL ;
- utiliser une couche Staging ;
- nettoyer et transformer les données ;
- alimenter la couche Core ;
- synchroniser les données avec INSERT / UPDATE / DELETE ;
- orchestrer le pipeline avec Apache Airflow ;
- exécuter l'infrastructure avec Docker ;
- analyser les données avec Power BI.

---

# 2. Architecture

```text
                         YouTube Data API
                                |
                                v
                    +-----------------------+
                    |      Extraction       |
                    |                       |
                    | Channel              |
                    | Playlist             |
                    | Video IDs            |
                    | Video Details        |
                    | Pagination            |
                    +-----------+-----------+
                                |
                                v
                       +----------------+
                       |    RAW JSON    |
                       |                |
                       | YT_data_*.json |
                       +-------+--------+
                               |
                               v
                    +-----------------------+
                    |      PostgreSQL       |
                    |                       |
                    |       STAGING         |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    |    Transformation     |
                    |                       |
                    | Duration              |
                    | Types                 |
                    | Null values           |
                    | Duplicates            |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    |         CORE          |
                    |                       |
                    | Clean analytical data |
                    +-----------+-----------+
                                |
                                v
                         +-------------+
                         |  Power BI   |
                         +-------------+

                       Apache Airflow
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
          Extraction DAG          Warehouse DAG
````

---

# 3. Technologies

| Technologie          | Utilisation               |
| -------------------- | ------------------------- |
| Python 3.12          | Développement             |
| YouTube Data API v3  | Extraction                |
| Requests             | Appels HTTP               |
| Pandas               | Transformation            |
| PostgreSQL 13        | Data Warehouse            |
| Apache Airflow 2.9.2 | Orchestration             |
| Redis                | Celery Broker             |
| Docker               | Conteneurisation          |
| Docker Compose       | Gestion des services      |
| Pytest               | Tests                     |
| Power BI             | Visualisation             |
| python-dotenv        | Variables d'environnement |

---

# 4. Structure du projet

```text
youtube-data-pipeline/
│
├── extraction/
│   ├── __init__.py
│   ├── extraction.py
│   ├── channel.py
│   ├── videos.py
│   └── content.py
│
├── transformation/
│   ├── __init__.py
│   └── cleaning.py
│
├── loading/
│   ├── __init__.py
│   ├── connexion.py
│   └── postgres.py
│
├── dags/
│   ├── extraction_dag.py
│   └── warehouse_dag.py
│
├── data/
│   └── YT_data_YYYY-MM-DD.json
│
├── tests/
│   ├── test_extraction.py
│   ├── test_transformation.py
│   ├── test_loading.py
│   └── test_dags.py
│
├── docker/
│   └── postgres/
│       └── init-multiple-databases.sh
│
├── config/
├── include/
├── logs/
│
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 5. Prérequis

Avant de lancer le projet, installer :

* Docker Desktop
* Git
* Python 3.12
* une clé YouTube Data API v3

Vérifier les installations :

```bash
python --version
```

```bash
docker --version
```

```bash
docker compose version
```

```bash
git --version
```

---

# 6. Installation du projet

Cloner le repository :

```bash
git clone <repository-url>
```

Entrer dans le projet :

```bash
cd youtube-data-pipeline
```

---

# 7. Environnement Python

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement sous Windows :

```powershell
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Vérifier Pytest :

```bash
pytest --version
```

---

# 8. Configuration du fichier .env

Créer un fichier :

```text
.env
```

Exemple :

```env
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY

CHANNEL_HANDLE=@mim-repository

ELT_DATABASE_NAME=youtube_db
ELT_DATABASE_USERNAME=youtube
ELT_DATABASE_PASSWORD=youtube

POSTGRES_CONN_HOST=postgres
POSTGRES_CONN_PORT=5432
POSTGRES_CONN_USERNAME=postgres
POSTGRES_CONN_PASSWORD=postgres

METADATA_DATABASE_NAME=postgres
METADATA_DATABASE_USERNAME=postgres
METADATA_DATABASE_PASSWORD=postgres

AIRFLOW_WWW_USER_USERNAME=admin
AIRFLOW_WWW_USER_PASSWORD=admin

AIRFLOW_UID=50000

FERNET_KEY=YOUR_FERNET_KEY
```

**Ne jamais publier le fichier `.env` sur GitHub.**

---

# 9. Lancer Docker

Construire les images :

```bash
docker compose build
```

Démarrer tous les services :

```bash
docker compose up -d
```

Vérifier les conteneurs :

```bash
docker compose ps
```

Voir les logs :

```bash
docker compose logs
```

Voir les logs d'un service spécifique :

```bash
docker compose logs airflow-webserver
```

```bash
docker compose logs airflow-scheduler
```

```bash
docker compose logs airflow-worker
```

```bash
docker compose logs postgres
```

Suivre les logs en temps réel :

```bash
docker compose logs -f airflow-worker
```

---

# 10. Services Docker

Le projet utilise les services suivants :

```text
PostgreSQL
Redis
Airflow Webserver
Airflow Scheduler
Airflow Worker
Airflow Init
```

Vérifier leur état :

```bash
docker compose ps
```

---

# 11. Airflow

Lancer les services :

```bash
docker compose up -d
```

Accéder à Airflow :

```text
http://localhost:8080
```

Identifiants :

```text
Username: admin
Password: admin
```

> Les identifiants réels dépendent des valeurs configurées dans `.env`.

---

# 12. Vérifier Airflow

Lister les DAGs :

```bash
docker compose exec airflow-webserver airflow dags list
```

Vérifier les erreurs d'import :

```bash
docker compose exec airflow-webserver airflow dags list-import-errors
```

Vérifier la base de données Airflow :

```bash
docker compose exec airflow-worker airflow db check
```

Dépauser le DAG :

```bash
docker compose exec airflow-webserver airflow dags unpause youtube_extraction
```

```bash
docker compose exec airflow-webserver airflow dags unpause youtube_warehouse
```

Déclencher manuellement le DAG d'extraction :

```bash
docker compose exec airflow-webserver airflow dags trigger youtube_extraction
```

Déclencher le DAG Data Warehouse :

```bash
docker compose exec airflow-webserver airflow dags trigger youtube_warehouse
```

Les DAGs peuvent également être lancés directement depuis l'interface Airflow.

---

# 13. Pipeline Airflow

## DAG 1 — Extraction

```text
youtube_extraction
        |
        v
YouTube API
        |
        v
Extraction
        |
        v
Raw JSON
```

## DAG 2 — Data Warehouse

```text
youtube_warehouse
        |
        v
load_staging
        |
        v
Staging PostgreSQL
        |
        v
load_core
        |
        v
Transformation
        |
        v
Core PostgreSQL
```

---

# 14. Exécution du projet avec Python

Pour tester l'extraction directement depuis Python :

```bash
python -m main
```

Si tu veux exécuter un module spécifique :

```bash
python -m transformation.cleaning
```

Pour tester le chargement PostgreSQL :

```bash
python -m loading.postgres
```

> Les modules doivent être exécutés depuis la racine du projet.

---

# 15. Tests

Le projet utilise **Pytest**.

## Lancer tous les tests

```bash
pytest -v
```

---

## Tester uniquement l'extraction

```bash
pytest tests/test_extraction.py -v
```

---

## Tester les transformations

```bash
pytest tests/test_transformation.py -v
```

---

## Tester PostgreSQL / Loading

```bash
pytest tests/test_loading.py -v
```

---

## Tester les DAGs

```bash
pytest tests/test_dags.py -v
```

---

## Arrêter après la première erreur

```bash
pytest -x -v
```

---

## Afficher les tests détaillés

```bash
pytest -vv
```

---

# 16. Vérification du JSON

Après l'extraction, vérifier le contenu du dossier :

```text
data/
```

Exemple :

```text
data/
└── YT_data_2026-09-17.json
```

Le JSON doit contenir les informations suivantes :

```json
{
    "videoId": "...",
    "title": "...",
    "publishedAt": "...",
    "duration": "...",
    "viewCount": 0,
    "likeCount": 0,
    "commentCount": 0
}
```

---

# 17. PostgreSQL

Entrer dans PostgreSQL :

```bash
docker compose exec postgres psql -U postgres
```

Se connecter à la base du Data Warehouse :

```sql
\c youtube_db
```

Lister les schémas :

```sql
\dn
```

Lister les tables :

```sql
\dt staging.*
```

```sql
\dt core.*
```

---

# 18. Vérifier les données Staging

Compter les vidéos :

```sql
SELECT COUNT(*)
FROM staging.videos;
```

Afficher les données :

```sql
SELECT *
FROM staging.videos
LIMIT 10;
```

---

# 19. Vérifier les données Core

Compter les vidéos :

```sql
SELECT COUNT(*)
FROM core.videos;
```

Afficher les données :

```sql
SELECT *
FROM core.videos
LIMIT 10;
```

---

# 20. Vérifier les doublons

Dans Staging :

```sql
SELECT video_id, COUNT(*)
FROM staging.videos
GROUP BY video_id
HAVING COUNT(*) > 1;
```

Dans Core :

```sql
SELECT video_id, COUNT(*)
FROM core.videos
GROUP BY video_id
HAVING COUNT(*) > 1;
```

Une requête sans résultat signifie qu'aucun doublon n'a été trouvé.

---

# 21. Vérifier la synchronisation

Vérifier le nombre de vidéos :

```sql
SELECT COUNT(*)
FROM staging.videos;
```

```sql
SELECT COUNT(*)
FROM core.videos;
```

Les deux couches doivent normalement contenir le même ensemble de vidéos après une exécution complète du pipeline.

---

# 22. Nettoyer les données

Pour supprimer les données Staging :

```sql
DELETE FROM staging.videos;
```

Pour supprimer les données Core :

```sql
DELETE FROM core.videos;
```

Pour supprimer toutes les données :

```sql
TRUNCATE TABLE staging.videos;
```

```sql
TRUNCATE TABLE core.videos;
```

---

# 23. Redémarrer Docker

Redémarrer tous les services :

```bash
docker compose restart
```

Redémarrer uniquement Airflow :

```bash
docker compose restart airflow-webserver airflow-scheduler airflow-worker
```

---

# 24. Arrêter Docker

Arrêter les conteneurs :

```bash
docker compose stop
```

Arrêter et supprimer les conteneurs :

```bash
docker compose down
```

---

# 25. Rebuild complet

Après une modification du `Dockerfile` ou des dépendances :

```bash
docker compose down
```

Puis :

```bash
docker compose build --no-cache
```

Et :

```bash
docker compose up -d
```

Vérifier :

```bash
docker compose ps
```

---

# 26. Nettoyage Docker

Voir les volumes :

```bash
docker volume ls
```

Voir les images :

```bash
docker images
```

Voir les conteneurs :

```bash
docker ps -a
```

> Attention : la suppression des volumes peut supprimer les données PostgreSQL.

Pour supprimer les conteneurs et les volumes du projet :

```bash
docker compose down -v
```

Puis reconstruire :

```bash
docker compose build
```

Et relancer :

```bash
docker compose up -d
```

---

# 27. Git

Vérifier l'état du repository :

```bash
git status
```

Ajouter les fichiers :

```bash
git add .
```

Créer un commit :

```bash
git commit -m "Complete YouTube data pipeline"
```

Envoyer vers GitHub :

```bash
git push origin main
```

Vérifier les fichiers ignorés :

```bash
git status --ignored
```

---

# 28. Fichiers à ne jamais publier

Le fichier `.env` doit être ignoré :

```gitignore
.env
```

Les autres fichiers générés peuvent également être ignorés :

```gitignore
__pycache__/
*.pyc
.venv/
logs/
data/*.json
```

Ne jamais publier :

* YouTube API Key
* Fernet Key
* mots de passe PostgreSQL
* credentials Airflow

---

# 29. Workflow complet

Pour démarrer le projet :

```bash
# 1. Entrer dans le projet
cd youtube-data-pipeline

# 2. Activer l'environnement Python
.venv\Scripts\activate

# 3. Construire les images
docker compose build

# 4. Démarrer Docker
docker compose up -d

# 5. Vérifier les services
docker compose ps

# 6. Vérifier Airflow
docker compose exec airflow-webserver airflow dags list

# 7. Vérifier les erreurs d'import
docker compose exec airflow-webserver airflow dags list-import-errors

# 8. Déclencher l'extraction
docker compose exec airflow-webserver airflow dags trigger youtube_extraction

# 9. Déclencher le Data Warehouse
docker compose exec airflow-webserver airflow dags trigger youtube_warehouse

# 10. Lancer les tests
pytest -v
```

---

# 30. Workflow recommandé

```text
        START
          |
          v
   docker compose up -d
          |
          v
      Check Docker
          |
          v
      Check Airflow
          |
          v
   Trigger Extraction DAG
          |
          v
       YouTube API
          |
          v
        Raw JSON
          |
          v
    Trigger Warehouse DAG
          |
          v
       PostgreSQL
          |
          v
       STAGING
          |
          v
    Transformation
          |
          v
         CORE
          |
          v
       Power BI
          |
          v
        Analysis
```

---

# 31. Power BI

Power BI peut être connecté à PostgreSQL afin d'analyser les données présentes dans :

```text
core.videos
```

Exemples de KPI :

* Nombre total de vidéos
* Nombre total de vues
* Nombre total de likes
* Nombre total de commentaires
* Durée moyenne des vidéos
* Vues par vidéo
* Likes par vidéo
* Commentaires par vidéo
* Évolution des publications

Architecture finale :

```text
YouTube
   ↓
Python
   ↓
Raw JSON
   ↓
Staging
   ↓
Transformation
   ↓
Core
   ↓
PostgreSQL
   ↓
Power BI
```

---

# 32. Résultat final

Le projet fournit un pipeline de données complet :

```text
Extract
   ↓
Store Raw Data
   ↓
Load Staging
   ↓
Transform
   ↓
Load Core
   ↓
Synchronize
   ↓
Analyze
```

L'utilisation de **Docker + PostgreSQL + Airflow + Python** permet de construire une architecture reproductible et automatisable.

---

# 33. Auteur

**Ali Kamal**

Projet réalisé dans le cadre d'un projet Data Engineering / Data Pipeline.

---

# 34. Licence

Projet réalisé à des fins éducatives.

````

## Les commandes essentielles à retenir

Pour ta démo, tu n'as pas besoin de montrer les 50 commandes. Les plus importantes sont celles-ci :

```powershell
# Démarrer
docker compose up -d

# Vérifier
docker compose ps

# Airflow
http://localhost:8080

# Vérifier les DAGs
docker compose exec airflow-webserver airflow dags list

# Vérifier les erreurs
docker compose exec airflow-webserver airflow dags list-import-errors

# Lancer les tests
pytest -v

# PostgreSQL
docker compose exec postgres psql -U postgres

# Arrêter
docker compose down
````

Et pour un **rebuild complet** après modification du `Dockerfile` :

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
docker compose ps
```

**Point important pour ton README :** évite de mettre les vrais mots de passe, la vraie `YOUTUBE_API_KEY` ou la vraie `FERNET_KEY`. Utilise uniquement des placeholders comme `YOUR_YOUTUBE_API_KEY`.

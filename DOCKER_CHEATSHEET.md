# 🐳 Docker Cheatsheet - YouTube Data Pipeline

Ce fichier contient toutes les commandes Docker et Docker Compose dont tu auras besoin pour l'installation, l'exécution et le débogage de ton projet. 
Toutes les commandes doivent être exécutées dans ton terminal depuis le dossier racine du projet (là où se trouve le fichier `docker-compose.yml`).

---

## 🛠️ 1. Installation & Lancement (Run / Installation)

**Construire l'image personnalisée (à faire la première fois ou si tu modifies le `Dockerfile`) :**
```bash
docker build -t youtube-airflow .
```

**Démarrer tout le projet en arrière-plan (Airflow, Postgres, Redis) :**
```bash
docker-compose up -d
```
*(Si ta version de Docker est récente, tu peux utiliser `docker compose up -d` sans le tiret)*

**Démarrer le projet ET forcer la reconstruction de l'image en même temps :**
```bash
docker-compose up -d --build
```

---

## 🛑 2. Arrêt et Nettoyage (Stop / Clean)

**Arrêter les conteneurs sans les supprimer (les données sont conservées) :**
```bash
docker-compose stop
```

**Arrêter et supprimer les conteneurs (les données dans la base de données sont conservées) :**
```bash
docker-compose down
```

**Arrêter le projet, supprimer les conteneurs ET supprimer toutes les données (remise à zéro totale de la base de données) :**
```bash
docker-compose down -v
```

---

## 🔍 3. Débogage & Suivi (Debugging)

**Voir le statut des conteneurs (qui est en ligne, qui a planté) :**
```bash
docker-compose ps
```

**Voir les logs de tous les conteneurs en temps réel (Appuie sur Ctrl+C pour quitter) :**
```bash
docker-compose logs -f
```

**Voir les logs d'un seul service spécifique (très utile pour trouver une erreur) :**
```bash
# Pour Airflow Webserver
docker-compose logs -f airflow-webserver

# Pour Airflow Scheduler
docker-compose logs -f airflow-scheduler

# Pour Airflow Worker
docker-compose logs -f airflow-worker

# Pour la base de données PostgreSQL
docker-compose logs -f postgres
```

---

## 💻 4. Interagir avec les conteneurs

**Ouvrir le terminal (bash) à l'intérieur du conteneur Airflow (Worker) pour tester un script Python :**
```bash
docker exec -it airflow-worker /bin/bash
```

**Se connecter directement à la base de données PostgreSQL en ligne de commande :**
```bash
docker exec -it postgres psql -U postgres -d youtube_db
```
*(Pour quitter l'interface psql, tape `\q` et appuie sur Entrée)*

---

## 🌐 5. Accès aux interfaces web
- **Apache Airflow :** [http://localhost:8080](http://localhost:8080) (Identifiants : `admin` / `admin` comme défini dans le `.env`)
- **PostgreSQL :** Port `5432` sur `localhost` (Tu peux te connecter avec DBeaver ou pgAdmin en utilisant l'utilisateur `postgres` et le mot de passe `postgres`).

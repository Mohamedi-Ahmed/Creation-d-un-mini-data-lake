# TP2 – Pipeline d’Ingestion de Données avec Docker et DuckDB

## Objectif

Construire un pipeline d’ingestion automatisé dans Docker, qui télécharge, nettoie, transforme et stocke des données dans DuckDB, avec persistance des fichiers.

## Description du pipeline

Le script Python effectue les étapes suivantes :

1. Téléchargement d’un fichier JSON via API (ex. OpenFoodFacts)
2. Normalisation et nettoyage des données :
   - Suppression de colonnes inutiles
   - Suppression des colonnes entièrement nulles
3. Sauvegarde locale en Parquet
4. Ingestion dans une base DuckDB persistante (fichier .duckdb)
5. Journalisation des étapes et erreurs dans un fichier log

## Arborescence

```
TP2_Pipeline_Docker_DuckDB/
├── data/                  # Fichiers sources JSON, sorties Parquet
├── etl/
│   └── etl_pipeline.py    # Script principal
├── logs/
│   └── pipeline.log       # Journalisation des erreurs/success
├── db/
│   └── database.duckdb    # Base DuckDB persistante
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── crontab.txt            # Tâche planifiée (optionnel)
```

## Dépendances

```
pip install duckdb pandas requests
```

## Build et exécution

```
docker-compose build
docker-compose up
```

## Cron : définition

Un **cron** est une tâche planifiée sous Linux/Unix. Elle permet d'exécuter automatiquement un script à intervalles réguliers (ex : toutes les 10 minutes, tous les jours à 2h, etc.).

Dans ce TP, un cron peut être utilisé à l’intérieur du container pour exécuter automatiquement `etl_pipeline.py` à fréquence définie.

Exemple dans `crontab.txt` :

```
*/10 * * * * root python /app/etl_pipeline.py >> /app/logs/pipeline.log 2>&1
```

Ce cron exécute le pipeline toutes les 10 minutes et redirige la sortie dans le fichier de log.

## Résultat attendu

- Données nettoyées disponibles en Parquet
- Base DuckDB mise à jour avec les dernières données
- Journal complet dans `logs/pipeline.log`

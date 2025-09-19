# TP2 – Pipeline d’Ingestion de Données avec Docker et DuckDB

## Objectif

Créer un pipeline d'ingestion automatisé qui :

1. Télécharge un fichier JSON (OpenFoodFacts)
2. Nettoie les données
3. Sauvegarde en Parquet
4. Charge dans DuckDB (base persistante)
5. Journalise le traitement dans un fichier log

## Structure du projet

```
TP2_Pipeline_Docker_DuckDB/
├── data/
├── db/
├── logs/
├── etl/
│   └── etl_pipeline.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── crontab.txt
└── README.md
```

## Cron : définition

Un **cron** est une tâche planifiée sous Linux/Unix. Elle permet d'exécuter automatiquement un script à intervalles réguliers (ex : toutes les 10 minutes, tous les jours à 2h, etc.).

Dans ce TP, un cron peut être utilisé à l’intérieur du container pour exécuter automatiquement `etl_pipeline.py` à fréquence définie.

Exemple dans `crontab.txt` :

```
*/10 * * * * root python /app/etl_pipeline.py >> /app/logs/pipeline.log 2>&1
```

Ce cron exécute le pipeline toutes les 10 minutes et redirige la sortie dans le fichier de log.

## Lancement

```bash
docker-compose up --build
```
## Résultat

- Fichier `openfood.parquet` dans `data/`
- Table `products` créée dans `database.duckdb`
- Log écrit dans `logs/pipeline.log`

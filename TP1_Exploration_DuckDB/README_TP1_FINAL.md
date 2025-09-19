# TP1 - Analyse exploratoire de données avec DuckDB (via Docker)

## Objectif

Ce TP vise à :

- Lire un fichier CSV contenant des données COVID
- Le convertir au format Parquet via DuckDB
- Comparer les performances de lecture CSV vs Parquet
- Exécuter l’ensemble du traitement dans un conteneur Docker

---

## Structure du projet

```
TP1_Exploration_DuckDB/
├── Dockerfile
├── docker-compose.yml
├── analysis_duckdb.py
├── data/
│   └── archive/
│       └── covid/
│           ├── covid_19_clean_complete.csv
│           └── covid_19_clean_complete.parquet (généré automatiquement)
```

---

## Lancement

Depuis le dossier `TP1_Exploration_DuckDB`, exécuter :

```bash
docker-compose up --build
```

---

## Résultats obtenus

### Temps de traitement

- Lecture CSV : **0.17 s**
- Lecture Parquet : **0.05 s**

### Requête SQL exécutée

Top 10 des régions avec le plus de cas :

| Rang | Pays           | Cas max |
| ---- | -------------- | ------- |
| 1    | US             | 4290259 |
| 2    | Brazil         | 2442375 |
| 3    | India          | 1480073 |
| 4    | Russia         | 816680  |
| 5    | South Africa   | 452529  |
| 6    | Mexico         | 395489  |
| 7    | Peru           | 389717  |
| 8    | Chile          | 347923  |
| 9    | United Kingdom | 300111  |
| 10   | Iran           | 293606  |

---

## Observations

- La lecture d’un fichier .parquet est **plus de 3 fois plus rapide** que celle du `.csv`
- DuckDB permet de faire cette conversion et les requêtes SQL directement, sans bibliothèque externe
- Compatible avec Docker

---

## Commande utilisée dans Docker

```sql
COPY covid_csv TO 'data/covid.parquet' (FORMAT PARQUET)
```

---

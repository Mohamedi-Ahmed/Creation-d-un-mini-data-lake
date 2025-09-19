# TP4 – Mini Data Lake Local avec DuckDB + Streamlit

## Objectifs

- Simuler un mini data lake local avec DuckDB
- Manipuler des fichiers Parquet partitionnés
- Créer une interface web avec Streamlit

## Fonctionnalités

- Lire des fichiers Parquet dynamiquement
- Créer/Supprimer des tables DuckDB
- Uploader un CSV et l’enregistrer comme table
- Exporter une table DuckDB en Parquet
- Visualiser un graphique par année

## Lancer l’application

```bash
docker build -t mini_datalake_app -f docker/Dockerfile .
docker run -p 8501:8501 mini_datalake_app
```

## Arborescence

```
tp4_mini_data_lake/
├── app/
│   └── app.py
├── data/
│   └── *.parquet
├── docker/
│   └── Dockerfile
└── README.md
```
import duckdb
import pandas as pd
from time import time

csv_path = "../data/archive/covid/covid_19_clean_complete.csv"
parquet_path = "../data/archive/covid/covid_19_clean_complete.parquet"

#Creation d'une db pour le tp3  
con = duckdb.connect(database="../data/covid.duckdb", read_only=False)

con.execute("DROP TABLE IF EXISTS covid_csv")
con.execute("DROP TABLE IF EXISTS covid_parquet")

start_csv = time()
con.execute(f"""
    CREATE TABLE covid_csv AS
    SELECT * FROM read_csv_auto('{csv_path}')
""")
csv_duration = time() - start_csv
print(f"Lecture CSV : {round(csv_duration,3):} s")

con.execute(f"COPY covid_csv TO '{parquet_path}' (FORMAT PARQUET)")
print("Sauvegarde en Parquet terminée.")

start_parquet = time()
con.execute(f"""
    CREATE TABLE covid_parquet AS
    SELECT * FROM read_parquet('{parquet_path}')
""")
parquet_duration = time() - start_parquet
print(f"Lecture Parquet : {round(parquet_duration,3):} s")

print("\nTop 10 des régions avec le plus de cas :")
print(con.execute("""
    SELECT "Country/Region", MAX(Confirmed) AS max_cases
    FROM covid_parquet
    GROUP BY "Country/Region"
    ORDER BY max_cases DESC
    LIMIT 10
""").df())

print(f"\nTemps CSV : {round(csv_duration,3):}s | Temps Parquet : {round(parquet_duration,3):}s")

# Création d'une table nettoyée pour le TP3 (covid_clean)
con.execute("""
    CREATE OR REPLACE TABLE covid_clean AS
    SELECT *
    FROM covid_parquet
    WHERE Confirmed IS NOT NULL AND Deaths IS NOT NULL AND Recovered IS NOT NULL
""")

print("\nTable 'covid_clean' créée avec succès.")
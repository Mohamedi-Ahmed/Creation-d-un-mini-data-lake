import duckdb
import pandas as pd
from time import time

csv_path = "../data/archive/covid/covid_19_clean_complete.csv"
parquet_path = "../data/archive/covid/covid_19_clean_complete.parquet"

con = duckdb.connect(database=":memory:")

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

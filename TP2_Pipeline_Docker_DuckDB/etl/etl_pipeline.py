import requests
import pandas as pd
import duckdb
import logging

log_path = "logs/pipeline.log"
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    url = "https://world.openfoodfacts.org/api/v0/product/737628064502.json"
    r = requests.get(url)
    product = r.json()

    df = pd.json_normalize(product)
    df_clean = df.dropna(axis=1, how="all")
    df_clean = df_clean.loc[:, ~df_clean.columns.str.contains("code|_tags|_id")]

    parquet_path = "data/openfood.parquet"
    df_clean.to_parquet(parquet_path, index=False)

    con = duckdb.connect("db/database.duckdb")
    con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM read_parquet(?)", [parquet_path])
    con.close()

    logging.info("Pipeline exécuté avec succès.")

except Exception as e:
    logging.error(f"Erreur : {str(e)}")

import streamlit as st
import duckdb
import pandas as pd
import os

st.set_page_config(page_title="Mini Data Lake", layout="wide")

DATA_PATH = "../data"
PARQUET_FOLDER = os.path.join(DATA_PATH, "parquet_export")
os.makedirs(PARQUET_FOLDER, exist_ok=True)

con = duckdb.connect("data_lake.duckdb")

st.title("Mini Data Lake - DuckDB + Streamlit")

if os.listdir(PARQUET_FOLDER):
    df_parquet = con.execute(f"SELECT * FROM read_parquet('{PARQUET_FOLDER}/*.parquet')").fetch_df()
    if 'year' in df_parquet.columns and 'confirmed' in df_parquet.columns:
        st.subheader("Graphique des cas confirmés par année (Parquet)")
        df_grouped = df_parquet.groupby('year')['confirmed'].sum().reset_index()
        st.bar_chart(df_grouped)

st.subheader("Tables DuckDB")
tables = con.execute("SHOW TABLES").fetchdf()["name"].tolist()
table_choice = st.selectbox("Choisir une table à afficher :", tables) if tables else None
st.write("Tables actuelles :", tables)

if table_choice:
    df_preview = con.execute(f"SELECT * FROM {table_choice} LIMIT 5").fetchdf()
    st.dataframe(df_preview)

    if st.button("Supprimer la table sélectionnée"):
        con.execute(f"DROP TABLE IF EXISTS {table_choice}")
        st.success(f"Table {table_choice} supprimée.")
        st.rerun()

st.subheader("Uploader un CSV pour créer une table")
uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")

if uploaded_file:
    df_new = pd.read_csv(uploaded_file)
    st.write(df_new.head())
    table_name = st.text_input("Nom de la nouvelle table")
    if st.button("Créer la table"):
        con.register("temp_df", df_new)
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM temp_df")
        st.success(f"Table {table_name} créée avec succès.")
        st.rerun()

st.subheader("Exporter une table en Parquet")
if tables:
    export_table = st.selectbox("Choisir une table à exporter :", tables, key="export")
    export_btn = st.button("Exporter la table")
    if export_btn and export_table:
        path = f"{PARQUET_FOLDER}/{export_table}.parquet"
        con.execute(f"COPY {export_table} TO '{path}' (FORMAT PARQUET)")
        st.success(f"{export_table} exportée dans {path}")
else:
    st.info("Aucune table disponible pour l'export.")

st.subheader("Graphique simple")
if tables:
    graph_table = st.selectbox("Choisir une table à visualiser :", tables, key="graph")
    if graph_table:
        df_graph = con.execute(f"SELECT * FROM {graph_table}").fetchdf()
        col_x = st.selectbox("Colonne X :", df_graph.columns, key="x_axis")
        col_y = st.selectbox("Colonne Y :", df_graph.columns, key="y_axis")
        generate_chart = st.button("Générer le graphique")
        if generate_chart:
            try:
                st.bar_chart(df_graph[[col_x, col_y]])
            except Exception as e:
                st.error(f"Erreur lors de la génération du graphique : {e}")

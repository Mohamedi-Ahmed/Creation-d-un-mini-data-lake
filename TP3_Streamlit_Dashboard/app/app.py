import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="COVID Dashboard", layout="wide")

# Connexion à la base duckdb
con = duckdb.connect(database="../data/covid.duckdb", read_only=True)

df = con.execute("SELECT * FROM covid_clean").fetch_df()

countries = st.multiselect("Select countries", df["Country/Region"].unique(), default=["US", "India", "Brazil"])

filtered_df = df[
    df["Country/Region"].isin(countries) &
    df["Country/Region"].apply(lambda x: isinstance(x, str) and not x.strip().isdigit())
]

# KPIs
st.markdown("### KPIs")
col1, col2 = st.columns(2)
col1.metric("Total rows", len(filtered_df))
col2.metric("Unique countries", filtered_df["Country/Region"].nunique())

# Graphiques
st.markdown("### Cas max par pays")
df_top = (
    filtered_df.groupby("Country/Region")["Confirmed"]
    .max()
    .reset_index(name="max_cases")
    .sort_values(by="max_cases", ascending=False)
    .head(10)
)

st.bar_chart(data=df_top, x="Country/Region", y="max_cases")

# Export CSV
st.download_button("Export to CSV", data=filtered_df.to_csv(index=False), file_name="filtered_data.csv")

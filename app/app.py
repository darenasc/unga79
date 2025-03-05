import sqlite3
from pathlib import Path
from random import randrange

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="#UNGA79",
    layout="wide",
    initial_sidebar_state="expanded",
)


"""
df is a pd.DataFrame with the following columns:
    - country
    - url
    - full_speech
    - summary
    - countries_mentioned
    - risks
    - haiku
"""

# TODO Add line chart with HDI vs other countries


@st.cache_data
def get_data(db: Path):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        rows = cursor.execute("""SELECT * FROM countries;""").fetchall()
        column_names = [x[0] for x in cursor.description]
        cursor.close()

    df = pd.DataFrame(rows, columns=column_names)
    return df


df = get_data(Path(__file__).absolute().parent / "countries.db")

if "random_initial_country" not in st.session_state:
    st.session_state.random_initial_country = randrange(len(df))
    st.session_state.disabled = False

with st.sidebar:
    country_selection = st.selectbox(
        "Country",
        df["country"].sort_values().to_list(),
        index=st.session_state.random_initial_country,
    )  # type:ignore

st.title(f"#UNGA79 {country_selection}")

col1, col2 = st.columns(2)

with col1:
    if df[df["country"] == country_selection]["summary"].values[0]:
        st.header("Summary")
        st.markdown(df[df["country"] == country_selection]["summary"].values[0])


with col2:
    st.video(df[df["country"] == country_selection]["url"].values[0])

    if df[df["country"] == country_selection]["haiku"].values[0]:
        st.header("Haiku")
        st.text(df[df["country"] == country_selection]["haiku"].values[0])


if df[df["country"] == country_selection]["risks"].values[0]:
    st.header("Risks")
    st.markdown(df[df["country"] == country_selection]["risks"].values[0])

if df[df["country"] == country_selection]["countries_mentioned"].values[0]:
    st.header("Countries mentioned")
    st.markdown(df[df["country"] == country_selection]["countries_mentioned"].values[0])

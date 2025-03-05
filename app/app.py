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

import time

import streamlit as st

from unga79 import database as dbase

# TODO Add line chart with HDI vs other countries

st.set_page_config(
    page_title="#UNGA79",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("#UNGA79")

df = dbase.select_country()

with st.sidebar:
    country_selection = st.selectbox(
        "Country", df["country"].sort_values().to_list()
    )  # type:ignore


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

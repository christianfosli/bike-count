"""
Bike Count App

Visualize data from bike counters in Stavanger kommune
"""

from datetime import timedelta

import pandas as pd
import streamlit as st

BIKE_STATS_URL = "https://opencom.no/dataset/90cef5d5-601e-4412-87e4-3e9e8dc59245/resource/4c71d19a-adc4-42e0-9bed-c990316479be/download/sykkeldata.csv"

BIKE_LOCS_URL = "https://opencom.no/dataset/1f64a769-9c10-4cc7-9db9-60ac74a7183e/resource/95d70356-d855-4430-9e04-c8d741e5761a/download/lokaliseringsykkeltellerestavanger.csv"


@st.cache_data(ttl=timedelta(days=1))
def get_locs() -> pd.DataFrame:
    return pd.read_csv(BIKE_LOCS_URL)


@st.cache_data(ttl=timedelta(hours=1))
def get_stats() -> pd.DataFrame:
    return pd.read_csv(BIKE_STATS_URL)


st.title("Sykkeltellere i Stavanger")

locs_df = get_locs()
sel_loc = st.selectbox(label="Velg plassering", options=locs_df["Navn"])

locs_df["Color"] = "#aaaaaa"
locs_df.loc[locs_df["Navn"] == sel_loc, "Color"] = "#ff0000"

st.map(locs_df, latitude="Latitude", longitude="Longitude", color="Color")

stats_df = get_stats()

stats_df = stats_df.loc[stats_df["Station_Name"] == sel_loc]

stats_df["Date_Time"] = pd.to_datetime(
    stats_df["Date"] + stats_df["Time"].apply(lambda t: f"T{t.split("-")[0]}")  # type: ignore
)

st.subheader("Passeringer per time")

max_date: pd.Timestamp = stats_df["Date_Time"].max()
default_from = max_date - timedelta(days=7)
from_dt, to_dt = st.date_input("Date range", (default_from, max_date))  # type: ignore
from_dt = pd.to_datetime(from_dt)
to_dt = pd.to_datetime(to_dt)


stats_df = stats_df.loc[stats_df["Date_Time"].between(from_dt, to_dt)]

# Combine passings in both lanes/directions, and project relevant cols
stats_df = stats_df.groupby("Date_Time").aggregate(
    {
        "Count": "sum",
        "Average_Speed": "mean",
        "Average_Temperature": "mean",
    }
)

# Add missing hours with count 0
stats_df = stats_df.asfreq(freq="h")
stats_df["Count"] = stats_df["Count"].fillna(0)

stats_df = stats_df.rename(columns={"Count": "Count per hour"})

st.line_chart(stats_df)

with st.expander("Tabellvisning"):
    st.dataframe(stats_df)


st.divider()

st.markdown(
    (
        ":material/dataset: Dataen er offentlig data fra stavanger kommune. "
        "Den er hentet fra [opencom.no/dataset/lokalisering-sykkeltellere-stavanger]( https://opencom.no/dataset/lokalisering-sykkeltellere-stavanger) "
        "og [opencom.no/dataset/sykkeldata](https://opencom.no/dataset/sykkeldata). "
    )
)

st.markdown(
    ":material/code: Appen's kildekode er tilgjengelig på [GitHub](https://github.com/christianfosli/bike-count)"
)

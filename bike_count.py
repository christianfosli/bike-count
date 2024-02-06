import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from datetime import date
from datetime import time

# See https://opencom.no/dataset/lokalisering-sykkeltellere-stavanger
BIKE_COUNTER_LOCATIONS_URL='https://opencom.no/dataset/1f64a769-9c10-4cc7-9db9-60ac74a7183e/resource/95d70356-d855-4430-9e04-c8d741e5761a/download/lokaliseringsykkeltellerestavanger.csv'

# See https://opencom.no/dataset/sykkeldata
BIKE_COUNT_DATA_URL='https://opencom.no/dataset/90cef5d5-601e-4412-87e4-3e9e8dc59245/resource/4c71d19a-adc4-42e0-9bed-c990316479be/download/sykkeldata.csv'

@st.cache_data(ttl=36000)
def load_counter_locations() -> pd.DataFrame:
    df = pd.read_csv(BIKE_COUNTER_LOCATIONS_URL)
    print('Fetched new counter location data')
    return df

@st.cache_data(ttl=3600)
def load_count_data() -> pd.DataFrame:
    df = pd.read_csv(BIKE_COUNT_DATA_URL)
    print('Fetched new bike count data')
    return df

if __name__ == '__main__':
    st.title('Sykkeltellere i Stavanger-område')

    data_loading = st.text('Laster data...')
    locations = load_counter_locations()
    data = load_count_data()
    data_loading = st.text('')

    st.subheader('Oversikt over tellere')

    dates = pd.to_datetime(data['Date'])
    min = dates.min().date()
    max = dates.max().date()
    date_slider: tuple[date, date] =  st.slider('Dato/tid', min, max, (min, max))
    (from_dt, to_dt) = tuple(map(lambda d: datetime.combine(d, time()), date_slider))

    data['Date'] = dates
    filtered_data = data.loc[(data['Date'] >= from_dt) & (data['Date'] <= to_dt)]

    location_counts: pd.Series = filtered_data.groupby(['Station_id'])['Count'].sum();
    locations_with_counts = pd.merge(locations, location_counts, on="Station_id")

    map_fig = px.scatter_mapbox(locations_with_counts, lat='Latitude', lon='Longitude', hover_name='Navn', zoom=10, size="Count" , color = 'Count', labels = { 'Count': 'Antall passeringer' })
    map_fig.update_layout(mapbox_style='open-street-map')
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(map_fig)

    st.subheader('Data fra bestemt teller')
    # TODO: make it possible to pick a specific counter to visialize

    st.subheader('Referansedata')
    with st.expander('Raw data'):
        st.text('Dataen kommer fra https://opencom.no/dataset/lokalisering-sykkeltellere-stavanger og https://opencom.no/dataset/sykkeldata')
        st.subheader('Tellere')
        st.write(locations)
        st.subheader('Passeringsdata')
        st.write(data)

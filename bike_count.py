import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import operator
from datetime import datetime
from datetime import date
from datetime import time

# See https://opencom.no/dataset/lokalisering-sykkeltellere-stavanger
BIKE_COUNTER_LOCATIONS_URL='https://opencom.no/dataset/1f64a769-9c10-4cc7-9db9-60ac74a7183e/resource/95d70356-d855-4430-9e04-c8d741e5761a/download/lokaliseringsykkeltellerestavanger.csv'

# See https://opencom.no/dataset/sykkeldata
BIKE_COUNT_DATA_URL='https://opencom.no/dataset/90cef5d5-601e-4412-87e4-3e9e8dc59245/resource/4c71d19a-adc4-42e0-9bed-c990316479be/download/sykkeldata.csv'

@st.cache_data(ttl=3600)
def load_counter_locations() -> pd.DataFrame:
    df = pd.read_csv(BIKE_COUNTER_LOCATIONS_URL)
    print('Fetched new counter location data')
    return df

@st.cache_data(ttl=3600)
def load_count_data() -> pd.DataFrame:
    df = pd.read_csv(BIKE_COUNT_DATA_URL)
    print('Fetched new bike count data')

    # The dataset includes counts per hour, but for our needs per date is sufficient, so we'll convert it to per date
    df: pd.DataFrame = df.groupby(['Station_id', 'Date', 'Lane_Name']).aggregate({'Station_Name': 'first', 'Count': 'sum', 'Average_Speed': 'mean', 'Average_Temperature': 'mean'}).reset_index() # type: ignore

    # We also want to parse the date as a datetime rather than a string, for filtering purposes
    df['Date'] = pd.to_datetime(df['Date'])

    return df

def date_filter(locations: pd.DataFrame, data: pd.DataFrame) -> tuple[tuple[datetime,datetime], pd.DataFrame, pd.DataFrame]:
    min = data['Date'].min().date()
    max = data['Date'].max().date()
    date_slider: tuple[date, date] = st.slider('Dato/tid', min, max, (min, max))
    st.info('Valgbar tidsrammet bestemmes av underliggende datasett. Se mer info under [referansedata](/#referansedata).', icon='ℹ️')

    (from_dt, to_dt) = tuple(map(lambda d: datetime.combine(d, time()), date_slider)) # convert to datetime for filtering
    filtered_data = data.loc[(data['Date'] >= from_dt) & (data['Date'] <= to_dt)]

    loc_counts: pd.Series = filtered_data.groupby(['Station_id'])['Count'].sum();
    locations_with_counts = pd.merge(locations, loc_counts, on='Station_id', how='left')
    locations_with_counts['Count'] = locations_with_counts['Count'].fillna(0)

    return ((from_dt, to_dt), locations_with_counts, filtered_data)

def render_overview_map(locations: pd.DataFrame, data: pd.DataFrame):
    st.subheader('Oversikt over tellere')
    map_fig = px.scatter_mapbox(locations, lat='Latitude', lon='Longitude', hover_name='Navn', zoom=10, size="Count" , color = 'Count', labels = { 'Count': 'Antall passeringer' })
    map_fig.update_layout(mapbox_style='open-street-map')
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(map_fig)

def render_specific_location(locations: pd.DataFrame, data: pd.DataFrame):
    st.subheader('Data fra bestemt teller')
    loc_dict = locations.groupby('Station_id').apply(dict, include_groups=False)
    options = locations.sort_values(by='Navn')['Station_id']
    sel_ix: int | None = pd.Index(options).get_loc(st.session_state.get('sel_id')) if 'sel_id' in st.session_state else None # type: ignore
    sel_id = st.selectbox('Velg teller', options, index=sel_ix, format_func=lambda id: f'{loc_dict[id]["Navn"].item()} ({int(loc_dict[id]["Count"].item())} passeringer)', key='sel_id')
    if sel_id == None:
        return

    loc_data = data[data['Station_id'] == sel_id]
    if loc_data.empty:
        st.warning(f'Fant ingen sykkeldata for {sel_id}')
    else:
        st.bar_chart(loc_data, x='Date', y='Count')


def render_raw_data(locations: pd.DataFrame, data: pd.DataFrame):
    st.subheader('Referansedata')
    with st.expander('Referansedata'):
        st.write(('Dataen er offentlig data fra stavanger kommune. '
                 'Den er hentet fra [opencom.no/dataset/lokalisering-sykkeltellere-stavanger](https://opencom.no/dataset/lokalisering-sykkeltellere-stavanger) '
                 'og [opencom.no/dataset/sykkeldata](https://opencom.no/dataset/sykkeldata). '
                 'Per Februar 2024 ser det ut til at det ikke finnes nyere data enn for slutten av 2022.'))
        st.subheader('Tellere')
        st.write(locations)
        st.subheader('Sykkeldata')
        st.write(data)

def app():
    st.title('Sykkeltellere i stavanger-område')

    data_loading = st.text('Laster data...')
    locations = load_counter_locations()
    data = load_count_data()
    data_loading.text('')

    ((from_dt, to_dt), locations_with_counts, filtered_data) = date_filter(locations, data)

    render_overview_map(locations_with_counts, filtered_data)
    render_specific_location(locations_with_counts, filtered_data)
    render_raw_data(locations, data)

if __name__ == '__main__':
    app()

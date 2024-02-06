import streamlit as st
import pandas as pd
import numpy as np

# See https://opencom.no/dataset/sykkeldata
BIKE_COUNT_DATA_URL='https://opencom.no/dataset/90cef5d5-601e-4412-87e4-3e9e8dc59245/resource/4c71d19a-adc4-42e0-9bed-c990316479be/download/sykkeldata.csv'

@st.cache_data
def load_data():
    df = pd.read_csv(BIKE_COUNT_DATA_URL)
    print('Fetched new bike count data')
    print(df.describe)
    return df

st.title('Sykkeltellere i Stavanger område')

data_load_state = st.text('Laster data...')
data = load_data()
data_load_state.text('Laster data... Ferdig!')



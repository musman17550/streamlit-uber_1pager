import streamlit as st
import pandas as pd
import numpy as np

#Title of app
st.title('Uber Pickups in NYC')

#Data path and type
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

#Loading data
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#Calling load_data
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data...done!')

#Viewing raw data
st.subheader('Raw data')
if st.checkbox('Show raw data'):
    st.write(data)

#Plotting a bar chart
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

#Plotting on a map
##st.subheader('Map of all pickups')
#st.map(data)

#Filtering busiest hour
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
import streamlit as st
import pandas as pd
import numpy as np
import re
import pydeck as pdk
import plotly.express as px


@st.cache(persist=True)
def load_data(path_to_data, nrows):
    data = pd.read_csv(path_to_data, nrows=nrows, parse_dates=[['CRASH DATE', 'CRASH TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: re.sub(r'[ ]', '_', str(x).lower())
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


DATA_URL = 'Motor_Vehicle_Collisions_-_Crashes.csv'

st.title("Motor Vihecle Collisions in NY City")
st.markdown("This is application is a Streamlit dashboard")

data = load_data(DATA_URL, 100000)

st.header('Where are the most people inhured in NYC?')
injured_people = st.slider('Number of persons injured in vehicle collisions', 0, 19)
st.map(data.query('number_of_persons_injured >= @injured_people')[['latitude', 'longitude']].dropna(how='any'))

st.header('How many collisions occur during a given time of day?')
hour = st.slider('Hour to look at', 0, 23)
filtered_data = data[data['date/time'].dt.hour == hour]

st.markdown('Vehicle collisions between %i:00 and %i:00' % (hour, (hour + 1) % 24))
midpoint = (np.median(filtered_data['latitude']), np.median(filtered_data['longitude']))
st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude': midpoint[0],
        'longitude': midpoint[1],
        'zoom': 11,
        'pitch': 50,
    },
    layers=[
        pdk.Layer(
            # extruded=True - enable 3D
            'HexagonLayer', data=filtered_data[['date/time', 'latitude', 'longitude']],
            get_position=['longitude', 'latitude'], radius=75, extruded=True,
            pickable=True, elevation_scale=4, elevation_range=[0, 1000]
        )
    ]
))

st.subheader('Breadkdown by minute between %i:00 and %i:00' % (hour, (hour + 1) % 24))
filtered_data = data[
    (data['date/time'].dt.hour >= hour) &
    (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered_data['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

if st.checkbox('Show Raw Data', False):
    st.subheader('Raw Data')
    st.write(data)

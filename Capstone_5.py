
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="AirBnB Visualization ", page_icon=":house_buildings:",layout="wide")

st.title(':globe_with_meridians: Airbnb Geospatial Visualization')
st.header('Please select the following filters:',divider = True)

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Cache the data loading process
@st.cache_resource
def load_data(file_path):
    return pd.read_csv(file_path)

file_path = r"F:\Capstone\Project 5\Final\c_df.csv"
df = load_data(file_path)

# Compute the bounds of the data
min_lat, max_lat = df['Latitude'].min(), df['Latitude'].max()
min_lon, max_lon = df['Longitude'].min(), df['Longitude'].max()

# Initialize the map and marker cluster only once
if 'map' not in st.session_state:
    st.session_state.map = folium.Map()
    st.session_state.map.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
    st.session_state.marker_cluster = MarkerCluster().add_to(st.session_state.map)

# Filters
property_type = st.selectbox('Property Type', df['property_type'].unique())
room_type = st.selectbox('Room Type', df['room_type'].unique())
bed_type = st.selectbox('Bed Type', df['bed_type'].unique())

# Apply filters
filtered_df = df[
    (df['property_type'] == property_type) &
    (df['room_type'] == room_type) &
    (df['bed_type'] == bed_type)
]

# Clear the existing markers before adding new ones
st.session_state.map = folium.Map()
st.session_state.map.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
marker_cluster = MarkerCluster().add_to(st.session_state.map)

for index, row in filtered_df.iterrows():
    popup_text = f"""
    <b>Name:</b> {row['name']}<br>
    <b>Country:</b> {row['Country']}<br>
    <b>Property Type:</b> {row['property_type']}<br>
    <b>Room Type:</b> {row['room_type']}<br>
    <b>Bed Type:</b> {row['bed_type']}<br>
    <b>Minimum Nights:</b> {row['minimum_nights']}<br>
    <b>Maximum Nights:</b> {row['maximum_nights']}<br>
    <b>Cancellation Policy:</b> {row['cancellation_policy']}<br>
    <b>Accommodates:</b> {row['accommodates']}<br>
    <b>Bedrooms:</b> {row['bedrooms']}<br>
    <b>Number of Reviews:</b> {row['number_of_reviews']}<br>
    <b>Bathrooms:</b> {row['bathrooms']}<br>
    <b>Amenities:</b> {row['amenities']}<br>
    <b>Price:</b> {row['price']}<br>
    <b>Review Score Rating:</b> {row['review_scores_rating']}
    """
    tooltip_text = f"Name: {row['name']}<br>Type: {row['property_type']}"
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=tooltip_text
    ).add_to(marker_cluster)

st.subheader('Geospatial Visualization', divider=True)
st_folium(st.session_state.map, width=800, height=600)

import streamlit as st
from geopy.distance import geodesic
import folium
from streamlit_folium import folium_static
import geocoder
from bg import backg

st.set_page_config(
    page_title="BinBuddy",
    page_icon="🗑️",
    layout="wide")
background_image = backg

st.markdown(background_image, unsafe_allow_html=True)


# Sample array of predefined locations (latitude, longitude)
predefined_locations = [
    {"name": "Location Lokmanya nagar", "coords": (21.1022, 78.9953), "type": "wet"},
    {"name": "Location Telephone Exchange", "coords": (21.1484, 79.1201), "type": "dry"},
    {"name": "Location Sitabardi", "coords": (21.1430, 79.0871), "type": "electronic"},
    {"name": "Location Chatrapati square", "coords": (21.1099, 79.0725), "type": "medicinal"},
]

def live():
    g = geocoder.ip('me')
    location = g.latlng
    # Input latitude and longitude
    lat = float(location[0])
    lon = float(location[1])
    return lat, lon

def find_nearest_location(user_location, locations):
    nearest_location = None
    shortest_distance = None
    for location in locations:
        distance = geodesic(user_location, location['coords']).km
        if shortest_distance is None or distance < shortest_distance:
            shortest_distance = distance
            nearest_location = location
    return nearest_location, shortest_distance

def map(lat, lon, nearest_location, distance_to_nearest):
    user_location = (lat, lon)
    st.header(f"Your location: {user_location}")
    st.header(f"The nearest location is: {nearest_location['name']}  {nearest_location['type']}")

    # Visualize the locations on a map
    map_center = user_location
    m = folium.Map(location=map_center, zoom_start=13,)

    # Mark the user location
    folium.Marker(user_location, popup="Your Location", icon=folium.Icon(color="blue")).add_to(m)

    # Mark the nearest location with its name and type
    folium.Marker(
        nearest_location['coords'], 
        popup=f"Nearest Location: {nearest_location['name']} ({nearest_location['type']})", 
        icon=folium.Icon(color="red"),
        tiles='CartoDB dark_matter'
    ).add_to(m)

    # Mark all predefined locations with their name and type
    for location in predefined_locations:
        folium.Marker(
            location['coords'], 
            popup=f"{location['name']} ({location['type']})", 
            icon=folium.Icon(color="green"),
            tiles='CartoDB dark_matter'
        ).add_to(m)

    # Display the map
    folium_static(m)

def book():
    lat, lon = live()
    nearest_location, distance_to_nearest = find_nearest_location((lat, lon), predefined_locations)
    # Assuming an average speed of 60 km/h for calculation
    average_speed_kmph = 10  # You can adjust this value as needed
    time_taken = distance_to_nearest * average_speed_kmph  # Time in hours
    s1="Your Bin companion is near "+ str(nearest_location["name"])+"."
    s1 = str(s1)
    st.title(s1)
    st.title(f'Estimated time to reach: {time_taken:.2f} min.')

# col1, col2 = st.columns([3, 1])
# with col2:
#     st.

# st.markdown("<br>", unsafe_allow_html=True)
import time

# if st.button('About'):
#     st.toast('BinBuddy utilizes real-time GPS tracking to locate nearby waste bins and recycling centers', icon='🗑️',)
#     time.sleep(1)
#     st.toast('Users can easily find the closest options for disposing of their waste responsibly')
#     # time.sleep(1)
#     # st.toast('Hooray!', icon='🎉')

# # st.info('BinBuddy utilizes real-time GPS tracking to locate nearby waste bins and recycling centersUsers can easily find the closest options for disposing of their waste responsibly', icon="ℹ")
# # # Add a button to trigger location retrieval
# if "button_clicked" not in st.session_state:
#     if st.button("Get Your Nearest BinBuddy"):
#         # Get the current location (based on IP address or GPS)
#         st.session_state["button_clicked"] = True
#         lat, lon = live()
        
#         # Find the nearest location
#         nearest_location, distance_to_nearest = find_nearest_location((lat, lon), predefined_locations)

#         # Display the map with the nearest location
#         map(lat, lon, nearest_location, distance_to_nearest)

#     # Add a button to book the nearest location
# if st.session_state.get("button_clicked"):
#     if st.button("On the Go!"):
#         st.session_state["button_near"] = True
#         book()  
#         col1, col2 = st.columns([3, 1])  # Adjust the column ratio as needed

#         # Display "Do More Trash Bash" message in the right column
#         with col2:
#             st.markdown("<h1 style='text-align: right; color: red;'>Do More Trash Bash</h1>", unsafe_allow_html=True)


# Initialize session state if not already done
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
if "about_button_clicked" not in st.session_state:
    st.session_state.about_button_clicked = False

# Handle the "About" button visibility
if not st.session_state.button_clicked and not st.session_state.about_button_clicked:
    if st.button('About'):
        st.toast('BinBuddy utilizes real-time GPS tracking to locate nearby waste bins and recycling centers', icon='🗑️',)
        st.session_state.about_button_clicked = True
        time.sleep(2)
        st.toast('Users can easily find the closest options for disposing of their waste responsibly')

# Add a button to trigger location retrieval
if not st.session_state.button_clicked:
    if st.button("Get Your Nearest BinBuddy"):
        st.session_state.button_clicked = True
        lat, lon = live()
        nearest_location, distance_to_nearest = find_nearest_location((lat, lon), predefined_locations)
        map(lat, lon, nearest_location, distance_to_nearest)

# Add a button to book the nearest location
if st.session_state.button_clicked:
    if st.button("On the Go!"):
        st.session_state.button_near = True
        book()  
        col1, col2 = st.columns([3, 1])  # Adjust the column ratio as needed

        # Display "Do More Trash Bash" message in the right column
        with col2:
            st.markdown("<h1 style='text-align: right; color: red;'>Do More Trash Bash</h1>", unsafe_allow_html=True)

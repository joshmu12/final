import streamlit as st
import pandas as pd

# web scraping / api 
from PIL import Image

import requests
import json

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

response = requests.get(url)

if response.status_code == 200:

        fpl_data = json.loads(response.text) # Parse the JSON content of the API response

        player_stats = fpl_data['elements']

        #player list 
        player_list = []
        for player in player_stats:
                player_list.append(player['first_name'] + " " + player['second_name'])
        player_list.sort()

else:
    print(f"Failed to retrieve FPL data. Status code: {response.status_code}")

st.set_page_config(

        page_title = "Fantasy Premier League Tracker",
        page_icon = "⚽️",
)

# sidebar 
from streamlit_option_menu import option_menu

with st.sidebar:
        selected = option_menu(
                menu_title = "Fantasy Premier League",
                options = ["Home" , "Players", "Teams"],
                icons = ["house","person", "people"]
        )

if selected == "Home":
        st.title("Fantasy Premier League Tracker")

# players stats search 

if selected == "Players":
        st.title("Players Search")
        

        st.write("Players List")
        result = st.selectbox("Enter player name:", player_list)



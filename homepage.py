import streamlit as st
import pandas as pd

# web scraping / api 
from PIL import Image

import requests
import json

stats_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

response = requests.get(stats_url)

if response.status_code == 200:

        fpl_data = json.loads(response.text) # Parse the JSON content of the API response

        player_stats = fpl_data['elements']

        #player list (sort and unsort)
        unsorted_player_list = []
        for player in player_stats:
                unsorted_player_list.append(player['first_name'] + " " + player['second_name'])
        
        sorted_player_list = []
        for player in player_stats:
                sorted_player_list.append(player['first_name'] + " " + player['second_name'])
        sorted_player_list.sort()

        # teams_list
        teams_list = []
        for teams in fpl_data["teams"]:
                teams_list.append(teams['name'])

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
        

        st.write("Players List") # search player 
        player_searched = st.selectbox("Enter player name:", sorted_player_list)
        
        #find player num in list
        searched_player_num = ''
        temp = 0
        for player in unsorted_player_list:
                if player == player_searched:
                        searched_player_num = temp
                else:
                        temp += 1 

        searched_player_id = player_stats[searched_player_num]['id'] # get player id in fpl data

        individual_url = f"https://fantasy.premierleague.com/api/element-summary/{searched_player_id}/" # transfer the data

        individual_response = requests.get(individual_url)

        if response.status_code == 200:

                individual_player_data = json.loads(individual_response.text) # Parse the JSON content of the API response

        else:
                print(f"Failed to retrieve FPL data. Status code: {response.status_code}")

        individual_player_match_data = individual_player_data['history']

        # first column 

        colA1, colA2, colA3 = st.columns ((3,4,3))
        # display player image 
        # first column 
        with colA1:
                player_code = player_stats[searched_player_num]['code']
        
                player_image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{player_code}.png"

                st.image(player_image_url, width = 140)

        # position getter function 
        def position_getter(num):
                if num == 1:
                        return "Goalkeeper"
                elif num == 2:
                        return "Defender"
                elif num == 3:
                        return "Midfielder"
                else:
                        return "Forward"

        #visualise details
        with colA2: 
                st.subheader(unsorted_player_list[searched_player_num]) # name
                st.write(f"Position: {position_getter(player_stats[searched_player_num]['element_type'])}") #positon
                st.write(f"Team: {teams_list[player_stats[searched_player_num]['team'] - 1]}")
                st.write(f"Minutes Played: {player_stats[searched_player_num]['minutes']} Minutes")

        with colA3:
                st.subheader("\n")
                st.write(f"Goals: {player_stats[searched_player_num]['goals_scored']} ")
                st.write(f"Assists: {player_stats[searched_player_num]['assists']} ")
                st.write(f"Clean Sheets: {player_stats[searched_player_num]['clean_sheets']} ")
                st.write(f"Total Points: {player_stats[searched_player_num]['total_points']} ")

        #second column 

        colB1, colB2, colB3 = st.columns (3)

        # player price 
        colB1.metric("Price", f"£{player_stats[searched_player_num]['now_cost'] / 10}")

        # ownership change numbers 
        ownership_change_overall = (individual_player_match_data[-2]['selected'])
        ownership_change_percentage = (individual_player_match_data[-1]['selected'] - ownership_change_overall )/ ownership_change_overall * 100
        colB2.metric("Ownership Percentage" , f"{player_stats[searched_player_num]['selected_by_percent']}%" , f"{round(ownership_change_percentage , 2)}%")

        #points per game 
        colB3.metric("Points Per Game", player_stats[searched_player_num]['points_per_game'])

        # visualise overall data

        #player_overall_data = player_stats[searched_player_num]

        #player_overall_df = pd.DataFrame(player_overall_data, index=[0])
        #player_overall_df = player_overall_df.T

        #st.write(player_overall_df)
        


        



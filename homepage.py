import streamlit as st
import pandas as pd

# web scraping / api 
from PIL import Image

import requests
import json
import plotly.express as px 

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

        # short form 
        short_teams_list = []
        for teams in fpl_data["teams"]:
                short_teams_list.append(teams['short_name'])

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
                options = ["Home" , "Players Detailed", "Teams / Fixtures", "Player Rankings", "Team Builder"],
                icons = ["house","person", "people", "bar-chart-fill", "cone-striped"]
        )

if selected == "Home":
        st.title("Fantasy Premier League Tracker")

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


# players stats search 

if selected == "Players Detailed":
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

        # points graph 
        player_points_overall_data = {}
        player_opponent_list = []
        player_points_list = []
        gameweek_count = []
        temp = 1

        for gameweek in individual_player_match_data: 
                player_opponent_list.append(short_teams_list[gameweek['opponent_team'] - 1])
                player_points_list.append(gameweek['total_points'])
                gameweek_count.append(gameweek['round'])
                temp += 1 

        player_points_overall_data = { 
                'Opponents' : player_opponent_list,
                'Points' : player_points_list,
                'Gameweek' : gameweek_count
        }

        individual_points_df = pd.DataFrame(player_points_overall_data)
        player_points_fig = px.scatter(individual_points_df, x = 'Gameweek', y = 'Points', text = 'Opponents', title = 'Points Change Graph')
        player_points_fig.add_trace(px.line(individual_points_df, x = 'Gameweek', y = 'Points').data[0])
        st.plotly_chart(player_points_fig)

        # price graph 
        player_price_overall_data = {}
        player_price_list = []
        temp = 0

        for gameweek in individual_player_match_data:
                temp = gameweek['value']
                temp = temp / 10 
                player_price_list.append(temp)

        player_price_overall_data = { 
                'Gameweek' : gameweek_count,
                'Price' : player_price_list
        }

        individual_price_df = pd.DataFrame(player_price_overall_data)
        player_price_fig = px.scatter(individual_price_df, x = 'Gameweek', y = 'Price', title = 'Price Change Graph')
        player_price_fig.add_trace(px.line(individual_price_df, x = 'Gameweek', y = 'Price').data[0])
        st.plotly_chart(player_price_fig)

        # selection graph 
        player_selection_overall_data = {}
        player_selection_list = []
        
        for gameweek in individual_player_match_data:
                player_selection_list.append(gameweek['selected'])

        player_selection_overall_data = {
                'Selected' : player_selection_list,
                'Gameweek': gameweek_count
        }

        individual_selection_df = pd.DataFrame(player_selection_overall_data)
        player_selection_fig = px.scatter(individual_selection_df, x = 'Gameweek', y = 'Selected', title = 'Selected by Users Number Graph')
        player_selection_fig.add_trace(px.line(individual_selection_df, x = 'Gameweek', y = 'Selected').data[0])
        st.plotly_chart(player_selection_fig)


if selected == "Teams / Fixtures":
        st.title ("Teams List")

        # Club Picker
        teams_searched = st.selectbox("Enter Club name:", teams_list)

        club_num = teams_list.index(teams_searched)
        team_data = fpl_data['teams'][club_num]

        #find team num in list
        colC1, colC2  = st.columns ((6,4))
        with colC1:
                team_code = team_data['code']
        
                team_image_url = f"https://resources.premierleague.com/premierleague/badges/100/t{team_code}.png"

                st.image(team_image_url, width = 150)

        with colC2 :
                st.title(team_data['name'])
        
        st.title('')

        st.subheader(f"{team_data['name']} Players on Top Form")
        st.title('')

        team_detailed_data = {}

        for players in player_stats:

                if players['team_code'] == team_code:

                        team_detailed_data [players['first_name'] + " " + players['second_name']] = players

        sorted_team_detailed_form_data = dict(sorted(team_detailed_data.items(), key=lambda item: item[1]['form'], reverse=True))

        # get players code

        sorted_player_key_list = list(sorted_team_detailed_form_data.keys())

        first_player = sorted_player_key_list[0]
        second_player = sorted_player_key_list[1]
        third_player = sorted_player_key_list[2]

        # first player 

        colD1, colD2, colD3  = st.columns ((2,4,4))

        # first player image 
        with colD1:
                st.subheader('1.')
        with colD2:

                first_player_image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{sorted_team_detailed_form_data[first_player]['code']}.png"

                st.image(first_player_image_url, width = 180)

        # first player details 
        with colD3: 
                st.subheader(sorted_team_detailed_form_data[first_player]['first_name'] + " " + sorted_team_detailed_form_data[first_player]['second_name']) # name
                st.write(f"Position: {position_getter(sorted_team_detailed_form_data[first_player]['element_type'])}") #positon
                st.write(f"Form: {sorted_team_detailed_form_data[first_player]['form']}")
                st.write(f"Price: {sorted_team_detailed_form_data[first_player]['now_cost'] / 10}")

        # second player 

        st.title('')

        colE1, colE2, colE3  = st.columns ((2,4,4))

        # second player image 
        with colE1:
                st.subheader('2.')
        with colE2:

                second_player_image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{sorted_team_detailed_form_data[second_player]['code']}.png"

                st.image(second_player_image_url, width = 180)

        # second player details 
        with colE3: 
                st.subheader(sorted_team_detailed_form_data[second_player]['first_name'] + " " + sorted_team_detailed_form_data[second_player]['second_name']) # name
                st.write(f"Position: {position_getter(sorted_team_detailed_form_data[second_player]['element_type'])}") #positon
                st.write(f"Form: {sorted_team_detailed_form_data[second_player]['form']}")
                st.write(f"Price: {sorted_team_detailed_form_data[second_player]['now_cost'] / 10}")

        # third player 

        st.title('')

        colF1, colF2, colF3  = st.columns ((2,4,4))

        # third player image 
        with colF1:
                st.subheader('3.')
        with colF2:

                third_player_image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{sorted_team_detailed_form_data[third_player]['code']}.png"

                st.image(third_player_image_url, width = 180)

        # third player details 
        with colF3: 
                st.subheader(sorted_team_detailed_form_data[third_player]['first_name'] + " " + sorted_team_detailed_form_data[third_player]['second_name']) # name
                st.write(f"Position: {position_getter(sorted_team_detailed_form_data[third_player]['element_type'])}") #positon
                st.write(f"Form: {sorted_team_detailed_form_data[third_player]['form']}")
                st.write(f"Price: {sorted_team_detailed_form_data[third_player]['now_cost'] / 10}")

        st.title('')

        # fixtures data

        st.subheader(f"{team_data['name']} Upcoming Fixtures")

        fixtures_url = "https://fantasy.premierleague.com/api/fixtures/?future=1" # transfer the data

        fixtures_response = requests.get(fixtures_url)

        if response.status_code == 200:

                fixtures_data = json.loads(fixtures_response.text) # Parse the JSON content of the API response

        else:
                print(f"Failed to retrieve FPL data. Status code: {response.status_code}")

        overall_team_fixtures_data = {}

        team_id = team_data['id']

        for match in fixtures_data:
                if match['team_a'] == team_id or match['team_h'] == team_id:
                        overall_team_fixtures_data[match['event']] = match

        def home_away(dict, team_id): # get home or away
                if dict['team_a'] == team_id:
                        return 'Away'
                else:
                        return 'Home'

        
        def opponent_team_getter(dict, team_id): # get opponenet team
                if dict['team_a'] == team_id:
                        return dict['team_h']
                else:
                        return dict['team_a']

        def opponent_team_level_getter(dict, team_id): # get opponenet team level
                if dict['team_a'] == team_id:
                        return dict['team_a_difficulty']
                else:
                        return dict['team_h_difficulty']


        filter_dict = {}
        temp = 0 

        for match, data in overall_team_fixtures_data.items():
                
                filter_dict[data['event']] = {
                        'Gameweek' : data['event'],
                        'Opponent' : short_teams_list[opponent_team_getter(data, team_id) - 1],
                        'Home / Away' : home_away(data, team_id),
                        'Difficulty Level' : (opponent_team_level_getter(data, team_id)),
                        'Photo_Code' : fpl_data['teams'][opponent_team_getter(data, team_id) - 1]['code']
                 }

        # get reference keys right 
        keys_temp = []
        for key in  filter_dict.keys():
                keys_temp.append(key)

        keys_temp = keys_temp[:5]
        
        
        # display fixtures
        colG1, colG2, colG3, colG4, colG5  = st.columns ((2,2,2,2,2))
        

        with colG1:
                if keys_temp[0] == '':
                        st.write('')
                else:
                        club_fixture1_image_url = f"https://resources.premierleague.com/premierleague/badges/100/t{filter_dict[keys_temp[0]]['Photo_Code']}.png"
                        st.write('')
                        st.image(club_fixture1_image_url, width = 140)
                        st.write(f'Gameweek: {filter_dict[keys_temp[0]]["Gameweek"]}') 
                        st.write(f'{filter_dict[keys_temp[0]]["Opponent"]} ({filter_dict[keys_temp[0]]["Home / Away"]})') 
                        st.write(f'Difficulty Level: {filter_dict[keys_temp[0]]["Difficulty Level"]}') 

        with colG2:
                if keys_temp[1] == '':
                        st.write('')
                else:
                        club_fixture1_image_url = f"https://resources.premierleague.com/premierleague/badges/100/t{filter_dict[keys_temp[1]]['Photo_Code']}.png"
                        st.write('')
                        st.image(club_fixture1_image_url, width = 140)
                        st.write(f'Gameweek: {filter_dict[keys_temp[1]]["Gameweek"]}')
                        st.write(f'VS {filter_dict[keys_temp[1]]["Opponent"]} ({filter_dict[keys_temp[1]]["Home / Away"]})') 
                        st.write(f'Difficulty Level: {filter_dict[keys_temp[1]]["Difficulty Level"]}') 

        with colG3:
                if keys_temp[2] == '':
                        st.write('')
                else:
                        club_fixture1_image_url = f"https://resources.premierleague.com/premierleague/badges/100/t{filter_dict[keys_temp[2]]['Photo_Code']}.png"
                        st.write('')
                        st.image(club_fixture1_image_url, width = 140)
                        st.write(f'Gameweek: {filter_dict[keys_temp[2]]["Gameweek"]}')
                        st.write(f'VS {filter_dict[keys_temp[2]]["Opponent"]} ({filter_dict[keys_temp[2]]["Home / Away"]})') 
                        st.write(f'Difficulty Level: {filter_dict[keys_temp[2]]["Difficulty Level"]}') 

        with colG4:
                if keys_temp[3] == '':
                        st.write('')
                else:
                        club_fixture1_image_url = f"https://resources.premierleague.com/premierleague/badges/100/t{filter_dict[keys_temp[3]]['Photo_Code']}.png"
                        st.write('')
                        st.image(club_fixture1_image_url, width = 140)
                        st.write(f'Gameweek: {filter_dict[keys_temp[3]]["Gameweek"]}')
                        st.write(f'VS {filter_dict[keys_temp[3]]["Opponent"]} ({filter_dict[keys_temp[3]]["Home / Away"]})') 
                        st.write(f'Difficulty Level: {filter_dict[keys_temp[3]]["Difficulty Level"]}') 

        with colG5:
                if keys_temp[4] == '':
                        st.write('')
                else:
                        club_fixture1_image_url = f"https://resources.premierleague.com/premierleague/badges/100/t{filter_dict[keys_temp[4]]['Photo_Code']}.png"
                        st.write('')
                        st.image(club_fixture1_image_url, width = 140)
                        st.write(f'Gameweek: {filter_dict[keys_temp[4]]["Gameweek"]}')
                        st.write(f'VS {filter_dict[keys_temp[4]]["Opponent"]} ({filter_dict[keys_temp[4]]["Home / Away"]})') 
                        st.write(f'Difficulty Level: {filter_dict[keys_temp[4]]["Difficulty Level"]}') 


        # fixtures graph
        st.title('')
        st.subheader(f"{team_data['name']} Fixtures Difficulty Bar Chart")
        difficulty_list = []
        gameweek_list = []

        for keys, values in filter_dict.items():
                gameweek_list.append(values['Gameweek'])
                difficulty_list.append(values['Difficulty Level'])

        display_fixtures_dict = {
                "Gameweek" : gameweek_list,
                'Difficulty Level' : difficulty_list 
        }
                

        fixtures_df = pd.DataFrame(display_fixtures_dict)
        fixtures_fig = px.bar(fixtures_df, x = 'Gameweek', y = 'Difficulty Level')
        st.plotly_chart(fixtures_fig)







        



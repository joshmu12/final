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

        # team short form 
        short_teams_list = []
        for teams in fpl_data["teams"]:
                short_teams_list.append(teams['short_name'])

        # goalkeeper list
        goalkeeper_details_list = []
        sorted_goalkeeper_name_list = []
        unsorted_goalkeeper_name_list = []
        for player in player_stats:
                if player['element_type'] == 1:
                        goalkeeper_details_list.append(player)
                        sorted_goalkeeper_name_list.append(player['first_name'] + " " + player['second_name'])
                        unsorted_goalkeeper_name_list.append(player['first_name'] + " " + player['second_name'])
        sorted_goalkeeper_name_list.sort()
        goalkeeper_details_list.insert(0,'None')
        sorted_goalkeeper_name_list.insert(0,'None')
        unsorted_goalkeeper_name_list.insert(0,'None')

        # defender list
        defender_details_list = []
        sorted_defender_name_list = []
        unsorted_defender_name_list = []
        for player in player_stats:
                if player['element_type'] == 2:
                        defender_details_list.append(player)
                        sorted_defender_name_list.append(player['first_name'] + " " + player['second_name'])
                        unsorted_defender_name_list.append(player['first_name'] + " " + player['second_name'])
        sorted_defender_name_list.sort()
        defender_details_list.insert(0,'None')
        sorted_defender_name_list.insert(0,'None')
        unsorted_defender_name_list.insert(0,'None')

        # midfielder list
        midfielder_details_list = []
        sorted_midfielder_name_list = []
        unsorted_midfielder_name_list = []
        for player in player_stats:
                if player['element_type'] == 3:
                        midfielder_details_list.append(player)
                        sorted_midfielder_name_list.append(player['first_name'] + " " + player['second_name'])
                        unsorted_midfielder_name_list.append(player['first_name'] + " " + player['second_name'])
        sorted_midfielder_name_list.sort()
        midfielder_details_list.insert(0,'None')
        sorted_midfielder_name_list.insert(0,'None')
        unsorted_midfielder_name_list.insert(0,'None')

        # forward list
        forward_details_list = []
        sorted_forward_name_list = []
        unsorted_forward_name_list = []
        for player in player_stats:
                if player['element_type'] == 4:
                        forward_details_list.append(player)
                        sorted_forward_name_list.append(player['first_name'] + " " + player['second_name'])
                        unsorted_forward_name_list.append(player['first_name'] + " " + player['second_name'])
        sorted_forward_name_list.sort()
        forward_details_list.insert(0,'None')
        sorted_forward_name_list.insert(0,'None')
        unsorted_forward_name_list.insert(0,'None')

        #fixtures
        fixtures_url = "https://fantasy.premierleague.com/api/fixtures/?future=1" # transfer the data

        fixtures_response = requests.get(fixtures_url)

        if response.status_code == 200:

                fixtures_data = json.loads(fixtures_response.text) # Parse the JSON content of the API response

        else:
                print(f"Failed to retrieve FPL data. Status code: {response.status_code}")

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
                menu_title = "Fantasy Premier League Tracker",
                options = ["Home" , "Players Detailed", "Teams / Fixtures", "Player Rankings", "Team Builder", "User Info"],
                icons = ["house", "people", "calendar-event", "bar-chart-fill", "cone-striped", "person-circle"]
        )


if selected == "Home":
        st.title("Fantasy Premier League Tracker")

        colU1, colU2 = st.columns((4,6))
        with colU1:
                st.image("https://www.premierleague.com/resources/rebrand/v7.137.1/i/elements/pl-main-logo.png", width = 150)
        with colU2:
                st.title('')
                st.write(f"This is a very legitimate tracker for Fantasy Premier League")
                st.write("Created by Joshua Hung")

        st.title('')
        st.title("Functions")
        st.title('')

        colV1, colV2 = st.columns((4,6))
        with colV1:
                st.image("https://static.vecteezy.com/system/resources/previews/010/159/990/original/people-icon-sign-symbol-design-free-png.png", width = 200)
        with colV2:
                st.subheader("Players Detailed")
                st.write('Able to check every detail stat of every single player in the Premier League, such as goals, assists, Fantasy price and etc.')

        st.title('')

        colW1, colW2 = st.columns((4,6))
        with colW1:
                st.image("https://static.vecteezy.com/system/resources/previews/005/988/959/original/calendar-icon-free-vector.jpg", width = 200)
        with colW2:
                st.subheader("Teams / Fixtures")
                st.write("Every team's hottest performing players can be acessed here. Fixtures can also be checked alongside the diffuculty fixture graph of the team.")

        st.title('')

        colX1, colX2 = st.columns((4,6))
        with colX1:
                st.image("https://www.shareicon.net/data/512x512/2015/12/01/680764_graph_512x512.png", width = 200)
        with colX2:
                st.subheader("Player Rankings")
                st.write("Top 10 players of any respective stat can be foundh here, such as price and goals. Their clubs and numbers for the respective stat is also shown.")

        st.title('')

        colY1, colY2 = st.columns((4,6))
        with colY1:
                st.image("https://us.123rf.com/450wm/puruan/puruan1701/puruan170101084/70489434-road-sign-cone-icon-in-single-color-danger-forbidden-plastic-transportation.jpg", width = 200)
        with colY2:
                st.subheader("Team Builder")
                st.write("Users can build their own team with every player possible in the Premier League. The built team's price and average points will be shown.")

        st.title('')

        colZ1, colZ2 = st.columns((4,6))
        with colZ1:
                st.image("https://static-00.iconduck.com/assets.00/person-circle-icon-2048x2048-7dykp8p2.png", width = 200)
        with colZ2:
                st.subheader("User Info")
                st.write("Users can track their own FPL stats. Users can also have access to their past week teams, and compare the points difference.")

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
                st.write(f"Price: £{sorted_team_detailed_form_data[first_player]['now_cost'] / 10}")

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
                st.write(f"Form: {sorted_team_detailed_form_data[second_player]['form']}") # buenos dias mr park 디즈 너트
                st.write(f"Price: £{sorted_team_detailed_form_data[second_player]['now_cost'] / 10}")

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
                st.write(f"Price: £{sorted_team_detailed_form_data[third_player]['now_cost'] / 10}")

        st.title('')

        # fixtures data

        st.subheader(f"{team_data['name']} Upcoming Fixtures")

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
                        st.write(f'VS {filter_dict[keys_temp[0]]["Opponent"]} ({filter_dict[keys_temp[0]]["Home / Away"]})') 
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
        opponent_list = []

        for keys, values in filter_dict.items():
                gameweek_list.append(values['Gameweek'])
                difficulty_list.append(values['Difficulty Level'])
                opponent_list.append(values['Opponent'])

        display_fixtures_dict = {
                "Gameweek" : gameweek_list,
                'Difficulty Level' : difficulty_list ,
                'Opponent' : opponent_list
        }
                

        fixtures_df = pd.DataFrame(display_fixtures_dict)
        fixtures_fig = px.bar(fixtures_df, x = 'Gameweek', y = 'Difficulty Level', text = 'Opponent')
        fixtures_fig.update_layout(font = dict(size = 20))
        st.plotly_chart(fixtures_fig)




if selected == "Team Builder":
        
        #formations 
        team_builder_team_details = []

        formations_dict = {
                '3 4 3' : {'Defender' : 3, 'Midfielder' : 4, 'Forward' : 3},
                '3 5 2' : {'Defender' : 3, 'Midfielder' : 5, 'Forward' : 2},
                '4 3 3' : {'Defender' : 4, 'Midfielder' : 3, 'Forward' : 3},
                '4 4 2' : {'Defender' : 4, 'Midfielder' : 4, 'Forward' : 2},
                '4 5 1' : {'Defender' : 4, 'Midfielder' : 5, 'Forward' : 1},
                '5 3 2' : {'Defender' : 5, 'Midfielder' : 3, 'Forward' : 2},
                '5 4 1' : {'Defender' : 5, 'Midfielder' : 4, 'Forward' : 1}
        }

        formations_list = []

        for formations in formations_dict.keys():
                formations_list.append(formations)

        user_formation = st.selectbox("Choose desired formation:" , formations_list)

        user_formation = formations_dict[user_formation]

        # remaining money for user 

        user_bank = 100

        # form 

        user_team_form = 0

        # average points per game

        user_team_average_points = 0 

        user_goalkeeper = 0

        filler1, goalkeeper_grid ,filler2  = st.columns ((4,2,4))
        #goalkeeper
        with goalkeeper_grid:
                goalkeeper = '1'
                
                player_searched_team_builder = st.selectbox("Enter player name:", sorted_goalkeeper_name_list, key = goalkeeper)

                if player_searched_team_builder == 'None':
                        goalkeeper_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_0_1-66.webp"
                        st.image(goalkeeper_jersey_url, width=70)
                        st.write("N/A") # web name
                        st.write("£0") # price 
                else:
                        #find player num in list
                        searched_player_num = 0
                        temp = 0

                        for player in unsorted_goalkeeper_name_list:
                                if player == player_searched_team_builder:
                                        searched_player_num = temp
                                else:
                                        temp += 1 

                        player_team_code = goalkeeper_details_list[searched_player_num]['team_code'] # get team id 

                        goalkeeper_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{player_team_code}_1-66.webp"
                        #jersey photo
                        st.image(goalkeeper_jersey_url, width=70)
                        st.write(goalkeeper_details_list[searched_player_num]['web_name']) # web name
                        st.write(f"£{goalkeeper_details_list[searched_player_num]['now_cost'] / 10}") # price 
                        user_goalkeeper = goalkeeper_details_list[searched_player_num]

        #defenders      
        defender_columns = st.columns (user_formation['Defender'])

        def defender_player_builder (player_search_key, number):
                player_searched_team_builder = st.selectbox("Enter player name:", sorted_defender_name_list, key = player_search_key)

                if player_searched_team_builder == 'None':
                        defender_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_0-66.webp"
                        st.image(defender_jersey_url, width=70)
                        st.write("N/A") # web name
                        st.write("£0") # price 
                else:
                        #find player num in list
                        searched_player_num = 0
                        temp = 0

                        for player in unsorted_defender_name_list:
                                if player == player_searched_team_builder:
                                        searched_player_num = temp
                                else:
                                        temp += 1 

                        player_team_code = defender_details_list[searched_player_num]['team_code'] # get team id 

                        defender_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{player_team_code}-66.webp"
                        #jersey photo
                        st.image(defender_jersey_url, width=70)
                        st.write(defender_details_list[searched_player_num]['web_name']) # web name
                        st.write(f"£{defender_details_list[searched_player_num]['now_cost'] / 10}") # price
                        user_defender [number] = defender_details_list[searched_player_num]

        user_defender = [0]*5
        for i, defender_grid in enumerate(defender_columns):
                if i == 0 : 
                        with defender_grid:
                                defender1 = 'defender1'
                                def_1 = 0
                                defender_player_builder(defender1, def_1)

                if i == 1 : 
                        with defender_grid:
                                defender2 = 'defender2'
                                def_2 = 1
                                defender_player_builder(defender2, def_2)
                
                if i == 2 : 
                        with defender_grid:
                                defender3 = 'defender3'
                                def_3 = 2
                                defender_player_builder(defender3, def_3)
                
                if i == 3 : 
                        with defender_grid:
                                defender4 = 'defender4'
                                def_4 = 3
                                defender_player_builder(defender4 ,def_4)

                if i == 4 : 
                        with defender_grid:
                                defender5 = 'defender5'
                                def_5 = 4
                                defender_player_builder(defender5, def_5)
       
        #midfielders 
        midfielder_columns = st.columns (user_formation['Midfielder'])

        def midfielder_player_builder (player_search_key, number):
                player_searched_team_builder = st.selectbox("Enter player name:", sorted_midfielder_name_list, key = player_search_key)

                if player_searched_team_builder == 'None':
                        midfielder_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_0-66.webp"
                        st.image(midfielder_jersey_url, width=70)
                        st.write("N/A") # web name
                        st.write("£0") # price 
                else:
                        #find player num in list
                        searched_player_num = 0
                        temp = 0

                        for player in unsorted_midfielder_name_list:
                                if player == player_searched_team_builder:
                                        searched_player_num = temp
                                else:
                                        temp += 1 

                        player_team_code = midfielder_details_list[searched_player_num]['team_code'] # get team id 

                        midfielder_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{player_team_code}-66.webp"
                        #jersey photo
                        st.image(midfielder_jersey_url, width=70)
                        st.write(midfielder_details_list[searched_player_num]['web_name']) # web name
                        st.write(f"£{midfielder_details_list[searched_player_num]['now_cost'] / 10}") # price
                        user_midfielder [number] = midfielder_details_list[searched_player_num]

        user_midfielder = [0] * 5 
        for i, midfielder_grid in enumerate(midfielder_columns):
                if i == 0 : 
                        with midfielder_grid:
                                midfielder1 = 'midfielder1'
                                mid_1 = 0
                                midfielder_player_builder(midfielder1, mid_1)

                if i == 1 : 
                        with midfielder_grid:
                                midfielder2 = 'midfielder'
                                mid_2 = 1
                                midfielder_player_builder(midfielder2, mid_2)
                
                if i == 2 : 
                        with midfielder_grid:
                                midfielder3 = 'midfielder3'
                                mid_3 = 2
                                midfielder_player_builder(midfielder3, mid_3)
                
                if i == 3 : 
                        with midfielder_grid:
                                midfielder4 = 'midfielder4'
                                mid_4 = 3
                                midfielder_player_builder(midfielder4, mid_4)

                if i == 4 : 
                        with midfielder_grid:
                                midfielder5 = 'midfielder5'
                                mid_5 = 4
                                midfielder_player_builder(midfielder5, mid_5)
                

        #forwards
        if user_formation['Forward'] == 1:
                forward_columns = st.columns ((4,2,4))
        else:
                forward_columns = st.columns (user_formation['Forward'])

        def forward_player_builder (player_search_key, number):
                player_searched_team_builder = st.selectbox("Enter player name:", sorted_forward_name_list, key = player_search_key)

                if player_searched_team_builder == 'None':
                        forward_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_0-66.webp"
                        st.image(forward_jersey_url, width=70)
                        st.write("N/A") # web name
                        st.write("£0") # price 
                else:
                        #find player num in list
                        forward_searched_player_num = 0
                        temp = 0

                        for player in unsorted_forward_name_list:
                                if player == player_searched_team_builder:
                                        forward_searched_player_num = temp
                                else:
                                        temp += 1 

                        player_team_code = forward_details_list[forward_searched_player_num]['team_code'] # get team id 

                        forward_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{player_team_code}-66.webp"
                        #jersey photo
                        st.image(forward_jersey_url, width=70)
                        st.write(forward_details_list[forward_searched_player_num]['web_name']) # web name
                        st.write(f"£{forward_details_list[forward_searched_player_num]['now_cost'] / 10}") # price
                        user_forward [number] = forward_details_list[forward_searched_player_num]

        user_forward = [0] * 3 

        for i, forward_grid in enumerate(forward_columns):
                if i == 0 : 
                        if user_formation['Forward'] == 1:
                                continue
                        else:
                                with forward_grid:
                                                forward1 = 'forward1'
                                                for_1 = 0
                                                forward_player_builder(forward1, for_1)


                if i == 1 : 
                        with forward_grid:
                                forward2 = 'forward2'
                                for_2 = 1
                                forward_player_builder(forward2,for_2)
                
                if i == 2 : 
                        if user_formation['Forward'] == 1:
                                continue
                        with forward_grid:
                                        forward3 = 'forward3'
                                        for_3 = 2
                                        forward_player_builder(forward3, for_3)

        complete_user_team = []
        abc = 0

        for player in user_defender:
                if player == 0:
                        continue
                complete_user_team.append(player)
        for player in user_midfielder:
                if player == 0:
                        continue
                complete_user_team.append(player)
        for player in user_forward:
                if player == 0:
                        continue
                complete_user_team.append(player)
        if user_goalkeeper == 0:
                abc = 0
        else:               
                complete_user_team.append(user_goalkeeper)


        # remaining money 
        for price in complete_user_team:
                if price == 0:
                        user_bank = 100
                else:
                        user_bank = user_bank - (price['now_cost'] /10)
        temp_form = 0
        # form 
        for form in complete_user_team:
        
                if form == 0:
                        user_team_form = 0 
                else:
                        temp_form = float(form['form'])
                        user_team_form = user_team_form + temp_form

        # average points
        temp_points = 0
        for points in complete_user_team:
                if points == 0:
                        user_team_average_points = 0 
                else:
                        temp_points = float(points['total_points'])
                        user_team_average_points =  user_team_average_points + temp_points
        
        current_gameweek = fixtures_data[0]['event'] - 1 
        user_team_average_points = user_team_average_points / current_gameweek

        # metrics 

        colH1, colH2, colH3 = st.columns (3) 

        current_gameweek = fixtures_data[0]['event'] - 1 

        # average price
        colH1.metric("Remaining Money", f"£{round(user_bank, 1)}")

        # form
        colH2.metric("Team Form", f"{round(user_team_form , 2)}")

        #points per game for whole team
        colH3.metric("Points Per Gameweek (Team)", round(user_team_average_points ))
        
if selected == "Player Rankings":

        st.title("Rankings by Categories")

        categories_dict = {
                'Price' : 'now_cost',
                'Goals' : 'goals_scored',
                'Assists' : 'assists',
                'Clean Sheets': 'clean_sheets',
                'Saves' : 'saves',
                'Minutes Played' : 'minutes',
                'Points' : 'total_points',
                'Points per Game' : 'points_per_game',
                'Most Transferred In' : 'transfers_in_event',
                'Most Transferred Out' : 'transfers_out_event',
                'Expected Goals' : 'expected_goals_per_90',
                'Expected Assists' : 'expected_assists_per_90',
                'Expected Goal Involvements' : 'expected_goal_involvements_per_90',
                'Form' : 'form',
                'Most Bonus Points' : 'bonus',
                'Yellow Cards' : 'yellow_cards',
                'Red Cards' : 'red_cards',
                'ICT Index' : 'ict_index'
        }

        categories_list = []

        for categories in categories_dict.keys():
                categories_list.append(categories)

        categories_searched = st.selectbox('Categories Ranking:', categories_list)

        later_use = ''

        later_use = categories_searched

        categories_searched = categories_dict[categories_searched]

        prevent_string_dict = {}

        prevent_string_dict = player_stats

        for player in prevent_string_dict:
                player['ict_index'] = float(player['ict_index'])

        sorted_specific_category_data = sorted(prevent_string_dict, key=lambda x: x[categories_searched], reverse = True)
        st.title('')
        st.title('')

        #player details
        def visualise_player (ranking, column1, column2, column3):

                with column1:
                        st.subheader(f"{ranking + 1}.")

                with column2:
                        player_image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{sorted_specific_category_data[ranking]['code']}.png"

                        st.image(player_image_url, width = 180)

                with column3:
                        # player details 
                        st.subheader(sorted_specific_category_data[ranking]['first_name'] + " " + sorted_specific_category_data[ranking]['second_name']) # name
                        st.write(f"Position: {position_getter(sorted_specific_category_data[ranking]['element_type'])}") #positon
                        st.write(f"Club: {teams_list[sorted_specific_category_data[ranking]['team'] - 1]}")
                        st.write(f"Price: £{sorted_specific_category_data[ranking]['now_cost'] / 10}")

                        if later_use != 'Price' :
                                st.write(f"{later_use}: {sorted_specific_category_data[ranking][categories_searched]}")


        #columns

        columns = ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']

        for col in columns:
                globals()[f'col{col}1'], globals()[f'col{col}2'], globals()[f'col{col}3'] = st.columns((2, 4, 4))
                st.title('')

        #visualising

        temp = 0 
        for index, col in enumerate(columns):
                visualise_player(index, globals()[f'col{col}1'], globals()[f'col{col}2'], globals()[f'col{col}3'])

if selected == 'User Info':
        st.title("User Info ")

        user_id = st.number_input("Enter your user number (Can be found on your teams page): ", min_value = 0)

        if user_id != 0:
                
                user_link = f"https://fantasy.premierleague.com/api/entry/{user_id}/"

                user_response = requests.get(user_link)

                if user_response.status_code == 200:

                        user_overall_data = json.loads(user_response.text) #parse json

                        colS1, colS2, colS3 = st.columns ((3))

                        with colS1:

                                fav_team_code = user_overall_data['favourite_team']

                                for teams in fpl_data['teams']:

                                        if fav_team_code == teams['id']:
                                                fav_team_code = teams['code']

                                team_image_url = f"https://resources.premierleague.com/premierleague/badges/100/t{fav_team_code}.png"

                                st.image(team_image_url, width = 120)


                        with colS2:

                                st.write(f"User Name: {user_overall_data['player_first_name']} {user_overall_data['player_last_name']}")
                                st.write(f"User Region: {user_overall_data['player_region_name']}")
                                st.write(f"Active Years: {user_overall_data['years_active']} ")

                        with colS3:

                                st.write(f"Overall Points: {user_overall_data['summary_overall_points']}")
                                st.write(f"Overall Rank: {user_overall_data['summary_overall_rank']}")
                                st.write(f"Current Gameweek Points: {user_overall_data['summary_event_points']}")

                        st.title("Team Points")

                        gameweek_number = st.number_input("Enter the Gameweek to be checked: ", min_value = 1, max_value = user_overall_data['current_event'] )

                        gameweek_check_link = f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{gameweek_number}/picks/"

                        if gameweek_number != 1:
                                difference_gameweek = f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{gameweek_number - 1}/picks/"

                                difference_gameweek_response = requests.get(difference_gameweek)

                                if difference_gameweek_response.status_code == 200:

                                        difference_gameweek_data = json.loads(difference_gameweek_response.text)

                        user_gameweek_response = requests.get(gameweek_check_link)

                        if user_gameweek_response.status_code == 200:

                                user_gameweek_data = json.loads(user_gameweek_response.text)
                                

                        else:
                                st.write('User ID not found, please re-enter.')

                        user_players = []

                        user_players_detailed = []

                        captain = []

                        for players in user_gameweek_data['picks'][:11]:

                                user_players.append(players['element'])

                        for players in user_players:

                                for player in player_stats:

                                        if players == player['id']:

                                                user_players_detailed.append(player)

                        for players in user_gameweek_data['picks'][:11]:
                                captain.append(players['is_captain'])

                        position_count = {
                                'Defenders' : 0,
                                'Midfielders' : 0,
                                'Forward' : 0
                        }

                        for player in user_players_detailed:

                                if player['element_type'] == 2:
                                        position_count['Defenders'] += 1
                                elif player['element_type'] == 3:
                                        position_count['Midfielders'] += 1
                                elif player['element_type'] == 4:
                                        position_count['Forward'] += 1

                        st.subheader(user_overall_data['name'])

                        def player_visualise (number):

                                individual_url = f"https://fantasy.premierleague.com/api/element-summary/{user_players_detailed[number]['id']}/" # transfer the data

                                individual_response = requests.get(individual_url)

                                if response.status_code == 200:

                                        individual_player_data = json.loads(individual_response.text) # Parse the JSON content of the API response
                                else:
                                        print("Player cannot be found")

                                if user_players_detailed[number]['element_type'] == 1:
                                        player_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{user_players_detailed[number]['team_code']}_1-66.webp"
                                else:
                                        player_jersey_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{user_players_detailed[number]['team_code']}-66.webp"

                                st.image(player_jersey_url, width = 70)
                                if captain[number] == True:

                                        st.write(f"{user_players_detailed[number]['web_name']} (C)") # web name
                                else:
                                        st.write(f"{user_players_detailed[number]['web_name']}") # web name

                                gameweek = 0
                                for index, player in enumerate(individual_player_data['history']):
                                        if player['round'] == gameweek_number:
                                                gameweek = index

                                if captain[number] == True:
                                        st.write(f"Points: {individual_player_data['history'][gameweek]['total_points']*2}")
                                else:
                                        st.write(f"Points: {individual_player_data['history'][gameweek]['total_points']}")
                                st.write(f"Price: {individual_player_data['history'][gameweek]['value'] / 10}")


                        colT1, colT2, colT3 = st.columns((4,2,4))

                        with colT2:
                                player_visualise(0)

                        defender_columns = st.columns (position_count['Defenders'])

                        user_defender = [0]*5

                        for i, defender_grid in enumerate(defender_columns):
                                if i == 0 : 
                                        with defender_grid:
                                                player_visualise(1)

                                if i == 1 : 
                                        with defender_grid:
                                                player_visualise(2)
                                
                                if i == 2 : 
                                        with defender_grid:
                                                player_visualise(3)
                                
                                if i == 3 : 
                                        with defender_grid:
                                                player_visualise(4)

                                if i == 4 : 
                                        with defender_grid:
                                                player_visualise(5)

                        midfielder_columns = st.columns (position_count['Midfielders'])

                        for i, midfielder_grid in enumerate(midfielder_columns):
                                if i == 0 : 
                                        with midfielder_grid:
                                                player_visualise(position_count['Defenders'] + 1 )

                                if i == 1 : 
                                        with midfielder_grid:
                                                player_visualise(position_count['Defenders'] + 2 )
                                
                                if i == 2 : 
                                        with midfielder_grid:
                                                player_visualise(position_count['Defenders'] + 3 )
                                
                                if i == 3 : 
                                        with midfielder_grid:
                                                player_visualise(position_count['Defenders'] + 4 )

                                if i == 4 : 
                                        with midfielder_grid:
                                                player_visualise(position_count['Defenders'] + 5 )

                        remaining = (10 - position_count['Defenders'] - position_count['Midfielders'])

                        if remaining == 1:
                                forward_columns = st.columns ((4,2,4))
                        else:
                                forward_columns = st.columns (remaining) 

                        for i, forward_grid in enumerate(forward_columns):
                                if i == 0 : 
                                        if remaining == 1:
                                                continue
                                        elif remaining == 2:
                                                with forward_grid:
                                                        player_visualise(-2)
                                        else:
                                                with forward_grid:
                                                        player_visualise(-3)


                                if i == 1 : 
                                        if remaining == 1:
                                                with forward_grid:
                                                        player_visualise(-1)
                                        elif remaining == 2:
                                                with forward_grid:
                                                        player_visualise(-1)
                                        else:
                                                with forward_grid:
                                                        player_visualise(-2)
                                
                                if i == 2 : 
                                        if remaining == 1:
                                                continue
                                        with forward_grid:
                                                if remaining == 3:
                                                        player_visualise(-1)

                        colT1, colT2 , colT3 = st.columns(3)
                        
                
                        if gameweek_number != 1:
                                with colT1:
                                        st.metric ("Points", user_gameweek_data['entry_history']['points'], user_gameweek_data['entry_history']['points'] - difference_gameweek_data['entry_history']['points'])
                                with colT2:
                                        st.metric("Gameweek Rank", user_gameweek_data['entry_history']['rank'], user_gameweek_data['entry_history']['rank'] - difference_gameweek_data['entry_history']['rank'])
                                with colT3:
                                        st.metric("Overall Rank", user_gameweek_data['entry_history']['overall_rank'], user_gameweek_data['entry_history']['overall_rank'] - difference_gameweek_data['entry_history']['overall_rank'])
                        else:
                                with colT1:
                                        st.metric ("Points", user_gameweek_data['entry_history']['points'])
                                with colT2:
                                        st.metric("Gameweek Rank", user_gameweek_data['entry_history']['rank'])
                                with colT3:
                                        st.metric("Overall Rank", user_gameweek_data['entry_history']['overall_rank'])


                                


                        

                        


                                


                






                



















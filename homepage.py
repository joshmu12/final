import streamlit as st
import pandas as pd

# web scraping 
from bs4 import BeautifulSoup
import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)

if response.status_code == 200: 

        data = BeautifulSoup(response.text , 'html')
        print(data)

from streamlit_option_menu import option_menu

df = pd.read_csv('fplAnalytics-playerStautsData (1).csv')

st.set_page_config(

        page_title = "Multipage App",
        page_icon = "⚽️",
)

def team_page(): #team page define 
        st.title("Teams")

def main():
        st.title('Players')

# sidebar 

with st.sidebar:

        selected = option_menu(
                menu_title = "Main Menu",
                options = ["Home", "Teams", "Players"],
        )


if selected == "Teams":
        team_page()
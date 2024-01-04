import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

df = pd.read_csv('fplAnalytics-playerStautsData (1).csv')

st.set_page_config(

        page_title = "Multipage App",
        page_icon = "⚽️",
)

def team_page(): #team page define 
        st.title("Teams")


# sidebar 

with st.sidebar:

        selected = option_menu(
                menu_title = "Main Menu",
                options = ["Home", "Teams", "Players"],
        )


if selected == "Teams":
        team_page()
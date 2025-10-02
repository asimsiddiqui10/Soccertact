from email.policy import default
import streamlit as st
import json
import requests

from modules.methods import getTeamGames, fetch_player_from_api
from modules.teamAnalysis import TeamAnalysis
import pandas as pd
import plotly.graph_objects as go

import sys


sys.path.append('/APP') 

with open("data/teams.json", "r") as f:
    teams_data = json.load(f)
with open("data/player_mapping.json", "r") as f:
    players_mapping = json.load(f)
with open("data/players.json", "r") as f:
    players_data = json.load(f)


if "season" not in st.session_state:
    st.session_state.season = None
if "teamId" not in st.session_state:
    st.session_state.teamId = None
if "playerId" not in st.session_state:
    st.session_state.playerId = None
if "gameId" not in st.session_state:
    st.session_state.gameId = None

if "xgData" not in st.session_state:
    st.session_state.xgData = None

if "xPass" not in st.session_state:
    st.session_state.xPass = None   

if "xEvent" not in st.session_state:
    st.session_state.xEvent = None 

# Helper function to get team short names
def get_team_options(teams_data):
    return {team["team_name"]: team["team_short_name"] for team in teams_data}

def get_players(season, team_id, players_mapping, players_data):
    matching_player_ids = list({
        mapping["playerId"]
        for mapping in players_mapping
        if mapping["season"] == season and mapping["teamId"] == team_id
    })

    players = []
    for player_id in matching_player_ids:
        # Check if player exists in players_data
        matching_player = next(
            (player for player in players_data if player["player_id"] == player_id),
            None,
        )
        if not matching_player:
            # Fallback to fetch player from API if not found
            fetched_player = fetch_player_from_api(player_id)
            if fetched_player:
                players_data.append(fetched_player)  # Cache fetched player data
                players.append({"id": player_id, "name": fetched_player["player_name"]})
        else:
            players.append({"id": player_id, "name": matching_player["player_name"]})

    return players

# Streamlit app
st.sidebar.title("SOCCERTACT MLS")

# Select Season
seasons = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013]
selected_season = st.sidebar.selectbox("Select Season", seasons, index=0)
st.session_state.season = selected_season

# Main Page Content
st.title("SoccerTact MLS Dashboard")

st.divider()# Bug fixes and performance improvements

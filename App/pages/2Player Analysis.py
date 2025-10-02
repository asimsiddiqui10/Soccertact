
import streamlit as st 
st.title("Coming Soon")

# if selected_season and team_id:
#     players = get_players(st.session_state.season, st.session_state.teamId, players_mapping, players_data)
#     players_options = [{"id": None, "name": "All Players"}] + players
#     selected_player = st.sidebar.selectbox(
#         "Select Player",
#         options=players_options,
#         format_func=lambda player: player["name"],  # Display player name
#     )
    
#     games = getTeamGames(season=selected_season, team_id=team_id)
#     selected_game = st.sidebar.selectbox(
#         "Select Game",
#         options=[{"id": None, "label": "All Games"}] + games,
#         format_func=lambda game: game["label"],
#     )
#     print("SELECTED GAME: ", selected_game)
#     st.session_state.gameId = selected_game["id"] if selected_game else None

# else:
#     selected_player = None
#     selected_game = None
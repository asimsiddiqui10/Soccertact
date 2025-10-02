import requests

def getTeam(team_id):
    """
    Fetch team details by team_id.
    
    Parameters:
    team_id (str): The ID of the team.
    
    Returns:
    dict: A dictionary containing team details (team_id, team_name, team_short_name, team_abbreviation).
    """
    url = f"https://app.americansocceranalysis.com/api/v1/mls/teams?team_id={team_id}"
    try:
        response = requests.get(url, headers={"accept": "application/json"})
        response.raise_for_status()
        team_data = response.json()
        return team_data[0] if team_data else None  # Return the first team if the response contains a list
    except Exception as e:
        print(f"Failed to fetch team details for team_id {team_id}: {e}")
        return None

def getAllTeamsForSeason(season):
    url = f"https://app.americansocceranalysis.com/api/v1/mls/teams?season={season}"
    try:
        response = requests.get(url, headers={"accept": "application/json"})
        response.raise_for_status()
        team_data = response.json()
        return team_data[0] if team_data else None  # Return the first team if the response contains a list
    except Exception as e:
        print(f"Failed to fetch team details for season {season}: {e}")
        return None


def getTeamGames(team_id, season, game_id=None):
    """
    Fetch games for a given team and season, optionally filtered by game_id.
    
    Parameters:
    team_id (str): The ID of the team.
    season (int): The season year.
    game_id (str, optional): The ID of the game (if specific game filtering is required).
    
    Returns:
    list: A list of games with HomeTeam vs AwayTeam information.
    """
    base_url = "https://app.americansocceranalysis.com/api/v1/mls/games"
    params = {
        "team_id": team_id,
        "season_name": season,
    }
    if game_id:
        params["game_id"] = game_id

    try:
        # Fetch games data
        response = requests.get(base_url, params=params, headers={"accept": "application/json"})
        response.raise_for_status()
        games = response.json()

        formatted_games = []
        for game in games:
            # Fetch home and away team details
            home_team = getTeam(game["home_team_id"])
            away_team = getTeam(game["away_team_id"])

            # Construct the formatted game information
            home_team_name = home_team["team_name"] if home_team else "Unknown"
            away_team_name = away_team["team_name"] if away_team else "Unknown"
            
            formatted_games.append({
                "label": f"{home_team_name} vs {away_team_name}",
                "value": game["game_id"],
            })
        
        return formatted_games

    except Exception as e:
        print(f"Failed to fetch games: {e}")
        return []

def fetch_player_from_api(player_id):
    url = f"https://app.americansocceranalysis.com/api/v1/mls/players?player_id={player_id}"
    try:
        response = requests.get(url, headers={"accept": "application/json"})
        response.raise_for_status()
        player_data = response.json()
        return player_data[0] if player_data else None
    except Exception as e:
        print(f"Failed to fetch player with ID {player_id}: {e}")
        return None

# Documentation updates

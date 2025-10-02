import requests
import pandas as pd
from scipy.stats import zscore
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import numpy as np
from mplsoccer import Radar, FontManager
import plotly.graph_objects as go
import plotly.express as px

URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-Regular.ttf')
serif_regular = FontManager(URL1)
URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-ExtraLight.ttf')
serif_extra_light = FontManager(URL2)
URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf')
rubik_regular = FontManager(URL3)
URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
robotto_thin = FontManager(URL4)
URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')
robotto_bold = FontManager(URL5)

class TeamAnalysis:
    def __init__(self, season, team_id, player_id=None, game_id=None):
        """
        Initializes the TeamAnalysis class.

        Parameters:
        - season (int): The season year.
        - team_id (str): The team ID.
        - player_id (str, optional): The player ID.
        - game_id (str, optional): The game ID.
        """
        self.season = season
        self.team_id = team_id
        self.player_id = player_id
        self.game_id = game_id

    def get_team_info(self):
        """
        Fetches detailed team information using the team ID.
        """
        url = f"https://app.americansocceranalysis.com/api/v1/mls/teams?team_id={self.team_id}"
        try:
            response = requests.get(url, headers={"accept": "application/json"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching team info: {e}")
            return None
    
    def get_team_info_all(self):
        """
        Fetches detailed team information for all teams.
        """
        url = "https://app.americansocceranalysis.com/api/v1/mls/teams"
        try:
            response = requests.get(url, headers={"accept": "application/json"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching team info: {e}")
            return []
    
    def get_team_name(self, team_id):
        """
        Returns the team name for a given team_id.
        Args:
            team_id (str): The ID of the team.
        Returns:
            str: The team name if found, otherwise "Unknown Team".
        """
        team_info = {team["team_id"]: team for team in self.get_team_info_all()}
        return team_info.get(team_id, {}).get('team_abbreviation', 'Unknown Team')


    def get_team_games(self):
        """
        Fetches games for the team in the given season, optionally filtered by game ID.
        """
        url = "https://app.americansocceranalysis.com/api/v1/mls/games"
        params = {
            "team_id": self.team_id,
            "season_name": self.season,
        }
        if self.game_id:
            params["game_id"] = self.game_id

        try:
            response = requests.get(url, params=params, headers={"accept": "application/json"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching team games: {e}")
            return []

    def get_player_info(self):
        """
        Fetches detailed player information using the player ID.
        """
        if not self.player_id:
            return None

        url = f"https://app.americansocceranalysis.com/api/v1/mls/players?player_id={self.player_id}"
        try:
            response = requests.get(url, headers={"accept": "application/json"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching player info: {e}")
            return None

    def match_columns(self, stats, data_columns):
        """
        Matches stats with columns in the DataFrame based on substring matching.

        Args:
            stats (list): List of stats to match.
            data_columns (list): List of column names in the DataFrame.

        Returns:
            dict: A mapping of stat to matched column names.
        """
        matched_stats = {}
        for stat in stats:
            for col in data_columns:
                if stat in col:
                    matched_stats[stat] = col
                    break
        return matched_stats

    def getTeamXGoals(self, isSeason=False, isTeam=False, split_by_game=False):
        """
        Fetch xGoals data for teams with optional filters for season, team, and split by game.

        Parameters:
        - season (int, optional): The season year (e.g., 2024). Defaults to None.
        - team (str, optional): The team ID. Defaults to None.
        - split_by_game (bool, optional): Whether to split data by game. Defaults to False.

        Returns:
        - pd.DataFrame: A DataFrame containing the xGoals data.
        """

        season = self.season
        teamId = self.team_id
        # Base URL
        base_url = "https://app.americansocceranalysis.com/api/v1/mls/teams/xgoals"
        
        # Build query parameters
        params = {}
        if isSeason:
            params["season_name"] = season
        if isTeam:
            params["team_id"] = teamId
        if split_by_game:
            params["split_by_games"] = "true"

        try:
            # Make the API request
            response = requests.get(base_url, params=params, headers={"accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            
            # Convert JSON data to a Pandas DataFrame
            if data:
                df = pd.DataFrame(data)
                return df
            else:
                print("No data found for the given parameters.")
                return pd.DataFrame()

        except Exception as e:
            print(f"Failed to fetch xGoals data: {e}")
            return pd.DataFrame()

    def getTeamXPass(self, isSeason=False, isTeam=False, split_by_game=False):
        """
        Fetch xPass data for teams with optional filters for season, team, and split by game.

        Parameters:
        - season (int, optional): The season year (e.g., 2024). Defaults to None.
        - team (str, optional): The team ID. Defaults to None.
        - split_by_game (bool, optional): Whether to split data by game. Defaults to False.

        Returns:
        - pd.DataFrame: A DataFrame containing the xPass data.
        """

        season = self.season
        teamId = self.team_id
        # Base URL
        base_url = "https://app.americansocceranalysis.com/api/v1/mls/teams/xpass"
        
        # Build query parameters
        params = {}
        if isSeason:
            params["season_name"] = season
        if isTeam:
            params["team_id"] = teamId
        if split_by_game:
            params["split_by_games"] = "true"

        try:
            # Make the API request
            response = requests.get(base_url, params=params, headers={"accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            
            # Convert JSON data to a Pandas DataFrame
            if data:
                df = pd.DataFrame(data)
                return df
            else:
                print("No data found for the given parameters.")
                return pd.DataFrame()

        except Exception as e:
            print(f"Failed to fetch xGoals data: {e}")
            return pd.DataFrame()

    def getTeamGoalsAdded(self, isSeason=False, isTeam=False, split_by_game=False):
        """
        Fetch xGoalsAdded data for teams with optional filters for season, team, and split by game.

        Parameters:
        - season (int, optional): The season year (e.g., 2024). Defaults to None.
        - team (str, optional): The team ID. Defaults to None.
        - split_by_game (bool, optional): Whether to split data by game. Defaults to False.

        Returns:
        - pd.DataFrame: A DataFrame containing the goals-added data.
        """

        season = self.season
        teamId = self.team_id
        # Base URL
        base_url = "https://app.americansocceranalysis.com/api/v1/mls/teams/goals-added"
        
        # Build query parameters
        params = {}
        if isSeason:
            params["season_name"] = season
        if isTeam:
            params["team_id"] = teamId
        if split_by_game:
            params["split_by_games"] = "true"

        try:
            # Make the API request
            response = requests.get(base_url, params=params, headers={"accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            
            # Convert JSON data to a Pandas DataFrame
            if data:
                df = pd.DataFrame(data)
                return df
            else:
                print("No data found for the given parameters.")
                return pd.DataFrame()

        except Exception as e:
            print(f"Failed to fetch xGoals data: {e}")
            return pd.DataFrame()

    def getChartData(self, stats, data, chartType):
        """
        Extracts the specified stats from the DataFrame and excludes the row with self.teamId.

        Args:
            stats (list): List of column names to extract.
            data (pd.DataFrame): The DataFrame to process.

        Returns:
            dict: A dictionary where keys are team IDs and values are arrays of stats.
        """
        matched_stats = self.match_columns(stats, data.columns)

        if chartType == "scatter": 
            filtered_data = data
            result = {
                row['team_id']: row[stats].tolist()
                for _, row in filtered_data.iterrows()
            }
            return result

        if chartType == "zscore":
            # Filter matched stats
            valid_stats = list(matched_stats.values())
            if not valid_stats:
                raise ValueError("None of the requested stats were found in the DataFrame.")

            # Calculate Z-scores
            zscore_data = data.copy()
            zscore_data[valid_stats] = (zscore_data[valid_stats] - zscore_data[valid_stats].mean()) / zscore_data[valid_stats].std()

            # Convert to dictionary {team_id: [z-scores]}
            result = {
                row['team_id']: row[valid_stats].tolist()
                for _, row in zscore_data.iterrows()
            }
            return result

    def createScatterPlot(self, data, labels):
        """
        Creates a scatter plot using the provided data.

        Args:
            data (dict): A dictionary where keys are team IDs and values are arrays of stats.
            labels (list): A list of labels for the X and Y axes.
        """
        if len(labels) != 2:
            st.error("You must select exactly 2 stats for a scatter plot.")
            return

        # Extract X and Y data
        x_label, y_label = labels
        x_data = [values[0] for values in data.values()]
        y_data = [values[1] for values in data.values()]
        team_ids = list(data.keys())

        # Fetch team information
        team_info = {team["team_id"]: team for team in self.get_team_info_all()}

        # Prepare hover text
        hover_text = [
            f"Team Name: {team_info[team_id]['team_name']}<br>"
            f"{x_label}: {x_value}<br>{y_label}: {y_value}"
            for team_id, x_value, y_value in zip(team_ids, x_data, y_data)
        ]

        # Create scatter plot
        fig = go.Figure()

        # Add scatter points
        for team_id, x_value, y_value, hover in zip(team_ids, x_data, y_data, hover_text):
            fig.add_trace(go.Scatter(
                x=[x_value],
                y=[y_value],
                mode='markers',
                text=hover,
                hoverinfo='text',
                marker=dict(
                    size=12,
                    color='red' if team_id == self.team_id else 'blue',  # Color self.teamId differently
                ),
                name=team_info[team_id]['team_name']
            ))

        # Customize layout
        fig.update_layout(
            title=f"Scatter Plot: {x_label} vs {y_label}",
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white",
            showlegend=False 
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig)

    def createZScorePlot(self, zscore_data, stats_labels):
        """
        Creates a Z-score swarm plot comparing the team with others.

        Args:
            zscore_data (dict): Dictionary where keys are team IDs and values are Z-scores of stats.
            stats_labels (list): List of stat labels corresponding to the Z-scores.
        """
        # Convert zscore_data into a DataFrame for easier plotting
        zscore_df = pd.DataFrame.from_dict(zscore_data, orient='index', columns=stats_labels)
        zscore_df.reset_index(inplace=True)
        zscore_df.rename(columns={'index': 'team_id'}, inplace=True)
        team_info = {team["team_id"]: team for team in self.get_team_info_all()}
        zscore_df['team_name'] = zscore_df['team_id'].map(lambda tid: team_info.get(tid, {}).get('team_name', 'Unknown Team'))

        fig = go.Figure()

        # Add points for each stat
        for stat in stats_labels:
            fig.add_trace(go.Scatter(
                x=zscore_df[stat],
                y=[stat] * len(zscore_df),
                mode='markers',
                marker=dict(size=8, color='green', opacity=0.7),
                hovertemplate="<b>Team ID:</b> %{text}<br><b>Z-Score:</b> %{x}<extra></extra>",
                text=zscore_df['team_name'],  # Add team IDs as hover text
                name=stat  # Name each trace with the stat
            ))

        # Highlight your team's performance
        your_team = zscore_df[zscore_df['team_id'] == self.team_id]
        for stat in stats_labels:
            fig.add_trace(go.Scatter(
                x=your_team[stat],
                y=[stat],
                mode='markers',
                marker=dict(size=12, color='red', symbol='diamond'),
                hovertemplate="<b>Your Team</b><br><b>Z-Score:</b> %{x}<extra></extra>",
                name=f"Your Team: {self.team_id}"
            ))

        # Customize layout
        fig.update_layout(
            title="Team Performance Comparison (Z-Score)",
            xaxis_title="Worse <---- Performance ----> Better",
            yaxis=dict(
                title="Metrics",
                tickmode="array",
                tickvals=list(range(len(stats_labels))),
                ticktext=stats_labels  # Set proper metric names
            ),
            template="plotly_white",
            showlegend=False  # Remove legend for cleaner visualization
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

    def createTrendChart(self,game_data, all_stats, selected_stat):
        """
        Creates a trend chart showing the selected stat over games.

        Args:
            game_data (pd.DataFrame): DataFrame containing game stats.
            all_stats (dict): Dictionary mapping display names to actual column names.
            selected_stat (str): The selected stat display name.
        """
        def get_opponent_team_id(row):
            return row['away_team_id'] if row['home_team_id'] == self.team_id else row['home_team_id']


        stat_column = all_stats[selected_stat]
        if stat_column not in game_data.columns:
            st.error(f"Selected stat '{stat_column}' not found in game data.")
            return

        # Fetch detailed game information
        game_info = self.get_team_games()
        game_info_df = pd.DataFrame(game_info)
        merged_data = pd.merge(game_data, game_info_df, on="game_id", how="inner")


        # Convert date_time_utc to datetime format
        merged_data['date_time_utc'] = pd.to_datetime(merged_data['date_time_utc'], format='%Y-%m-%d %H:%M:%S %Z', errors='coerce')

        # Add game labels including date to avoid duplicates
        merged_data['game_name'] = (
            merged_data['home_team_id'] + " vs " + merged_data['away_team_id'] + " (" + 
            merged_data['date_time_utc'].dt.strftime('%Y-%m-%d') + ")"
        )
        merged_data['score'] = merged_data['home_score'].fillna(0).astype(int).astype(str) + " - " + merged_data['away_score'].fillna(0).astype(int).astype(str)
        merged_data['opponent_team_id'] = merged_data.apply(get_opponent_team_id, axis=1)

        merged_data['opponent_name'] =  merged_data['opponent_team_id'].apply(lambda tid: self.get_team_name(tid))
        # Sort by date_time_utc
        merged_data.sort_values(by='date_time_utc', inplace=True)
        merged_data['opponent_name_date'] = (
            merged_data['opponent_name'] + " (" + merged_data['date_time_utc'].dt.strftime('%Y-%m-%d') + ")"
        )

        # Create the trend chart
        fig = px.line(
            merged_data,
            x='opponent_name_date',
            y=stat_column,
            text='score',
            title=f"{selected_stat} Trend Over Games",
            labels={'game_name': 'Game', stat_column: selected_stat},
        )

        # Customize chart appearance
        fig.update_traces(mode='lines+markers', textposition='top center')
        fig.update_layout(
            xaxis_title="Games",
            yaxis_title=selected_stat,
            xaxis=dict(tickangle=45, showgrid=False),
            yaxis=dict(showgrid=True),
            template="plotly_white",
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig)

    
    def getDfForAutoInsight(self, data):
        """
        Prepares data for Auto Insight by adding team names and calculating Z-scores for all stats.

        Args:
            data (pd.DataFrame): The input data containing team stats.

        Returns:
            pd.DataFrame: The processed DataFrame with team names and Z-scores.
        """
        # Ensure the input has team_id
        if 'team_id' not in data.columns:
            raise ValueError("The data must contain a 'team_id' column.")

        team_info = {team["team_id"]: team for team in self.get_team_info_all()}
        data['team_name'] = data['team_id'].map(lambda tid: team_info.get(tid, {}).get('team_name', 'Unknown Team'))
        numeric_cols = data.select_dtypes(include='number').columns
        zscore_cols = {col: f"{col}_zscore" for col in numeric_cols}  # Mapping for new Z-score column names

        for col in numeric_cols:
            data[zscore_cols[col]] = zscore(data[col], nan_policy='omit')
        return data

    def getAutoInsightData(self, autoInsightData, stats_selected_values, type):
        """
        Extracts data for selected stats in a JSON format for Auto Insight scatter plots.

        Args:
            autoInsightData (pd.DataFrame): The processed DataFrame with stats and Z-scores.
            stats_selected_values (list): List of selected stats to include in the JSON.

        Returns:
            dict: A JSON-like structure with team data for the selected stats.
        """
        # Ensure all selected stats exist in the DataFrame
        missing_stats = [stat for stat in stats_selected_values if stat not in autoInsightData.columns]
        if missing_stats:
            raise ValueError(f"The following stats are missing in the data: {missing_stats}")

        # Initialize the JSON structure
        scatter_data = {}

        # Iterate through the teams
        for _, row in autoInsightData.iterrows():
            team_id = row['team_id']
            team_name = row['team_name']

            # Collect the selected stats and their Z-scores
            stats_data = {}
            for stat in stats_selected_values:
                # if type == "scatter":
                stats_data[stat] = row[stat]
                z_score_col = f"{stat}_zscore"
                stats_data[z_score_col] = row[z_score_col] if z_score_col in autoInsightData.columns else None

            # Add team data to the JSON structure
            scatter_data[team_id] = {
                "teamName": team_name,
                **stats_data
            }

        return scatter_data
   
    # def getAutoInsightZData(self, data, stats):



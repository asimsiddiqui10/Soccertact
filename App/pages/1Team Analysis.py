import streamlit as st
import json
import requests
import os

from modules.methods import getTeamGames, fetch_player_from_api, getTeam
from modules.teamAnalysis import TeamAnalysis
from modules.promptGenerator import PromptBuilder
from modules.autoInsights import AutoInsights

import pandas as pd
import plotly.graph_objects as go
import sys



with open("data/teams.json", "r") as f:
    teams_data = json.load(f)

# Define the path to the JSON file
feedback_file_path = "data/scatter_feedback.json"

# Ensure the JSON file exists and is initialized
if not os.path.exists(feedback_file_path):
    os.makedirs(os.path.dirname(feedback_file_path), exist_ok=True)  # Ensure directory exists
    with open(feedback_file_path, "w") as f:
        json.dump([], f)  # Initialize with an empty list

# Load existing feedbacks or initialize if the file is empty
if os.path.getsize(feedback_file_path) > 0:  # Check if file is not empty
    with open(feedback_file_path, "r") as feed:
        feedbacks = json.load(feed)
else:
    feedbacks = []  # Initialize as an empty list if the file is empty


print(feedbacks)
def get_team_options(teams_data):
    return {team["team_name"]: team["team_short_name"] for team in teams_data}

if "season" not in st.session_state:
    st.session_state.season = "2024"  

if st.session_state.season:     
    team_options = get_team_options(teams_data)
    team_names = list(team_options.keys())
    selected_team = st.sidebar.selectbox("Select Team", team_names)
    team_id = next(
    (team["team_id"] for team in teams_data if team["team_name"] == selected_team), None,)
    st.session_state.teamId = team_id
else: 
    st.write("Please choose a season")


team_analysis = TeamAnalysis(
    season=st.session_state.season,
    team_id=st.session_state.teamId,
    player_id=st.session_state.get("playerId"),
    game_id=st.session_state.get("gameId"),
)


all_stats = {
    'Shots For': 'shots_for', 
    'Shots Against': 'shots_against', 
    'Goals For': 'goals_for',
    'Goals Against': 'goals_against',
    'Goal Difference': 'goal_difference',
    'xGoal for': 'xgoals_for',
    'xGoal Against': 'xgoals_against',
    'xGoal Difference':  'xgoal_difference',
    'Goal Difference - xGoal Difference': 'goal_difference_minus_xgoal_difference',
    'Points': 'points',
    'xPoints': 'xpoints',
    'Attempted Passes For': 'attempted_passes_for',
    'Pass Completion Per For': 'pass_completion_percentage_for',
    'xPass Completion Perc For': 'xpass_completion_percentage_for',
    'Passes Completed Over Expected For': 'passes_completed_over_expected_for',
    'Passes Completed Over Expected Per 100 For': 'passes_completed_over_expected_p100_for',
    'Average Vertical Distance For': 'avg_vertical_distance_for',
    'Attempted Passes Against': 'attempted_passes_against',
    'Pass Completion Perc Against': 'pass_completion_percentage_against',
    'xPass Completion Perc Against': 'xpass_completion_percentage_against',
    'Passes Completed Over Expected Against': 'passes_completed_over_expected_against',
    'Passes Completed Over Expected Per 100 Against': 'passes_completed_over_expected_p100_against',
    'Average Vertical Distance Against': 'avg_vertical_distance_against',
    'Passes Completed Over Expected Difference': 'passes_completed_over_expected_difference',
    'Average Vertical Distance Difference': 'avg_vertical_distance_difference'
}
myTeamName = getTeam(st.session_state.teamId)
# Sidebar or main app layout
st.title(f"Team Dashboard - {myTeamName.get('team_name')}")

# Lets prepare our data for the team dashboard
df_xgoals_all_teams = team_analysis.getTeamXGoals(isSeason=True, isTeam=False)
df_xgoals_my_team = team_analysis.getTeamXGoals(isSeason=True, isTeam=True)
df_xgoals_my_team_events = team_analysis.getTeamXGoals(isSeason=True, isTeam=True, split_by_game=True)

df_xpass_all_teams = team_analysis.getTeamXPass(isSeason=True, isTeam=False)
df_xpass_my_team = team_analysis.getTeamXPass(isSeason=True, isTeam=True)
df_xpass_my_team_events = team_analysis.getTeamXPass(isSeason=True, isTeam=True, split_by_game=True)

df_all_teams_combined = pd.merge(
df_xgoals_all_teams, df_xpass_all_teams, on="team_id", how="outer", suffixes=("_xgoals", "_xpass")
)

## Auto Insight Code
autoInsightData = team_analysis.getDfForAutoInsight(df_all_teams_combined)

promptBuilder = PromptBuilder(
        team_name= myTeamName.get('team_name'),
        player_name=None,
        game_id=None,
    )
gemini = AutoInsights()
# st.write(autoInsightData)

if df_xgoals_my_team["team_id"].iloc[0] == df_xpass_my_team["team_id"].iloc[0]:
    df_xgoals_my_team = df_xgoals_my_team.add_suffix("_xgoals")
    df_xpass_my_team = df_xpass_my_team.add_suffix("_xpass")
    df_xgoals_my_team["team_id"] = df_xgoals_my_team["team_id_xgoals"]
    df_my_team_combined = pd.concat([df_xgoals_my_team, df_xpass_my_team], axis=1)
    df_my_team_combined = df_my_team_combined.loc[:, ~df_my_team_combined.columns.duplicated()]
else:
    raise ValueError("Team ID mismatch between my_team DataFrames!")

# Combine my_team_events DataFrames on game_id
df_my_team_events_combined = pd.merge(
    df_xgoals_my_team_events, df_xpass_my_team_events, on="game_id", how="outer", suffixes=("_xgoals", "_xpass")
)

### SCATTER PLOTS
# Multiselect for xGoals_stats
stats_selection = st.sidebar.multiselect(
    "Select 2 Stats For Scatter Plot:",
    options=list(all_stats.keys()),
    default=['xGoal for', 'xGoal Against'],
    max_selections=5
)


if len(stats_selection) == 2: 
    stats_selected_values = [all_stats[stat] for stat in stats_selection]
    scatterPlotData = team_analysis.getChartData(stats_selected_values, df_all_teams_combined, chartType='scatter')
    st.header("📈 Scatter Plot Analysis")
    team_analysis.createScatterPlot(scatterPlotData, stats_selection)

    autoInsightScatterPlotData = team_analysis.getAutoInsightData(autoInsightData, stats_selected_values, "scatter")
    prompt = promptBuilder.buildPrompt(autoInsightScatterPlotData, "scatter", stats_selected_values)
    response = gemini.generate_content(prompt)

    with st.expander("**AUTO INSIGHTS**"):
        st.write(response)

        # Initialize session state for feedback and rating
        if "rating" not in st.session_state:
            st.session_state.rating = 1
        if "feedback" not in st.session_state:
            st.session_state.feedback = ""

        # Feedback Loop
        st.markdown("### Provide Feedback")
        st.session_state.rating = st.slider(
            "Rate the insights (1-5):",
            min_value=1,
            max_value=5,
            step=1,
            value=st.session_state.rating,
            key="rating_slider"
        )
        st.session_state.feedback = st.text_area(
            "Provide your feedback:",
            value=st.session_state.feedback,
            key="feedback_textarea"
        )
        submitted = st.button("Submit Feedback")
        
        if submitted:
            # Check if rating or feedback is valid
            if st.session_state.rating > 1 or st.session_state.feedback.strip():
                feedback_data = {
                    "Response": response,
                    "Rating": st.session_state.rating,
                    "Feedback": st.session_state.feedback.strip()
                }

                # Add feedback to the list and maintain a maximum of 5 entries
                feedbacks.append(feedback_data)
                if len(feedbacks) > 5:
                    feedbacks.pop(0)  # Remove the oldest feedback
                
                # Save updated feedbacks to the JSON file
                with open(feedback_file_path, "w") as f:
                    json.dump(feedbacks, f, indent=4)
                
                st.success("Feedback submitted successfully!")

                # Clear feedback and rating
                st.session_state.rating = 1
                st.session_state.feedback = ""
            else:
                st.warning("Please provide a rating greater than 0 or valid feedback before submitting.")

else:
    st.write("Select 2 stats for Scatter plot")

st.divider()
### Z-SCORE PLOT
tab1, tab2 = st.tabs(["📈 SCORING", "📈 PASSING"])
xGoals_stats = {
    'Shots For': 'shots_for', 
    'Shots Against': 'shots_against', 
    'Goals For': 'goals_for',
    'Goals Against': 'goals_against',
    'Goal Difference': 'goal_difference',
    'xGoal for': 'xgoals_for',
    'xGoal Against': 'xgoals_against',
    'xGoal Difference':  'xgoal_difference',
    'Goal Diff - xGoal Diff': 'goal_difference_minus_xgoal_difference',
    'Points': 'points',
    'xPoints': 'xpoints'
}

xPass_stats = {'Attempted Passes For': 'attempted_passes_for',
    'Pass Comp Per For': 'pass_completion_percentage_for',
    'xPass Comp Perc For': 'xpass_completion_percentage_for',
    'Passes Comp Over Exp For': 'passes_completed_over_expected_for',
    'Passes Comp Over Exp Per 100 For': 'passes_completed_over_expected_p100_for',
    'Avg Vertical Distance For': 'avg_vertical_distance_for',
    'Attempted Passes Against': 'attempted_passes_against',
    'Pass Comp Perc Against': 'pass_completion_percentage_against',
    'xPass Comp Perc Against': 'xpass_completion_percentage_against',
    'Passes Comp Over Exp Ag': 'passes_completed_over_expected_against',
    'Passes Comp Over Exp Per 100 Against': 'passes_completed_over_expected_p100_against',
    'Avg Vertical Distance Against': 'avg_vertical_distance_against',
    'Passes Comp Over Exp Diff': 'passes_completed_over_expected_difference',
    'Avg Vertical Distance Diff': 'avg_vertical_distance_difference'
}

with tab1:
    st.header("📈 Scoring Analysis")
    # Get Z-score data for xGoals
    zscoreDataXG = team_analysis.getChartData(
        stats=list(xGoals_stats.values()),  # Use all xGoals stats
        data=df_all_teams_combined,
        chartType='zscore'
    )
    
    # Create Z-Score plot for xGoals
    team_analysis.createZScorePlot(zscoreDataXG, list(xGoals_stats.keys()))
    xg_zscores = team_analysis.getAutoInsightData(autoInsightData, list(xGoals_stats.values()), "zscores") 
    zscoreprompt = promptBuilder.buildPrompt(xg_zscores, "zscores", list(xGoals_stats.values()))
    response = gemini.generate_content(zscoreprompt)

    with st.expander(f"**AUTO INSIGHTS**"):
        st.write(response)

# Tab 2: xPass Z-Scores
with tab2:
    st.header("📈 Passing Analysis")
    # Get Z-score data for xPass
    zscoreDataXP = team_analysis.getChartData(
        stats=list(xPass_stats.values()),  # Use all xPass stats
        data=df_all_teams_combined,
        chartType='zscore'
    )
    # Create Z-Score plot for xPass
    team_analysis.createZScorePlot(zscoreDataXP, list(xPass_stats.keys()))
    xp_zscores = team_analysis.getAutoInsightData(autoInsightData, list(xPass_stats.values()), "zscores")
    zPscoreprompt = promptBuilder.buildPrompt(xp_zscores, "zscores", list(xPass_stats.values()))
    response = gemini.generate_content(zPscoreprompt)

    with st.expander(f"**AUTO INSIGHTS**"):
        st.write(response)

### Trend chart 
# selected_stat = st.sidebar.selectbox("Select a stat for trend analysis:", list(all_stats.keys()))
# games_data = df_my_team_events_combined
# team_analysis.createTrendChart(df_my_team_events_combined, all_stats, selected_stat)



# if not df_all_teams_combined.empty:
#     st.write("All Teams Data:", df_all_teams_combined)
# else:
#     st.write("No xGoals data available for the selected team and season.")

# if not df_my_team_combined.empty:
#     st.write("My Team:", df_my_team_combined)
# else:
#     st.write("No xGoals data available for the selected team and season.")

# if not df_my_team_events_combined.empty:
#     st.write("My Event Data:", df_my_team_events_combined)
# else:
#     st.write("No xGoals data available for the selected team and season.")




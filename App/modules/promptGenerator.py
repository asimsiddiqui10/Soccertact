
import json 

with open("data/scatter_feedback.json", "r") as f:
    feedback = json.load(f)

class PromptBuilder:
    def __init__(self,team_name, player_name=None, game_id=None):
        self.team_name = team_name
        self.player_id = player_name
        self.game_id = game_id


    def describe_level(z_score):
        if z_score >= 1.5:
            description = "outstanding"
        elif z_score >= 1:
            description = "excellent"
        elif z_score >= 0.5:
            description = "good"
        elif z_score >= -0.5:
            description = "average"
        elif z_score >= -1:
            description = "below average"
        else:
            description = "poor"

        return description

    def getFeedback(self, dataType):
        if dataType == "scatter":
            structured_feedback = []
            for idx, item in enumerate(feedback):
                structured_feedback.append(
                    f"Feedback {idx + 1}:\n"
                    f"**Response:**\n{item['Response']}\n"
                    f"**Rating:** {item['Rating']}\n"
                    f"**Feedback Comment:** {item['Feedback']}\n"
                    f"**Priority Suggestion:** {self.extractPrioritySuggestion(item['Feedback'])}\n"
                )
            return "\n".join(structured_feedback)
        else:
            return f"No feedback available for data type '{dataType}'"

    def extractPrioritySuggestion(self, feedback_comment):
        # Extract specific actionable suggestions from feedback
        # Modify this logic to identify priorities in the feedback
        if "change structure" in feedback_comment.lower():
            return "Revise the response structure to align with user suggestions."
        elif "clarify" in feedback_comment.lower():
            return "Focus on improving clarity in the response."
        elif "specific" in feedback_comment.lower():
            return "Add specific examples or metrics for better insight."
        else:
            return "General improvement requested."
        
    def getExampleInference(self, dataType):
        if dataType == "scatter":
            exampleResponse = (
                "Good: \
                Philadelphia Union's offensive efficiency has been impressive, with their xGoals For consistently \
                exceeding the league average. This demonstrates their ability to create and convert high-quality scoring opportunities.\
                Bad:\
                The defensive performance shows room for improvement, as their xGoals Against is significantly \
                above the league average. This suggests they are allowing opponents too many high-quality chances.\
                Can Improve:\
                Philadelphia Union should focus on tightening their defensive structure to reduce xGoals Against.\
                Enhancing their transition defense could also help mitigate counterattacks.\
                Compare to Other Team:\
                Compared to LAFC, Philadelphia Union has a slightly lower xGoals For, indicating their offense is less potent.\
                However, their xGoals Against is also slightly better, suggesting a marginally stronger defense."
            )
        elif dataType == "zscores":
            exampleResponse = (
            "Inter Miami demonstrates exceptional offensive efficiency, \
            consistently converting chances into goals at a rate far exceeding expectations, \
            which highlights their clinical edge in attack. However, defensive metrics reveal some vulnerabilities, \
            with higher-than-average shots and expected goals conceded,\
            suggesting room for improvement in limiting opponent opportunities.\
            Their significant overperformance in goal difference compared to expected metrics points to reliance on high-impact moments, \
            likely driven by standout players or moments of brilliance. \
            While this approach has yielded strong results, sustaining this level of performance will require maintaining their finishing efficiency and addressing defensive frailties to mitigate potential regression toward expected outcomes."
            )
        return exampleResponse

    def getDataTypeRelationship(self, dataType, stats):
        if dataType == "scatter":
            return f"build relationship between {stats[0]} and {stats[1]}, deriving insight while comparing against other teams"
        if dataType == "zscores":
            return f"Derive insights from z-score values from all statistics while building relationship between the all stats, their z-scores and values."
        return ""

    def buildPrompt(self, data, dataType, stats):
        data_json = json.dumps(data, indent=2)
        # System message
        system_message1 = {
            "role": "model",
            "content": (
                "You are a US-based MLS soccer scout. "
                "You provide succinct and to-the-point summaries of soccer teams and players "
                "based on data. You talk in soccer terms about data. "
                "You use the information given to you from the data and derive insights "
                "on teams and players. Your current job is to assess teams in Major League Soccer."
            )
        }

        system_message2 = {
            "role": "model",
            "content":  "Please refer to these stat definitions for your inference: \
            \n\n- **Shots For**: The total number of shots a team attempts during matches. Indicates attacking activity. **High is better.** \
            \n- **Shots Against**: The total number of shots opponents attempt against a team. Reflects defensive vulnerability. **High is worse.** \
            \n- **Goals For**: The total number of goals a team scores. Measures offensive effectiveness. **High is better.** \
            \n- **Goals Against**: The total number of goals a team concedes. Highlights defensive performance. **High is worse.** \
            \n- **Goal Difference**: The difference between Goals For and Goals Against. Positive values indicate dominance. **Higher positive values are better.** \
            \n- **xGoal For**: Expected goals a team is predicted to score based on the quality of chances. Reflects chance creation. **High is better.** \
            \n- **xGoal Against**: Expected goals a team is predicted to concede based on opponent chances. Indicates defensive quality. **Low is better.** \
            \n- **xGoal Difference**: The difference between xGoal For and xGoal Against. Suggests balance of chances created versus allowed. **Higher values indicate better balance.** \
            \n- **Goal Difference - xGoal Difference**: The gap between actual goal difference and expected goal difference. Measures over/underperformance. **A smaller gap indicates consistency.** \
            \n- **Points**: The total number of points a team earns from matches (wins = 3, draws = 1, losses = 0). Reflects results. **High is better.** \
            \n- **xPoints**: Expected points based on performance metrics like xGoals. Highlights how results align with performance. **Higher values indicate better predicted performance.** \
            \n- **Attempted Passes For**: The total number of passes a team attempts. Indicates possession-oriented play. **High is better.** \
            \n- **Pass Completion Perc For**: Percentage of passes a team successfully completes. Reflects passing accuracy. **High is better.** \
            \n- **xPass Completion Perc For**: Expected pass completion percentage based on pass difficulty. Measures precision under pressure. **Higher values indicate better performance.** \
            \n- **Passes Completed Over Expected For**: Number of completed passes beyond what is expected. Shows exceptional passing quality. **High is better.** \
            \n- **Passes Completed Over Expected Per 100 For**: Normalized version of Passes Completed Over Expected for every 100 passes. Useful for comparisons. **High is better.** \
            \n- **Average Vertical Distance For**: Average forward distance of passes. Indicates directness in attack. **High suggests direct attacking intent.** \
            \n- **Attempted Passes Against**: The total number of passes opponents attempt against a team. Reflects defensive exposure. **High is worse.** \
            \n- **Pass Completion Perc Against**: Percentage of passes opponents successfully complete. Highlights defensive pressure. **Low is better.** \
            \n- **xPass Completion Perc Against**: Expected pass completion percentage for opponents. Measures defensive disruptiveness. **Low indicates better disruption.** \
            \n- **Passes Completed Over Expected Against**: Number of passes opponents complete beyond expected. Indicates defensive lapses. **Low is better.** \
            \n- **Passes Completed Over Expected Per 100 Against**: Normalized version of Passes Completed Over Expected Against for every 100 passes. **Low is better.** \
            \n- **Average Vertical Distance Against**: Average forward distance of opponent passes. Reflects opponent directness. **Low suggests better control over opponent progression.** \
            \n- **Passes Completed Over Expected Difference**: The net difference between passes completed over expected for and against. Measures overall passing advantage. **Higher values are better.** \
            \n- **Average Vertical Distance Difference**: The net difference between average vertical distances for and against. Indicates dominance in progressing play. **Higher values indicate greater dominance.**"
        }


        user_message = {
            "role": "user", 
            "content": f"For {self.team_name} {self.getDataTypeRelationship(dataType, stats)} based on the following data {data_json}"
        }


        user_message1 = {
            "role": "user",
            "content": f"Please refer to this desired sample response{self.getExampleInference(dataType)}. Follow the structure of the this response when formating your respoonse. Change the structure based on feedback."
        }

        user_message2 = {
            "role": "user",
            "content": f"Do not refer back to values, z-scores or actual values in your response. \
            Rather use these: \
            z_score >= 1.5 Outstanding; \
            z_score >= 1: excellent \
            z_score >= 0.5: good \
            z_score >= -0.5: average \
            z_score >= -1: below average \
            else poor \
            For stats that have Against or Aga/against in their name reverse this. For example xGoal Against\
            z_score >= 1.5 poor; \
            z_score >= 1: below average \
            z_score >= 0.5: average \
            z_score >= -0.5: excellent \
            z_score >= -1: outstanding \
            else outstanding"
        }

        user_message3 = {
        "role": "user",
        "content": (
            "Here is an example of how to interpret the data:\n"
            "If a team's xGoal Against is high, it means they are allowing too many quality scoring chances, "
            "which is a weakness. Conversely, a low xGoal Against value indicates strong defensive performance."
        )
        }

        user_message4 = {
        "role": "user",
        "content": (
            "For stats with 'Against' in their name, **lower values and z-scores are better.** For example:\n"
            "- A high 'Shots Against' value indicates the team is allowing many shots, which is a defensive weakness.\n"
            "- A low 'Shots Against' value reflects strong defensive control."
        )
        }
        
        user_message5 = {
            "role": "user",
            "content": (
                "Based on the following feedback and ratings, revise your response:\n\n"
                f"{self.getFeedback('scatter')}\n\n"
                "### Instructions for Revision:\n"
                "1. Review the feedback and prioritize changes based on user suggestions.\n"
                "2. Revise the structure, language, or content of the response as explicitly requested in the feedback.\n"
                "3. Ensure the updated response is:\n"
                "   - Concise and well-structured.\n"
                "   - Consistent with soccer analytics terms.\n"
                "   - Adapted to align with user-provided suggestions (e.g., structural changes, clarity, or adding specific comparisons).\n"
                "4. Highlight key insights derived from the data while incorporating user feedback."
            )
        }
        

        return [system_message1, system_message2, user_message, user_message1 ,user_message2 ,user_message3, user_message4, user_message5]


import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from flask import Flask, render_template, request
from app.model.Stat_Predictor_Model import preprocess_data, predict_points, predict_assists, predict_rebounds   
from app.utils.Past_Seasons_Stats_Collector import get_past_seasons_stats
from app.utils.Against_Opponent_Stats_Collector import get_against_opp_stats
            
app = Flask(__name__, 
            template_folder=str(Path(__file__).parent.parent.parent / 'templates'),
            static_folder=str(Path(__file__).parent.parent.parent / 'static'))

@app.route('/')
def main():
    return render_template('home.html')

@app.route("/predict_stats", methods=["POST"])
def predict_stats_route():
    player_name = request.form.get("player_name", "").lower().replace(' ', '_')
    player_name = '_'.join(player_name.split('_')[:2])
    player_name_app_display = player_name.replace('_', ' ').title()
    opp_team_name = request.form.get("team_name", "").upper()

    if not opp_team_name:
        return render_template('error.html', error_message="Opposing team name cannot be empty.")

    df1 = get_past_seasons_stats(player_name)
    if isinstance(df1, dict) and "error" in df1:
        return render_template('error.html', error_message=df1["error"])
    
    df2 = get_against_opp_stats(player_name, opp_team_name)
    if isinstance(df2, dict) and "error" in df2:
        return render_template('error.html', error_message=df2["error"])

    df = preprocess_data(df1, df2)

    points = round(predict_points(df), 1)
    assists = round(predict_assists(df), 1)
    rebounds = round(predict_rebounds(df), 1)

    return render_template('result.html', data=df, player_name=player_name_app_display, opp_team_name=opp_team_name, points=points, assists=assists, rebounds=rebounds)

if __name__ == '__main__':
    app.run(debug=True)


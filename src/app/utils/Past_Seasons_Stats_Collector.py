import pandas as pd
import requests
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', None)
from io import StringIO
from sqlalchemy import create_engine
from config import db_config
import os

# engine = create_engine(f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
DATABASE_URL = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)

def get_past_seasons_stats(player_name):
    first_name, last_name = player_name.split('_')
    formatted_name = last_name[:5] + first_name[:2] + "01"
    url = f"https://www.basketball-reference.com/players/{formatted_name[0]}/{formatted_name}.html"

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Player not found. Status code: " + str(response.status_code)}

    soup = BeautifulSoup(response.text, 'html.parser')

    div = soup.find('div', id='div_per_game')
    if div is None:
        return {"error": "Table not found."}
    
    df = pd.read_html(StringIO(str(div)))[0]

    # skip season if player did not play
    seasons = ['2021-22', '2022-23', '2023-24']
    dfs = []

    for season in seasons:
        seasons_df = df[df['Season'] == season]
        if seasons_df.empty:
            continue
        dfs.append(seasons_df)

    df = pd.concat(dfs)
    
    df['Player Name'] = player_name
    
    df.to_sql(f"{player_name}_past_seasons_stats", engine, if_exists='append')
    
    return df




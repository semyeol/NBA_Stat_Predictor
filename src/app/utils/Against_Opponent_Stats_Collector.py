import pandas as pd
import requests
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', None)
from io import StringIO
from sqlalchemy import create_engine
from config import db_config

engine = create_engine(f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

def get_against_opp_stats(player_name, opp_team_name):
    first_name, last_name = player_name.split('_')
    formatted_name = last_name[:5] + first_name[:2] + "01"
    urls = [
        f"https://www.basketball-reference.com/players/{formatted_name[0]}/{formatted_name}/gamelog/2024",
        f"https://www.basketball-reference.com/players/{formatted_name[0]}/{formatted_name}/gamelog/2023",
        f"https://www.basketball-reference.com/players/{formatted_name[0]}/{formatted_name}/gamelog/2022"
    ]

    df = pd.DataFrame()

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('div', id='div_pgl_basic')
            if div is not None:
                df_temp = pd.read_html(StringIO(str(div)))[0]
                df = pd.concat([df, df_temp])
            else:
                print(f"Table not found for URL: {url}")
        else:
            print(f"Error {response.status_code} for URL: {url}")

    df = df[~df['GS'].isin(['Did Not Play', 'Did Not Dress', 'Inactive', 'Not With Team'])]

    df = df.dropna()

    df = df[df['Opp'].str.contains(opp_team_name)]
    if df.empty:
        return {"error": "No games against this team found."}
    
    df['Player Name'] = player_name
    
    df.to_sql(f"{player_name}_against_{opp_team_name}", engine,if_exists='append')

    return df




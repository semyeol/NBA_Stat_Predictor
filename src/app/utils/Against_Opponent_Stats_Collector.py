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

def get_against_opp_stats(player_name, opp_team_name):
    first_name, last_name = player_name.split('_')
    formatted_name = last_name[:5] + first_name[:2] + "01"
    urls = [
        f"https://www.basketball-reference.com/players/{formatted_name[0]}/{formatted_name}/gamelog/2024",
        f"https://www.basketball-reference.com/players/{formatted_name[0]}/{formatted_name}/gamelog/2023",
        f"https://www.basketball-reference.com/players/{formatted_name[0]}/{formatted_name}/gamelog/2022"
    ]

    print(f"URLS: {urls}")

    df = pd.DataFrame()

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('div', id='div_pgl_basic')
            if div is not None:
                df_temp = pd.read_html(StringIO(str(div)))[0]

                print(f"Data for URL: {url}")
                print(df_temp)

                df = pd.concat([df, df_temp])
            else:
                print(f"Table not found for URL: {url}")
        else:
            print(f"Error {response.status_code} for URL: {url}")

    print(f"Opponent team names: {df['Opp'].unique()}")  # print opponent team names

    filtered_data = df[df['Opp'] == opp_team_name]
    print(f"Filtered data for {opp_team_name}:")  # print message
    print(filtered_data)  # print filtered data

    print(f"GS values: {filtered_data['GS'].unique()}")  # print GS values

    df = df[~df['GS'].isin(['Did Not Play', 'Did Not Dress', 'Inactive', 'Not With Team'])]

    df['Unnamed: 5'] = df['Unnamed: 5'].fillna('')
    df = df[df['Opp'].str.contains(opp_team_name)]
    print(f"Data after second filter:")  # print message
    print(df)  # print data after second filter

    print(f"Rows with missing values:")  # print message
    print(df[df.isna().any(axis=1)])  # print rows with missing values
    # df = df.fillna(0)
    df = df.dropna()
    
    if df.empty:
        return {"error": "No games against this team found."}
    
    df['Player Name'] = player_name

    df.to_sql(f"{player_name}_against_{opp_team_name}", engine,if_exists='append')


    return df




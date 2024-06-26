import pandas as pd
from sqlalchemy import create_engine
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os

def get_data(player_name, opp_team_name_abbr):
    # engine = create_engine('postgresql://postgres:password@localhost:5432/statpredictor')
    DATABASE_URL = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
    past_seasons_table = f"{player_name}_past_seasons_stats"
    against_opp_table = f"{player_name}_against_{opp_team_name_abbr}"
    df1 = pd.read_sql(f"SELECT * FROM {past_seasons_table}", engine)
    df2 = pd.read_sql(f"SELECT * FROM {against_opp_table}", engine)
    return df1, df2

def preprocess_data(df1, df2):
    # fill missing values
    imputer = SimpleImputer(strategy='mean')
    df1[['PTS', 'AST', 'TRB']] = imputer.fit_transform(df1[['PTS', 'AST', 'TRB']])

    # this column would show up in some players' df and was causing errors
    if 'Unnamed: 31' in df1.columns:
        df1 = df1.drop('Unnamed: 31', axis=1)

    df = df1.merge(df2, on='Player Name', suffixes=('_df1', '_df2'))

    # print("NaN values:")
    # print(df.isna().any())

    # print("df columns: ")
    # print(df.columns)

    df = convert_to_numeric(df)
    df = calculate_weighted_average(df)
    # drop original dataframes' columns
    df = df.drop(['PTS_df1', 'AST_df1', 'TRB_df1', 'PTS_df2', 'AST_df2', 'TRB_df2'], axis=1)
    # drop unnecessary columns
    df = df.drop(['Season', 'Date', 'Age_df1', 'Age_df2', 'Tm_df1', 'Tm_df2', 'Opp', 'Unnamed: 5', 'Unnamed: 7', 'MP_df1', 'MP_df2', '+/-', 'Lg', 'Pos', 'Awards'], axis=1)
    return df

def convert_to_numeric(df):
    for col in ['PTS_df1', 'PTS_df2', 'AST_df1', 'AST_df2', 'TRB_df1', 'TRB_df2']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def calculate_weighted_average(df):
    for col in ['PTS', 'AST', 'TRB']:
        df[f'{col}_weighted'] = (df[f'{col}_df1'] * 0.80) + (df[f'{col}_df2'] * 0.20)
    return df

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = X_train.drop('Player Name', axis=1)
    X_test = X_test.drop('Player Name', axis=1)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test

def test_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse

def predict_stat(model, player):
    # player_df = player.to_frame().T
    stat = model.predict(player)
    return stat[0]

def predict_points(df):
    X = df.drop('PTS_weighted', axis=1)  
    y = df['PTS_weighted']  # Target variable
    model, X_test, y_test = train_model(X, y)
    # mse = test_model(model, X_test, y_test)
    # print(f'Mean Squared Error for points: {mse}')
    player = df.iloc[[0]]  
    player = player.drop(['PTS_weighted', 'Player Name'], axis=1)
    points = predict_stat(model, player)
    print(f'Predicted points: {points}')
    return points

def predict_assists(df):
    X = df.drop('AST_weighted', axis=1)  
    y = df['AST_weighted']  # Target variable
    model, X_test, y_test = train_model(X, y)
    # mse = test_model(model, X_test, y_test)
    # print(f'Mean Squared Error for assists: {mse}')
    player = df.iloc[[0]]  
    player = player.drop(['AST_weighted', 'Player Name'], axis=1)
    assists = predict_stat(model, player)
    print(f'Predicted assists: {assists}')
    return assists

def predict_rebounds(df):
    X = df.drop('TRB_weighted', axis=1) 
    y = df['TRB_weighted']  # Target variable
    model, X_test, y_test = train_model(X, y)
    # mse = test_model(model, X_test, y_test)
    # print(f'Mean Squared Error for rebounds: {mse}')
    player = df.iloc[[0]]  
    player = player.drop(['TRB_weighted', 'Player Name'], axis=1)
    rebounds = predict_stat(model, player)
    print(f'Predicted rebounds: {rebounds}')
    return rebounds

def main():
    player_name = input("Enter player name: ").replace(' ', '_').lower()
    opp_team_name_abbr = input("Enter opposing team name abbreviation: ")
    df1, df2 = get_data(player_name, opp_team_name_abbr)
    df = preprocess_data(df1, df2)
    
    predict_points(df)
    predict_assists(df)
    predict_rebounds(df)

if __name__ == "__main__":
    main()
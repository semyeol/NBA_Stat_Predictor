import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


engine = create_engine('postgresql://postgres:password@localhost:5432/statpredictor')

player_name = input("Enter player name: ")
player_name = player_name.replace(' ', '_').lower()
opp_team_name_abbr = input("Enter opposing team name abbreviation: ")

past_seasons_table = f"{player_name}_past_seasons_stats"
against_opp_table = f"{player_name}_against_{opp_team_name_abbr}"

df1= pd.read_sql(f"SELECT * FROM {past_seasons_table}", engine)
df2 = pd.read_sql(f"SELECT * FROM {against_opp_table}", engine)

# fill missing values
imputer = SimpleImputer(strategy='mean')
df1[['PTS', 'AST', 'TRB']] = imputer.fit_transform(df1[['PTS', 'AST', 'TRB']])

# merge dataframes
df = df1.merge(df2, on='Player Name', suffixes=('_df1', '_df2'))

# convert categorical values to numerical values
df['PTS_df1'] = pd.to_numeric(df['PTS_df1'], errors='coerce')
df['PTS_df2'] = pd.to_numeric(df['PTS_df2'], errors='coerce')
df['AST_df1'] = pd.to_numeric(df['AST_df1'], errors='coerce')
df['AST_df2'] = pd.to_numeric(df['AST_df2'], errors='coerce')
df['TRB_df1'] = pd.to_numeric(df['TRB_df1'], errors='coerce')
df['TRB_df2'] = pd.to_numeric(df['TRB_df2'], errors='coerce')

# calculate weighted average columns
df['PTS_weighted'] = (df['PTS_df1'] * 0.80) + (df['PTS_df2'] * 0.20)
df['AST_weighted'] = (df['AST_df1'] * 0.80) + (df['AST_df2'] * 0.20)
df['TRB_weighted'] = (df['TRB_df1'] * 0.80) + (df['TRB_df2'] * 0.20)

# drop original dataframes' columns
# print(df.columns)
df = df.drop(['PTS_df1', 'AST_df1', 'TRB_df1', 'PTS_df2', 'AST_df2', 'TRB_df2'], axis=1)

# split the data into a training set and a testing set
df = df.drop(['Season', 'Date', 'Age_df1', 'Age_df2', 'Tm_df1', 'Tm_df2', 'Opp', 'Unnamed: 5', 'Unnamed: 7', 'MP_df1', 'MP_df2', '+/-', 'Lg', 'Pos', 'Awards'], axis=1)

### print(df.columns)

X = df.drop('PTS_weighted', axis=1)  # Features
### print(X.columns)

y = df['PTS_weighted']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = X_train.drop('Player Name', axis=1)
X_test = X_test.drop('Player Name', axis=1)

### print("Features in X_train:", X_train.columns)
### print("Features in X_test:", X_test.columns)

# train the model
model = LinearRegression()
model.fit(X_train, y_train)

# evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# predict stats
player = df.iloc[0]  # Replace this with the player you want to predict
player = player.drop(['PTS_weighted', 'Player Name'])
### print("Features in player:", player.index if isinstance(player, pd.Series) else player.columns)

player_df = player.to_frame().T
points = model.predict(player_df)

print(f'Predicted points: {points[0]}')


# Target variables
y_ast = df['AST_weighted']  # Assists
y_trb = df['TRB_weighted']  # Total rebounds

# Split the data for assists
X_train_ast, X_test_ast, y_train_ast, y_test_ast = train_test_split(X, y_ast, test_size=0.2, random_state=42)
X_train_ast = X_train_ast.drop('Player Name', axis=1)
X_test_ast = X_test_ast.drop('Player Name', axis=1)

# Train the model for assists
model_ast = LinearRegression()
model_ast.fit(X_train_ast, y_train_ast)

# Evaluate the model for assists
y_pred_ast = model_ast.predict(X_test_ast)
mse_ast = mean_squared_error(y_test_ast, y_pred_ast)
print(f'Mean Squared Error for Assists: {mse_ast}')

assists = model_ast.predict(player_df)
print(f'Predicted assists: {assists[0]}')

# Split the data for total rebounds
X_train_trb, X_test_trb, y_train_trb, y_test_trb = train_test_split(X, y_trb, test_size=0.2, random_state=42)
X_train_trb = X_train_trb.drop('Player Name', axis=1)
X_test_trb = X_test_trb.drop('Player Name', axis=1)

# Train the model for total rebounds
model_trb = LinearRegression()
model_trb.fit(X_train_trb, y_train_trb)

# Evaluate the model for total rebounds
y_pred_trb = model_trb.predict(X_test_trb)
mse_trb = mean_squared_error(y_test_trb, y_pred_trb)
print(f'Mean Squared Error for Total Rebounds: {mse_trb}')

rebounds = model_trb.predict(player_df)
print(f'Predicted rebounds: {rebounds[0]}')




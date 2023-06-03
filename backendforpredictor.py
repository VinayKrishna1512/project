import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf
cf.go_offline()
#import plotly.graph_objects as go
#import plotly.express as px
balls = pd.read_csv('IPL_Ball_by_Ball_2008_2022.csv')
#balls.shape
matches=pd.read_csv('IPL_Matches_2008_2022.csv')
#matches.shape
#balls.head()
#balls.info()
#balls.describe()
#matches.head()
#matches['City'].value_counts().iplot()
total_score = balls.groupby(['ID', 'innings']).sum()['total_run'].reset_index()
#total_score.head()
total_score = total_score[total_score['innings']==1]
# total_score.head()
#fig = px.histogram(total_score,nbins=30, x='total_run')
#fig.show()
total_score['target'] = total_score['total_run'] + 1
match_df = matches.merge(total_score[['ID','target']], on='ID')
#match_df.head()
#match_df['Team1'].unique()
teams = [
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad', 
    'Delhi Capitals', 
    'Chennai Super Kings',
    'Gujarat Titans', 
    'Lucknow Super Giants', 
    'Kolkata Knight Riders',
    'Punjab Kings', 
    'Mumbai Indians'
]
match_df['Team1'] = match_df['Team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['Team2'] = match_df['Team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')

match_df['Team1'] = match_df['Team1'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['Team2'] = match_df['Team2'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['Team1'] = match_df['Team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['Team2'] = match_df['Team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df = match_df[match_df['Team1'].isin(teams)]
match_df = match_df[match_df['Team2'].isin(teams)]
match_df = match_df[match_df['WinningTeam'].isin(teams)]
match_df['method'].unique()
match_df['method'].value_counts()
match_df = match_df[match_df['method'].isna()]
#match_df.shape
#match_df.columns
match_df = match_df[['ID','City','Team1','Team2','WinningTeam','target']].dropna()
#match_df.head()
match_df.isna().sum()
match_df = match_df[['ID','City','Team1','Team2','WinningTeam','target']].dropna()
#match_df.head()
match_df.isna().sum()
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

balls = balls[balls['BattingTeam'].isin(teams)]
balls_df = match_df.merge(balls, on='ID')
#balls_df.head()
balls_df['BattingTeam'].value_counts()
#fig = px.bar(balls_df['BattingTeam'].value_counts())
#fig.show()
#balls_df.columns
balls_df = balls_df[balls_df['innings']==2]
# (balls_df.shape)
# balls_df.head()
balls_df['current_score'] = balls_df.groupby('ID')['total_run'].cumsum()
#print(balls_df)
balls_df['runs_left'] = np.where(balls_df['target']-balls_df['current_score']>=0, balls_df['target']-balls_df['current_score'], 0)
print(balls_df)
balls_df['balls_left'] = np.where(120 - balls_df['overs']*6 - balls_df['ballnumber']>=0,120 - balls_df['overs']*6 - balls_df['ballnumber'], 0)
balls_df['wickets_left'] = 10 - balls_df.groupby('ID')['isWicketDelivery'].cumsum()
balls_df['current_run_rate'] = (balls_df['current_score']*6)/(120-balls_df['balls_left'])
balls_df['required_run_rate'] = np.where(balls_df['balls_left']>0, balls_df['runs_left']*6/balls_df['balls_left'], 0)
def result(row):
    return 1 if row['BattingTeam'] == row['WinningTeam'] else 0
balls_df['result'] = balls_df.apply(result, axis=1)
balls_df.head()
index1 = balls_df[balls_df['Team2']==balls_df['BattingTeam']]['Team1'].index
index2 = balls_df[balls_df['Team1']==balls_df['BattingTeam']]['Team2'].index
balls_df.loc[index1, 'BowlingTeam'] = balls_df.loc[index1, 'Team1']
balls_df.loc[index2, 'BowlingTeam'] = balls_df.loc[index2, 'Team2']
# print(balls_df.head())
final_df = balls_df[['BattingTeam', 'BowlingTeam','City','runs_left','balls_left','wickets_left','current_run_rate','required_run_rate','target','result']]
#print(final_df.head())
# print(final_df.describe())
final_df.isna().sum()
#print(final_df.shape)
print(final_df.sample(final_df.shape[0]))
print(final_df.sample())
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


X = final_df.drop('result', axis=1)
y = final_df['result']
X.shape, y.shape
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)
trf = ColumnTransformer([('trf', OneHotEncoder(sparse=False,drop='first'),['BattingTeam','BowlingTeam','City'])],remainder = 'passthrough')

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
pipe = Pipeline(steps=[
    ('step1',trf),
    ('step2',RandomForestClassifier())
])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_pred, y_test))
pipe.predict_proba(X_test)
teams
final_df['City'].unique()
import pickle
pickle.dump(pipe, open('pipe.pkl','wb'))

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

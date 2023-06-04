import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sb
import tkinter as tk
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")
# print(matches.head(3))
# print(deliveries.head(3))
# 1.Plotting a Histogram for the number of matches played in each season by each teams.
def matches_per_season():
    season = np.sort(matches['season'].unique())
    # print("The Number of Seasons in all are",len(season), "which are" , season)
    plt.rcParams["figure.figsize"][0] = 15
    plt.rcParams["figure.figsize"][1] = 6
    matches['season'].hist(color='#6DA65A', bins=20, grid=False)
    plt.title("Histogram to show number of matches Played In Each Season of IPL", fontsize=20)
    plt.xlabel("Years in Which the IPL Was Played", fontsize=15)
    plt.ylabel("Matches Played in the Season", fontsize=15)
    plt.xticks(np.arange(2008, 2018, step=1), rotation=40)
    plt.show()
# 2. finding the number of teams in all seasons of IPL
def wins_to_totalmatches():

    #Finding the unique teams in the IPL Matches
    team1 = matches['team1'].unique()
    # Finding the number of matches played as team1 and team2 by the teams 
    team1_all = pd.crosstab(index = matches['team1'], columns = 'count')
    team2_all = pd.crosstab(index = matches['team2'], columns = 'count')
    # Adding both the numbers to get the total number of matches
    final_team = team1_all.add(team2_all)
    #Finding the total matches won by the team
    winner = pd.crosstab(index = matches['winner'], columns = "count")
    final_team['wins'] = winner['count']

    final_team[['count', 'wins']].plot(kind = 'bar' ,  width = 0.7,   color=['#93BEFE' , '#F93D43'],fontsize = 12)

    plt.xlabel("Teams Who Played IPL Seasons", fontsize = 14)
    plt.title("Grouped Bar Plot for total matches and wins of Each Team in All Seasons", fontsize = 18)
    plt.show()


# 3 A.Toss Win/Loss V/S Match Win/Loss
def win_tosswin():
    win_game = matches[matches['toss_winner'] == matches['winner']]
    toss_win = pd.crosstab(index = win_game['winner'], columns = 'count')
    toss_all = pd.crosstab(index = matches['toss_winner'], columns = 'count')
    toss_all['won_match'] = toss_win['count']
    toss_all['percent'] = toss_win['count'] / toss_all['count']
    plt.rcParams["figure.figsize"][0] = 15
    plt.rcParams["figure.figsize"][1] = 8
    toss_all['percent'].plot(kind = 'barh', width = 0.6, fontsize = 15)
    plt.ylabel("Various Teams Playing in IPL", fontsize =21)
    plt.title("Horizontal Bar Chart For percent win for the team when it won the toss" , fontsize = 20)
    plt.show()
# 4 Finding the top 15 player of the match players and plotting a chart
def top_15_potm():
    player = matches['player_of_match']
    from collections import Counter
    count = Counter(player).values()
    list1 = pd.DataFrame({'Player' :matches['player_of_match'].unique()})
    list1['count'] = count
    list1 = list1[list1['count'] > 8].sort_values(by = 'count', ascending = False)
    #plotting the Doughnut Chart

    plt.rcParams["figure.figsize"][0] = 8
    plt.rcParams["figure.figsize"][1] = 8
    plt.pie(list1['count'], labels = list1['Player'], wedgeprops = {'linewidth' : 7, 'edgecolor' : 'white'})
    my_circle = plt.Circle(( 0,0) , 0.7 , color = 'White')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.title("Doughnut Chart for top 15 Cricketers who have been Man of the Matches", fontsize= 18)
    plt.show()


# 5 Getting The Scores of All Team in each Season in IPL
def score_all_teams():
    s = deliveries.match_id.replace(matches.set_index('id')['season'])
    deliveries['season'] = s
    # print(deliveries['season'].unique())

    fig, ax = plt.subplots(figsize=(16,10))
    deliveries_by_season = deliveries.groupby(['season' , 'batting_team']).sum()
    deliveries_by_season['batsman_runs'].unstack().plot(kind = 'bar',ax = ax, width = 0.4, fontsize = 16)
    plt.title("Runs Scored by Teams In The Seasons of IPL" , fontsize = 25)
    plt.ylabel("Runs Scored By Teams" ,fontsize = 20)
    plt.xlabel("Seasons Of IPL", fontsize = 20)
    ax.legend(loc='center left', bbox_to_anchor=(1, 1))
    plt.show()

# 6 Getting The Wickets of All Team in each Season in IPL
def wickets_all_teams():
    deliveries['player_dismissed_no'] = deliveries['player_dismissed']
    deliveries['player_dismissed_no'] = np.where(deliveries['player_dismissed_no'].isnull(), 0 , 1)
    wickets_by_season = deliveries.groupby(['season' , 'bowling_team']).sum()
    fig, ax = plt.subplots(figsize=(16,10))
    wickets_by_season['player_dismissed_no'].unstack().plot(kind = 'bar',ax = ax, width = 0.4, fontsize = 16)
    plt.title("Wickets Taken by Teams In The Seasons of IPL" , fontsize = 25)
    plt.ylabel("Wickets Taken By Teams" ,fontsize = 20)
    plt.xlabel("Seasons Of IPL", fontsize = 20)
    ax.legend(loc='center left', bbox_to_anchor=(1, 1))
    plt.show()
    

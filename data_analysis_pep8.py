'''
Code for data analysis
'''
import tkinter as tk
from collections import Counter
import subprocess
from tkinter import Label
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def click_here():
    '''
    used to connect qtdesigner to this code
    '''

    matches_sheet = pd.read_csv("matches.csv")
    deliveries_sheet = pd.read_csv("deliveries.csv")

    def matches_per_season():
        # Finds the number of matches played per season and plots a histogram
        plt.rcParams["figure.figsize"] = (15, 6)
        matches_sheet['season'].hist(color='#6DA65A', bins=20, grid=False)
        plt.title("Total number of matches played per Season of IPL",
                  fontsize=20)
        plt.xlabel("Years in Which the IPL Was Played", fontsize=15)
        plt.ylabel("Matches Played in the Season", fontsize=15)
        plt.xticks(np.arange(2008, 2018, step=1), rotation=40)
        plt.show()

    def wins_to_total_matches():
        # Finds the total wins compared to total matches played by each team

        # To find the mamtches played by each teams
        all_team1 = pd.crosstab(index=matches_sheet['team1'], columns='count')
        all_team2 = pd.crosstab(index=matches_sheet['team2'], columns='count')
        # To get the overall matches we add them
        overall_team = all_team1.add(all_team2)
        # To get the number of overall matches won by the team
        winner = pd.crosstab(index=matches_sheet['winner'], columns="count")
        overall_team['wins'] = winner['count']
        overall_team[['count', 'wins']].plot(kind='bar',
                                             width=0.7,
                                             color=['#93BEFE', '#F93D43'],
                                             fontsize=12)
        plt.xlabel("Teams Who Played IPL Seasons", fontsize=14)
        plt.title("the total wins compared to the total\
    matches played by each team", fontsize=18)
        plt.show()

    def win_toss_win():
        '''
        Finds the percentage of matches the team that won the toss
        and wins the match
        '''
        # Checks if the toss winner was the winner of the match
        game_win = matches_sheet[matches_sheet['toss_winner'] ==
                                 matches_sheet['winner']]
        toss_win = pd.crosstab(index=game_win['winner'], columns='count')
        all_toss = pd.crosstab(index=matches_sheet['toss_winner'],
                               columns='count')
        all_toss['won_match'] = toss_win['count']
        all_toss['percent'] = toss_win['count'] / all_toss['count']
        plt.rcParams["figure.figsize"] = (15, 8)
        all_toss['percent'].plot(kind='barh', width=0.6, fontsize=15)
        plt.ylabel("Various Teams Playing in IPL", fontsize=21)
        plt.title("Percentage win for\
    the team that has won the toss", fontsize=20)
        plt.show()

    def top_15_potm():
        '''
        Finds the player of the matches throughout each seasons
        and gives the top 15 among them
        '''
        # Stores all the player of the match players
        player_name = matches_sheet['player_of_match']
        # Counts the number of times each player was player of the match
        count = Counter(player_name).values()
        l_1 = pd.DataFrame({'Player': matches_sheet[
            'player_of_match'].unique()})
        l_1['count'] = count
        l_1 = l_1[l_1['count'] > 8].sort_values(by='count', ascending=False)
        # plotting the doughnut chart
        plt.rcParams["figure.figsize"] = (8, 8)
        plt.pie(l_1['count'], labels=l_1['Player'],
                wedgeprops={'linewidth': 7, 'edgecolor': 'white'})
        my_circle = plt.Circle((0, 0), 0.7, color='White')
        p_1 = plt.gcf()
        p_1.gca().add_artist(my_circle)
        plt.title("Top 15 Cricketers in the list\
    of Man of the Matches throughout IPL", fontsize=18)
        plt.show()

    def score_all_teams():
        # Plots the total score of each team per season for all seasons

        # replacing the column of seasons with its index per season
        s_1 = deliveries_sheet.match_id.replace(matches_sheet.set_index('id')[
            'season'])
        deliveries_sheet['season'] = s_1

        fig, ax = plt.subplots(figsize=(16, 10))
        deliveries_by_season = deliveries_sheet.groupby(['season',
                                                         'batting_team']).sum()
        deliveries_by_season['batsman_runs'].unstack().plot(kind='bar',
                                                            ax=ax, width=0.4,
                                                            fontsize=16)
        plt.title("Runs Scored by each Teams per Season in IPL", fontsize=25)
        plt.ylabel("Runs Scored By Teams", fontsize=20)
        plt.xlabel("Seasons Of IPL", fontsize=20)
        ax.legend(loc='center left', bbox_to_anchor=(1, 1))
        plt.show()

    def wickets_all_teams():
        # Plots the wickets taken by each team per season for allseasons

        # replacing the column of seasons with its index per season
        s_1 = deliveries_sheet.match_id.replace(matches_sheet.set_index('id')[
            'season'])
        deliveries_sheet['season'] = s_1
        deliveries_sheet['player_dismissed_no'] = \
            deliveries_sheet['player_dismissed']

        player_dismissed = deliveries_sheet['player_dismissed_no'].isnull()
        deliveries_sheet['player_dismissed_no'] = np.where(player_dismissed,
                                                           0, 1)
        wickets_by_season = deliveries_sheet.groupby(['season',
                                                      'bowling_team']).sum()
        fig, ax = plt.subplots(figsize=(16, 10))
        wickets_by_season['player_dismissed_no'].unstack().plot(kind='bar',
                                                                ax=ax,
                                                                width=0.4,
                                                                fontsize=16)
        plt.title("Wickets Taken by each Teams per Season in IPL", fontsize=25)
        plt.ylabel("Wickets Taken By Teams", fontsize=20)
        plt.xlabel("Seasons Of IPL", fontsize=20)
        ax.legend(loc='center left', bbox_to_anchor=(1, 1))
        plt.show()

    def run_streamlit():
        subprocess.Popen(["streamlit", "run", "streamlit_pep8.py"])

    # Creating the gui interface
    root = tk.Tk()
    root.title("IPL Analysis")
    root.geometry("665x250+350+250")
    # have to make it center aligned
    label1 = Label(root, text="IPL DATA ANALYSIS",
                   font="Helvetica 16 bold italic")
    label1.pack()

    # Creating Buttons for each function in our main code

    btn_matches_per_season = tk.Button(root, text="Matches Per Season",
                                       command=matches_per_season)
    btn_matches_per_season.pack()

    btn_wins_to_total_matches = tk.Button(root, text="Wins to Total Matches",
                                          command=wins_to_total_matches)
    btn_wins_to_total_matches.pack()

    btn_win_toss_win = tk.Button(root, text="Win/Toss Win",
                                 command=win_toss_win)
    btn_win_toss_win.pack()

    btn_top_15_potm = tk.Button(root, text="Top 15 Players of the Match",
                                command=top_15_potm)
    btn_top_15_potm.pack()

    btn_score_all_teams = tk.Button(root, text="Scores of All Teams",
                                    command=score_all_teams)
    btn_score_all_teams.pack()

    btn_wickets_all_teams = tk.Button(root, text="Wickets of All Teams",
                                      command=wickets_all_teams)
    btn_wickets_all_teams.pack()

    btn_streamlit = tk.Button(root, text="Predict Probability",
                              command=run_streamlit)
    btn_streamlit.pack()
    # Used to Run the GUI interface
    root.mainloop()

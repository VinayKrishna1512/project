"""
This module provides functionality for backend operations.
"""
import pickle
import numpy as np
import pandas as pd
import cufflinks as cf
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


cf.go_offline()
try:
    # Storing the data in "deliveries" and "dsofmatch" variables.
    deliveries = pd.read_csv('IPL_Ball_by_Ball_2008_2022.csv')
    dsofmatch = pd.read_csv('IPL_Matches_2008_2022.csv')

    # Making a variable "total_score" to calculate the total runs per match
    total_score = deliveries.groupby(['ID',
                                      'innings']).sum()[
                                          'total_run'].reset_index()

    # Filtering out the 1st innings data only.
    total_score = total_score[total_score['innings'] == 1]

    total_score['target'] = total_score['total_run'] + 1

    # Merging data of "total_score" into "dsofmatch" on common column "ID".
    dsofmatch = dsofmatch.merge(total_score[['ID', 'target']], on='ID')

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

    # Updating team names to match the desired format.
    dsofmatch['Team1'] = dsofmatch['Team1'].str.replace('Delhi Daredevils',
                                                        'Delhi Capitals')
    dsofmatch['Team2'] = dsofmatch['Team2'].str.replace('Delhi Daredevils',
                                                        'Delhi Capitals')
    dsofmatch['WinningTeam'] = dsofmatch['WinningTeam'].str.replace(
        'Delhi Daredevils', 'Delhi Capitals')

    dsofmatch['Team1'] = dsofmatch['Team1'].str.replace('Kings XI Punjab',
                                                        'Punjab Kings')
    dsofmatch['Team2'] = dsofmatch['Team2'].str.replace('Kings XI Punjab',
                                                        'Punjab Kings')
    dsofmatch['WinningTeam'] = dsofmatch['WinningTeam'].str.replace(
        'Kings XI Punjab', 'Punjab Kings')

    dsofmatch['Team1'] = dsofmatch['Team1'].str.replace('Deccan Chargers',
                                                        'Sunrisers Hyderabad')
    dsofmatch['Team2'] = dsofmatch['Team2'].str.replace('Deccan Chargers',
                                                        'Sunrisers Hyderabad')
    dsofmatch['WinningTeam'] = dsofmatch['WinningTeam'].str.replace(
        'Deccan Chargers', 'Sunrisers Hyderabad')

    # Dropping teams which didn't play more seasons or are not active.
    dsofmatch = dsofmatch[dsofmatch['Team1'].isin(teams)]
    dsofmatch = dsofmatch[dsofmatch['Team2'].isin(teams)]
    dsofmatch = dsofmatch[dsofmatch['WinningTeam'].isin(teams)]

    dsofmatch = dsofmatch[['ID', 'City', 'Team1', 'Team2',
                           'WinningTeam', 'target']].dropna()

    '''
    Updating the "BattingTeam" column in "deliveries" DataFrame to
    match the desired team names.
    '''
    deliveries['BattingTeam'] = deliveries['BattingTeam'].str.replace(
        'Kings XI Punjab', 'Punjab Kings')
    deliveries['BattingTeam'] = deliveries['BattingTeam'].str.replace(
        'Delhi Daredevils', 'Delhi Capitals')
    deliveries['BattingTeam'] = deliveries['BattingTeam'].str.replace(
        'Deccan Chargers', 'Sunrisers Hyderabad')

    # Filtering out deliveries data for the desired teams.
    deliveries = deliveries[deliveries['BattingTeam'].isin(teams)]

    # Merging "dsofmatch" into "deliveries" on the common column "ID".
    dsofdeliveries = dsofmatch.merge(deliveries, on='ID')

    # Filtering out the 2nd innings data only.
    dsofdeliveries = dsofdeliveries[dsofdeliveries['innings'] == 2]

    # Creating additional columns for analysis.
    dsofdeliveries['current_score'] = dsofdeliveries.groupby('ID')[
        'total_run'].cumsum()
    required_run = dsofdeliveries['target'] - dsofdeliveries['current_score']
    dsofdeliveries['runs_left'] = np.where(required_run >= 0, required_run, 0)
    remaining_ball = 120 - dsofdeliveries['overs'] * 6 - dsofdeliveries[
        'ballnumber']
    dsofdeliveries['balls_left'] = np.where(remaining_ball >= 0,
                                            remaining_ball, 0)
    dsofdeliveries['wickets_left'] = 10 - dsofdeliveries.groupby('ID')[
        'isWicketDelivery'].cumsum()
    crr = (dsofdeliveries['current_score'] * 6) / (120 - dsofdeliveries[
        'balls_left'])
    dsofdeliveries['current_run_rate'] = crr
    rrr = dsofdeliveries['runs_left'] * 6 / dsofdeliveries['balls_left']
    dsofdeliveries['required_run_rate'] = np.where(dsofdeliveries[
        'balls_left'] > 0, rrr, 0)

    def result(row):
        '''
        This function performs to check the data set whether the batting team
        the match.
        '''
        return 1 if row['BattingTeam'] == row['WinningTeam'] else 0

    # Changing the "result" column to binary values (0 for loss, 1 for win).
    dsofdeliveries['result'] = dsofdeliveries.apply(result, axis=1)

    index1 = dsofdeliveries[dsofdeliveries['Team2'] == dsofdeliveries[
        'BattingTeam']]['Team1'].index
    index2 = dsofdeliveries[dsofdeliveries['Team1'] == dsofdeliveries[
        'BattingTeam']]['Team2'].index

    '''
    Assigning values from the "Team1" and "Team2" columns
    to the "BowlingTeam" column based on specific indices
    '''
    dsofdeliveries.loc[index1, 'BowlingTeam'] = dsofdeliveries.loc[index1,
                                                                   'Team1']
    dsofdeliveries.loc[index2, 'BowlingTeam'] = dsofdeliveries.loc[index2,
                                                                   'Team2']

    # Creating the final DataFrame "final_df" with the selected columns.
    final_df = dsofdeliveries[['BattingTeam', 'BowlingTeam', 'City',
                               'runs_left', 'balls_left', 'wickets_left',
                               'current_run_rate', 'required_run_rate',
                               'target', 'result']]

    # Assigning the dependent and independent variables.
    X = final_df.drop('result', axis=1)
    y = final_df['result']

    # Splitting the data into training and testing sets.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01,
                                                        random_state=42)

    # Applying OneHotEncoder on BattingTeam, BowlingTeam, and City.
    trf = ColumnTransformer([('trf', OneHotEncoder(sparse=False, drop='first'),
                              ['BattingTeam', 'BowlingTeam', 'City'])],
                            remainder='passthrough')

    # Creating a pipeline with OneHotEncoder and RandomForestClassifier.
    pipe = Pipeline(steps=[
        ('step1', trf),
        ('step2', RandomForestClassifier())
    ])

    # Fitting the pipeline on the training data.
    pipe.fit(X_train, y_train)

    # Predicting the target variable for the test data.
    y_pred = pipe.predict(X_test)

    # Calculating the accuracy score.
    print(accuracy_score(y_pred, y_test))

    # Saving the trained model.
    with open('pipe.pkl', 'wb') as file:
        pickle.dump(pipe, file)

except FileNotFoundError as e:
    print(f"File not found: {e.filename}")
except NameError as e:
    print(f"NameError occurred: {e}")
except ValueError as e:
    print(f"ValueError occurred: {e}")

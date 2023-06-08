'''
Stream lit browser for IPL Predictor
'''
import streamlit as st
import pickle
import pandas as pd
# Reading the file
try:
    pipe = pickle.load(open('pipe.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model file not found. Please make sure 'pipe.pkl' is present.")
    st.stop()

st.title("IPL WIN PREDICTOR")

teams = [
        "Chennai Super Kings", "Mumbai Indians", "Gujarat Titans",
        "Lucknow Super Giants", "Rajasthan Royals",
        "Royal Challengers Bangalore", "Punjab Kings",
        "Kolkata Knight Riders", "Delhi Capitals", "Sunrisers Hyderabad"
        ]

cities = [
         "Chennai", "Mumbai", "Ahmedabad", "Jaipur", "Bengaluru",
         "Kolkata", "Dharamsala", "Delhi", "Hyderabad"
         ]
# Creating boxes to input data
column1, column2 = st.columns(2)

with column1:
    BattingTeam = st.selectbox("Select the batting team", sorted(teams))

with column2:
    BowlingTeam = st.selectbox("Select the bowling team", sorted(teams))

City = st.selectbox("Select Host city", sorted(cities))
target = st.number_input("Target", value=0, step=1, format="%d")

column3, column4, column5 = st.columns(3)

with column3:
    score = st.number_input("Score", value=0, step=1, format="%d")

with column4:
    overs = st.number_input("Overs", value=0, step=1, format="%d")

with column5:
    wickets = st.number_input("Wickets", value=0, step=1, format="%d")

if score > target:
    st.error("Score should not be greater than the target.")
elif BattingTeam == BowlingTeam:
    st.error("Both cannot be the same team")
elif overs > 20:
    st.error("Overs should not exceed 20.")
elif wickets > 10:
    st.error("Wickets should not exceed 10.")
# Finding the probability if the button is clicked
elif st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    current_run_rate = score / overs
    required_run_rate = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({
        'BattingTeam': [BattingTeam],
        'BowlingTeam': [BowlingTeam],
        'City': [City],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'target': [target],
        'current_run_rate': [current_run_rate],
        'required_run_rate': [required_run_rate]
    })
    # Stores the trained value pipe into result as a list of list
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(BattingTeam + " - " + str(round(win * 100)) + "%")
    st.header(BowlingTeam + " - " + str(round(loss * 100)) + "%")

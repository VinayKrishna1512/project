import streamlit as st
import pickle
import pandas as pd
pipe = pickle.load(open('pipe.pkl', 'rb'))
st.title("IPL WIN PREDICTOR")

teams = [
        "Chennai Super Kings", "Mumbai Indians", "Gujarat Titans",
        "Lucknow Super Giants", "Rajasthan Royals",
        "Royal Challengers Bangalore", "Kings XI Punjab",
        "Kolkata Knight Riders", "Delhi Capitals", "Sunrisers Hyderabad"
        ]

cities = [
         "Chennai", "Mumbai", "Ahmedabad", "Lucknow", "Jaipur", "Bengaluru",
         "Mohali", "Kolkata", "Dharamsala", "Guwahati", "Delhi", "Hyderabad"
         ]

column1, column2 = st.beta_columns(2)

with column1:
    batting_team = st.selectbox("Select the batting team", sorted(teams))

with column2:
    bowling_team = st.selectbox("Select the bowling team", sorted(teams))

select_city = st.selectbox("Select Host city", sorted(cities))
target = st.number_input("Target")

column3, column4, column5 = st.beta_columns(3)

with column3:
    score = st.number_input("Score")

with column4:
    overs = st.number_input("Overs")

with column5:
    wickets = st.number_input("Wickets")

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [select_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + " - " + str(round(win * 100)) + "%")
    st.header(bowling_team + " - " + str(round(loss * 100)) + "%")

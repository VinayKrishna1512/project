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
          "Kolkata", "Dharamsala", "Guwahati", "Delhi", "Hyderabad"
         ]

column1, column2 = st.beta_columns(2)

with column1:
    BattingTeam = st.selectbox("Select the batting team", sorted(teams))

with column2:
    BowlingTeam = st.selectbox("Select the bowling team", sorted(teams))

City = st.selectbox("Select Host city", sorted(cities))
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

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(BattingTeam + " - " + str(round(win * 100)) + "%")
    st.header(BowlingTeam + " - " + str(round(loss * 100)) + "%")

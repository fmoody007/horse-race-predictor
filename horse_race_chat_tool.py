import streamlit as st
import json
import numpy as np
import pandas as pd

# Streamlit UI Header
st.title("🏇 Horse Race Predictor")

# File Upload: Race Card (Image)
uploaded_image = st.file_uploader("Upload Race Card (Image)", type=["png", "jpg", "jpeg"])

# File Upload: Race Data (JSON)
uploaded_json = st.file_uploader("Upload Race Data (JSON format)", type=["json"])

# Track Condition Dropdown
track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Turf"])

# Live Odds Input
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {2: '2/1', 4: '5/2'})")

# Function: Predict Best Horse
def predict_best_horse(race_data, track_condition, live_odds):
    best_horse = None
    highest_odds = float("inf")

    for horse in race_data["horses"]:
        horse_number = str(horse.get("number", ""))
        if isinstance(live_odds, dict) and horse_number in map(str, live_odds.keys()):
            odds_value = live_odds[horse_number]
            numeric_odds = sum(map(float, odds_value.split("/"))) if "/" in odds_value else float(odds_value)

            if numeric_odds < highest_odds:
                highest_odds = numeric_odds
                best_horse = horse["name"]

    return best_horse if best_horse else "No clear best horse found."

# Processing JSON Data
race_data = None
if uploaded_json:
    race_data = json.load(uploaded_json)

# Convert Live Odds Input (Text) to Dictionary
try:
    live_odds = json.loads(live_odds_input) if live_odds_input else {}
except json.JSONDecodeError:
    live_odds = {}
    st.error("Invalid JSON format in Live Odds input. Please correct it.")

# Process Prediction
if race_data and isinstance(race_data, dict):  # ✅ FIXED: Ensures correct format
    best_horse = predict_best_horse(race_data, track_condition, live_odds)
    st.success(f"🏆 Best Horse Prediction: **{best_horse}**")
else:
    st.warning("Please upload valid race data to proceed.")

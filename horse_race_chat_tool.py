import streamlit as st
import pytesseract
import numpy as np
import pandas as pd
from PIL import Image

# Function to process race card images and extract text
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to determine the best horse based on race data
def predict_best_horse(race_data, track_condition, live_odds):
    best_horse = None
    best_odds = float('inf')

    for horse in race_data["horses"]:
        if not isinstance(live_odds, dict):
            live_odds = {}

        horse_number = str(horse.get('number', ''))
        if horse_number in map(str, live_odds.keys()):
            horse_odds = live_odds[horse_number]

            # Check if this horse has better odds
            if float(horse_odds.replace('/', '.')) < best_odds:
                best_horse = horse
                best_odds = float(horse_odds.replace('/', '.'))

    return best_horse

# Streamlit UI
st.title("Horse Race Predictor")

# Upload Race Card (Image)
uploaded_image = st.file_uploader("Upload Race Card (Image)", type=["png", "jpg", "jpeg"])

# Upload Race Data (JSON)
uploaded_json = st.file_uploader("Upload Race Data (JSON format)", type=["json"])

# Track Condition Selection
track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Good"])

# Enter Live Odds Manually
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {2: '2/1', 4: '5/2'})")

# Process Inputs
if st.button("Predict Best Horse"):
    race_data = None
    if uploaded_json is not None:
        race_data = pd.read_json(uploaded_json)

    live_odds = {}
    if live_odds_input:
        try:
            live_odds = eval(live_odds_input)  # Ensure safe parsing
        except:
            st.error("Invalid JSON format for live odds.")

   if race_data is not None and not race_data.empty:
    best_horse = predict_best_horse(race_data, track_condition, live_odds)
        if best_horse:
            st.success(f"Best Horse Prediction: {best_horse['name']}")
        else:
            st.warning("No best horse could be determined.")
    else:
        st.error("Please upload valid race data.")

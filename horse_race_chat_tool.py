import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import json

# Function to process the race card image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to process JSON race data
def load_race_data(json_file):
    return json.load(json_file)

# Function to predict the best horse
def predict_best_horse(race_data, track_condition, live_odds):
    best_horse = None
    best_score = float('-inf')

    for horse in race_data["horses"]:
        horse_number = str(horse.get("number", ""))
        
        if isinstance(live_odds, dict) and horse_number in map(str, live_odds.keys()):
            odds = live_odds.get(horse_number, "99/1")
        else:
            odds = "99/1"

        # Convert odds to numerical probability (basic estimation)
        if "/" in odds:
            num, denom = odds.split("/")
            probability = float(denom) / (float(num) + float(denom))
        else:
            probability = 0.01  # Default fallback

        # Scoring formula considering track condition, odds, and past performance
        score = probability * 100

        if score > best_score:
            best_horse = horse
            best_score = score

    return best_horse

# Streamlit App
st.title("Horse Race Predictor")

# File upload section
uploaded_image = st.file_uploader("Upload Race Card (Image)", type=["png", "jpg", "jpeg"])
uploaded_json = st.file_uploader("Upload Race Data (JSON format)", type=["json"])

# Track condition selection
track_condition = st.selectbox("Track Condition", ["Fast", "Good", "Sloppy", "Muddy"])

# Live odds input
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {2: '2/1', 4: '5/2'})")

# Process user inputs
race_data = None
if uploaded_json:
    race_data = json.load(uploaded_json)

if live_odds_input:
    try:
        live_odds = json.loads(live_odds_input)
    except json.JSONDecodeError:
        st.error("Invalid JSON format in live odds.")
        live_odds = {}
else:
    live_odds = {}

# **Fixed Indentation Issue Here**
if race_data is not None and not race_data.empty:
    best_horse = predict_best_horse(race_data, track_condition, live_odds)

    if best_horse:
        st.subheader("Predicted Best Horse")
        st.write(f"🏇 **Horse Number:** {best_horse['number']}")
        st.write(f"📌 **Horse Name:** {best_horse['name']}")
        st.write(f"🎯 **Predicted Score:** {best_horse.get('score', 'N/A')}")
    else:
        st.warning("No strong prediction found.")
else:
    st.warning("Please upload a valid race data file.")

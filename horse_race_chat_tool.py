import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import numpy as np
import json

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def load_race_data(file):
    if file.name.endswith('.json'):
        return json.load(file)
    elif file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        extracted_text = extract_text_from_image(Image.open(file))
        return {'raw_text': extracted_text}
    else:
        return None

def predict_best_horse(race_data, track_condition, live_odds):
    if not race_data or 'horses' not in race_data:
        return "No valid race data found."
    
    horses = race_data['horses']
    best_horse = None
    best_odds = float('inf')
    
    for horse in horses:
        horse_number = str(horse.get('number', ''))
        if horse_number in live_odds:
            odds = live_odds[horse_number]
            numeric_odds = eval(odds.replace('/', '/'))
            if numeric_odds < best_odds:
                best_odds = numeric_odds
                best_horse = horse['name']
    
    return best_horse if best_horse else "No clear best horse found."

st.title("🐎 Horse Race Predictor 🏆")

uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])
track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Turf", "Synthetic"])
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {2: '2/1', 4: '5/2'})")

if st.button("Run Prediction"):
    if uploaded_file is not None:
        race_data = load_race_data(uploaded_file)
        live_odds = json.loads(live_odds_input) if live_odds_input else {}
        best_horse = predict_best_horse(race_data, track_condition, live_odds)
        st.write(f"🏆 **Best Horse Prediction:** {best_horse}")
    else:
        st.error("Please upload a race card file.")

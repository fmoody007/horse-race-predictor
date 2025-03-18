import streamlit as st
import pytesseract
from PIL import Image
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

def extract_odds_from_json(race_data):
    """Extracts odds directly from JSON if available"""
    odds_dict = {}
    if "horses" in race_data:
        for horse in race_data["horses"]:
            horse_number = str(horse.get("number", ""))
            horse_odds = horse.get("odds", "99/1")  # Default to high odds if missing
            odds_dict[horse_number] = horse_odds
    return odds_dict

def predict_best_horse(race_data, track_condition):
    """Predicts the best horse based on extracted odds and conditions."""
    if not race_data or 'horses' not in race_data:
        return "No valid race data found."
    
    horses = race_data['horses']
    best_horse = None
    best_odds = float('inf')
    
    live_odds = extract_odds_from_json(race_data)  # Automatically extract odds
    
    for horse in horses:
        horse_number = str(horse.get('number', ''))
        if horse_number in live_odds:
            odds_value = live_odds[horse_number]
            numeric_odds = eval(odds_value.replace('/', '/'))
            if numeric_odds < best_odds:
                best_odds = numeric_odds
                best_horse = horse['name']
    
    return best_horse if best_horse else "No clear best horse found."

st.title("🐎 Horse Race Predictor 🏆")

uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])
track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Turf", "Synthetic"])

if st.button("Run Prediction"):
    if uploaded_file is not None:
        race_data = load_race_data(uploaded_file)
        best_horse = predict_best_horse(race_data, track_condition)
        st.write(f"🏆 **Best Horse Prediction:** {best_horse}")
    else:
        st.error("Please upload a race card file.")

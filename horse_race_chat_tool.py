import streamlit as st
import pandas as pd
import numpy as np
import pytesseract
from PIL import Image
import json
import easyocr

# Initialize OCR reader
reader = easyocr.Reader(["en"])

# Function to extract text from an image
def extract_text_from_image(image):
    extracted_text = reader.readtext(image, detail=0)
    return "\n".join(extracted_text)

# Function to process JSON race card
def load_race_data(json_file):
    try:
        race_data = json.load(json_file)
        return race_data
    except Exception as e:
        st.error(f"Error loading race data: {e}")
        return None

# Function to predict the best horses
def predict_best_horses(race_data, track_condition, live_odds):
    horses = []
    
    for horse in race_data["horses"]:
        horse_number = str(horse.get("number", ""))
        odds = live_odds.get(horse_number, "N/A")

        # Use a scoring system based on odds and other factors
        performance_score = np.random.uniform(0, 1)  # Placeholder scoring system
        
        horses.append({
            "number": horse_number,
            "name": horse["name"],
            "odds": odds,
            "score": performance_score
        })
    
    # Sort horses based on the highest score
    horses_sorted = sorted(horses, key=lambda x: x["score"], reverse=True)

    return horses_sorted[:3] if horses_sorted else []

# Streamlit UI
st.title("🏇 Horse Race Predictor")
st.write("Upload a race card image or JSON file to analyze and predict race outcomes.")

# Upload section
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

# Track condition selection
track_condition = st.selectbox("Select Track Condition", ["Fast", "Sloppy", "Muddy", "Good"])

# Live odds input
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {'2': '2/1', '4': '5/2'})")

# Convert live odds input to dictionary
try:
    live_odds = json.loads(live_odds_input) if live_odds_input else {}
except json.JSONDecodeError:
    st.error("Invalid JSON format for live odds.")
    live_odds = {}

if uploaded_file:
    if uploaded_file.type == "application/json":
        # Process JSON file
        race_data = load_race_data(uploaded_file)
    else:
        # Process image file
        st.image(uploaded_file, caption="📸 Uploaded Race Card", use_container_width=True)
        extracted_text = extract_text_from_image(uploaded_file)
        st.text_area("Extracted Race Card Text", extracted_text, height=200)
        st.warning("⚠️ Image processing is still experimental. Verify extracted data.")

        # Placeholder for extracted race data (would need structured parsing)
        race_data = {"horses": []}  # Modify this to parse race details from text
    
    # Make predictions
    if race_data and race_data.get("horses"):
        best_horses = predict_best_horses(race_data, track_condition, live_odds)

        # Display predictions
        if best_horses:
            st.subheader("🏆 Predicted Top Horses")
            for i, horse in enumerate(best_horses, 1):
                st.write(f"**#{i} - {horse['name']}** (Odds: {horse['odds']})")
        else:
            st.warning("⚠️ No clear best horse found. Please check the input data.")
    else:
        st.error("❌ No race data found in the uploaded file.")

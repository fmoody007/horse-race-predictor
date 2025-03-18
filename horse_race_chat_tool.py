import streamlit as st
import pandas as pd
import json
import easyocr
import numpy as np
from PIL import Image
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(["en"], gpu=False)

# Function to extract text from an image
def extract_text_from_image(image):
    try:
        image_np = np.array(image.convert("RGB"))  # Convert to numpy array
        extracted_text = reader.readtext(image_np, detail=0)
        return " ".join(extracted_text)
    except Exception as e:
        return None

# Function to parse live odds from extracted text
def extract_live_odds(text):
    odds_pattern = re.compile(r"(\d+)[^\d]+(\d+/\d+|\d+)")
    return {match[0]: match[1] for match in odds_pattern.findall(text)}

# Function to parse race data from JSON
def parse_json_race_data(json_file):
    try:
        data = json.load(json_file)
        return data
    except Exception:
        return None

# Function to predict top 3 horses based on odds
def predict_best_horses(race_data, live_odds):
    if not race_data or "horses" not in race_data:
        return None

    horses = race_data["horses"]
    ranked_horses = []

    for horse in horses:
        number = str(horse.get("number", ""))
        if number in live_odds:
            odds = live_odds[number]
            ranked_horses.append((horse["name"], odds))

    if not ranked_horses:
        return None

    # Sort horses based on odds (lower is better)
    ranked_horses.sort(key=lambda x: float(x[1].split('/')[0]) / float(x[1].split('/')[1]) if '/' in x[1] else float(x[1]))

    # Return top 3 horses
    return [h[0] for h in ranked_horses[:3]]

# Streamlit App UI
st.title("🏇 Horse Race Predictor")

# Upload image or JSON
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

# Select track condition
track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Good", "Muddy"])

race_data = None
live_odds = {}

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type in ["png", "jpg", "jpeg"]:
        # Process image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Race Card", use_column_width=True)
        extracted_text = extract_text_from_image(image)

        if extracted_text:
            st.write("✅ **Extracted Race Data:**", extracted_text)
            live_odds = extract_live_odds(extracted_text)
            st.write("✅ **Extracted Live Odds:**", live_odds)
        else:
            st.error("⚠️ Could not extract readable text from the image. Try uploading a clearer image.")

    elif file_type == "json":
        # Process JSON
        race_data = parse_json_race_data(uploaded_file)

        if race_data:
            st.write("✅ **Parsed Race Data:**", race_data)
        else:
            st.error("⚠️ Invalid JSON format. Please check the structure.")

# Predict the best horses
if st.button("Predict Best Horses"):
    if race_data and live_odds:
        result = predict_best_horses(race_data, live_odds)
        if result:
            st.write("🏆 **Best Horse Predictions (Top 3):**", result)
        else:
            st.error("⚠️ No valid predictions found. Ensure odds were extracted correctly.")
    else:
        st.error("⚠️ Please upload a valid race data JSON file or an image with readable text.")

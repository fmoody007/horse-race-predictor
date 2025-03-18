import streamlit as st
import pandas as pd
import numpy as np
import easyocr
import cv2
from PIL import Image
import json
import torch

# Initialize EasyOCR reader
reader = easyocr.Reader(["en"])

# Function to extract text from an uploaded image
def extract_text_from_image(image_path):
    extracted_text = reader.readtext(image_path, detail=0)
    return " ".join(extracted_text)

# Function to parse race data from JSON
def parse_json_race_data(json_file):
    try:
        data = json.load(json_file)
        return data
    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
        return None

# Function to predict the best horse based on race data and live odds
def predict_best_horse(race_data, live_odds):
    if not race_data or "horses" not in race_data:
        return "No valid race data found."

    horses = race_data["horses"]
    ranked_horses = []

    for horse in horses:
        number = str(horse.get("number", ""))
        if number in live_odds:
            odds = live_odds[number]
            ranked_horses.append((horse["name"], odds))

    if not ranked_horses:
        return "No clear best horse found."

    # Sort horses based on odds (lower is better)
    ranked_horses.sort(key=lambda x: float(x[1].split('/')[0]) / float(x[1].split('/')[1]) if '/' in x[1] else float(x[1]))

    # Return top 3 horses
    top_horses = [h[0] for h in ranked_horses[:3]]
    return top_horses

# Streamlit App UI
st.title("🏇 Horse Race Predictor")

# Upload image or JSON
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

# Select track condition
track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Good", "Muddy"])

# Enter Live Odds (JSON format)
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {2: '2/1', 4: '5/2'})")

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type in ["png", "jpg", "jpeg"]:
        # Process image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Race Card", use_column_width=True)
        extracted_text = extract_text_from_image(uploaded_file)
        st.write("Extracted Race Data:", extracted_text)

    elif file_type == "json":
        # Process JSON
        race_data = parse_json_race_data(uploaded_file)
        if race_data:
            st.write("Parsed Race Data:", race_data)

# Convert input odds
try:
    live_odds = json.loads(live_odds_input) if live_odds_input else {}
except json.JSONDecodeError:
    st.error("Invalid JSON format for odds.")
    live_odds = {}

# Predict the best horse
if st.button("Predict Best Horse"):
    if uploaded_file and file_type == "json":
        result = predict_best_horse(race_data, live_odds)
        st.write("🏆 Best Horse Prediction:", result)
    else:
        st.error("Please upload a valid race data JSON file.")

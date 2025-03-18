import streamlit as st
import pandas as pd
import numpy as np
import easyocr
import json
import cv2
import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path, detail=0)
    return " ".join(results)

def extract_data_from_json(json_file):
    """Extract race details from a JSON file."""
    try:
        race_data = json.load(json_file)
        return race_data
    except json.JSONDecodeError:
        return None

def predict_best_horses(race_data, live_odds):
    """Predict top horses based on provided race data and live odds."""
    if not race_data or 'horses' not in race_data:
        return None, None, None
    
    horses = race_data['horses']
    horse_scores = {}
    for horse in horses:
        horse_number = str(horse.get('number', ''))
        if horse_number in live_odds:
            odds = live_odds[horse_number]
            score = 1 / (float(odds.split('/')[0]) / float(odds.split('/')[1]))
            horse_scores[horse_number] = score
    
    sorted_horses = sorted(horse_scores, key=horse_scores.get, reverse=True)
    return sorted_horses[:3] if len(sorted_horses) >= 3 else sorted_horses

st.title("Horse Race Predictor")

uploaded_file = st.file_uploader("Upload Race Card (JSON or Image)", type=["json", "png", "jpg", "jpeg"])
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {\"2\": \"2/1\", \"4\": \"5/2\"})")
track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Muddy", "Good"])

if uploaded_file:
    extracted_text = ""
    race_data = None
    
    if uploaded_file.type == "application/json":
        race_data = extract_data_from_json(uploaded_file)
    else:
        image = Image.open(uploaded_file)
        extracted_text = extract_text_from_image(uploaded_file)
        st.image(image, caption="Uploaded Race Card", use_container_width=True)
    
    if race_data is None and not extracted_text:
        st.error("Could not extract valid race data. Please upload a readable image or valid JSON file.")
    else:
        try:
            live_odds = json.loads(live_odds_input) if live_odds_input else {}
            best_horses = predict_best_horses(race_data, live_odds)
            if best_horses:
                st.success(f"🏆 Best Horse Predictions: {', '.join(best_horses)}")
            else:
                st.warning("No clear best horse found. Ensure race data and odds are correct.")
        except json.JSONDecodeError:
            st.error("Invalid odds format. Please enter odds in JSON format.")

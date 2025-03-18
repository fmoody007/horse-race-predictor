import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import json
import io

# Function to extract text from images using OCR
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to parse extracted text into structured race details
def parse_race_details(text):
    # Extract relevant race details (modify as needed for accuracy)
    lines = text.split("\n")
    race_data = []
    for line in lines:
        if line.strip():  # Avoid empty lines
            race_data.append(line.strip())

    return "\n".join(race_data)  # Return formatted text for display

# Function to process race data from JSON
def process_json_data(json_data):
    try:
        data = json.loads(json_data)
        return pd.DataFrame(data["horses"])  # Convert horses list to DataFrame
    except Exception as e:
        st.error(f"Error processing JSON: {e}")
        return None

# Streamlit UI
st.title("🏇 Horse Race Predictor - Image & JSON Support")

# Upload file
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["png", "jpg", "jpeg"]:  # If an image is uploaded
        image = Image.open(uploaded_file)
        extracted_text = extract_text_from_image(image)
        st.subheader("Extracted Race Details:")
        st.text(parse_race_details(extracted_text))

    elif file_type == "json":  # If a JSON file is uploaded
        json_data = uploaded_file.getvalue().decode("utf-8")
        race_df = process_json_data(json_data)
        if race_df is not None:
            st.subheader("Race Data (From JSON):")
            st.write(race_df)

    else:
        st.error("Unsupported file format. Please upload a PNG, JPG, JPEG, or JSON file.")

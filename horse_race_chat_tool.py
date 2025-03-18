import streamlit as st
import pandas as pd
import json
import requests
from PIL import Image
import numpy as np
import io

st.title("🏇 Horse Race Predictor - Image & JSON Auto Extraction")

# **Web-Based OCR Function**
def extract_text_from_image(image_file):
    api_key = "helloworld"  # Free demo key from OCR.Space
    url = "https://api.ocr.space/parse/image"
    
    # Convert image to byte stream
    image_bytes = io.BytesIO()
    image_file.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()

    response = requests.post(
        url,
        files={"filename": ("image.png", image_bytes, "image/png")},
        data={"apikey": api_key, "language": "eng"}
    )

    result = response.json()
    
    if result.get("ParsedResults"):
        return result["ParsedResults"][0]["ParsedText"]
    else:
        return "❌ OCR Failed! Try another image."

# Upload file (Image or JSON)
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["png", "jpg", "jpeg"]:  
        # Process Image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Race Card", use_column_width=True)
        
        # Extract text via OCR API
        extracted_text = extract_text_from_image(image)

        st.subheader("🔍 Extracted Race Details:")
        st.text(extracted_text)

    elif file_type == "json":  
        # Process JSON
        json_data = uploaded_file.getvalue().decode("utf-8")
        try:
            race_data = json.loads(json_data)
            race_df = pd.DataFrame(race_data["horses"])
            st.subheader("🏇 Race Data Extracted:")
            st.write(race_df)
        except Exception as e:
            st.error(f"Error processing JSON: {e}")

    else:
        st.error("❌ Unsupported file format. Please upload PNG, JPG, or JSON.")

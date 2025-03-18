import streamlit as st
import pandas as pd
import json
import requests
from PIL import Image
import numpy as np
import io

st.title("🏇 Horse Race Predictor - Image & JSON Auto Extraction")

# **OCR API Function (For Image Extraction)**
def extract_text_from_image(image_file):
    api_key = "helloworld"  # Free demo key from OCR.Space
    url = "https://api.ocr.space/parse/image"
    
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

# **Horse Prediction Model**
def predict_best_horses(race_data):
    if not race_data or "horses" not in race_data:
        return "❌ No race data found!"

    horses = race_data["horses"]
    horse_df = pd.DataFrame(horses)

    # Basic horse ranking logic (Can be improved with AI in the future)
    horse_df["odds_numeric"] = horse_df["odds"].astype(str).replace({"/": "."}, regex=True).astype(float)
    horse_df = horse_df.sort_values(by=["odds_numeric"], ascending=True)  # Lower odds = better ranking

    # Select top 3
    top_3_horses = horse_df.head(3)
    winner = top_3_horses.iloc[0]
    runner_up = top_3_horses.iloc[1] if len(top_3_horses) > 1 else None
    third_place = top_3_horses.iloc[2] if len(top_3_horses) > 2 else None

    # Display results
    st.subheader("🏆 Prediction Results:")
    st.success(f"🥇 Winner: {winner['horse']} ({winner['odds']})")
    if runner_up is not None:
        st.info(f"🥈 Runner-Up: {runner_up['horse']} ({runner_up['odds']})")
    if third_place is not None:
        st.warning(f"🥉 Third Place: {third_place['horse']} ({third_place['odds']})")

# **File Upload (Image or JSON)**
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["png", "jpg", "jpeg"]:  
        # Process Image
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Uploaded Race Card", use_column_width=True)
        
        # Extract text via OCR API
        extracted_text = extract_text_from_image(image)
        st.subheader("🔍 Extracted Race Details:")
        st.text(extracted_text)

        # **TODO: Convert extracted text to structured race data**
        # (Future improvement: Auto-convert text into JSON format)

    elif file_type == "json":  
        # Process JSON
        json_data = uploaded_file.getvalue().decode("utf-8")
        try:
            race_data = json.loads(json_data)
            race_df = pd.DataFrame(race_data["horses"])
            st.subheader("🏇 Race Data Extracted:")
            st.write(race_df)

            # **Run Prediction Model**
            predict_best_horses(race_data)

        except Exception as e:
            st.error(f"❌ Error processing JSON: {e}")

    else:
        st.error("❌ Unsupported file format. Please upload PNG, JPG, or JSON.")

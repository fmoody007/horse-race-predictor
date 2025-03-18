import streamlit as st
import pandas as pd
import json
import easyocr
from PIL import Image
import numpy as np

st.title("🏇 Horse Race Predictor - Image & JSON Auto Extraction")

# Initialize OCR reader (EasyOCR)
reader = easyocr.Reader(["en"])  # English language

# Upload file (Image or JSON)
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["png", "jpg", "jpeg"]:  
        # Process Image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Race Card", use_column_width=True)
        
        # Convert image to array for OCR
        image_np = np.array(image)
        extracted_text = reader.readtext(image_np, detail=0)

        st.subheader("🔍 Extracted Race Details:")
        extracted_text_cleaned = "\n".join(extracted_text)
        st.text(extracted_text_cleaned)

        # Future: Implement logic to structure the text into a table
        st.warning("⚠️ OCR Extracted the text! (Needs manual verification)")

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

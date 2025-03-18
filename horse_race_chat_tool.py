import streamlit as st
import pandas as pd
from PIL import Image
import json

st.title("🏇 Horse Race Predictor - Image & JSON Support")

# Upload file
uploaded_file = st.file_uploader("Upload Race Card (Image or JSON)", type=["png", "jpg", "jpeg", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["png", "jpg", "jpeg"]:  
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Race Card", use_column_width=True)
        st.warning("📌 Image uploaded! Please analyze manually or use an external OCR tool.")

    elif file_type == "json":  
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

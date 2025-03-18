import easyocr
import numpy as np
from PIL import Image
import io

reader = easyocr.Reader(['en'])  # Initialize OCR reader

def extract_text_from_image(uploaded_file):
    try:
        # Convert the uploaded file into an image
        image = Image.open(uploaded_file).convert("RGB")

        # Convert image into a NumPy array
        image_array = np.array(image)

        # Use EasyOCR to extract text
        extracted_text = reader.readtext(image_array, detail=0)

        return " ".join(extracted_text)  # Return extracted text as a single string

    except Exception as e:
        return f"Error processing image: {e}"

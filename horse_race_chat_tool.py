import json
import streamlit as st
def extract_text_from_image(image):
    """Extracts text from an uploaded image of a race card."""
    text = pytesseract.image_to_string(image)
    return text

def parse_race_card(text):
    """Parses raw text from a race card image into structured race data."""
    # Placeholder parsing logic (requires fine-tuning based on OCR output structure)
    lines = text.split("\n")
    race_data = []
    
    for line in lines:
        parts = line.split()
        if len(parts) > 2:  # Basic filtering
            try:
                horse_number = int(parts[0])  # Assume first value is the horse number
                horse_name = " ".join(parts[1:-1])  # Middle values as horse name
                odds = parts[-1]  # Last value assumed to be odds
                race_data.append({"number": horse_number, "name": horse_name, "odds": odds, "scratched": False})
            except ValueError:
                continue
    
    return race_data

def predict_best_horse(race_data, track_condition, live_odds):
    """Predicts the best horse based on conditions, live odds, and past wins."""
   for horse in race_data["horses"]:
    if not isinstance(live_odds, dict):
        live_odds = {}

    horse_number = str(horse.get('number', ''))
    if horse_number in map(str, live_odds.keys()):
        horse_odds = live_odds[horse_number]
    if horse_number in map(str, live_odds.keys()):
        horse_odds = live_odds[horse_number]
horse_number = str(horse.get('number', ''))
if horse_number in map(str, live_odds.keys()):
    horse_odds = live_odds[horse_number]  # Safely access the odds
    
    sorted_horses = sorted(
        race_data,
        key=lambda x: (
            x['odds'],
            -jockey_rating(x.get('jockey', 'Unknown')),
            -track_condition_bonus(x, track_condition),
            -previous_win_bonus(x)
        )
    )
    return sorted_horses[0] if sorted_horses else None

def jockey_rating(jockey_name):
    jockey_performance = {"Paco Lopez": 95, "Mychel Sanchez": 90, "Kendrick Carmouche": 85}
    return jockey_performance.get(jockey_name, 75)

def track_condition_bonus(horse, track_condition):
    wet_track_runners = {"Paco Lopez": 10, "Mychel Sanchez": 8, "Kendrick Carmouche": 7}
    return wet_track_runners.get(horse.get('jockey', ''), 0) if track_condition.lower() in ["sloppy", "wet"] else 0

def previous_win_bonus(horse):
    return 10 if horse.get('last_race_win', False) else 0

# Streamlit Chat-Based UI
st.title("🏇 Horse Race Predictor (Chat Mode)")

# Image Upload for OCR
image_file = st.file_uploader("Upload Race Card (Image)", type=["png", "jpg", "jpeg"])

if image_file is not None:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Race Card", use_column_width=True)
    extracted_text = extract_text_from_image(image)
    race_data = parse_race_card(extracted_text)
    st.json(race_data)

# Upload JSON for structured race data
uploaded_file = st.file_uploader("Upload Race Data (JSON format)", type=["json"])

track_condition = st.selectbox("Track Condition", ["Fast", "Sloppy", "Wet"])
live_odds_input = st.text_area("Enter Live Odds (JSON format, e.g., {2: '2/1', 4: '5/2'})")

if uploaded_file is not None:
    race_data = json.load(uploaded_file)
    live_odds = json.loads(live_odds_input) if live_odds_input else {}
    
    best_horse = predict_best_horse(race_data, track_condition, live_odds)
    
    if best_horse:
        st.success(f"🏆 The Best Horse to Bet On: {best_horse['name']} (Horse #{best_horse['number']}, Odds: {best_horse['odds']})")
    else:
        st.error("No valid selection available.")

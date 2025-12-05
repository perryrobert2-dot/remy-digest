import json
import os
import config

def load_hansard():
    """Loads the mock Hansard data."""
    # We look for data relative to the project root
    filepath = os.path.join(config.BASE_DIR, 'data', 'hansard_mock.json')
    
    if not os.path.exists(filepath):
        print(f"DEBUG: Hansard file not found at {filepath}")
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_latest_scoop(electorate_name):
    """
    Main function called by the site builder.
    Returns a dictionary with image, headline, and subtext.
    """
    # 1. Load the raw data
    data = load_hansard()
    if not data:
        return None

    # 2. Check if this data applies to the requested electorate
    # (For the MVP, we are forcing 'New England' to match the mock data)
    if electorate_name != "New England":
        return None

    text = data.get('speech_text', '').lower()
    mp = data.get('mp_name', 'Unknown MP')

    # 3. Generate Satire (The Logic)
    if "barbecue" in text or "dark ages" in text:
        return {
            "image": "https://storage.googleapis.com/remys-digest-public-assets/static/Two-Eyed%20Prone%20Beetroot%20in%20Suit.png",
            "headline": f"Sausage Shortage Panic in {electorate_name}",
            "subtext": f"{mp} seen hoarding onions; claims 'War on Weekend' requires strategic reserves."
        }
    
    return None
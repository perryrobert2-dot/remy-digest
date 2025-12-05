import json
import os
import random
import config

def load_hansard():
    """Loads the mock Hansard data."""
    filepath = os.path.join(config.BASE_DIR, 'data', 'hansard_mock.json')
    
    if not os.path.exists(filepath):
        print("Hansard file not found.")
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_hansard_satire(data):
    """
    Generates a headline based on speech text.
    """
    text = data['speech_text'].lower()
    mp = data['mp_name']
    
    # Satire Logic: Twist the politician's words into a local news event
    if "barbecue" in text:
        return {
            "headline": f"Sausage Shortage Panic in {data['electorate']}",
            "subtext": f"{mp} seen hoarding onions; claims 'War on Weekend' requires strategic reserves."
        }
    elif "dark ages" in text:
        return {
            "headline": "Local Man Yells at Candle",
            "subtext": "Insists wax is unreliable technology; demands nuclear-powered torch."
        }
    else:
        return {
            "headline": "Politician Speaks, Birds Fall from Sky",
            "subtext": "Boredom levels reach critical mass in parliament."
        }

def main():
    print("--- Starting The Remy Digest (Hansard Edition) ---")
    
    data = load_hansard()
    
    if data:
        print(f"\nAnalyzing speech by {data['mp_name']}...")
        print(f"Original Quote: \"{data['speech_text'][:60]}...\"")
        
        satire = generate_hansard_satire(data)
        
        print(f"\nHEADLINE: {satire['headline']}")
        print(f"SUBTEXT:  {satire['subtext']}")

if __name__ == "__main__":
    main()
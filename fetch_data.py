import requests
import json
import os
import config

def get_voting_record(mp_id):
    """
    Fetches the most recent voting divisions for a specific MP.
    """
    url = f"{config.API_BASE_URL}/people/{mp_id}.json"
    params = {'key': config.API_KEY}
    
    print(f"🎣 Casting line for {mp_id}...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Check if the request failed
        data = response.json()
        
        # We are interested in the 'policy_comparisons' or 'divisions' 
        # depending on what you want to satirize. 
        # Let's grab the raw structure to inspect first.
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data for {mp_id}: {e}")
        return None

def save_raw_data(electorate_name, data):
    """
    Saves the fetched data to a file so we don't have to hit the API constantly.
    """
    if not data:
        return

    # Create a 'data' folder if it doesn't exist
    data_dir = os.path.join(config.BASE_DIR, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filename = f"{electorate_name.lower().replace(' ', '_')}_raw.json"
    filepath = os.path.join(data_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    print(f"📦 Catch of the day saved to: {filename}")

def main():
    print("--- Starting The Remy Digest Fact Harvest ---")
    
    for electorate, details in config.ELECTORATE_MAP.items():
        mp_id = details['mp_id']
        raw_data = get_voting_record(mp_id)
        save_raw_data(electorate, raw_data)

    print("--- Harvest Complete. Ready for Satirization. ---")

if __name__ == "__main__":
    main()
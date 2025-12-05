import os
import json
import random
from google import genai
from google.genai import types

# --- Configuration ---
KEYS_FILE = "keys.json"
STAFF_FILE = os.path.join("data", "staff.json")
HEADLINES_FILE = os.path.join("data", "latest_headlines.json")
OUTPUT_FILE = os.path.join("data", "stories.json")

# --- THE TROPPO MANDATE ---
POLITICAL_MANDATE = """
1. THE MENAGERIE: Do NOT use Foxes or Dingoes for the story characters.
   - Use: Wombats (Union reps), Echidnas (Prickly locals), Koalas (Lazy council workers), Bin Chickens/Ibis (Garbage collectors), Cane Toads (Invaders), Cockatoos (Loud neighbors).
2. THE VISUAL RULE: The 'Visual Prompt' must describe a SCENE. It must NEVER describe the reporter/writer.
   - BAD: "Puddles the dog looking at a pothole."
   - GOOD: "A close up of a massive pothole in the road with a traffic cone inside it."
3. NO HUMANS: The world is inhabited only by anthropomorphic animals.
"""

def load_json(filepath):
    try:
        with open(filepath, 'r') as f: return json.load(f)
    except FileNotFoundError: return None

def main():
    keys = load_json(KEYS_FILE)
    staff = load_json(STAFF_FILE)
    headlines = load_json(HEADLINES_FILE)

    if not keys or not staff: 
        print("Error: Missing keys or staff.json")
        return

    # Fallback if scraper failed
    if not headlines:
        headlines = [{"clean_title": "Man fights snake over last beer", "source_query": "Backup"}]

    print(f"--- The War Room is Active ---")
    
    client = genai.Client(api_key=keys.get("gemini"))

    prompt = f"""
    You are the Editor of 'The Remyverse'.
    
    MANDATE:
    {POLITICAL_MANDATE}
    
    STAFF (Do NOT put these characters in the images!):
    {json.dumps(staff)}

    NEWS FEED:
    {json.dumps(headlines)}

    TASK:
    Select exactly 5 stories to cover the following sections.
    1. **masthead** (Soliloquy): Remy's tragic take.
    2. **campaign** (Meme): A pro-Independent meme (Blue Wren).
    3. **news** (Standard): Local news.
    4. **backpage** (Standard): The "Troppo" story (crazy/bizarre).
    5. **letters** (Standard): A reader complaint.

    OUTPUT FORMAT (JSON Array):
    [
        {{
            "section": "...",
            "writer_key": "...",
            "headline": "...",
            "subtext": "...",
            "body": "...",
            "visual_prompt": "A detailed description of the scene for the image generator. MUST NOT INCLUDE THE WRITER. Specify the animal species explicitly (e.g. 'A Koala sleeping'). NO HUMANS.",
            "format": "standard/soliloquy/meme",
            "featured": true/false,
            "image": null
        }}
    ]
    """

    story_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "section": {"type": "STRING", "enum": ["masthead", "campaign", "news", "backpage", "letters"]},
                "writer_key": {"type": "STRING"},
                "headline": {"type": "STRING"},
                "subtext": {"type": "STRING"},
                "body": {"type": "STRING"},
                "visual_prompt": {"type": "STRING"},
                "format": {"type": "STRING", "enum": ["standard", "soliloquy", "debate", "meme"]},
                "featured": {"type": "BOOLEAN"},
                "image": {"type": "STRING", "nullable": True}
            },
            "required": ["section", "writer_key", "headline", "subtext", "body", "visual_prompt", "format", "featured"]
        }
    }

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=story_schema
            )
        )
        
        new_stories = json.loads(response.text)
        new_stories = new_stories[:5] # Hard limit

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(new_stories, f, indent=4)
            
        print(f"Success! {len(new_stories)} stories commissioned. (Strict Anti-Conflation Protocols Active)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
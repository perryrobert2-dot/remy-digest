import json
import os
import time
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# --- Configuration ---
KEYS_FILE = "keys.json"
DATA_FILE = os.path.join("data", "stories.json")
IMAGE_DIR = os.path.join("output", "images")
RELATIVE_IMG_PATH = "images"
MODEL_ID = "gemini-2.5-flash-image"

# THE NO-GO ZONE
NEGATIVE_PROMPT = "NO HUMANS, NO PEOPLE, NO MAN, NO WOMAN, NO CHILD, NO FACES, NO TEXT, NO WATERMARKS, NO SIGNATURES, NO BLUR, NO DISTORTION."

def load_keys():
    try:
        with open(KEYS_FILE, 'r') as f: return json.load(f)
    except FileNotFoundError: return None

def main():
    keys = load_keys()
    if not keys: return

    client = genai.Client(api_key=keys.get("gemini"))

    try:
        with open(DATA_FILE, 'r') as f: stories = json.load(f)
    except FileNotFoundError:
        print("No stories found.")
        return

    os.makedirs(IMAGE_DIR, exist_ok=True)
    print(f"--- The Darkroom is Open ({MODEL_ID}) ---")
    
    updated_count = 0

    for i, story in enumerate(stories):
        # SKIP if image already exists (Protects manual uploads)
        if story.get("image"): 
            print(f"Skipping {story['headline']} (Image already assigned)")
            continue

        print(f"\nDeveloping photo for: {story['headline']}")
        
        # 1. Base Style
        base_style = "Style: Ligne Claire (Herge/Tintin), editorial cartoon, flat colors, clear lines."
        
        # 2. Format Adjustments
        fmt = story.get('format', 'standard')
        visual_prompt = story.get('visual_prompt', story['headline'])
        
        composition = "COMPOSITION: Wide shot, establish the scene."
        if fmt == "soliloquy":
            composition = "COMPOSITION: Theatrical spotlight on a single subject. Dark background."
        elif fmt == "meme":
            composition = "COMPOSITION: Subject centered, solid background, plenty of negative space at top and bottom."

        # 3. The Prompt Payload
        full_prompt = f"""
        {base_style}
        SUBJECT: {visual_prompt}
        {composition}
        IMPORTANT: {NEGATIVE_PROMPT}
        """

        while True:
            print(f"Shooting ({fmt})...")
            try:
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                    )
                )

                image_data = None
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if part.inline_data:
                            image_data = part.inline_data.data
                            break
                
                if not image_data:
                    print("Error: Model returned text. Retrying...")
                    time.sleep(1)
                    continue

                image = Image.open(BytesIO(image_data))
                image.show()

                choice = input(">> [K]eep, [R]etry, or [S]kip? ").lower()

                if choice == 'k':
                    slug = "".join(x for x in story['headline'] if x.isalnum())[:20]
                    filename = f"{slug}_{int(time.time())}.png"
                    save_path = os.path.join(IMAGE_DIR, filename)
                    image.save(save_path)
                    story['image'] = f"{RELATIVE_IMG_PATH}/{filename}"
                    updated_count += 1
                    break 
                elif choice == 's': break
                elif choice == 'r': print("Retrying generation...")
            
            except Exception as e:
                print(f"Camera Jammed: {e}")
                break

    if updated_count > 0:
        with open(DATA_FILE, 'w') as f:
            json.dump(stories, f, indent=4)
        print(f"\nSuccess! {updated_count} photos approved.")

if __name__ == "__main__":
    main()
import json
import os
import time
import google.generativeai as genai
from io import BytesIO
from PIL import Image

# --- Configuration ---
KEYS_FILE = "keys.json"
DATA_FILE = os.path.join("data", "stories_generated.json")
IMAGE_DIR = "assets"

# SELECTED MODEL FROM YOUR LIST
MODEL_ID = "models/gemini-2.5-flash-image"

def load_keys():
    try:
        with open(KEYS_FILE, 'r') as f: return json.load(f)
    except FileNotFoundError: return None

def main():
    keys = load_keys()
    if not keys: 
        print("❌ Keys file missing.")
        return

    # Handle both key names
    api_key = keys.get("GEMINI_API_KEY") or keys.get("gemini")
    if not api_key:
        print("❌ API Key not found.")
        return

    # Configure the SDK
    genai.configure(api_key=api_key)
    
    # Initialize the Model
    model = genai.GenerativeModel(MODEL_ID)

    if not os.path.exists(DATA_FILE):
        print("❌ No stories found. Run generate_news.py first.")
        return

    with open(DATA_FILE, 'r') as f: 
        content_dict = json.load(f)

    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    print(f"--- 📸 The Darkroom is Open ({MODEL_ID}) ---")
    
    updated_count = 0

    for section_key, story in content_dict.items():
        
        # Skip if no prompt
        if "image_prompt" not in story or not story["image_prompt"]:
            continue

        # Skip if image already exists
        if story.get("image_path") and os.path.exists(story["image_path"]): 
            print(f"Skipping {section_key} (Image already exists)")
            continue

        print(f"\nDeveloping photo for section: {section_key}")
        print(f"Headline: {story['headline']}")
        
        # Construct Prompt
        full_prompt = f"""
        Generate an image.
        Art Style: Ligne Claire, Hergé style, Tintin style, flat colors, clear black outlines, vintage comic book coloring.
        Subject: {story['image_prompt']}
        NO HUMANS, NO REALISTIC PEOPLE, NO TEXT, NO WATERMARKS, NO BLUR.
        """

        while True:
            print(f"   Shooting...")
            
            try:
                # API Call using the SDK
                response = model.generate_content(full_prompt)
                
                # Check if we got an image back
                if not response.parts:
                    print("   ⚠️  Film overexposed (Blocked by safety filter).")
                    break
                
                # Extract image data (it comes as inline_data in parts)
                img_part = None
                for part in response.parts:
                    if part.inline_data:
                        img_part = part
                        break
                
                if not img_part:
                    print("   ⚠️  No image data returned.")
                    break

                # Convert raw bytes to Image
                image = Image.open(BytesIO(img_part.inline_data.data))
                image.show()

                choice = input("   >> [K]eep, [R]etry, or [S]kip? ").lower()

                if choice == 'k':
                    filename = f"{section_key}_{int(time.time())}.png"
                    save_path = os.path.join(IMAGE_DIR, filename)
                    
                    image.save(save_path)
                    
                    story['image_path'] = f"assets/{filename}"
                    updated_count += 1
                    print(f"   ✅ Saved to {save_path}")
                    break 
                elif choice == 's': 
                    break
                elif choice == 'r': 
                    print("   🔄 Retrying generation...")

            except Exception as e:
                print(f"   ❌ Camera Jammed: {e}")
                break
            
    # Save JSON updates
    if updated_count > 0:
        with open(DATA_FILE, 'w') as f:
            json.dump(content_dict, f, indent=4)
        print(f"\nSuccess! {updated_count} photos developed.")

if __name__ == "__main__":
    main()
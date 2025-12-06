import google.generativeai as genai
import json
import os

# 1. Load your API Key
if not os.path.exists('keys.json'):
    print("❌ keys.json not found!")
    exit()

with open('keys.json') as f:
    keys = json.load(f)

# Handle both key names just in case
api_key = keys.get("GEMINI_API_KEY") or keys.get("gemini")
if not api_key:
    print("❌ No API Key found in keys.json")
    exit()

# 2. Configure the SDK
genai.configure(api_key=api_key)

print("📡 Querying Google for available models...")
print("=========================================")

try:
    # 3. List all models
    count = 0
    for m in genai.list_models():
        # We are looking for models that can generate content
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
            print(f"   Disp: {m.display_name}")
            print(f"   Vers: {m.version}")
            print(f"   Cap:  {m.supported_generation_methods}")
            print("-----------------------------------------")
            count += 1
            
    print(f"\n✅ Found {count} available models.")
    
except Exception as e:
    print(f"❌ Error connecting to Google: {e}")
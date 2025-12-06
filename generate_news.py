import json
import os
import google.generativeai as genai
from story_manager import StoryManager

# --- CONFIGURATION ---
# Load API Key
with open('keys.json') as f:
    keys = json.load(f)

genai.configure(api_key=keys["GEMINI_API_KEY"])

# UPDATE: Using the new stable Gemini 2.5 Flash model
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize the Story Engine
director = StoryManager()

# --- THE NEWSROOM CAST ---
CAST = {
    "Remy": {
        "species": "Dachshund",
        "voice": "Dignified, weary, slightly aristocratic. Uses words like 'alas' and 'furthermore'.",
        "role": "Editor-in-Chief",
        "style": "engraving"
    },
    "Swoop": {
        "species": "Australian Magpie",
        "voice": "Paranoid, gossipy, fast-paced Noir detective. Starts sentences with 'I saw it!'. Obsessed with shiny things.",
        "role": "Crime Reporter",
        "style": "ligne_claire"
    },
    "Bunty": {
        "species": "Standard Poodle",
        "voice": "Snobbish, uses incorrect French, obsessed with property values and 'curation'.",
        "role": "Social Correspondent",
        "style": "ligne_claire"
    },
    "Binnsy": {
        "species": "Australian White Ibis (Bin Chicken)",
        "voice": "Pompous, academic, unbearable. Sees garbage as 'found art installations'.",
        "role": "Arts Critic",
        "style": "ligne_claire"
    },
    "Sly": {
        "species": "Red Fox",
        "voice": "Slick, deceptive, fast-talking. Uses real estate buzzwords like 'STCA' and 'Renovator's Delight'.",
        "role": "Real Estate Agent",
        "style": "ligne_claire"
    },
    "Mick_and_Scampy": {
        "species": "Mallard Drake (Mick) & Sugar Glider (Scampy)",
        "voice": "Mick is a bloke who loves utes and common sense. Scampy is a nervous, high-energy policy doctor using buzzwords. They bicker.",
        "role": "Political Correspondents",
        "style": "ligne_claire"
    },
    "Buster": {
        "species": "British Bulldog",
        "voice": "Gruff, cliché-heavy ('Full credit to the boys', 'Gave 110%'). Loves meat pies.",
        "role": "Sports Desk",
        "style": "ligne_claire"
    },
    "Madame_Mews": {
        "species": "Black Cat",
        "voice": "Cryptic, aloof, slightly insulting. Gives terrible, lazy advice.",
        "role": "Agony Aunt / Mystic",
        "style": "ligne_claire"
    },
    "Dazza": {
        "species": "Cane Toad",
        "voice": "Chaotic, sweaty, slang-heavy. Hates 'Southerners'. Loves humidity and XXXX Gold.",
        "role": "Northern Correspondent",
        "style": "ligne_claire"
    },
    "Zoomie": {
        "species": "Jack Russell Terrier",
        "voice": "Brainrot generation. 'No cap', 'fr fr', '💀', 'skibidi'. Hyperactive. Rides an E-bike.",
        "role": "Youth Reporter",
        "style": "ligne_claire"
    },
    "Coco": {
        "species": "Persian Cat",
        "voice": "Influencer. Obsessed with selfies, lighting, and avocado toast. Vapid.",
        "role": "Lifestyle Influencer",
        "style": "ligne_claire"
    },
    "Webster": {
        "species": "Huntsman Spider",
        "voice": "Highly anxious, types fast, terrified of shoes. Tech support lingo.",
        "role": "Webmaster / IT",
        "style": "ligne_claire"
    }
}

def generate_article(section, headlines, writer_key):
    """
    Generates a story using the specific persona and injecting any plot instructions.
    """
    writer = CAST.get(writer_key, CAST["Remy"])
    
    # 1. Check for Plot Directions (The Arc)
    plot_instruction = director.get_direction(writer_key)
    
    # 2. Special Logic: Sussan Ley Sibilance
    # If any headline mentions Sussan Ley, we add specific instructions
    sussan_logic = ""
    headline_str = str(headlines)
    if "Ley" in headline_str or "Sussan" in headline_str:
        sussan_logic = """
        SPECIAL INSTRUCTION: Opposition Leader Sussan Ley is mentioned.
        - You MUST use sibilance in her quotes (elongate 's' sounds like 'thisss').
        - She must reference 'Numerology' or 'The Numbers' as the reason for her decisions.
        """

    # 3. Build the Prompt
    prompt = f"""
    You are {writer['species']} named {writer_key}.
    Role: {writer['role']}
    Personality: {writer['voice']}
    
    TASK: Write a short article (max 250 words) for the '{section}' section of 'The Remy Digest'.
    
    CONTEXT / HEADLINES:
    {json.dumps(headlines)}
    
    {plot_instruction}
    {sussan_logic}
    
    CONSTRAINTS:
    - Keep it satirical but grounded in the persona.
    - If this is Local News, strictly refer to Cromer/Northern Beaches. NO TROPICAL REFERENCES (unless you are Dazza).
    - If you are Dazza, you ONLY talk about Queensland/NT chaos.
    - If you are Mick/Scampy, contrast the rough bloke vs the polished doctor.
    
    OUTPUT FORMAT:
    Return strictly Valid JSON. Do not include markdown formatting.
    {{ 
        "headline": "The satirical headline", 
        "body": "The story text...", 
        "image_prompt": "A description for the AI artist in {writer['style']} style..." 
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean markdown if present to ensure JSON parsing
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"❌ Error generating {section}: {e}")
        # Return a fallback so the site doesn't crash
        return {
            "headline": f"Writer {writer_key} is Napping", 
            "body": "Content could not be generated. The writer is currently chasing a ball.", 
            "image_prompt": f"Sleeping {writer['species']}"
        }

def main():
    print("🗞️  Spinning up the Newsroom...")
    
    # Check if headlines exist
    headline_file = "data/current_headlines.json"
    if not os.path.exists(headline_file):
        print(f"❌ Error: {headline_file} not found. Run 'gather_headlines.py' first.")
        return

    with open(headline_file) as f:
        news_budget = json.load(f)
    
    output = {}

    # --- ASSIGNMENTS (Connecting Writers to Desks) ---
    
    print("   ...Remy is writing the Front Page")
    output["front_page"] = generate_article("Front Page", news_budget["local_news"], "Remy")
    
    print("   ...Mick & Scampy are arguing in Canberra")
    output["politics"] = generate_article("Capital Hill", news_budget["national_news"], "Mick_and_Scampy")
    
    print("   ...Swoop is scanning for crime")
    output["local"] = generate_article("Crime Watch", news_budget["local_news"], "Swoop")
    
    print("   ...Binnsy is judging art")
    output["arts"] = generate_article("Arts Review", news_budget["local_news"], "Binnsy")
    
    print("   ...Sly is selling a shack")
    output["real_estate"] = generate_article("Property", [], "Sly") 
    
    print("   ...Buster is eating a pie (Sport)")
    output["sport"] = generate_article("Sport", news_budget["local_news"], "Buster")
    
    print("   ...Zoomie is doing wheelies")
    output["youth_sport"] = generate_article("Youth Sport", [], "Zoomie")

    print("   ...Coco is taking selfies")
    output["lifestyle"] = generate_article("Lifestyle", [], "Coco")

    print("   ...Madame Mews is gazing into the void")
    output["horoscope"] = generate_article("Horoscope", [], "Madame_Mews")

    print("   ...Dazza is drinking a Gold (Troppo)")
    output["troppo"] = generate_article("Troppo News", news_budget["troppo_corner"], "Dazza")

    print("   ...Webster is logging the errors")
    output["tech"] = generate_article("Tech Support", [], "Webster")

    # Save the generated stories
    output_path = "data/stories_generated.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=4)
        
    print(f"✅ Edition Generated. Saved to {output_path}")
    
    # Advance the plot for tomorrow
    director.advance_plot()

if __name__ == "__main__":
    main()
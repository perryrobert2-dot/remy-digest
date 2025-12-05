import feedparser
import json
import os

# --- Configuration ---
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "latest_headlines.json")

# Keywords that indicate a "Troppo" story (High Priority)
CRAZY_KEYWORDS = [
    "croc", "alligator", "shark", "snake", "python", "ufo", "alien",
    "attack", "brawl", "fight", "naked", "nude", "stolen", "beer", "pub",
    "toilet", "spider", "weird", "bizarre", "ghost", "mystery", "crash",
    "man", "woman", "florida", "boar", "pig", "drunken", "rampage"
]

def score_headline(text):
    """Gives a story points for being crazy."""
    text = text.lower()
    score = 0
    for word in CRAZY_KEYWORDS:
        if word in text:
            score += 1
    return score

def get_google_news_headlines(query):
    encoded_query = query.replace(" ", "+")
    # expanded to 'when:7d' (past 7 days) to find older but crazier news
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}+when:7d&hl=en-AU&gl=AU&ceid=AU:en"
    
    print(f"Scanning horizon for: {query}...")
    feed = feedparser.parse(rss_url)
    
    results = []
    for entry in feed.entries:
        clean_title = entry.title.split(' - ')[0]
        # Ignore boring stuff
        if "council" in clean_title.lower() or "meeting" in clean_title.lower():
            continue
            
        results.append({
            'source_query': query,
            'title': clean_title,
            'link': entry.link,
            'published': entry.published,
            'clean_title': clean_title,
            'crazy_score': score_headline(clean_title)
        })
    return results

# Expanded Search Radius
targets = [
    "site:ntnews.com.au",           # The Gold Standard
    "Cairns Post",                  # Tropical North
    "Townsville Bulletin",          # North QLD
    "Gold Coast Bulletin",          # The Florida of Australia
    "Far North Queensland News",    # General Tropical
    "Northern Territory News"       # General NT
]

def main():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

    all_stories = []
    for target in targets:
        stories = get_google_news_headlines(target)
        all_stories.extend(stories)

    # SORT BY CRAZINESS (Highest score first)
    # This ensures "Man fights Croc" beats "Council approves budget"
    sorted_stories = sorted(all_stories, key=lambda x: x['crazy_score'], reverse=True)

    # Take top 15 candidates for the AI to choose from
    top_picks = sorted_stories[:15]

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(top_picks, f, indent=4)
        print(f"\nSuccess! Caught {len(top_picks)} potential stories.")
        print("Top 3 Craziest Headlines found:")
        for i, s in enumerate(top_picks[:3]):
            print(f"{i+1}. [{s['crazy_score']} pts] {s['clean_title']}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()
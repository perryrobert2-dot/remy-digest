import feedparser
import json
import urllib.parse
import questionary
import os
from datetime import datetime

# --- Configuration ---
RSS_BASE = "https://news.google.com/rss/search"

# Ensure data directory exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- SEARCH QUERIES ---

# 1. The Local Beat (Expanded to ensure hits)
LOCAL_QUERY = '("Northern Beaches" OR "Manly" OR "Dee Why" OR "Brookvale" OR "Frenchs Forest" OR "Cromer" OR "Narrabeen" OR "Warringah" OR "Mackellar")'

# 2. Macquarie St (State News)
STATE_QUERY = '("NSW Government" OR "Chris Minns" OR "Transport for NSW" OR "NSW Police") -site:ntnews.com.au'

# 3. Canberra Bubble (National - targeted at our MPs and the Opposition)
NATIONAL_QUERY = '("Federal Politics" OR "Anthony Albanese" OR "Sussan Ley" OR "Peter Dutton" OR "Sophie Scamps" OR "Zali Steggall") when:2d'

# 4. The Troppo Zone (The "Crazy" Filter)
# We search specifically for these keywords to find the "crazy" stories
TROPPO_KEYWORDS = [
    "croc", "snake", "attack", "pub", "naked", "ute", "mango", "stolen", 
    "ufo", "shark", "dugong", "giant", "toad"
]
# Construct query: (Source A OR Source B) AND (Keyword A OR Keyword B)
trop_kw_str = " OR ".join(TROPPO_KEYWORDS)
TROPPO_QUERY = f'(source:"NT News" OR source:"Cairns Post" OR source:"Townsville Bulletin" OR source:"Gold Coast Bulletin") AND ({trop_kw_str})'

def fetch_feed(category, query, limit=5):
    """
    Fetches headlines from Google News RSS based on a search query.
    """
    print(f"🕵️  Scouting {category}...")
    
    # URL Encode the query
    encoded_query = urllib.parse.quote(query)
    # Construct Google News RSS URL (Region: AU, Language: English)
    rss_url = f"{RSS_BASE}?q={encoded_query}&hl=en-AU&gl=AU&ceid=AU:en"
    
    feed = feedparser.parse(rss_url)
    
    headlines = []
    # Safeguard: check if entries exist
    if not feed.entries:
        print(f"   (No results found for query: {query})")
        return []

    for entry in feed.entries[:limit]:
        # Clean title "Title - Source" -> "Title"
        clean_title = entry.title.split(" - ")[0]
        
        # Safe access to source title
        source_title = "Unknown Source"
        if hasattr(entry, 'source') and hasattr(entry.source, 'title'):
            source_title = entry.source.title
        
        headlines.append({
            "title": clean_title,
            "url": entry.link,
            "source": source_title,
            "published": entry.published if hasattr(entry, 'published') else "Just now"
        })
        
    return headlines

def select_stories(category, articles):
    """
    Interactive menu to let the user choose which stories make the cut.
    """
    if not articles:
        print(f"⚠️  No stories found for {category}. Skipping selection.")
        return []

    # Create choices for the menu
    choices = [
        questionary.Choice(
            title=f"{a['title']} ({a['source']})",
            value=a,
            checked=True  # Default to selecting all
        )
        for a in articles
    ]

    # Show the interactive checkbox menu
    selected = questionary.checkbox(
        f"Select stories for {category}:",
        choices=choices
    ).ask()

    return selected

def main():
    print("\n🗞️  THE REMY DIGEST: MORNING SCOUT 🗞️")
    print("=======================================")

    news_budget = {
        "local_news": [],
        "state_news": [],
        "national_news": [],
        "troppo_corner": []
    }

    # --- Mission 1: Local News ---
    raw_local = fetch_feed("Local News", LOCAL_QUERY, limit=10)
    news_budget["local_news"] = select_stories("Local News", raw_local)

    # --- Mission 2: State News ---
    raw_state = fetch_feed("NSW State News", STATE_QUERY, limit=5)
    news_budget["state_news"] = select_stories("State News", raw_state)

    # --- Mission 3: National News ---
    raw_nat = fetch_feed("Federal Politics", NATIONAL_QUERY, limit=5)
    news_budget["national_news"] = select_stories("National News", raw_nat)

    # --- Mission 4: Troppo Corner ---
    raw_troppo = fetch_feed("Troppo/Crazy News", TROPPO_QUERY, limit=8)
    news_budget["troppo_corner"] = select_stories("Troppo Corner", raw_troppo)

    # --- Save to JSON ---
    output_path = os.path.join(DATA_DIR, "current_headlines.json")
    with open(output_path, "w") as f:
        json.dump(news_budget, f, indent=4)

    print(f"\n✅ News Budget locked in '{output_path}'.")
    print(f"   Local: {len(news_budget['local_news'])}")
    print(f"   State: {len(news_budget['state_news'])}")
    print(f"   Natl:  {len(news_budget['national_news'])}")
    print(f"   Crazy: {len(news_budget['troppo_corner'])}")

if __name__ == "__main__":
    main()
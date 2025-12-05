import feedparser
import json
import os

# 1. Setup paths
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "latest_headlines.json")

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_google_news_headlines(query):
    # q={query} -> Search term
    # gl=AU -> Geo-location Australia
    # ceid=AU:en -> Country endpoint Australia (English)
    encoded_query = query.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-AU&gl=AU&ceid=AU:en"
    
    print(f"Fetching headlines for: {query}...")
    feed = feedparser.parse(rss_url)
    
    results = []
    for entry in feed.entries[:5]: # Limit to top 5 stories per target
        results.append({
            'source_query': query,
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            # Clean title by removing the source suffix (e.g. " - ABC News")
            'clean_title': entry.title.split(' - ')[0] 
        })
    return results

# 2. Define Targets
targets = [
    "site:ntnews.com.au",           # NT News specific
    "Manly Observer",               # Local keyword
    "Northern Beaches Advocate"     # Local keyword
]

# 3. Gather Data
all_stories = []
for target in targets:
    stories = get_google_news_headlines(target)
    all_stories.extend(stories)

# 4. Save to JSON
try:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_stories, f, indent=4)
    print(f"\nSuccess! Saved {len(all_stories)} headlines to {OUTPUT_FILE}")
except Exception as e:
    print(f"Error saving file: {e}")

# Display for verification
print("-" * 30)
for story in all_stories:
    print(f"[{story['source_query']}] {story['clean_title']}")
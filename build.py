import json
import os
import datetime

# --- CONFIGURATION ---
CONTENT_FILE = "data/stories_generated.json"
# FIX: Change OUTPUT_FILE to include the 'output' directory
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "index.html")
ASSET_DIR = "assets" 

# Define the "Desks" (The Scroll Order)
SECTIONS = {
    "THE FRONT PAGE": [
        {"key": "front_page", "type": "lead"},
        {"key": "politics", "type": "special_politics"},
        {"key": "local", "type": "standard"}
    ],
    "THE PULSE": [
        {"key": "real_estate", "type": "standard"},
        {"key": "arts", "type": "review"},
        {"key": "lifestyle", "type": "standard"}
    ],
    "THE VOICES": [
        {"key": "tech", "type": "terminal"},  
        {"key": "horoscope", "type": "mystic"}
    ],
    "THE BACK PAGE": [
        {"key": "sport", "type": "standard"},
        {"key": "youth_sport", "type": "youth"}, 
        {"key": "troppo", "type": "warning"}     
    ]
}

def load_content():
    if not os.path.exists(CONTENT_FILE):
        return {}
    with open(CONTENT_FILE, "r") as f:
        return json.load(f)

def render_politics_header():
    """Custom HTML for the Mick & Scampy showdown"""
    return """
    <div class="politics-header">
        <div class="pol-candidate">
            <img src="assets/scamps_glider.png" alt="Scampy" class="pol-avatar">
            <div class="pol-name">The Teal Deal</div>
        </div>
        <div class="pol-vs">VS</div>
        <div class="pol-candidate">
            <img src="assets/regan_mallard.png" alt="Mick" class="pol-avatar">
            <div class="pol-name">The Independent</div>
        </div>
    </div>
    """

def render_article(data, layout_type):
    """Renders a single story based on its layout type"""
    if not data or "headline" not in data:
        return ""

    # --- IMAGE HANDLING (No change) ---
    img_html = ""
    if layout_type == "special_politics":
        img_html = render_politics_header()
    elif "image_path" in data and data["image_path"]:
        img_html = f'<div class="article-image"><img src="{data["image_path"]}" alt="News Image"></div>'
    
    # --- STYLING LOGIC (No change) ---
    css_class = "article-box"
    icon = ""
    
    if layout_type == "special_politics": css_class += " style-politics"
    elif layout_type == "review": css_class += " style-arts"; icon = "🧐 "
    elif layout_type == "youth": css_class += " style-youth"; icon = "⚡ "
    elif layout_type == "warning": css_class += " style-troppo"; icon = "🐊 "
    elif layout_type == "terminal": css_class += " style-tech"; icon = "💻 "
    elif layout_type == "mystic": css_class += " style-mystic"; icon = "🔮 "
    elif layout_type == "lead": css_class += " style-lead"

    # --- HTML ASSEMBLY ---
    html = f"""
    <article class="{css_class}">
        {img_html}
        <h3 class="headline">{icon}{data['headline']}</h3>
        <div class="body-text">
            {data['body'].replace(chr(10), '<br><br>')}
        </div>
    </article>
    """
    return html

def build_html():
    content = load_content()
    if not content:
        print("❌ No content found. Run generate_news.py first.")
        return

    # Ensure output directory exists before writing
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # --- HTML HEAD & CSS (Omitted for brevity; remains the same) ---
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Remy Digest</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Chomsky&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Permanent+Marker&display=swap');
            
            :root {
                --paper: #f4f1ea;
                --ink: #2a2a2a;
                --accent: #2c4f54; 
                --alert: #d9534f;
            }

            html { scroll-behavior: smooth; }

            body {
                background-color: #222;
                font-family: 'Libre Baskerville', serif;
                margin: 0;
                display: flex;
                justify-content: center;
            }

            .mobile-container {
                background-color: var(--paper);
                width: 100%;
                max-width: 450px;
                min-height: 100vh;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
                border-left: 1px solid #ddd;
                border-right: 1px solid #ddd;
            }

            /* --- MASTHEAD --- */
            header {
                text-align: center;
                padding: 20px 10px;
                border-bottom: 3px double var(--ink);
            }
            h1 {
                font-family: 'Chomsky', serif;
                font-size: 3.5rem;
                margin: 0;
                line-height: 1;
            }
            .tagline {
                font-style: italic;
                font-size: 0.9rem;
                color: #555;
                margin-top: 5px;
            }

            /* --- NAV TICKER FIX --- */
            .nav-ticker {
                background: var(--ink);
                color: var(--paper);
                white-space: nowrap;
                overflow-x: auto;
                padding: 10px;
                font-family: sans-serif;
                text-transform: uppercase;
                font-weight: bold;
                font-size: 0.8rem;
                position: sticky;
                top: 0;
                z-index: 100;
                border-bottom: 2px solid #000;
            }
            .nav-item {
                display: inline-block;
                margin-right: 20px;
                opacity: 0.9;
                text-decoration: none;
                color: var(--paper);
            }
            .nav-item:hover {
                text-decoration: underline;
                color: #fff;
            }

            /* --- SECTIONS --- */
            .desk-header {
                background: #e0ded5;
                padding: 10px 15px;
                border-top: 2px solid var(--ink);
                border-bottom: 1px solid var(--ink);
                font-family: sans-serif;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 0;
                scroll-margin-top: 40px; 
            }

            /* --- ARTICLE BOXES --- */
            .article-box {
                padding: 20px;
                border-bottom: 1px solid #ccc;
            }
            .article-image img {
                width: 100%;
                height: auto;
                border: 1px solid #333;
                margin-bottom: 15px;
                filter: sepia(0.2);
            }
            .headline {
                font-size: 1.4rem;
                margin-top: 0;
                margin-bottom: 10px;
                line-height: 1.2;
            }
            .body-text {
                font-size: 1rem;
                line-height: 1.5;
                color: #333;
                text-align: justify;
            }

            /* --- SPECIAL STYLES --- */
            .style-lead .headline { font-size: 1.8rem; }
            
            .style-politics { background-color: #fcfcfc; }
            .politics-header {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 1px dashed #aaa;
                padding-bottom: 10px;
            }
            .pol-candidate { text-align: center; width: 40%; }
            .pol-avatar { width: 80px; height: 80px; object-fit: contain; mix-blend-mode: multiply; }
            .pol-name { font-size: 0.7rem; font-weight: bold; text-transform: uppercase; margin-top: 5px; }
            .pol-vs { font-weight: bold; font-style: italic; color: #888; }

            .style-arts {
                font-family: 'Georgia', serif;
                font-style: italic;
                background: #f9f9f9;
                border-left: 4px solid #666;
            }

            .style-youth {
                font-family: 'Courier New', monospace;
                background: #eef;
                border: 2px dashed #66f;
            }
            .style-youth .headline {
                font-family: 'Permanent Marker', cursive;
                color: #33c;
            }

            .style-troppo {
                border: 3px solid var(--alert);
                background: #fff0f0;
            }

            .style-tech {
                background: #222;
                color: #0f0;
                font-family: 'Courier New', monospace;
            }
            .style-tech .body-text { color: #0f0; }
            .style-tech .headline { color: #0f0; text-transform: uppercase; }

            /* --- FOOTER --- */
            footer {
                text-align: center;
                padding: 40px 20px;
                background: var(--ink);
                color: var(--paper);
                font-size: 0.8rem;
            }
        </style>
    </head>
    <body>
        <div class="mobile-container">
            
            <header id="top">
                <img src="assets/remy_masthead.png" style="max-width: 150px; display: block; margin: 0 auto 10px auto;">
                <h1>The Remy Digest</h1>
                <div class="tagline">"Factual Receipts. Fictional Coping Mechanisms."</div>
                <div class="tagline">Vol. 1 | Cromer, NSW | Est. 2025</div>
            </header>

            <div class="nav-ticker">
                <a href="#front" class="nav-item">THE FRONT</a>
                <a href="#pulse" class="nav-item">THE PULSE</a>
                <a href="#voices" class="nav-item">THE VOICES</a>
                <a href="#back" class="nav-item">THE BACK PAGE</a>
                <span class="nav-item">WEATHER: 24°C & HUMID</span>
            </div>

            """

    # --- RENDER LOOP ---
    for section_name, items in SECTIONS.items():
        # Clean slug (e.g., "THE FRONT PAGE" -> "front")
        slug = section_name.lower().replace(" page", "").replace("the ", "")
        
        # Inject the ID for navigation
        html += f'<div id="{slug}" class="desk-header">{section_name}</div>'
        
        for item in items:
            key = item["key"]
            layout = item["type"]
            
            # Check if we have data for this key
            if key in content:
                html += render_article(content[key], layout)
            else:
                print(f"⚠️ Warning: Missing content for section '{key}'")

    # --- CLOSE TAGS ---
    html += """
            <footer>
                <p>&copy; 2025 The Remy Digest.</p>
                <p>Generated by Remy, Squeak & The Team.</p>
                <p>Beware of the Ibis.</p>
                <br>
                <a href="#top" style="color: #888; text-decoration: none;">↑ Back to Top</a>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # Check if the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Write the final HTML file to the correct output folder
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Website built successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_html()
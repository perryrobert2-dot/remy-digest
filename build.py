import json
import os

# --- Configuration ---
DATA_FILE = os.path.join('data', 'stories.json')
STAFF_FILE = os.path.join('data', 'staff.json')
OUTPUT_DIR = 'output'

# Static Assets
PITD_IMAGE = "https://storage.googleapis.com/remys-digest-public-assets/static/pitd-comic-strip.png"
HEADER_LOGO = "https://storage.googleapis.com/remys-digest-public-assets/static/Professor%20Dachshund%20Desk%20Scene.jpg"

SECTION_DISPLAY_NAMES = {
    "masthead": "The Daily Bark",
    "campaign": "The Teal Deal",
    "pitd": "The Echo Chamber",
    "news": "Local News",
    "backpage": "Troppo",
    "letters": "Inbox",
    "arts": "Culture",
    "sport": "Sport"
}

def load_json(path):
    try:
        with open(path, 'r') as f: return json.load(f)
    except FileNotFoundError: return {}

def get_display_name(key):
    return SECTION_DISPLAY_NAMES.get(key.lower(), key.upper())

def get_html_template(title, nav_links, content_html):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | The Remy Digest</title>
        <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,700;1,300&family=UnifrakturMaguntia&family=Anton&family=Patrick+Hand&display=swap" rel="stylesheet">
        
        <style>
            body {{ font-family: 'Merriweather', serif; background-color: #F5F1E6; color: #1a1a1a; margin: 0; padding: 0; }}
            
            /* HEADER STYLES */
            header {{ 
                padding: 20px; 
                border-bottom: 3px double #1a1a1a; 
                background-color: #F5F1E6; 
                display: flex; 
                align-items: center; 
                justify-content: center;
                gap: 20px;
            }}
            .header-logo {{ 
                height: 120px; 
                width: auto; 
                border: 2px solid #1a1a1a; 
                box-shadow: 4px 4px 0px #000;
            }}
            .header-text {{ text-align: left; }}
            h1 {{ font-family: 'UnifrakturMaguntia', cursive; font-size: 4rem; margin: 0; line-height: 1; }}
            .tagline {{ font-style: italic; margin-top: 5px; font-size: 1.1rem; }}
            
            /* NAV */
            nav {{ text-align: center; padding: 15px 0; border-bottom: 1px solid #1a1a1a; background-color: #Eae5d6; }}
            .nav-item {{ color: #1a1a1a; text-decoration: none; margin: 0 15px; font-weight: 900; text-transform: uppercase; font-size: 0.9rem; }}
            .nav-item:hover {{ color: #B93B3B; text-decoration: underline; }}
            
            .container {{ max-width: 800px; margin: 30px auto; padding: 0 20px; }}
            
            /* WRITER BLOCK (Small circle for standard stories) */
            .writer-block {{ display: flex; align-items: center; margin-bottom: 15px; border-bottom: 1px dotted #ccc; padding-bottom: 10px;}}
            .writer-img {{ width: 60px; height: 60px; border-radius: 50%; border: 2px solid #1a1a1a; margin-right: 15px; object-fit: cover; }}
            .writer-name {{ font-weight: 900; text-transform: uppercase; display: block; }}
            
            /* STORY CARD */
            .story-card {{ padding-bottom: 40px; margin-bottom: 40px; border-bottom: 1px solid #1a1a1a; }}
            .story-img {{ width: 100%; border: 1px solid #1a1a1a; margin: 15px 0; filter: sepia(15%); }}
            
            p {{ font-size: 1.1rem; line-height: 1.6; color: #222; margin-bottom: 15px; white-space: pre-line; }}

            /* SOLILOQUY / COMIC BOX STYLE */
            .soliloquy-container {{
                margin: 20px 0;
            }}
            .soliloquy-image-large {{
                width: 100%;
                display: block;
                border: 3px solid #000;
                margin-bottom: -3px; /* Connects to the box below */
                position: relative;
                z-index: 2;
            }}
            .soliloquy-box {{ 
                font-family: 'Patrick Hand', cursive; /* Comic Font */
                font-size: 1.4rem;
                background: #fff; 
                padding: 25px; 
                border: 3px solid #000; 
                box-shadow: 8px 8px 0px rgba(0,0,0,0.8);
                white-space: pre-wrap;
                line-height: 1.4;
                position: relative;
                z-index: 1;
            }}
            
            /* MEME */
            .meme-container {{ position: relative; display: inline-block; width: 100%; margin: 20px 0; }}
            .meme-img {{ width: 100%; display: block; }}
            .meme-text {{ 
                position: absolute; left: 0; width: 100%; text-align: center; 
                font-family: 'Anton', sans-serif; color: white; font-size: 2.5rem; 
                text-transform: uppercase; 
                text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
                line-height: 1.1; pointer-events: none; padding: 0 10px;
            }}
            .meme-top {{ top: 10px; }}
            .meme-bottom {{ bottom: 10px; }}
            
            /* COMIC STRIP */
            .comic-img {{ width: 100%; display: block; border: 2px solid black; }}
        </style>
    </head>
    <body>
        <header>
            <img src="{HEADER_LOGO}" class="header-logo" alt="Remy at Desk">
            <div class="header-text">
                <h1>The Remy Digest</h1>
                <div class="tagline">"Factual Receipts. Fictional Coping Mechanisms."</div>
            </div>
        </header>
        <nav>
            <a href="index.html" class="nav-item">Front Page</a>
            {nav_links}
        </nav>
        <div class="container">
            <h3 style="border-bottom: 2px solid black;">{title}</h3>
            {content_html}
        </div>
    </body>
    </html>
    """

def generate_story_html(story, staff_db):
    writer_key = story.get('writer_key', '').lower()
    writer = staff_db.get(writer_key, {})
    w_name = writer.get('name', 'Staff')
    w_img = writer.get('image', 'https://placehold.co/60x60/png?text=Writer')
    
    # FORMAT: SOLILOQUY (Special Comic Box Layout)
    if story.get('format') == 'soliloquy':
        # Use the writer's image as the main visual (Large)
        return f"""
        <div class="story-card">
            <span style="background:black;color:white;padding:2px 5px;text-transform:uppercase;font-size:0.7rem;">The Daily Bark</span>
            <h2>{story['headline']}</h2>
            
            <div class="soliloquy-container">
                <img src="{w_img}" class="soliloquy-image-large" alt="Remy on Stage">
                <div class="soliloquy-box">{story['body']}</div>
            </div>
        </div>
        """

    # STANDARD WRITER BLOCK
    writer_html = f"""
    <div class="writer-block">
        <img src="{w_img}" class="writer-img">
        <div><span class="writer-name">{w_name}</span><span>{writer.get('title','')}</span></div>
    </div>
    """
    
    img_tag = ""
    if story.get('image'):
        if story.get('format') == 'meme':
            img_tag = f"""
            <div class="meme-container">
                <img src="{story['image']}" class="meme-img">
                <div class="meme-text meme-top">{story['headline']}</div>
                <div class="meme-text meme-bottom">{story['subtext']}</div>
            </div>
            """
        else:
            img_tag = f'<img src="{story["image"]}" class="story-img">'

    body_html = f"<p>{story['body']}</p>"
    if story.get('format') == 'meme':
        body_html = f"<p style='text-align:center; font-weight:bold;'>{story['body']}</p>"

    headline_html = f"<h2>{story['headline']}</h2>"
    if story.get('format') == 'meme': headline_html = "" 

    display_section = get_display_name(story['section'])

    return f"""
    <div class="story-card">
        <span style="background:black;color:white;padding:2px 5px;text-transform:uppercase;font-size:0.7rem;">{display_section}</span>
        {headline_html}
        {writer_html}
        {img_tag}
        {body_html}
    </div>
    """

def main():
    stories = load_json(DATA_FILE)
    staff = load_json(STAFF_FILE)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sections = sorted(list(set(s['section'] for s in stories)))
    
    if "pitd" not in sections: sections.append("pitd")
    
    nav_links = ""
    for sec in sorted(sections):
        display_name = get_display_name(sec)
        # CRITICAL FIX: .lower() forces the filename to be lowercase
        nav_links += f'<a href="{sec.lower()}.html" class="nav-item">{display_name}</a>\n'

    idx_content = "".join([generate_story_html(s, staff) for s in stories if s.get('featured')])
    if not idx_content: idx_content = "<p>No featured stories today.</p>"
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(get_html_template("Front Page", nav_links, idx_content))

    for sec in sections:
        if sec == "pitd":
            sec_content = f"""
            <div class="story-card">
                <h2>The Echo Chamber</h2>
                <p><i>A visual record of the endless debate.</i></p>
                <img src="{PITD_IMAGE}" class="comic-img" alt="Philosopher in the Dark Comic Strip">
            </div>
            """
        else:
            sec_stories = [s for s in stories if s['section'] == sec]
            sec_content = "".join([generate_story_html(s, staff) for s in sec_stories])
        
        display_name = get_display_name(sec)
        # CRITICAL FIX: .lower() forces the filename to be lowercase
        with open(os.path.join(OUTPUT_DIR, f'{sec.lower()}.html'), 'w') as f:
            f.write(get_html_template(display_name, nav_links, sec_content))

    print("The Remy Digest is published.")

if __name__ == "__main__":
    main()
import json
import os
import config

def load_stories():
    """
    Loads the raw list of stories from the data/stories.json file.
    Returns an empty list if the file is missing or broken.
    """
    filepath = os.path.join(config.BASE_DIR, 'data', 'stories.json')
    
    if not os.path.exists(filepath):
        # Graceful fallback if the file doesn't exist yet
        return []
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: Could not decode data/stories.json. Please check your JSON syntax.")
        return []
    except Exception as e:
        print(f"Error loading stories: {e}")
        return []

def get_stories_by_section(section_name):
    """
    Returns a list of stories for a specific section (e.g., 'Sport', 'Arts').
    
    Special Logic:
    - If the section is 'News' (Front Page), it returns stories marked as 'News'
      OR stories marked as 'featured: true' from other sections.
    """
    all_stories = load_stories()
    
    # Filter logic
    filtered_stories = []
    
    for story in all_stories:
        story_section = story.get('section')
        is_featured = story.get('featured', False)
        
        if section_name == "News":
            # Front page gets "News" items AND any "Featured" items
            if story_section == "News" or is_featured:
                filtered_stories.append(story)
        else:
            # Standard sections just get their own stories
            if story_section == section_name:
                filtered_stories.append(story)
                
    return filtered_stories
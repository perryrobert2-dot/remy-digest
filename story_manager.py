import json
import os

STORY_FILE = "data/stories.json"

class StoryManager:
    def __init__(self):
        self.data = self._load_data()
        self.current_arc_id = self.data["meta"]["current_arc"]
        self.day = str(self.data["meta"]["day"])
        self.active_arc = self.data["arcs"].get(self.current_arc_id, {})

    def _load_data(self):
        # Default seed data if file is missing
        if not os.path.exists(STORY_FILE):
            print("⚠️ Story file not found. Using default seed.")
            return {
                "meta": {"current_arc": "hard_rubbish_war", "day": 1, "status": "active"},
                "arcs": {}
            }
        with open(STORY_FILE, "r") as f:
            return json.load(f)

    def get_direction(self, persona_name):
        """
        Returns the specific plot direction for a character on the current day.
        """
        day_script = self.active_arc.get("days", {}).get(self.day, {})
        
        # Check if this character has a script today
        instruction = day_script.get(persona_name)
        
        if instruction:
            print(f"🎬 ACTION: Directing {persona_name} for Day {self.day} of arc '{self.current_arc_id}'")
            return f"\n\n*** SPECIAL PLOT INSTRUCTION (STORY ARC DAY {self.day}) ***\n{instruction}\n**************************************************"
        return ""

    def advance_plot(self):
        """
        Increments the day counter.
        """
        current = int(self.data["meta"]["day"])
        # Simple check to see if next day exists in keys
        next_day = str(current + 1)
        
        if next_day in self.active_arc.get("days", {}):
            self.data["meta"]["day"] = current + 1
            print(f"⏩ Plot advanced to Day {self.data['meta']['day']}")
        else:
            print("🏁 Story Arc Complete (or holding at final day).")
            
        # Save state
        with open(STORY_FILE, "w") as f:
            json.dump(self.data, f, indent=4)
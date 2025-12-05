import os

# Directory settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Site Settings
SITE_TITLE = "The Remy Digest"

# TVFY API Configuration
# REPLACE 'YOUR_KEY_HERE' with your actual API key
API_KEY = "Gv2bM9C84dQPFvNnkVBVcidf" 
API_BASE_URL = "https://theyvoteforyou.org.au/api/v1"

# Mapping Electorates to MPs (as of late 2024/2025)
# This helps us find the right voting records.
ELECTORATE_MAP = {
    "Mackellar": {"mp_id": "Sophie_Scamps", "name": "Sophie Scamps"},
    "Warringah": {"mp_id": "Zali_Steggall", "name": "Zali Steggall"},
    "Wentworth": {"mp_id": "Allegra_Spender", "name": "Allegra Spender"},
    "North Sydney": {"mp_id": "Kylea_Tink", "name": "Kylea Tink"}
}

# List of electorates for navigation
ELECTORATES = list(ELECTORATE_MAP.keys())
"""Reads secrets and API keys from environment variables (or a local .env file)."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "hfc-app-b33ed-firebase-adminsdk-oqged-96055b305b.json")

EDAMAM_RECIPES_APP_ID = os.getenv("EDAMAM_RECIPES_APP_ID", "")
EDAMAM_RECIPES_APP_KEY = os.getenv("EDAMAM_RECIPES_APP_KEY", "")
EDAMAM_NUTRITION_APP_ID = os.getenv("EDAMAM_NUTRITION_APP_ID", "")
EDAMAM_NUTRITION_APP_KEY = os.getenv("EDAMAM_NUTRITION_APP_KEY", "")

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")

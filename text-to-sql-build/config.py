import os
from dotenv import load_dotenv

load_dotenv()

GHAYMAH_API_KEY = os.getenv("GHAYMAH_API_KEY")

if not GHAYMAH_API_KEY:
    raise ValueError("Missing API Key")
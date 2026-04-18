from openai import OpenAI
from config import GHAYMAH_API_KEY

client = OpenAI(
    api_key=GHAYMAH_API_KEY,
    base_url="https://genai.ghaymah.systems"
)
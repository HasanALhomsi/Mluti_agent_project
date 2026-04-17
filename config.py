import os
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import create_engine, text

load_dotenv()

# ── LLM Client ──────────────────────────────
client = OpenAI(
    api_key=os.getenv("GHAYMAH_API_KEY"),
    base_url=os.getenv("GHAYMAH_BASE_URL")
)
MODEL = os.getenv("MODEL_NAME")

# ── PostgreSQL Connection ────────────────────
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME")
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# إنشاء الـ Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # يتأكد أن الاتصال شغال
    pool_size=5,
    max_overflow=10
)

def test_connection():
    """اختبار الاتصال بقاعدة البيانات"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ تم الاتصال بـ PostgreSQL بنجاح!")
        return True
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False
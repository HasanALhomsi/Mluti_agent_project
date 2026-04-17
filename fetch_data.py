import pandas as pd
from sqlalchemy import text, inspect
from config import engine

def fetch_all_tables():
    """عرض كل الجداول الموجودة في قاعدة البيانات"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("⚠️  لا توجد جداول في قاعدة البيانات")
            return
        
        print(f"📋 الجداول الموجودة: {tables}\n")
        return tables
        
    except Exception as e:
        print(f"❌ خطأ: {e}")

def fetch_table_data(table_name: str, limit: int = 10):
    """جلب وطباعة بيانات جدول معين"""
    try:
        with engine.connect() as conn:
            # جلب البيانات
            result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
            rows = result.fetchall()
            columns = result.keys()
            
            # تحويل لـ DataFrame
            df = pd.DataFrame(rows, columns=columns)
            
            print(f"✅ جدول: {table_name}")
            print(f"📊 عدد الصفوف المعروضة: {len(df)}")
            print("=" * 60)
            print(df.to_string(index=False))
            print("=" * 60)
            
            return df
            
    except Exception as e:
        print(f"❌ خطأ في جلب البيانات: {e}")

def fetch_table_stats(table_name: str):
    """إحصاءات سريعة عن الجدول"""
    try:
        with engine.connect() as conn:
            # عدد الصفوف الكلي
            count = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar()
            
            print(f"\n📈 إحصاءات جدول {table_name}:")
            print(f"   إجمالي الصفوف: {count}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")


# ── تشغيل كل شيء ──────────────────────────
if __name__ == "__main__":
    print("🚀 جلب البيانات من Supabase...\n")
    
    # 1. عرض الجداول
    tables = fetch_all_tables()
    
    if tables:
        for table in tables:
            # 2. إحصاءات كل جدول
            fetch_table_stats(table)
            
            # 3. طباعة أول 10 صفوف
            fetch_table_data(table, limit=10)
            print("\n")
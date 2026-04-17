import pandas as pd
from sqlalchemy import text
from config import engine

# قراءة الـ CSV
df = pd.read_csv("dataset/Online Sales Data.csv")

# تنظيف أسماء الأعمدة
df.columns = df.columns.str.lower().str.replace(' ', '_')

print(f"📊 عدد الصفوف: {len(df)}")
print(f"📋 الأعمدة: {list(df.columns)}")
print(df.head())

# رفع البيانات لـ Supabase
df.to_sql(
    name='products',
    con=engine,
    if_exists='replace',  # يستبدل الجدول لو موجود
    index=False
)

print("✅ تم رفع البيانات لـ Supabase بنجاح!")
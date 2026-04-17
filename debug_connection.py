import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")
print(f"URL: {url[:50]}...\n")  # نطبع أول 50 حرف فقط للأمان

# اختبار 1: sslmode=require
print("🔄 اختبار 1: sslmode=require ...")
try:
    conn = psycopg2.connect(url + "?sslmode=require", connect_timeout=15)
    print("✅ نجح!")
    conn.close()
except Exception as e:
    print(f"❌ {e}\n")

# اختبار 2: sslmode=disable  
print("🔄 اختبار 2: sslmode=disable ...")
try:
    conn = psycopg2.connect(url + "?sslmode=disable", connect_timeout=15)
    print("✅ نجح!")
    conn.close()
except Exception as e:
    print(f"❌ {e}\n")

# اختبار 3: بدون أي SSL
print("🔄 اختبار 3: بدون SSL ...")
try:
    conn = psycopg2.connect(url, connect_timeout=15)
    print("✅ نجح!")
    conn.close()
except Exception as e:
    print(f"❌ {e}\n")

# اختبار 4: sslmode=allow
print("🔄 اختبار 4: sslmode=allow ...")
try:
    conn = psycopg2.connect(url + "?sslmode=allow", connect_timeout=15)
    print("✅ نجح!")
    conn.close()
except Exception as e:
    print(f"❌ {e}\n")
# test_db.py
from config import test_connection, engine
from sqlalchemy import text, inspect

if test_connection():
    # عرض الجداول الموجودة
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n📋 الجداول الموجودة في قاعدة البيانات:")
    for table in tables:
        print(f"   - {table}")
import json
import pandas as pd
from sqlalchemy import text
from config import engine   # ← استيراد الـ engine من config

def execute_query(sql_query: str) -> dict:
    try:
        print(f"   🔍 تنفيذ: {sql_query}")

        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()

        df = pd.DataFrame(rows, columns=columns)

        return {
            "success": True,
            "query": sql_query,
            "results": df.to_dict(orient="records"),
            "row_count": len(df)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": sql_query
        }
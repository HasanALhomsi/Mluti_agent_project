import json
import pandas as pd
from sqlalchemy import text
from config import engine   # ← استيراد الـ engine من config

def execute_query(sql_info: dict) -> dict:
    """
    ينفذ الـ SQL Query على PostgreSQL في Ghaymah
    """
    try:
        # استخراج الـ Query من JSON
        response_text = sql_info["response"]

        # تنظيف الـ JSON لو فيه backticks
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        response_data = json.loads(response_text)
        sql_query = response_data.get("sql_query", "")

        print(f"   🔍 تنفيذ: {sql_query}")

        # تنفيذ الـ Query على PostgreSQL
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()

        # تحويل النتائج إلى DataFrame
        df = pd.DataFrame(rows, columns=columns)

        return {
            "success": True,
            "query": sql_query,
            "results": df.to_dict(orient="records"),
            "row_count": len(df)
        }

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"خطأ في تحليل JSON: {str(e)}",
            "query": ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": sql_query if "sql_query" in locals() else ""
        }
import json
from sqlalchemy import text, inspect
from config import client, MODEL, engine

def get_schema_from_db() -> str:
    """
    يجلب مخطط الجداول تلقائياً من PostgreSQL
    """
    try:
        inspector = inspect(engine)
        schema_str = ""

        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            schema_str += f"\nTable: {table_name}\n"
            schema_str += "Columns:\n"
            for col in columns:
                schema_str += f"  - {col['name']} ({col['type']})\n"

        return schema_str

    except Exception as e:
        return f"خطأ في جلب الـ Schema: {str(e)}"


def convert_to_sql(user_question: str, context: str = "") -> dict:
    """
    يحول سؤال المستخدم إلى SQL Query
    """
    # جلب الـ Schema من قاعدة البيانات تلقائياً
    db_schema = get_schema_from_db()

    prompt = f"""
    أنت خبير SQL متخصص في PostgreSQL.
    
    مخطط قاعدة البيانات:
    {db_schema}
    
    السياق الإضافي: {context}
    
    سؤال المستخدم: {user_question}
    
    اكتب PostgreSQL Query صحيحة.
    أجب بـ JSON فقط بهذا الشكل:
    {{
        "sql_query": "SELECT ...",
        "explanation": "شرح الـ Query"
    }}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return {
        "question": user_question,
        "response": response.choices[0].message.content
    }
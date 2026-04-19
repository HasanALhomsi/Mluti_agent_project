import json
import psycopg2
from psycopg2 import OperationalError, ProgrammingError
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

tables_file = "./text_to_sql_build/data/tables.json"
# PostgreSQL connection parameters from config.py
db_connection_params = {
    "host": DB_HOST,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "port": DB_PORT
}

def map_type(col_type):
    if col_type.lower() in ["text", "varchar", "char"]:
        return "TEXT"
    elif col_type.lower() in ["number", "integer", "int", "real", "float"]:
        return "INTEGER"
    elif col_type.lower() in ["boolean", "bool"]:
        return "BOOLEAN"
    else:
        return "TEXT"

def get_schema(tables_file=tables_file):
    with open(tables_file, "r") as f:
        tables_data = json.load(f)

    return tables_data

def build_schema_from_llm(schema: str) -> str:
    tables = schema.get("tables", [])
    columns = schema.get("columns", {})

    output_lines = []

    for table in tables:
        output_lines.append(f"table {table}(")

        for col in columns.get(table, []):
            col_name = col.get("column", "unknown")
            col_type = map_type(col.get("type", "text"))
            is_primary = col.get("isPrimary", False)

            line = f"{col_name} {col_type}"
            if is_primary:
                line += " primary"

            output_lines.append(line)

        output_lines.append(")")

    return "\n".join(output_lines)

def execute_query(sql):
    conn = psycopg2.connect(
        host=db_connection_params["host"],
        database=db_connection_params["database"],
        user=db_connection_params["user"],
        password=db_connection_params["password"],
        port=db_connection_params["port"]
    )
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()

        return {
            "success": True,
            "result": set(result),
            "error": None,
            "type": None
        }

    except OperationalError as e:
        conn.close()
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "type": "operational"
        }

    except ProgrammingError as e:
        conn.close()
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "type": "programming"
        }

    except Exception as e:
        conn.close()
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "type": "unknown"
        }
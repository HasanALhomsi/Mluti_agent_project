import re
import json

def clean_selection_tables(text: str):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    try:
        data = json.loads(text)

        if "tables" in data and "columns" in data:
            return data
        else:
            raise ValueError("Invalid schema format")

    except (json.JSONDecodeError, ValueError):
        return {
            "tables": [],
            "columns": {}
        }

def clean_sql_output(text: str) -> str:
    print("\n🔍 Raw SQL Output:\n", text)
    if not text:
        return ""

    text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    match = re.search(r"select .*", text, re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(0)
    else:
        return ""

    text = text.split(";")[0]

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    if not text.lower().startswith("select"):
        return ""

    return text
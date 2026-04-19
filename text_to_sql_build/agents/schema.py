from text_to_sql_build.llm.models import DeepSeek
from text_to_sql_build.services.sql_generator import llm_selection_schema
from text_to_sql_build.services.tables import build_schema_from_llm, get_schema

def select_schema(question, model=DeepSeek):
    db_schema = get_schema()
    selected = llm_selection_schema(question, db_schema, model)
    return build_schema_from_llm(selected)
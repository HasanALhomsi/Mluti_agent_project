from services.sql_generator import llm_generate_sql, llm_plan_sql, llm_review_sql
from llm.models import DeepSeek

def generate_sql_from_agents(question, schema, model=DeepSeek):
    plan = llm_plan_sql(question, schema, model)
    sql = llm_generate_sql(question, schema, plan, model)

    print("\n🧠 PLAN:\n", plan)

    for _ in range(1):
        new_sql = llm_review_sql(question, schema, sql, model)
        if not new_sql or new_sql == sql:
            break
        sql = new_sql

    return sql
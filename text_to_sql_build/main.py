import asyncio

from text_to_sql_build.agents.schema import select_schema
from text_to_sql_build.agents.sql import generate_sql_from_agents
from text_to_sql_build.services.sql_generator import llm_debug_sql
from text_to_sql_build.services.tables import execute_query

async def run_text_to_sql_pipeline(question, debug=False, reviewer=False):
    print("\n" + "="*80)
    print("🧠 QUESTION:", question)
    print("="*80)

    try:
        schema = "products, sales, customers"  # Fallback schema
        schema = await asyncio.to_thread(select_schema, question)

        if not schema.strip():
            raise ValueError("Empty schema from LLM")

    except Exception as e:
        print("\n⚠️ Schema selection failed, using full schema")
        print("Error:", e)

    print("\n📦 SCHEMA:\n", schema)

    try:
        sql = await asyncio.to_thread(generate_sql_from_agents, question, schema)

        if not sql:
            raise ValueError("Empty SQL generated")

    except Exception as e:
        print("\n⚠️ SQL generation failed")
        print("Error:", e)
        sql = ""

    print("\n🧾 GENERATED SQL:\n", sql)

    if(debug):
        max_debug_rounds = 2
        result = None

        for i in range(max_debug_rounds + 1):
            print(f"\n⚙️ Execution attempt {i+1}")

            exec_result = await asyncio.to_thread(execute_query, sql)
            print("Execution result:", exec_result)
            if exec_result["success"]:
                print("✅ Execution success")
                result = exec_result
                break

            print("❌ Execution failed")
            print("Error:", exec_result["error"])

            if i == max_debug_rounds:
                result = exec_result
                break

            print("🛠️ Debugging SQL...")

            new_sql = await asyncio.to_thread(llm_debug_sql,question,schema,sql,exec_result["error"])

            if not new_sql or new_sql == sql:
                print("⚠️ Debugger did not improve SQL")
                result = exec_result
                break

            sql = new_sql

        print("🔁 New SQL:\n", sql)

    return sql

async def text_to_sql_agent(question, debug=False, reviewer=False):
    result = await run_text_to_sql_pipeline(question, debug, reviewer)
    print("\n✅ DONE")

    return result
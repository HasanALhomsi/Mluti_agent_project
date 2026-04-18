def build_sql_prompt(question, schema, plan=""):
    return f"""
        You are a SQL expert.

        Question:
        {question}

        Schema:
        {schema}

        Plan:
        {plan}

        Generate the SQL query based on the plan.

        Rules:
        - Follow the plan strictly
        - Use correct tables and columns
        - Output ONLY SQL
        - Single line only

        SQL:
        """

def build_schema_linking_prompt(question, schema):
    return f"""
        You are a database expert.
    
        Your task is to select ONLY the necessary tables and columns needed to answer the question.

        Database schema:
        {schema}

        Question:
        {question}

        Return format (STRICT JSON):
        {
        "tables": ["table1", "table2"],
        "columns": {
            "table1": [
            { "type": "int", "column": "col1 name", "isPrimary": true },
            { "type": "varchar", "column": "col2 name", "isPrimary": false }
            ],
            "table2": [
            { "type": "int", "column": "col1 name", "isPrimary": true }
            ]
        }}

        Rules:
        - Only include necessary tables
        - Only include necessary columns
        - Do NOT include explanations
        - Output ONLY valid JSON
        """

def review_sql_prompt(question, schema, sql):
    return f"""
        You are an expert SQL reviewer.

        Your task is to verify whether the SQL query correctly answers the question.

        Question:
        {question}

        Schema:
        {schema}

        SQL:
        {sql}

        Instructions:
        - If the SQL is correct, return it unchanged
        - If the SQL is incorrect, fix it
        - Ensure correct columns and tables
        - Ensure proper JOINs if needed
        - Do NOT explain anything
        - Output ONLY the SQL query
        - Output must be in a single line

        SQL:
        """

def debug_sql_prompt(question, schema, sql, error):
    return f"""
        You are a SQL debugging expert.

        The following SQL query failed during execution.

        Question:
        {question}

        Schema:
        {schema}

        SQL:
        {sql}

        Error:
        {error}

        Your task:
        - Fix the SQL query based on the error
        - Ensure it answers the question correctly
        - Do NOT explain anything
        - Output ONLY the corrected SQL
        - Output must be in a single line

        SQL:
        """

def plan_sql_prompt(question, schema):
    return f"""
        You are a SQL query planner.

        Your task is to analyze the question and create a structured plan for the SQL query.

        Question:
        {question}

        Schema:
        {schema}

        Create a plan with the following format:

        Tables: ...
        Columns: ...
        Conditions: ...
        Aggregation: ...
        Grouping: ...
        Ordering: ...

        Rules:
        - Be concise
        - Only include necessary elements
        - Do NOT write SQL
        - Do NOT explain

        Plan:
        """
import asyncio

from agents.document_type_agent import detect_document_type
from agents.data_extraction_agent import extract_data
from agents.database_query_agent import execute_query
from agents.product_analysis_agent import analyze_products
from agents.explanation_agent import generate_explanation
from text_to_sql_build.main import text_to_sql_agent

def run_pipeline(file_path: str, user_question: str) -> str:
    """
    تشغيل كامل Pipeline للـ Multi-Agent System
    """
    print("🚀 بدء تشغيل النظام...\n")
    
    # Agent 1: تحديد نوع الملف
    print("📄 Agent 1: تحديد نوع الملف...")
    doc_info = detect_document_type(file_path)
    print(f"   النوع: {doc_info['doc_type']}\n")
    
    # Agent 2: استخراج البيانات
    print("🔍 Agent 2: استخراج البيانات...")
    extracted = extract_data(doc_info)
    print(f"   تم استخراج البيانات بنجاح\n")

    entry_pormpt = f"insert this products into database fields: {extracted['fields']} values: {extracted['values']}"
    print("entry_prompt is:", entry_pormpt)

    # Agent 3: ادخال المبيعات لقاعدة البيانات
    print("💬 Agent 3: ادخال المبيعات لقاعدة البيانات")
    enty_sql_info = asyncio.run(text_to_sql_agent(entry_pormpt))
    print(f"   تم توليد الـ Query\n")
    print(f"   SQL Query:\n{enty_sql_info}\n")

    # Agent 4: تنفيذ الـ Query
    print("🗄️  Agent 4: تنفيذ الـ Query على قاعدة البيانات...")
    query_results = execute_query(enty_sql_info)
    if query_results["success"]:
        print(f"   عدد النتائج: {query_results['row_count']}\n")
    else:
        print(f"   خطأ: {query_results['error']}\n")

    # Agent 5: تحويل السؤال إلى SQL
    print("💬 Agent 5: تحويل السؤال إلى SQL...")
    sql_info = asyncio.run(text_to_sql_agent(user_question, True, True))
    print(f"   تم توليد الـ Query\n")
    print(f"   SQL Query:\n{sql_info}\n")
    
    # Agent 6: تنفيذ الـ Query
    print("🗄️  Agent 6: تنفيذ الـ Query على قاعدة البيانات...")
    query_results = execute_query(sql_info)
    if query_results["success"]:
        print(f"   عدد النتائج: {query_results['row_count']}\n")
    else:
        print(f"   خطأ: {query_results['error']}\n")
    
    # Agent 7: تحليل المنتجات
    print("📊 Agent 7: تحليل البيانات...")
    analysis = analyze_products(query_results, user_question)
    print(f"   تم التحليل بنجاح\n")
    
    # Agent 8: توليد الشرح النهائي
    print("✍️  Agent 8: كتابة الإجابة النهائية...")
    final_answer = generate_explanation(user_question, analysis)
    
    print("=" * 50)
    print("✅ الإجابة النهائية:")
    print("=" * 50)
    print(final_answer)
    
    return final_answer


# تشغيل المثال
if __name__ == "__main__":
    answer = run_pipeline(
        file_path="data/productss.pdf",
        user_question="Give me all products that have a price higher than 800"
    )
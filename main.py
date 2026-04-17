from agents.document_type_agent import detect_document_type
from agents.data_extraction_agent import extract_data
from agents.text_to_sql_agent import convert_to_sql
from agents.database_query_agent import execute_query
from agents.product_analysis_agent import analyze_products
from agents.explanation_agent import generate_explanation

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
    
    # Agent 3: تحويل السؤال إلى SQL
    print("💬 Agent 3: تحويل السؤال إلى SQL...")
    sql_info = convert_to_sql(user_question, extracted["structured_data"])
    print(f"   تم توليد الـ Query\n")
    
    # Agent 4: تنفيذ الـ Query
    print("🗄️  Agent 4: تنفيذ الـ Query على قاعدة البيانات...")
    query_results = execute_query(sql_info)
    if query_results["success"]:
        print(f"   عدد النتائج: {query_results['row_count']}\n")
    else:
        print(f"   خطأ: {query_results['error']}\n")
    
    # Agent 5: تحليل المنتجات
    print("📊 Agent 5: تحليل البيانات...")
    analysis = analyze_products(query_results, user_question)
    print(f"   تم التحليل بنجاح\n")
    
    # Agent 6: توليد الشرح النهائي
    print("✍️  Agent 6: كتابة الإجابة النهائية...")
    final_answer = generate_explanation(user_question, analysis)
    
    print("=" * 50)
    print("✅ الإجابة النهائية:")
    print("=" * 50)
    print(final_answer)
    
    return final_answer


# تشغيل المثال
if __name__ == "__main__":
    answer = run_pipeline(
        file_path="data/products2.pdf",
        user_question="ما هي المنتجات الأكثر مبيعاً هذا الشهر؟"
    )
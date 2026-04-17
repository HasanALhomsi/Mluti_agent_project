import json
from config import client, MODEL

def analyze_products(query_results: dict, user_question: str) -> dict:
    """
    يحلل نتائج قاعدة البيانات
    """
    results_str = json.dumps(
        query_results.get("results", []), 
        ensure_ascii=False, 
        indent=2
    )
    
    prompt = f"""
    أنت محلل بيانات خبير.
    
    سؤال المستخدم: {user_question}
    
    نتائج قاعدة البيانات:
    {results_str}
    
    قم بتحليل شامل يتضمن:
    1. الإحصاءات الأساسية (متوسط، أعلى قيمة، أدنى قيمة)
    2. الأنماط والاتجاهات
    3. أهم الملاحظات
    4. توصيات بناءً على البيانات
    
    أجب بـ JSON منظم.
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return {
        "analysis": response.choices[0].message.content,
        "data_count": query_results.get("row_count", 0)
    }

import json
from config import client, MODEL

def generate_explanation(
    user_question: str,
    analysis_result: dict,
    language: str = "arabic"
) -> str:
    """
    يولد شرحاً واضحاً للمستخدم
    """
    analysis_str = json.dumps(
        analysis_result, 
        ensure_ascii=False
    )
    
    prompt = f"""
    أنت مساعد ذكي متخصص في شرح البيانات.
    
    سؤال المستخدم: {user_question}
    
    نتيجة التحليل: {analysis_str}
    
    اكتب إجابة واضحة ومفيدة باللغة {language}:
    - ابدأ بالإجابة المباشرة
    - اذكر الأرقام المهمة
    - اشرح الأنماط بلغة بسيطة
    - اختم بتوصية عملية
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    return response.choices[0].message.content

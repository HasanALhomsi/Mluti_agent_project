from config import client, MODEL

def detect_document_type(file_path: str) -> dict:
    """
    يحدد نوع الملف المرفوع
    """
    extension = file_path.split('.')[-1].lower()
    
    type_map = {
        'pdf': 'PDF Document',
        'png': 'Image',
        'jpg': 'Image',
        'jpeg': 'Image',
        'xlsx': 'Excel File',
        'csv': 'CSV File',
        'txt': 'Text File'
    }
    
    doc_type = type_map.get(extension, 'Unknown')
    
    prompt = f"""
    تم رفع ملف من نوع: {doc_type}
    مسار الملف: {file_path}
    
    حدد:
    1. نوع الملف
    2. طريقة المعالجة المناسبة
    3. هل يحتوي على جداول أو نصوص أو صور؟
    
    أجب بـ JSON فقط.
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return {
        "file_path": file_path,
        "doc_type": doc_type,
        "analysis": response.choices[0].message.content
    }
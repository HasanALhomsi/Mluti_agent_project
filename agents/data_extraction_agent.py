import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
from config import client, MODEL

def extract_data(file_info: dict) -> dict:
    """
    يستخرج البيانات من الملف حسب نوعه
    """
    file_path = file_info["file_path"]
    doc_type = file_info["doc_type"]
    extracted_text = ""
    
    # استخراج من PDF
    if doc_type == "PDF Document":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""
    
    # استخراج من صورة (OCR)
    elif doc_type == "Image":
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(
            image, 
            lang='ara+eng'  # دعم العربية والإنجليزية
        )
    
    # استخراج من Excel
    elif doc_type == "Excel File":
        df = pd.read_excel(file_path)
        extracted_text = df.to_string()
    
    # استخراج من CSV
    elif doc_type == "CSV File":
        df = pd.read_csv(file_path)
        extracted_text = df.to_string()
    
    # تنظيف وتنظيم البيانات بالـ LLM
    prompt = f"""
    البيانات المستخرجة من الملف:
    {extracted_text[:3000]}
    
    قم بـ:
    1. تنظيف البيانات
    2. استخراج الأعمدة والقيم المهمة
    3. تحديد ما إذا كانت تحتوي على بيانات منتجات
    
    أجب بـ JSON منظم.
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return {
        "raw_text": extracted_text,
        "structured_data": response.choices[0].message.content
    }
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
from config import client, MODEL
import re

def clean_extraction_info_response(text: str) -> str:
    # Remove <think>...</think> (including multiline)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # Remove ```json or ``` blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

import json

def extract_main_items(clean_text: str):
    try:
        data = json.loads(clean_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {e}")

    items = data.get("items", [])
    date = data.get("date")

    if not items:
        return (), ""

    # 🔹 Collect dynamic fields from all items
    dynamic_fields = set()
    for item in items:
        dynamic_fields.update(item.keys())

    # 🔹 Ensure consistent order (important for DB)
    dynamic_fields = sorted(dynamic_fields)

    # 🔹 Add fixed field
    fields = tuple(dynamic_fields + ["date"])

    values_list = []

    for item in items:
        row_values = []

        for field in dynamic_fields:
            value = item.get(field)

            # Proper formatting
            if isinstance(value, str):
                row_values.append(repr(value))
            else:
                row_values.append(str(value))

        # Add date
        row_values.append(repr(date))

        value_tuple = f"({', '.join(row_values)})"
        values_list.append(value_tuple)

    values = ", ".join(values_list)

    return fields, values

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
    
    response = clean_extraction_info_response(response.choices[0].message.content)
    fields, values = extract_main_items(response)
    print("The response is:",response)
    return {
        "raw_text": extracted_text,
        "structured_data": response,
        "fields": fields,
        "values": values
    }
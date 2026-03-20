import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

MODEL = st.secrets["GROQ_MODEL"]

EXTRACTION_PROMPT = """
You are a medical data extraction system.
Your job is to extract ONLY real information from the given medical report text.

STRICT RULES:
- Do NOT generate fake/sample data
- Do NOT assume values
- If something is missing → keep it empty ""
- Ignore OCR noise or garbage text
- Extract only visible and meaningful medical data

Return ONLY valid JSON in this format:
{
  "patient": {
    "age": "",
    "gender": ""
  },
  "tests": [
    {
      "name": "",
      "value": "",
      "unit": "",
      "normalRange": "",
      "status": ""
    }
  ]
}
"""

def safe_json_load(text):
    try:
        return json.loads(text)
    except:
        return {"error": "Invalid JSON from model", "raw_output": text}

def extract_medical_data(ocr_text):
    if not ocr_text or len(ocr_text.strip()) < 20:
        return {"error": "No valid text extracted from report"}

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": ocr_text}
            ],
            temperature=0
        )

        raw_output = response.choices[0].message.content.strip()

        if raw_output.startswith("```"):
            raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        return safe_json_load(raw_output)
    except Exception as e:
        return {"error": f"Extraction failed: {str(e)}"}
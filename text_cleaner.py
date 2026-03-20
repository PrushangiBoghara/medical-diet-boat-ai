import re

def clean_text(text):
    """
    Clean OCR extracted text:
    - Remove multiple newlines
    - Keep letters, numbers, punctuation useful for medical reports
    - Strip leading/trailing spaces
    """
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[^a-zA-Z0-9.\n:%/-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)  # normalize spaces
    return text.strip()
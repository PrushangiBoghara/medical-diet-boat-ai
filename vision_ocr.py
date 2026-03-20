import streamlit as st
import json
from PIL import Image
import io
import os

# For Google Vision
from google.cloud import vision
from google.oauth2 import service_account

# For Tesseract OCR
import pytesseract
from pdf2image import convert_from_bytes

# -----------------------------
# ✅ Google Vision Client
# -----------------------------
def get_vision_client():
    try:
        creds_json = st.secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        if not creds_json:
            return None  # No Google credentials, skip

        creds_dict = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        client = vision.ImageAnnotatorClient(credentials=credentials)
        return client

    except Exception as e:
        st.warning(f"Google Vision setup failed: {e}")
        return None

# -----------------------------
# ✅ Extract text from images using Tesseract
# -----------------------------
def tesseract_ocr_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text

# -----------------------------
# ✅ Extract text from PDFs using Tesseract
# -----------------------------
def tesseract_ocr_pdf(file_bytes):
    try:
        pages = convert_from_bytes(file_bytes)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page) + "\n"
        return text
    except Exception as e:
        st.error(f"Tesseract PDF OCR failed: {e}")
        return ""

# -----------------------------
# ✅ Main OCR function
# -----------------------------
def extract_text_with_vision(uploaded_file):
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.type.lower()

    client = get_vision_client()

    # -----------------------------
    # 1️⃣ Try Google Vision if possible
    # -----------------------------
    if client:
        try:
            if "image" in file_type:
                image = vision.Image(content=file_bytes)
                response = client.text_detection(image=image)
                texts = response.text_annotations
                if texts:
                    return texts[0].description
            elif "pdf" in file_type:
                image = vision.Image(content=file_bytes)
                response = client.document_text_detection(image=image)
                if response.full_text_annotation:
                    return response.full_text_annotation.text
        except Exception as e:
            st.warning(f"Google Vision failed, falling back to Tesseract: {e}")

    # -----------------------------
    # 2️⃣ Fallback to Tesseract OCR
    # -----------------------------
    if "image" in file_type:
        return tesseract_ocr_image(file_bytes)
    elif "pdf" in file_type:
        return tesseract_ocr_pdf(file_bytes)
    else:
        st.warning("Unsupported file type, attempting Tesseract OCR as image")
        return tesseract_ocr_image(file_bytes)

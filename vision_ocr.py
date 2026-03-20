import streamlit as st
import json
from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image
import io
import fitz  # pymupdf

def get_vision_client():
    try:
        creds_json = st.secrets["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
        creds_dict = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        client = vision.ImageAnnotatorClient(credentials=credentials)
        return client
    except Exception as e:
        st.error(f"❌ Google Vision setup failed: {e}")
        return None

def extract_text_with_vision(uploaded_file):
    client = get_vision_client()
    if client is None:
        return ""

    try:
        file_bytes = uploaded_file.read()
        file_type = uploaded_file.type

        # -----------------------------
        # IMAGE HANDLING
        # -----------------------------
        if "image" in file_type:
            image = vision.Image(content=file_bytes)
            response = client.text_detection(image=image)
            texts = response.text_annotations
            return texts[0].description if texts else ""

        # -----------------------------
        # PDF HANDLING (ALL PAGES)
        # -----------------------------
        elif "pdf" in file_type:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            full_text = ""
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img_bytes = pix.tobytes("png")
                image = vision.Image(content=img_bytes)
                response = client.document_text_detection(image=image)
                if response.full_text_annotation:
                    full_text += response.full_text_annotation.text + "\n"
            return full_text

        else:
            st.warning("Unsupported file type")
            return ""

    except Exception as e:
        st.error(f"❌ OCR Extraction failed: {e}")
        return ""
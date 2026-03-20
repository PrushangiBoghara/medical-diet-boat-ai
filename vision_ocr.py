import streamlit as st
from PIL import Image
import io
import easyocr
import numpy as np

# EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_with_vision(uploaded_file):
    try:
        file_bytes = uploaded_file.read()
        file_type = uploaded_file.type.lower()

        if "image" in file_type:
            image = Image.open(io.BytesIO(file_bytes))
            result = reader.readtext(np.array(image), detail=0)
            return "\n".join(result)
        else:
            st.warning("Only image OCR is supported. For PDFs, please paste the text.")
            return ""

    except Exception as e:
        st.error(f"OCR failed: {e}")
        return ""
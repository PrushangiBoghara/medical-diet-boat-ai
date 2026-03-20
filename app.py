import streamlit as st
from vision_ocr import extract_text_with_vision
from text_cleaner import clean_text
from extractor import extract_medical_data
from diet_generator import generate_diet_plan

st.set_page_config(page_title="AI Diet Planner", layout="wide")
st.title("🥗 AI Medical Diet Planner")
st.markdown("Upload your medical report (PDF/Image) or paste text directly to get a personalized diet plan.")

# -----------------------------
# ✅ File uploader
# -----------------------------
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

# -----------------------------
# ✅ Text input as fallback
# -----------------------------
user_text = st.text_area("Or paste your report text here (if OCR fails)", height=200)

# -----------------------------
# ✅ Generate diet plan
# -----------------------------
if st.button("Generate Diet Plan"):

    # Step 1: Extract text
    text = ""
    if uploaded_file:
        with st.spinner("Processing uploaded file..."):
            text = extract_text_with_vision(uploaded_file)
            if not text.strip():
                st.warning("OCR failed. You can paste the report text in the text area below.")
    elif user_text.strip():
        text = user_text
    else:
        st.error("Please upload a file or paste text.")
        st.stop()

    # Step 2: Clean text
    cleaned_text = clean_text(text)

    # Step 3: Extract structured medical data
    structured_data = extract_medical_data(cleaned_text)

    if "error" in structured_data:
        st.error("Extraction failed. Showing raw output:")
        st.text(structured_data.get("raw_output", "No output"))
    else:
        # Step 4: Show extracted data
        st.subheader("📊 Extracted Medical Data")
        st.json(structured_data)

        # Step 5: Generate diet plan
        diet_plan = generate_diet_plan(structured_data)
        st.subheader("🥗 Personalized Diet Plan")
        st.write(diet_plan)

        # Step 6: Download option
        st.download_button(
            label="Download Diet Plan",
            data=diet_plan,
            file_name="diet_plan.txt"
        )
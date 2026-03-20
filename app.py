import streamlit as st
from vision_ocr import extract_text_with_vision
from text_cleaner import clean_text
from extractor import extract_medical_data
from diet_generator import generate_diet_plan

st.set_page_config(page_title="AI Diet Planner", layout="wide")

st.title("🥗 AI Medical Diet Planner")
st.markdown("Upload your medical report (PDF or Image) and get a personalized diet plan.")

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg", "bmp"])

if uploaded_file:
    st.success("File uploaded successfully!")

    if st.button("Generate Diet Plan"):
        with st.spinner("Processing report..."):
            # Step 1: OCR
            text = extract_text_with_vision(uploaded_file)

        if not text or len(text.strip()) < 20:
            st.error("❌ OCR failed. Please upload a clear medical report.")
            st.stop()

        st.write("✅ Extracted Text Preview:")
        st.text(text[:1000])

        # Step 2: Clean Text
        cleaned_text = clean_text(text)

        # Step 3: Extract Structured Data
        structured_data = extract_medical_data(cleaned_text)

        # Step 4: Handle Extraction Errors
        if "error" in structured_data:
            st.error("Extraction failed. Showing raw output.")
            st.text(structured_data.get("raw_output", "No output"))
        else:
            # Step 5: Show Extracted Data
            st.subheader("📊 Extracted Medical Data")
            st.json(structured_data)

            # Step 6: Generate Diet Plan
            diet_plan = generate_diet_plan(structured_data)

            # Step 7: Show Diet Plan
            st.subheader("🥗 Personalized Diet Plan")
            st.write(diet_plan)

            # Step 8: Download Option
            st.download_button(
                label="Download Diet Plan",
                data=diet_plan,
                file_name="diet_plan.txt"
            )
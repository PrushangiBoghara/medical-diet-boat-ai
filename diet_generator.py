import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

DIET_PROMPT = """
You are a professional diet planner.
Create a personalized Indian diet plan based on:
- Medical conditions
- Abnormal test values
- Age and gender

Include:
- Breakfast
- Lunch
- Dinner
- Snacks
- Foods to avoid

Keep it simple, practical, and healthy.
"""

def generate_diet_plan(structured_data):
    try:
        response = client.chat.completions.create(
            model=st.secrets["GROQ_MODEL"],
            messages=[
                {"role": "system", "content": DIET_PROMPT},
                {"role": "user", "content": str(structured_data)}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating diet plan: {str(e)}"
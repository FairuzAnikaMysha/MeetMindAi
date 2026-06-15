import streamlit as st
import google.generativeai as genai
import pdfplumber

from report_generator import generate_pdf

genai.configure(
    api_key="AQ.Ab8RN6IlD0sh9c-2TydsWvJ_Ot0kLwU81MUH16sxHk7q5BHbSg"
)

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(
    page_title="MeetMind AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MeetMind AI")
st.caption("AI Powered Meeting Intelligence Assistant")

uploaded_file = st.file_uploader(
    "Upload Meeting Transcript",
    type=["pdf", "txt"]
)

meeting_notes = st.text_area(
    "Or Paste Meeting Notes",
    height=250
)

text = ""

if uploaded_file:

    if uploaded_file.name.endswith(".pdf"):

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

    else:

        text = uploaded_file.read().decode("utf-8")

if meeting_notes:
    text += "\n" + meeting_notes

if st.button("Analyze Meeting"):

    if not text.strip():

        st.warning(
            "Please upload a transcript or paste notes."
        )

        st.stop()

    prompt = f"""
You are a professional business analyst.

Analyze this meeting transcript.

Provide:

1. Executive Summary

2. Key Decisions

3. Action Items

4. Task Owners

5. Deadlines

6. Follow-up Email

Meeting Notes:

{text[:20000]}
"""

    try:

        with st.spinner("Analyzing Meeting..."):

            response = model.generate_content(prompt)

            result = response.text

        st.markdown(result)

        pdf_file = generate_pdf(result)

        st.download_button(
            "📄 Download Report",
            pdf_file,
            file_name="meeting_report.pdf",
            mime="application/pdf"
        )

    except Exception as e:

        st.error(str(e))

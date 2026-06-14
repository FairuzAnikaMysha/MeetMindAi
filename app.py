%%writefile app.py

import streamlit as st
import google.generativeai as genai
import pdfplumber

from report_generator import generate_pdf

# Configure API Key. Please replace "YOUR_GEMINI_API_KEY" with your actual key.
genai.configure(api_key="AQ.Ab8RN6IlD0sh9c-2TydsWvJ_Ot0kLwU81MUH16sxHk7q5BHbSg")

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
    type=["pdf","txt"]
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

        text = str(uploaded_file.read(),"utf-8")

if meeting_notes:
    text += meeting_notes

if st.button("Analyze Meeting"):

    if text.strip() == "":
        st.warning("Please upload or enter meeting notes.")
        st.stop()

    prompt = f"""
You are a professional business analyst.

Analyze the meeting transcript.

Return:

1. Executive Summary

2. Key Decisions

3. Action Items

4. Task Owners

5. Deadlines

6. Follow-up Email

Meeting Notes:

{text}
"""

    with st.spinner("Analyzing Meeting..."):

        response = model.generate_content(prompt)

        result = response.text

    st.session_state["report"] = result

    st.markdown(result)

    pdf_file = generate_pdf(result)

    st.download_button(
        label="Download Report",
        data=pdf_file,
        
        file_name="meeting_report.pdf",
        mime="application/pdf"
    )
    %%writefile report_generator.py
from fpdf import FPDF
from io import BytesIO

def generate_pdf(report_content: str) -> BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Split content by lines to fit within PDF page width
    for line in report_content.split('\n'):
        # Add a line break after each line to ensure proper formatting
        pdf.multi_cell(0, 10, txt=line)
    
    # Save the PDF to a BytesIO object
    pdf_output = BytesIO()
    # FPDF.output(dest='S') returns the document as a byte string directly
    # The double call to output() and then encode('latin1') is redundant and incorrect.
    # We should just get the byte string once and write it.
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

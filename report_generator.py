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

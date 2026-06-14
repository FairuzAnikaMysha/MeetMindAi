from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO


def generate_pdf(content):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "MeetMind AI Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    for line in content.split("\n"):

        if line.strip():

            elements.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

    doc.build(elements)

    buffer.seek(0)

    return buffer

"""
export.py
Export Chat to PDF, TXT and Markdown
"""

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# ----------------------------------------
# Export TXT
# ----------------------------------------

def export_txt(messages):

    text = ""

    for message in messages:

        role = message["role"].capitalize()

        content = message["content"]

        text += f"{role}\n"

        text += "-" * 40 + "\n"

        text += content + "\n\n"

    return text


# ----------------------------------------
# Export Markdown
# ----------------------------------------

def export_markdown(messages):

    md = "# Chat History\n\n"

    for message in messages:

        role = message["role"].capitalize()

        md += f"## {role}\n\n"

        md += message["content"] + "\n\n"

    return md


# ----------------------------------------
# Export PDF
# ----------------------------------------

def export_pdf(messages, filename="chat_history.pdf"):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<b>Professional RAG Chatbot</b>",
            styles["Title"]
        )
    )

    for message in messages:

        role = message["role"].capitalize()

        content = message["content"]

        story.append(
            Paragraph(
                f"<b>{role}</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                content,
                styles["BodyText"]
            )
        )

    pdf.build(story)

    return filename
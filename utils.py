"""
utils.py
Document Reader + Chunking
"""

from pypdf import PdfReader
from docx import Document
import pandas as pd
import re


# ----------------------------------------
# Clean Text
# ----------------------------------------

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ----------------------------------------
# Read PDF
# ----------------------------------------

def read_pdf(file):

    pdf = PdfReader(file)

    pages = []

    for page_number, page in enumerate(pdf.pages):

        text = page.extract_text()

        if text:

            pages.append(
                {
                    "text": clean_text(text),
                    "source": file.name,
                    "page": page_number + 1
                }
            )

    return pages


# ----------------------------------------
# Read DOCX
# ----------------------------------------

def read_docx(file):

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return [
        {
            "text": clean_text(text),
            "source": file.name,
            "page": 1
        }
    ]


# ----------------------------------------
# Read TXT
# ----------------------------------------

def read_txt(file):

    text = file.read().decode("utf-8")

    return [
        {
            "text": clean_text(text),
            "source": file.name,
            "page": 1
        }
    ]


# ----------------------------------------
# Read CSV
# ----------------------------------------

def read_csv(file):

    df = pd.read_csv(file)

    return [
        {
            "text": df.to_string(index=False),
            "source": file.name,
            "page": 1
        }
    ]


# ----------------------------------------
# Read Excel
# ----------------------------------------

def read_excel(file):

    df = pd.read_excel(file)

    return [
        {
            "text": df.to_string(index=False),
            "source": file.name,
            "page": 1
        }
    ]


# ----------------------------------------
# Split Text
# ----------------------------------------

def split_text(
    pages,
    chunk_size=500,
    overlap=100
):

    chunks = []

    for page in pages:

        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = {

                "text": text[start:end],

                "source": page["source"],

                "page": page["page"]

            }

            chunks.append(chunk)

            start += chunk_size - overlap

    return chunks
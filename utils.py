import os
import pandas as pd

from pypdf import PdfReader
from docx import Document


# ==========================================================
# PDF READER
# ==========================================================

def read_pdf(file):

    """
    Read PDF file and return
    a list of page dictionaries.

    Returns:
    [
        {
            "text": "...",
            "page": 1,
            "source": "sample.pdf"
        }
    ]
    """

    reader = PdfReader(file)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        try:

            text = page.extract_text()

            if text:

                pages.append(

                    {
                        "text": text.strip(),

                        "page": page_number,

                        "source": file.name

                    }

                )

        except Exception:

            continue

    return pages


# ==========================================================
# DOCX READER
# ==========================================================

def read_docx(file):

    """
    Read DOCX file.
    """

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return [

        {

            "text": text,

            "page": 1,

            "source": file.name

        }

    ]


# ==========================================================
# TXT READER
# ==========================================================

def read_txt(file):

    """
    Read TXT file.
    """

    text = file.read().decode("utf-8")

    return [

        {

            "text": text,

            "page": 1,

            "source": file.name

        }

    ]
    # ==========================================================
# CSV READER
# ==========================================================

def read_csv(file):

    """
    Read CSV file and convert
    all rows into plain text.
    """

    df = pd.read_csv(file)

    text = df.to_string(index=False)

    return [

        {

            "text": text,

            "page": 1,

            "source": file.name

        }

    ]


# ==========================================================
# EXCEL READER
# ==========================================================

def read_excel(file):

    """
    Read Excel file and convert
    all sheets into text.
    """

    excel = pd.ExcelFile(file)

    pages = []

    for sheet in excel.sheet_names:

        df = pd.read_excel(

            excel,

            sheet_name=sheet

        )

        pages.append(

            {

                "text": df.to_string(index=False),

                "page": sheet,

                "source": file.name

            }

        )

    return pages


# ==========================================================
# PROCESS DOCUMENTS
# ==========================================================

def process_documents(uploaded_files):

    """
    Process uploaded files
    and return all pages.
    """

    all_pages = []

    for file in uploaded_files:

        extension = os.path.splitext(

            file.name

        )[1].lower()

        try:

            # -----------------------------
            # PDF
            # -----------------------------

            if extension == ".pdf":

                all_pages.extend(

                    read_pdf(file)

                )

            # -----------------------------
            # DOCX
            # -----------------------------

            elif extension == ".docx":

                all_pages.extend(

                    read_docx(file)

                )

            # -----------------------------
            # TXT
            # -----------------------------

            elif extension == ".txt":

                all_pages.extend(

                    read_txt(file)

                )

            # -----------------------------
            # CSV
            # -----------------------------

            elif extension == ".csv":

                all_pages.extend(

                    read_csv(file)

                )

            # -----------------------------
            # EXCEL
            # -----------------------------

            elif extension == ".xlsx":

                all_pages.extend(

                    read_excel(file)

                )

        except Exception as e:

            print(

                f"Error processing {file.name}: {e}"

            )

    return all_pages
    # ==========================================================
# SMART TEXT SPLITTER
# ==========================================================

def split_text(

    pages,

    chunk_size=600,

    overlap=100

):

    """
    Split documents into overlapping chunks while
    preserving metadata (source & page).
    """

    chunks = []

    for page in pages:

        text = page["text"]

        source = page["source"]

        page_no = page["page"]

        # Skip empty pages

        if not text.strip():

            continue

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append(

                {

                    "text": chunk,

                    "source": source,

                    "page": page_no

                }

            )

            # Stop when we reach end

            if end >= len(text):

                break

            # Overlap

            start += chunk_size - overlap

    return chunks


# ==========================================================
# DOCUMENT INFORMATION
# ==========================================================

def document_summary(pages):

    """
    Return useful statistics about
    uploaded documents.
    """

    total_documents = len(

        set(

            page["source"]

            for page in pages

        )

    )

    total_pages = len(pages)

    total_characters = sum(

        len(page["text"])

        for page in pages

    )

    return {

        "documents": total_documents,

        "pages": total_pages,

        "characters": total_characters

    }


# ==========================================================
# VALIDATE DOCUMENTS
# ==========================================================

def validate_documents(pages):

    """
    Remove empty pages.
    """

    cleaned = []

    for page in pages:

        if page["text"].strip():

            cleaned.append(page)

    return cleaned

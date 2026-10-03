from io import BytesIO
from typing import List, Dict

from pypdf import PdfReader


def extract_documents(uploaded_file) -> List[Dict]:
    """
    Extract text from every page of an uploaded PDF.

    Returns:
        List of dictionaries containing:
        - text
        - document name
        - page number
    """

    file_bytes = uploaded_file.getvalue()
    reader = PdfReader(BytesIO(file_bytes))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text or not text.strip():
            continue

        documents.append(
            {
                "text": text.strip(),
                "document": uploaded_file.name,
                "page": page_number,
            }
        )

    return documents
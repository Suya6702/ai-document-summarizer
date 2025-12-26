#extractor.py
from PyPDF2 import PdfReader
import docx
from fastapi import UploadFile


def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return " ".join(text)

    elif filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return " ".join(p.text for p in doc.paragraphs if p.text)

    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")


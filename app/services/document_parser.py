from pathlib import Path
from io import BytesIO
from pypdf import PdfReader
from docx import Document

def extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)

def extract_docx(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    paragraphs = []
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)
    return "\n".join(paragraphs)

def extract_txt(file_bytes: bytes) -> str:
    return file_bytes.decode(
        "utf-8",
        errors="ignore"
    )

def parse_document(
    filename: str,
    file_bytes: bytes
) -> str:
    extension = Path(filename).suffix.lower()
    if extension == ".pdf":
        return extract_pdf(file_bytes)
    if extension == ".docx":
        return extract_docx(file_bytes)
    if extension == ".txt":
        return extract_txt(file_bytes)
    raise ValueError(
        f"Unsupported file type: {extension}"
    )

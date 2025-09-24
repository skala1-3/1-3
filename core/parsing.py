# core/parsing.py
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document   # python-docx 라이브러리 사용


def parse_pdf(file_path: str) -> str:
    """PDF 파일에서 텍스트 추출"""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  # None 체크
            text += page_text + "\n"
    return text.strip()


def parse_docx(file_path: str) -> str:
    """DOCX 파일에서 텍스트 추출"""
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text.strip()


def parse_document(file_path: str) -> str:
    """확장자에 따라 PDF/DOCX 파싱"""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return parse_docx(file_path)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {ext}")

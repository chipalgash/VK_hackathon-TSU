import json
from typing import Any, List


def extract_text_from_txt(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        return f.read()


def extract_text_from_json(path: str) -> str:
    def recurse(obj: Any) -> List[str]:
        parts: List[str] = []
        if isinstance(obj, dict):
            for v in obj.values():
                parts.extend(recurse(v))
        elif isinstance(obj, list):
            for el in obj:
                parts.extend(recurse(el))
        elif isinstance(obj, str):
            parts.append(obj)
        return parts

    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return " ".join(recurse(data))


def extract_text_from_pdf(path: str) -> str:
    try:
        import PyPDF2
    except ImportError:
        raise RuntimeError("Установите PyPDF2: pip install PyPDF2")
    text_parts: List[str] = []
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text_parts.append(page.extract_text() or '')
    return "\n".join(text_parts)


def extract_text_from_docx(path: str) -> str:
    try:
        from docx import Document
    except ImportError:
        raise RuntimeError("Установите python-docx: pip install python-docx")
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

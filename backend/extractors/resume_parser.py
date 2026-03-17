# extractors/resume_parser.py
# Parses PDF / DOCX / plain text resumes into clean text

import io
import re
import hashlib
import pdfplumber

def parse_resume_file(file_bytes: bytes, filename: str) -> dict:
    """
    Parse resume file and return extracted text + metadata.
    Supports PDF and TXT files.
    """
    ext = filename.lower().split(".")[-1]
    text = ""

    if ext == "pdf":
        text = _parse_pdf(file_bytes)
    elif ext in ["txt", "text"]:
        text = file_bytes.decode("utf-8", errors="ignore")
    elif ext == "docx":
        text = _parse_docx(file_bytes)
    else:
        text = file_bytes.decode("utf-8", errors="ignore")

    text = clean_text(text)
    file_hash = hashlib.md5(file_bytes).hexdigest()

    return {
        "text": text,
        "file_hash": file_hash,
        "filename": filename,
        "word_count": len(text.split()),
        "char_count": len(text),
        "page_estimate": max(1, len(text) // 2000)
    }


def _parse_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using pdfplumber."""
    parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    parts.append(page_text)
    except Exception as e:
        raise ValueError(f"PDF parsing failed: {str(e)}")

    if not parts:
        raise ValueError(
            "Could not extract text from PDF. "
            "Please use a text-based PDF (not scanned/image) "
            "or paste your resume as text."
        )
    return "\n".join(parts)


def _parse_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        raise ValueError(f"DOCX parsing failed: {str(e)}")


def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r'\x00', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[^\S\n]{2,}', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def extract_metadata(text: str) -> dict:
    """Extract basic metadata from resume text."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Email detection
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)

    # Phone detection
    phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
    phones = re.findall(phone_pattern, text)

    # LinkedIn
    linkedin = "linkedin.com" in text.lower()

    # GitHub
    github = "github.com" in text.lower()

    # Year range for experience estimation
    years = re.findall(r'\b(19|20)\d{2}\b', text)
    years = [int(y) for y in years if 1990 <= int(y) <= 2025]
    experience_years = 0
    if len(years) >= 2:
        experience_years = max(years) - min(years)

    # Education detection
    education_keywords = ["bachelor", "master", "phd", "b.tech", "m.tech",
                          "b.e", "m.e", "bca", "mca", "degree", "university",
                          "college", "institute"]
    has_education = any(kw in text.lower() for kw in education_keywords)

    education_level = "Unknown"
    if any(kw in text.lower() for kw in ["phd", "doctorate", "ph.d"]):
        education_level = "PhD"
    elif any(kw in text.lower() for kw in ["master", "m.tech", "m.e", "mca", "mba", "m.s"]):
        education_level = "Master's"
    elif has_education:
        education_level = "Bachelor's"

    # Candidate name — usually first non-empty line
    name = lines[0] if lines else "Unknown"
    if len(name) > 50 or "@" in name or any(c.isdigit() for c in name[:5]):
        name = "Unknown"

    return {
        "candidate_name": name,
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "has_linkedin": linkedin,
        "has_github": github,
        "experience_years": experience_years,
        "education_level": education_level,
        "word_count": len(text.split()),
    }

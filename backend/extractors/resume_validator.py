# extractors/resume_validator.py
# Detects if an uploaded PDF is actually a resume or something else
# (invoice, book, certificate, legal doc, etc.)

import re
from typing import Tuple


# ── RESUME SIGNALS ─────────────────────────────────────────────
# Words commonly found in real resumes
RESUME_SIGNALS = [
    # Sections
    "experience", "education", "skills", "summary", "objective",
    "work history", "employment", "projects", "certifications",
    "achievements", "responsibilities", "qualifications",
    "professional experience", "work experience", "career",

    # Job-related
    "engineer", "developer", "manager", "analyst", "designer",
    "intern", "consultant", "architect", "specialist", "coordinator",
    "director", "officer", "associate", "executive", "lead",

    # Education
    "university", "college", "bachelor", "master", "phd", "degree",
    "b.tech", "m.tech", "b.e", "m.e", "bca", "mca", "graduation",

    # Contact
    "email", "phone", "linkedin", "github", "portfolio", "address",

    # Time markers typical in resumes
    "present", "current", "jan", "feb", "mar", "apr",
    "2019", "2020", "2021", "2022", "2023", "2024",
]

# ── NON-RESUME SIGNALS ─────────────────────────────────────────
# Words that suggest this is NOT a resume
NON_RESUME_SIGNALS = {
    "invoice": "invoice/billing document",
    "receipt": "receipt",
    "bill to": "invoice/billing document",
    "total amount": "financial document",
    "tax invoice": "tax document",
    "gst": "tax document",
    "payable": "financial document",
    "chapter": "book or academic paper",
    "abstract": "research paper",
    "references\n": "research paper",
    "bibliography": "research paper",
    "hereby certify": "certificate",
    "this is to certify": "certificate",
    "certificate of": "certificate",
    "awarded to": "certificate/award",
    "legal notice": "legal document",
    "agreement between": "legal document",
    "terms and conditions": "legal document",
    "whereas": "legal document",
    "hereinafter": "legal document",
    "plaintiff": "legal document",
    "defendant": "legal document",
    "affidavit": "legal document",
    "table of contents": "book or report",
    "index\n": "book or report",
    "disclaimer": "legal/policy document",
    "privacy policy": "policy document",
    "terms of service": "policy document",
    "purchase order": "purchase order",
    "delivery note": "logistics document",
    "packing list": "logistics document",
    "medical report": "medical document",
    "prescription": "medical document",
    "diagnosis": "medical document",
    "patient name": "medical document",
    "salary slip": "payslip",
    "pay slip": "payslip",
    "net salary": "payslip",
    "gross salary": "payslip",
    "deductions": "payslip",
    "bank statement": "bank statement",
    "account number": "bank/financial document",
    "transaction history": "bank statement",
    "balance": "financial document",
}


def validate_resume(text: str) -> Tuple[bool, str, str]:
    """
    Validate if extracted text is actually a resume.

    Returns:
        (is_valid, error_message, document_type)
        - is_valid: True if it looks like a resume
        - error_message: human-readable message if invalid
        - document_type: detected type if not a resume
    """
    if not text or len(text.strip()) < 50:
        return False, "The uploaded file appears to be empty or could not be read. Please upload a text-based PDF resume.", "empty"

    text_lower = text.lower()

    # ── Check for non-resume signals first ────────────────────
    for signal, doc_type in NON_RESUME_SIGNALS.items():
        if signal in text_lower:
            return (
                False,
                f"The uploaded file appears to be a {doc_type}, not a resume. "
                f"Please upload your CV or resume in PDF format.",
                doc_type
            )

    # ── Count resume signals ───────────────────────────────────
    resume_score = sum(1 for signal in RESUME_SIGNALS if signal in text_lower)

    # ── Additional checks ──────────────────────────────────────
    has_email   = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text))
    has_year    = bool(re.search(r'\b(19|20)\d{2}\b', text))
    has_name    = len(text.strip().split('\n')[0].strip()) < 60  # first line is usually a name
    word_count  = len(text.split())

    # Too short — not a proper resume
    if word_count < 80:
        return (
            False,
            f"The uploaded PDF has very little text ({word_count} words). "
            "A resume should have at least 150 words. "
            "If your PDF is scanned, please paste your resume text instead.",
            "too_short"
        )

    # Too long — probably a book or report
    if word_count > 5000:
        return (
            False,
            f"The uploaded file is very long ({word_count} words). "
            "This looks like a document, book, or report rather than a resume. "
            "Please upload only your resume (1-3 pages).",
            "too_long"
        )

    # Very low resume score
    if resume_score < 3:
        return (
            False,
            "The uploaded file does not look like a resume. "
            "A resume should contain sections like Experience, Education, and Skills. "
            "Please upload your CV or resume.",
            "unrecognized_document"
        )

    # Needs at least email or year + reasonable resume score
    if resume_score < 5 and not has_email and not has_year:
        return (
            False,
            "The uploaded file may not be a resume. "
            "Please make sure you are uploading your CV or resume with your experience, education, and skills.",
            "low_confidence"
        )

    # ── Passed all checks ──────────────────────────────────────
    return True, "", "resume"


def get_validation_details(text: str) -> dict:
    """
    Returns detailed validation info for debugging.
    """
    text_lower = text.lower()
    resume_score = sum(1 for s in RESUME_SIGNALS if s in text_lower)
    found_signals = [s for s in RESUME_SIGNALS if s in text_lower]

    non_resume_found = []
    for signal, doc_type in NON_RESUME_SIGNALS.items():
        if signal in text_lower:
            non_resume_found.append({"signal": signal, "type": doc_type})

    return {
        "word_count":        len(text.split()),
        "resume_score":      resume_score,
        "found_signals":     found_signals[:10],
        "non_resume_found":  non_resume_found,
        "has_email":         bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)),
        "has_year":          bool(re.search(r'\b(19|20)\d{2}\b', text)),
        "char_count":        len(text),
    }

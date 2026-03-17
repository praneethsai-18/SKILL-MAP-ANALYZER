# main.py — SkillMap AI ML Backend
# FastAPI app wiring all ML components together

import os
import json
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="SkillMap AI — ML Backend",
    description="Resume skill gap analyzer powered by spaCy + BERT. No external AI APIs.",
    version="2.0.0"
)

# ── CORS — allow all origins including file:// ─────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.options("/{rest_of_path:path}")
async def preflight(rest_of_path: str):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# ── Lazy import ML components (load on first request) ──────────
def get_components():
    from extractors.resume_parser import parse_resume_file, extract_metadata
    from extractors.skill_extractor import extract_skills
    from analyzers.skill_analyzer import get_analyzer
    from analyzers.battle_analyzer import get_battle_analyzer
    from database.connection import AnalysisCollection, ResumeCollection, SkillsCollection
    return {
        "parse_resume": parse_resume_file,
        "extract_metadata": extract_metadata,
        "extract_skills": extract_skills,
        "analyzer": get_analyzer(),
        "battle_analyzer": get_battle_analyzer(),
        "analyses": AnalysisCollection,
        "resumes": ResumeCollection,
        "skills": SkillsCollection
    }


# ── HEALTH CHECK ───────────────────────────────────────────────
@app.get("/")
def health():
    return {
        "status": "SkillMap AI ML Backend is running",
        "version": "2.0.0",
        "models": "spaCy + BERT (all-MiniLM-L6-v2)",
        "database": "MongoDB",
        "note": "No external AI APIs — everything runs locally"
    }

@app.get("/health")
def health_check():
    from database.connection import ping_db
    db_ok = ping_db()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }


# ── POST /analyze — PDF file upload ───────────────────────────
@app.post("/analyze")
async def analyze_pdf(
    resume: UploadFile = File(...),
    roles: str = Form(...)
):
    """
    Analyze uploaded PDF resume against selected roles.
    Uses spaCy + BERT for skill extraction, no external APIs.
    """
    c = get_components()

    # Parse roles
    try:
        roles_list = json.loads(roles)
        if not isinstance(roles_list, list) or len(roles_list) == 0:
            raise ValueError("Empty roles list")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid roles format. Send a JSON array of role names.")

    # Read and parse file
    file_bytes = await resume.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    try:
        parsed = c["parse_resume"](file_bytes, resume.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    resume_text = parsed["text"]
    if len(resume_text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Could not extract enough text from the PDF. Please use a text-based PDF or paste text instead."
        )

    # ── Validate it is actually a resume ──────────────────────
    from extractors.resume_validator import validate_resume
    is_valid, error_msg, doc_type = validate_resume(resume_text)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Extract metadata + skills
    metadata = c["extract_metadata"](resume_text)
    metadata["filename"] = resume.filename
    resume_skills = c["extract_skills"](resume_text)

    if not resume_skills:
        raise HTTPException(
            status_code=400,
            detail="No recognizable skills found in the resume. Please ensure the resume contains technical skills."
        )

    # Run analysis
    result = _run_analysis(c, resume_text, resume_skills, roles_list, metadata, parsed.get("file_hash"))
    return result


# ── POST /analyze-text — paste resume text ────────────────────
@app.post("/analyze-text")
async def analyze_text(
    resume_text: str = Form(...),
    roles: str = Form(...)
):
    """
    Analyze pasted resume text against selected roles.
    Uses spaCy + BERT for skill extraction, no external APIs.
    """
    c = get_components()

    if not resume_text or len(resume_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Resume text is too short. Please provide at least 50 characters.")

    try:
        roles_list = json.loads(roles)
        if not isinstance(roles_list, list) or len(roles_list) == 0:
            raise ValueError("Empty roles list")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid roles format. Send a JSON array of role names.")

    # ── Validate it is actually a resume ──────────────────────
    from extractors.resume_validator import validate_resume
    is_valid, error_msg, doc_type = validate_resume(resume_text)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Extract metadata + skills
    metadata = c["extract_metadata"](resume_text)
    metadata["filename"] = "Pasted Resume"
    resume_skills = c["extract_skills"](resume_text)

    if not resume_skills:
        raise HTTPException(
            status_code=400,
            detail="No recognizable skills found in the pasted text. Please ensure the text contains technical skills."
        )

    result = _run_analysis(c, resume_text, resume_skills, roles_list, metadata, None)
    return result


# ── Core analysis runner ───────────────────────────────────────
def _run_analysis(c, resume_text, resume_skills, roles_list, metadata, file_hash):
    """Run single or battle analysis based on role count."""
    session_id = str(uuid.uuid4())

    if len(roles_list) == 1:
        # Single role analysis
        role_result = c["analyzer"].analyze_single(
            resume_text, resume_skills, roles_list[0], metadata
        )

        from analyzers.skill_analyzer import SkillAnalyzer
        overall_score = max(10, min(98, round(
            role_result["match_score"] * 0.7 +
            role_result["ats_score"] * 0.2 +
            sum(role_result["strength_scores"].values()) / len(role_result["strength_scores"]) * 0.1
        )))

        result = {
            "mode": "single",
            "session_id": session_id,
            "candidate_name": metadata.get("candidate_name", "Unknown"),
            "detected_skills": resume_skills,
            "total_experience_years": metadata.get("experience_years", 0),
            "roles": [role_result],
            "winner_role": roles_list[0],
            "skill_overlap": {"all_roles_need": [], "two_roles_need": [], "winner_only": []},
            "overall_resume_score": overall_score,
            "career_gap_note": "No significant gaps detected"
        }
    else:
        # Battle mode
        result = c["battle_analyzer"].analyze_battle(
            resume_text, resume_skills, roles_list, metadata
        )
        result["mode"] = "battle"
        result["session_id"] = session_id

    # Save to MongoDB
    try:
        save_data = {
            "session_id": session_id,
            "mode": result.get("mode"),
            "candidate_name": result.get("candidate_name"),
            "roles_analyzed": roles_list,
            "overall_score": result.get("overall_resume_score"),
            "winner_role": result.get("winner_role"),
            "resume_skills_count": len(resume_skills),
            "file_hash": file_hash
        }
        analysis_id = c["analyses"].save(save_data)
        result["analysis_id"] = analysis_id

        # Track skill frequency in DB
        for skill in resume_skills:
            from data.skill_taxonomy import get_skill_category
            cat = get_skill_category(skill)
            try:
                c["skills"].increment_skill(skill, cat)
            except Exception:
                pass

    except Exception as db_err:
        print(f"⚠️ DB save failed (non-critical): {db_err}")

    return result


# ── GET /roles — list all available roles ─────────────────────
@app.get("/roles")
def get_roles():
    """Return all available role names."""
    from data.skill_taxonomy import ROLE_PROFILES
    roles = []
    for role_name, profile in ROLE_PROFILES.items():
        roles.append({
            "name": role_name,
            "required_skills_count": len(profile.get("required", [])),
            "salary_range": profile.get("salary_range", "Market dependent")
        })
    return {"roles": roles, "total": len(roles)}


# ── GET /skills/trending — most common resume skills ──────────
@app.get("/skills/trending")
def get_trending_skills():
    """Return most frequently seen skills across all analyses."""
    try:
        from database.connection import SkillsCollection
        trending = SkillsCollection.get_trending(20)
        return {
            "trending": [
                {"name": s["name"], "count": s.get("count", 0), "category": s.get("category", "")}
                for s in trending
            ]
        }
    except Exception:
        return {"trending": [], "note": "MongoDB not connected"}


# ── GET /analyses/history — recent analyses ───────────────────
@app.get("/analyses/history")
def get_history(session_id: str = None, limit: int = 20):
    """Return recent analyses."""
    try:
        from database.connection import AnalysisCollection
        if session_id:
            items = AnalysisCollection.find_by_session(session_id, limit)
        else:
            items = AnalysisCollection.find_recent(limit)
        # Convert ObjectId to string
        for item in items:
            item["_id"] = str(item["_id"])
        return {"analyses": items, "total": len(items)}
    except Exception as e:
        return {"analyses": [], "error": str(e)}


# ── GET /stats — database statistics ─────────────────────────
@app.get("/stats")
def get_stats():
    """Return usage statistics."""
    try:
        from database.connection import AnalysisCollection
        stats = AnalysisCollection.get_stats()
        return stats
    except Exception:
        return {"total": 0, "single": 0, "battle": 0, "note": "MongoDB not connected"}

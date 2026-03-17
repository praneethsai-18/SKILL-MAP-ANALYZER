# database/connection.py
# MongoDB connection + all collection schemas

import os
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "skillmap_ai")

# ── Global client ──────────────────────────────────────────────
_client = None
_db = None

def get_db():
    """Get MongoDB database instance."""
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGODB_URI)
        _db = _client[DB_NAME]
        _create_indexes(_db)
        print(f"✅ MongoDB connected: {MONGODB_URI}/{DB_NAME}")
    return _db

def _create_indexes(db):
    """Create indexes for performance."""
    # analyses collection
    db.analyses.create_index([("created_at", DESCENDING)])
    db.analyses.create_index([("session_id", ASCENDING)])
    db.analyses.create_index([("mode", ASCENDING)])

    # resumes collection
    db.resumes.create_index([("file_hash", ASCENDING)], unique=True, sparse=True)
    db.resumes.create_index([("created_at", DESCENDING)])

    # skills collection
    db.skills.create_index([("name", ASCENDING)], unique=True)
    db.skills.create_index([("category", ASCENDING)])

    print("✅ MongoDB indexes created")

def ping_db():
    """Test database connection."""
    try:
        db = get_db()
        db.command("ping")
        return True
    except ConnectionFailure:
        return False


# ── Collection helpers ─────────────────────────────────────────

class AnalysisCollection:
    """Helper for analyses collection."""

    @staticmethod
    def save(analysis_data: dict) -> str:
        db = get_db()
        analysis_data["created_at"] = datetime.utcnow()
        analysis_data["updated_at"] = datetime.utcnow()
        result = db.analyses.insert_one(analysis_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_id(analysis_id: str) -> dict:
        from bson import ObjectId
        db = get_db()
        return db.analyses.find_one({"_id": ObjectId(analysis_id)})

    @staticmethod
    def find_by_session(session_id: str, limit: int = 20) -> list:
        db = get_db()
        cursor = db.analyses.find(
            {"session_id": session_id},
            sort=[("created_at", DESCENDING)],
            limit=limit
        )
        return list(cursor)

    @staticmethod
    def find_recent(limit: int = 50) -> list:
        db = get_db()
        cursor = db.analyses.find(
            {},
            sort=[("created_at", DESCENDING)],
            limit=limit
        )
        return list(cursor)

    @staticmethod
    def delete(analysis_id: str) -> bool:
        from bson import ObjectId
        db = get_db()
        result = db.analyses.delete_one({"_id": ObjectId(analysis_id)})
        return result.deleted_count > 0

    @staticmethod
    def get_stats() -> dict:
        db = get_db()
        total = db.analyses.count_documents({})
        single = db.analyses.count_documents({"mode": "single"})
        battle = db.analyses.count_documents({"mode": "battle"})
        return {"total": total, "single": single, "battle": battle}


class ResumeCollection:
    """Helper for resumes collection — cache parsed resumes."""

    @staticmethod
    def save(resume_data: dict) -> str:
        db = get_db()
        resume_data["created_at"] = datetime.utcnow()
        result = db.resumes.insert_one(resume_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_hash(file_hash: str) -> dict:
        db = get_db()
        return db.resumes.find_one({"file_hash": file_hash})


class SkillsCollection:
    """Helper for skills collection — skill frequency tracking."""

    @staticmethod
    def increment_skill(skill_name: str, category: str):
        db = get_db()
        db.skills.update_one(
            {"name": skill_name},
            {
                "$inc": {"count": 1},
                "$set": {"category": category, "updated_at": datetime.utcnow()},
                "$setOnInsert": {"created_at": datetime.utcnow()}
            },
            upsert=True
        )

    @staticmethod
    def get_trending(limit: int = 20) -> list:
        db = get_db()
        cursor = db.skills.find(
            {},
            sort=[("count", DESCENDING)],
            limit=limit
        )
        return list(cursor)

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from gridfs import GridFS
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = BASE_DIR / "ai_interview_system.db"

# ─────────────────────────────────────────────────────────────────────────────
# Relational DB (SQLAlchemy: MySQL / SQLite)
# ─────────────────────────────────────────────────────────────────────────────

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{SQLITE_DB_PATH}",
)

try:
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
        )
    else:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        # Test connection
        with engine.connect() as conn:
            pass
except Exception as err:
    print(f"Warning: Could not connect to primary SQL database ({err}). Falling back to local SQLite database.")
    DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# MongoDB Database (PyMongo / Motor)
# ─────────────────────────────────────────────────────────────────────────────

MONGODB_URI = os.getenv("MONGODB_URI") or os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ai_interview_system")

mongo_client = None
mongo_db = None
mongo_fs = None

try:
    from pymongo import MongoClient

    mongo_client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=2000,
        connectTimeoutMS=2000,
    )
    mongo_db = mongo_client[MONGODB_DB_NAME]
    mongo_fs = GridFS(mongo_db)
except Exception as mongo_err:
    print(f"Warning: MongoDB setup failed ({mongo_err}). MongoDB features will run in deferred mode.")
    mongo_client = None
    mongo_db = None
    mongo_fs = None


def check_mongo_connection() -> dict:
    """Check MongoDB server status and ping result."""
    if mongo_client is None:
        return {"status": "disabled", "message": "MongoClient not initialized"}
    try:
        mongo_client.admin.command("ping")
        return {"status": "connected", "database": MONGODB_DB_NAME, "url": MONGODB_URI}
    except Exception as err:
        return {"status": "disconnected", "message": str(err), "url": MONGODB_URI}


def get_mongo_db():
    """Dependency helper for accessing MongoDB instance."""
    if mongo_db is None:
        raise RuntimeError("MongoDB connection is not established. Check your MONGODB_URL setting.")
    return mongo_db


def has_mongo_storage() -> bool:
    return mongo_db is not None and mongo_fs is not None


def save_uploaded_file(file_bytes: bytes, filename: str, metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """Store a file in MongoDB GridFS and return the generated file ID."""
    if not has_mongo_storage():
        return None

    file_record = {
        "filename": filename,
        "metadata": metadata or {},
        "uploaded_at": datetime.now(timezone.utc),
    }
    file_id = mongo_fs.put(file_bytes, **file_record)
    return str(file_id)


def save_candidate_profile(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Persist candidate metadata in MongoDB under an upserted user-based profile."""
    if not has_mongo_storage():
        return {"status": "skipped", "message": "MongoDB is not connected; candidate files were still saved locally."}

    profile = dict(candidate)
    user_id = profile.get("user_id")
    email = profile.get("email")

    if not user_id and not email:
        raise ValueError("A candidate profile must include either user_id or email.")

    filter_query = {"user_id": user_id} if user_id is not None else {"email": email}
    profile["updated_at"] = datetime.now(timezone.utc)
    profile.setdefault("created_at", profile["updated_at"])

    collection = mongo_db["candidate_profiles"]
    collection.update_one(filter_query, {"$set": profile}, upsert=True)
    saved_profile = collection.find_one(filter_query)
    if saved_profile is None:
        return {"status": "skipped", "message": "MongoDB profile save did not return a document."}

    return {
        "status": "saved",
        "profile_id": str(saved_profile.get("_id")),
        "user_id": saved_profile.get("user_id"),
        "email": saved_profile.get("email"),
    }

"""
JARVIS — PostgreSQL/SQLite DB Engine (SQLAlchemy)
Handles persistent memory (History, Profile, Summaries) using high-level ORM.
"""

import uuid
from sqlalchemy import create_engine, Column, String, Text, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import Uuid
from jarvis.config import DATABASE_URL

# Use SQLite as fallback if no DATABASE_URL is provided
if not DATABASE_URL or "localhost" in DATABASE_URL:
    ENGINE_URL = "sqlite:///jarvis_memory.db"
    engine = create_engine(ENGINE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"
    user_id = Column(String(50), primary_key=True)
    owner_name = Column(String(100), default="Hajeera")
    user_name = Column(String(100), default="Hajeera")
    preferred_lang = Column(String(10), default="en")
    preferred_voice = Column(String(50), default="en-IN-Wavenet-B")
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(String(50), index=True)
    role = Column(String(20), nullable=False) # 'user' or 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class MemorySummary(Base):
    __tablename__ = "memory_summaries"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(String(50), index=True)
    summary_text = Column(Text, nullable=False)
    last_processed_at = Column(DateTime(timezone=True), server_default=func.now())

def init_db():
    """
    Creates tables and seeds default profile for Hajeera.
    """
    try:
        Base.metadata.create_all(bind=engine)
        
        # Seed default owner
        db = SessionLocal()
        if not db.query(UserProfile).filter(UserProfile.user_id == "default_user").first():
            profile = UserProfile(
                user_id="default_user",
                owner_name="Hajeera",
                user_name="Hajeera"
            )
            db.add(profile)
            db.commit()
        db.close()
        return True
    except Exception as e:
        print(f"[JARVIS Error] DB migration failed: {e}")
        return False


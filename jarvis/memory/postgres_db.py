"""
JARVIS — PostgreSQL/SQLite DB Engine (SQLAlchemy)
Handles persistent memory using high-level ORM.
"""

import uuid
from sqlalchemy import create_engine, Column, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Uuid
from jarvis.config import DATABASE_URL

# Use SQLite as fallback if no DATABASE_URL is provided
if not DATABASE_URL or "localhost" in DATABASE_URL:
    ENGINE_URL = "sqlite:///jarvis_memory.db"
    # SQLite needs special handling for threading
    engine = create_engine(ENGINE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"

    # Using native Uuid type (SQLAlchemy 2.0+) for portability
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(String(50), index=True)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class UserPreference(Base):
    __tablename__ = "user_preferences"
    key = Column(String(50), primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Contact(Base):
    __tablename__ = "contacts"
    name = Column(String(100), primary_key=True)
    phone_number = Column(String(20), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

def init_db():
    """
    Automatically creates tables if they don't exist.
    Called on system startup.
    """
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        print(f"[JARVIS Error] DB migration failed: {e}")
        return False

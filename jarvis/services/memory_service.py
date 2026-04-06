"""
JARVIS — Memory Service
Abstraction layer for database operations using SQLAlchemy sessions.
"""

from contextlib import contextmanager
from typing import List, Optional
from jarvis.memory.postgres_db import SessionLocal, Conversation

@contextmanager
def get_db():
    """
    Context manager for safe database session handling.
    Prevents memory leaks by ensuring the session is closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MemoryService:
    """
    Service layer for conversation persistence and contextual memory.
    """

    @staticmethod
    def save_interaction(user_id: str, user_msg: str, ai_resp: str) -> bool:
        """
        Saves a conversation turn to the database.
        """
        try:
            with get_db() as db:
                new_convo = Conversation(
                    user_id=user_id,
                    user_message=user_msg,
                    ai_response=ai_resp
                )
                db.add(new_convo)
                db.commit()
                return True
        except Exception as e:
            print(f"[MemoryService Error] Save failed: {e}")
            return False

    @staticmethod
    def get_recent_history(user_id: str, limit: int = 5) -> List[Conversation]:
        """
        Retrieves the last N interactions for a user to provide context to the LLM.
        """
        try:
            with get_db() as db:
                history = db.query(Conversation)\
                    .filter(Conversation.user_id == user_id)\
                    .order_by(Conversation.timestamp.desc())\
                    .limit(limit)\
                    .all()
                # Return in chronological order for better LLM context
                return list(reversed(history))
        except Exception as e:
            print(f"[MemoryService Error] History retrieval failed: {e}")
            return []

    @staticmethod
    def clear_history(user_id: str) -> bool:
        """
        Wipes history for a user if requested (Siri-like privacy control).
        """
        try:
            with get_db() as db:
                db.query(Conversation).filter(Conversation.user_id == user_id).delete()
                db.commit()
                return True
        except Exception as e:
            print(f"[MemoryService Error] Wipe failed: {e}")
            return False

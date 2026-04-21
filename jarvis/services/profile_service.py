"""
JARVIS — Profile Service
Manages user-specific data, identity (Owner vs. User), and preferences.
"""

from typing import Optional
from jarvis.memory.postgres_db import SessionLocal, UserProfile

class ProfileService:
    @staticmethod
    def get_profile(user_id: str = "default_user") -> UserProfile:
        """Retrieves or creates the user profile."""
        db = SessionLocal()
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id, owner_name="Hajeera", user_name="Hajeera")
            db.add(profile)
            db.commit()
            db.refresh(profile)
        db.close()
        return profile

    @staticmethod
    def update_user_name(user_id: str, new_name: str) -> bool:
        """Updates the current user's name (distinct from Owner Hajeera)."""
        try:
            db = SessionLocal()
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if profile:
                profile.user_name = new_name
                db.commit()
            db.close()
            return True
        except Exception as e:
            print(f"[ProfileService Error] Update failed: {e}")
            return False

    @staticmethod
    def get_owner_identity() -> str:
        """Returns the permanent owner's name."""
        return "Hajeera"

    @staticmethod
    def get_user_identity(user_id: str = "default_user") -> str:
        """Returns the current user's name."""
        profile = ProfileService.get_profile(user_id)
        return profile.user_name


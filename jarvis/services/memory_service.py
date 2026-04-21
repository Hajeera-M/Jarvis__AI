"""
JARVIS — Memory Service
Handles the triple-layer memory strategy: raw context (last 20 messages) and long-term summaries.
"""

from typing import List, Tuple, Dict, Any
from jarvis.memory.postgres_db import SessionLocal, Conversation, MemorySummary
from jarvis.models.groq_model import think as groq_reason
from sqlalchemy import desc

class MemoryService:
    @staticmethod
    def get_context(user_id: str = "default_user", raw_limit: int = 20) -> str:
        """
        Retrieves recent context + long-term summaries.
        """
        db = SessionLocal()
        
        # 1. Fetch Latest Summary
        summary = db.query(MemorySummary).filter(MemorySummary.user_id == user_id)\
                    .order_by(desc(MemorySummary.last_processed_at)).first()
        summary_text = summary.summary_text if summary else ""
        
        # 2. Fetch Raw Conversations (Last 20)
        history = db.query(Conversation).filter(Conversation.user_id == user_id)\
                    .order_by(desc(Conversation.timestamp)).limit(raw_limit).all()
        history = list(reversed(history)) # Chronological order
        
        db.close()
        
        # 3. Format context string
        context_str = f"LONG-TERM SUMMARY: {summary_text}\n\n" if summary_text else ""
        for msg in history:
            role_label = "User" if msg.role == "user" else "AI"
            context_str += f"{role_label}: {msg.content}\n"
            
        return context_str

    @staticmethod
    def save_message(user_id: str, role: str, content: str):
        """Saves a single message and triggers summarization if threshold met."""
        db = SessionLocal()
        new_msg = Conversation(user_id=user_id, role=role, content=content)
        db.add(new_msg)
        db.commit()
        
        # Check if summarization is needed (e.g., every 30 messages)
        count = db.query(Conversation).filter(Conversation.user_id == user_id).count()
        if count % 30 == 0 and count > 0:
            MemoryService.summarize_history(user_id)
            
        db.close()

    @staticmethod
    def summarize_history(user_id: str):
        """Compresses all BUT the most recent 20 messages into a new summary."""
        db = SessionLocal()
        
        # Get all messages except the latest 20
        all_msgs = db.query(Conversation).filter(Conversation.user_id == user_id)\
                     .order_by(desc(Conversation.timestamp)).offset(20).all()
        
        if not all_msgs:
            db.close()
            return

        text_to_summarize = "\n".join([f"{m.role}: {m.content}" for m in reversed(all_msgs)])
        
        # 1. Ask LLM to summarize
        prompt = f"Summarize the following chat history into key facts and the current conversational state:\n\n{text_to_summarize}"
        system_prompt = "You are a memory compression engine. Summarize precisely and briefly."
        new_summary_text = groq_reason(prompt, system_prompt=system_prompt)
        
        if new_summary_text:
            new_summary = MemorySummary(user_id=user_id, summary_text=new_summary_text)
            db.add(new_summary)
            db.commit()
            
        db.close()


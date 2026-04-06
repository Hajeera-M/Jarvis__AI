from fastapi import FastAPI, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import asyncio
import logging
import traceback

# Ensure the 'jarvis' folder is in the path so agents can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis.agents.controller import MasterController
from jarvis.memory.postgres_db import init_db

# 1. Structured Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("jarvis_api.log")
    ]
)
logger = logging.getLogger("JARVIS-X")

# Initialize database schema at startup
try:
    init_db()
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

app = FastAPI(title="JARVIS-X API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JarvisRequest(BaseModel):
    input: str
    user_id: str = "default_user"

# Global context to persist state across API calls
context = {"intent": None, "entity": None, "entities": {}, "active_intents": set(), "last_skill": None}

@app.get("/health")
async def health():
    """Production health check endpoint."""
    return {
        "status": "running",
        "service": "JARVIS-X",
        "version": "1.0.0",
        "timestamp": asyncio.get_event_loop().time()
    }

@app.post("/jarvis")
async def jarvis_api(req: JarvisRequest):
    global context
    logger.info(f"EVENT: jarvis_request | USER: {req.user_id} | INPUT: {req.input}")
    
    try:
        # 2. Async Execution (Prevent blocking the event loop with heavy reasoning/DB calls)
        # Using the new MasterController 'Agent Routing' logic
        output, new_context = await asyncio.to_thread(
            MasterController.handle_user_input, req.input, context, req.user_id
        )
        
        # Persist the context
        context = new_context
        logger.info(f"EVENT: jarvis_response | USER: {req.user_id} | OUTPUT: {output}")
        
        return {**output, "status": "success"}

    except Exception as e:
        logger.error(f"EVENT: jarvis_error | USER: {req.user_id} | ERROR: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "error": "Internal AI Processing Error",
            "response": "I'm sorry, experimental systems are recalibrating. Please try again.",
            "status": "error"
        }

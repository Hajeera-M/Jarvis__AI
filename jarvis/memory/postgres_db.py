"""
JARVIS — PostgreSQL DB Connection
Handles connection and schema setup for the local database.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_URL

# Singleton connection holding
_conn = None

def get_connection():
    """
    Returns a persistent connection to the PostgreSQL database.
    Falls back to SQLite if Postgres is unavailable.
    """
    global _conn
    if _conn is None or (hasattr(_conn, 'closed') and _conn.closed):
        try:
            if not DATABASE_URL or "localhost" in DATABASE_URL:
                # Fallback to SQLite for truly local development if no DB_URL
                import sqlite3
                print("[JARVIS] Using local SQLite database for memory (PostgreSQL not configured).")
                _conn = sqlite3.connect("jarvis_memory.db", check_same_thread=False)
                _conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            else:
                _conn = psycopg2.connect(DATABASE_URL)
                _conn.autocommit = True
        except Exception as e:
            print(f"[JARVIS Error] Could not connect to DB: {e}. Falling back to SQLite.")
            import sqlite3
            _conn = sqlite3.connect("jarvis_memory.db", check_same_thread=False)
            _conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    return _conn

def init_db():
    """
    Creates the necessary tables if they don't exist.
    """
    conn = get_connection()
    if not conn:
        return False
        
    try:
        cur = conn.cursor()
        # Handle SQLite vs Postgres cursor differences
        is_sqlite = str(type(conn)).find('sqlite3') != -1
        
        # Create conversations table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT if is_sqlite else SERIAL PRIMARY KEY,
                user_input TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''.replace('INTEGER PRIMARY KEY AUTOINCREMENT if is_sqlite else SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT' if is_sqlite else 'SERIAL PRIMARY KEY'))
        
        # Create user_preferences table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create contacts table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                name TEXT PRIMARY KEY,
                phone_number TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit() if is_sqlite else None
        return True
    except Exception as e:
        print(f"[JARVIS Error] DB initialization failed: {e}")
        return False

def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """
    Helper to execute an arbitrary query.
    """
    conn = get_connection()
    if not conn:
        return [] if fetch else False
    
    is_sqlite = str(type(conn)).find('sqlite3') != -1
    # Replace %s with ? for SQLite if needed
    if is_sqlite and params:
        query = query.replace('%s', '?')
        # SQLite doesn't support ILIKE
        query = query.replace('ILIKE', 'LIKE')
        
    try:
        # Use simple cursor for SQLite since row_factory is set
        cur = conn.cursor() if is_sqlite else conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params or ())
        if fetch:
            res = cur.fetchall()
            return res
        if is_sqlite:
            conn.commit()
        return True
    except Exception as e:
        print(f"[JARVIS Error] Query execution failed: {e}")
        return [] if fetch else False

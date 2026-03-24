"""
JARVIS — Memory Manager
High-level API for saving and retrieving conversation history.
"""

from memory.postgres_db import execute_query, init_db

# Try to initialize the database on import
_db_initialized = init_db()

def save_interaction(user_input: str, assistant_response: str) -> bool:
    """
    Save a turn of conversation to the database.
    """
    if not _db_initialized:
        return False
        
    query = '''
        INSERT INTO conversations (user_input, assistant_response)
        VALUES (%s, %s)
    '''
    return execute_query(query, (user_input, assistant_response), fetch=False)

def get_recent_history(limit: int = 5) -> list[str]:
    """
    Retrieve the most recent conversation turns as a formatted string list.
    """
    if not _db_initialized:
        return []
        
    query = '''
        SELECT user_input, assistant_response 
        FROM conversations 
        ORDER BY timestamp DESC 
        LIMIT %s
    '''
    
    results = execute_query(query, (limit,), fetch=True)
    if not results:
        return []
        
    # Results come back newest first due to ORDER BY, so we reverse it for chronological context
    history = []
    for row in reversed(results):
        history.append(f"User: {row['user_input']}")
        history.append(f"JARVIS: {row['assistant_response']}")
        
    return history

def search_memory(keyword: str, limit: int = 5) -> list[str]:
    """
    Super basic keyword search in past conversations.
    """
    if not _db_initialized:
        return []
        
    query = '''
        SELECT user_input, assistant_response, timestamp
        FROM conversations 
        WHERE user_input ILIKE %s OR assistant_response ILIKE %s
        ORDER BY timestamp DESC 
        LIMIT %s
    '''
    
    search_term = f"%{keyword}%"
    results = execute_query(query, (search_term, search_term, limit), fetch=True)
    
    history = []
    if results:
        for row in results: 
            date_str = row['timestamp'].strftime("%Y-%m-%d %H:%M")
            history.append(f"[{date_str}] User: {row['user_input']}\n[{date_str}] JARVIS: {row['assistant_response']}")
        
    return history

def store_preference(key: str, value: str):
    query = "INSERT INTO user_preferences (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP"
    execute_query(query, (key.lower(), value))

def get_preference(key: str):
    query = "SELECT value FROM user_preferences WHERE key = %s"
    res = execute_query(query, (key.lower(),), fetch=True)
    return res[0]['value'] if res else None

def store_contact(name: str, phone: str):
    query = "INSERT INTO contacts (name, phone_number) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET phone_number = EXCLUDED.phone_number, updated_at = CURRENT_TIMESTAMP"
    execute_query(query, (name.lower(), phone))

def get_contact_phone(name: str):
    query = "SELECT phone_number FROM contacts WHERE name = %s"
    res = execute_query(query, (name.lower(),), fetch=True)
    return res[0]['phone_number'] if res else None

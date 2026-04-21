"""
JARVIS — Memory Tool
Allows agents to store and retrieve user preferences and contacts.
"""

from memory import memory_manager

def manage_memory(action: str, key: str, value: str = None) -> str:
    """
    Store or retrieve information from memory.
    
    Args:
        action: 'store_pref', 'get_pref', 'store_contact', 'get_contact'
        key: The key or name to look up
        value: The value to store (required for 'store' actions)
        
    Returns:
        Status or retrieved value
    """
    try:
        if action == "store_pref":
            memory_manager.store_preference(key, value)
            return f"Stored preference: {key} = {value}"
            
        elif action == "get_pref":
            val = memory_manager.get_preference(key)
            return val if val else f"No preference found for '{key}'."
            
        elif action == "store_contact":
            memory_manager.store_contact(key, value)
            return f"Stored contact: {key} = {value}"
            
        elif action == "get_contact":
            val = memory_manager.get_contact_phone(key)
            return val if val else f"No contact found for '{key}'."
            
        else:
            return f"Error: Unknown memory action '{action}'."
            
    except Exception as e:
        return f"Memory tool error: {e}"


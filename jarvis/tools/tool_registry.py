"""
JARVIS — Tool Registry
Maps string tool names to actual Python functions.
"""

from jarvis.tools.search_tool import search_web
from jarvis.tools.file_tool import read_file, write_file
from jarvis.tools.system_tool import get_system_info, open_url
from jarvis.tools.whatsapp_tool import send_whatsapp_message
from jarvis.tools.memory_tool import manage_memory


def call_tool(tool_name: str, tool_input: str) -> str:
    """
    Dispatch a tool call to the appropriate function.
    """
    try:
        if tool_name == "search":
            return search_web(tool_input)
            
        elif tool_name == "whatsapp":
            # Expecting direct input or simple split if model sends multi-param
            # For simplicity, we assume model sends "number|message"
            if "|" in tool_input:
                parts = tool_input.split("|", 1)
                return send_whatsapp_message(parts[0].strip(), parts[1].strip())
            return "Error: WhatsApp tool requires input in 'number|message' format."

        elif tool_name == "read_file":
            return read_file(tool_input)
            
        elif tool_name == "write_file":
            return write_file(tool_input)
            
        elif tool_name == "system_info":
            return get_system_info(tool_input)
            
        elif tool_name == "open_url":
            return open_url(tool_input)
            
        elif tool_name == "memory":
            # Expecting "action|key|value"
            parts = tool_input.split("|")
            action = parts[0].strip()
            key = parts[1].strip() if len(parts) > 1 else ""
            value = parts[2].strip() if len(parts) > 2 else None
            return manage_memory(action, key, value)
            
        else:
            return f"Error: Tool '{tool_name}' not found."
            
    except Exception as e:
        return f"Error executing tool '{tool_name}': {e}"

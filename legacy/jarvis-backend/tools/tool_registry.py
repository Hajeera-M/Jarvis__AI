"""
JARVIS-X — Tool Registry
Central mapping of tool names to their execution functions.
"""

import json
from tools.web_search import search
from tools.file_system import read_file, write_file, list_files
from tools.browser_tool import open_url


async def execute_tool(tool_name: str, tool_input: str) -> str:
    """
    Execute a tool by name with the given input.
    
    Args:
        tool_name: Name of the tool to execute
        tool_input: Input string/JSON for the tool
    
    Returns:
        Tool result as a string
    """
    tool_name = tool_name.lower().strip()

    if tool_name == "search":
        return await search(tool_input)

    elif tool_name == "open_url":
        return await open_url(tool_input)

    elif tool_name == "read_file":
        return await read_file(tool_input)

    elif tool_name == "write_file":
        try:
            data = json.loads(tool_input)
            path = data.get("path", "output.txt")
            content = data.get("content", "")
            return await write_file(path, content)
        except json.JSONDecodeError:
            return "Error: write_file input must be JSON with 'path' and 'content' keys"

    elif tool_name == "list_files":
        return await list_files(tool_input or ".")

    else:
        return f"Unknown tool: {tool_name}"

"""
JARVIS — File System Tool
Provides basic file reading/writing sandboxed to a specific directory.
"""

import os
import json
from jarvis.config import SANDBOX_DIR

def _safe_path(filename: str) -> str:
    """Ensure the target path is inside the sandbox directory."""
    base_name = os.path.basename(filename)
    return os.path.join(SANDBOX_DIR, base_name)

def read_file(filename: str) -> str:
    """Read contents of a file in the sandbox."""
    if not filename:
        return "Error: No filename provided"
        
    path = _safe_path(filename)
    
    if not os.path.exists(path):
        return f"File not found: {filename}"
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"--- Content of {filename} ---\n{content}"
    except Exception as e:
        return f"Failed to read file: {e}"

def write_file(args_json: str) -> str:
    """
    Write content to a file in the sandbox.
    args_json should be a JSON string like: {"path": "file.txt", "content": "hello"}
    """
    try:
        args = json.loads(args_json)
        filename = args.get("path")
        content = args.get("content")
        
        if not filename or not content:
            return "Error: Missing path or content in JSON arguments."
            
        path = _safe_path(filename)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"Successfully wrote to {filename}"
    except json.JSONDecodeError:
        return "Error: Input must be a valid JSON string with 'path' and 'content' keys."
    except Exception as e:
        return f"Failed to write file: {e}"


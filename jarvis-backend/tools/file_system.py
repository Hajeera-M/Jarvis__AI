"""
JARVIS-X — File System Tool
Safe file operations within a sandboxed directory.
"""

import os
from config import SANDBOX_DIR


def _safe_path(path: str) -> str:
    """Ensure path is within the sandbox directory."""
    # Normalize and resolve the path within sandbox
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))
    if not full_path.startswith(os.path.normpath(SANDBOX_DIR)):
        raise PermissionError(f"Access denied: path must be within sandbox directory")
    return full_path


async def read_file(path: str) -> str:
    """Read a file from the sandbox directory."""
    safe = _safe_path(path)
    if not os.path.exists(safe):
        return f"File not found: {path}"
    
    try:
        with open(safe, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def write_file(path: str, content: str) -> str:
    """Write content to a file in the sandbox directory."""
    safe = _safe_path(path)
    
    try:
        os.makedirs(os.path.dirname(safe), exist_ok=True)
        with open(safe, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written successfully: {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


async def list_files(path: str = ".") -> str:
    """List files in a directory within the sandbox."""
    safe = _safe_path(path)
    
    if not os.path.exists(safe):
        return f"Directory not found: {path}"
    
    try:
        entries = os.listdir(safe)
        if not entries:
            return f"Directory is empty: {path}"
        
        formatted = []
        for entry in sorted(entries):
            full = os.path.join(safe, entry)
            entry_type = "📁" if os.path.isdir(full) else "📄"
            formatted.append(f"  {entry_type} {entry}")
        
        return f"Contents of {path}:\n" + "\n".join(formatted)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

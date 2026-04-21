"""
JARVIS — File Automation Service
Scans standard local user directories and executes file launching securely.
"""

import os
import platform
import subprocess

class FileAutomationService:
    @staticmethod
    def get_search_dirs() -> list:
        """Returns standard Windows user directories for fast scoped searching."""
        user_profile = os.environ.get('USERPROFILE', '')
        if not user_profile:
            return []
        
        return [
            os.path.join(user_profile, 'Desktop'),
            os.path.join(user_profile, 'Documents'),
            os.path.join(user_profile, 'Downloads')
        ]

    @staticmethod
    def open_system_folder(folder_name: str) -> str:
        name = folder_name.lower()
        user_profile = os.environ.get('USERPROFILE', '')
        
        known_folders = {
            "desktop": os.path.join(user_profile, 'Desktop'),
            "documents": os.path.join(user_profile, 'Documents'),
            "downloads": os.path.join(user_profile, 'Downloads'),
            "jarvis": os.getcwd()  # The project root
        }
        
        path = known_folders.get(name)
        if path and os.path.exists(path):
            os.startfile(path)
            return f"Opened {folder_name.title()} folder."
            
        return f"Could not locate the system folder {folder_name}."

    @staticmethod
    def search_and_open(filename: str) -> str:
        """Deep search across standard directories and launch the first match."""
        target = filename.lower()
        search_dirs = FileAutomationService.get_search_dirs()
        search_dirs.append(os.getcwd()) # Include project directory
        
        for root_dir in search_dirs:
            if not os.path.exists(root_dir):
                continue
                
            for dirpath, _, filenames in os.walk(root_dir):
                for f in filenames:
                    # Partial matching: "synopsis" matches "Project_Synopsis.pdf"
                    if target in f.lower():
                        full_path = os.path.join(dirpath, f)
                        try:
                            os.startfile(full_path)
                            return f"Opened file: {f}"
                        except Exception as e:
                            return f"Found {f} but failed to open it. {str(e)}"
                            
                # Check folder names too
                dirname = os.path.basename(dirpath).lower()
                if target == dirname:
                    try:
                        os.startfile(dirpath)
                        return f"Opened folder: {os.path.basename(dirpath)}"
                    except:
                        pass
                        
        return f"Sorry, I couldn't find any file or folder conceptually matching '{filename}'."

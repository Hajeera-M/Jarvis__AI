"""
JARVIS — Browser Tool
Opens URLs in the default system browser.
"""

import webbrowser


async def open_url(url: str) -> str:
    """
    Open a URL in the user's default browser.
    
    Args:
        url: The URL to open
    
    Returns:
        Confirmation message
    """
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        webbrowser.open(url)
        return f"Opened {url} in browser"
    except Exception as e:
        return f"Failed to open URL: {str(e)}"


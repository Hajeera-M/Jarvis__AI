"""
JARVIS — Browser Service
Autonomous web navigation and interaction via Playwright.
"""

import os
import asyncio
import logging
from playwright.async_api import async_playwright

logger = logging.getLogger("JARVIS")

class BrowserService:
    @staticmethod
    async def browse_and_summarize(url: str, task: str = "Summarize this page") -> str:
        """Navigates to a URL and performs a task autonomously."""
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                logger.info(f"Navigating to {url}...")
                await page.goto(url, wait_until="networkidle")
                
                # Basic task: Extract text
                content = await page.content()
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                
                await browser.close()
                return f"I visited {url}. Here is what I found: {text[:1000]}..."
            except Exception as e:
                logger.error(f"Browser Task Failed: {e}")
                return f"I tried to visit {url} but encountered an error: {str(e)}"

    @staticmethod
    async def perform_action(url: str, action_description: str) -> str:
        """
        Future implementation: Use LLM to generate playwright commands 
        to click/type based on the page state.
        """
        return "Autonomous web actions (clicking/typing) are initialized but require higher-tier reasoning to execute safely."

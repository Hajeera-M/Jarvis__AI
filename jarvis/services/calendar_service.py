"""
JARVIS — Calendar Service
Manages tasks and events for the user.
"""

import os
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("JARVIS")

CALENDAR_FILE = os.path.join(os.getcwd(), "data", "calendar.json")

class CalendarService:
    @staticmethod
    def _load_calendar():
        if not os.path.exists(CALENDAR_FILE):
            return {"events": []}
        try:
            with open(CALENDAR_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"events": []}

    @staticmethod
    def _save_calendar(data):
        os.makedirs(os.path.dirname(CALENDAR_FILE), exist_ok=True)
        with open(CALENDAR_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def add_event(title: str, date_str: str, time_str: str = "09:00"):
        """Adds an event to the calendar."""
        data = CalendarService._load_calendar()
        event = {
            "title": title,
            "date": date_str,
            "time": time_str,
            "created_at": datetime.now().isoformat()
        }
        data["events"].append(event)
        CalendarService._save_calendar(data)
        return f"Successfully added '{title}' to your calendar for {date_str} at {time_str}."

    @staticmethod
    def get_upcoming_events(days: int = 7):
        """Retrieves events for the next N days."""
        data = CalendarService._load_calendar()
        now = datetime.now()
        upcoming = []
        
        for event in data["events"]:
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                if now <= event_date <= now + timedelta(days=days):
                    upcoming.append(event)
            except:
                continue
        
        if not upcoming:
            return "You have no upcoming events for the next week."
        
        resp = "Here are your upcoming events:\n"
        for e in sorted(upcoming, key=lambda x: x["date"]):
            resp += f"- {e['date']} {e['time']}: {e['title']}\n"
        return resp

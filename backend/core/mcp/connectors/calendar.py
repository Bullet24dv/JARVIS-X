from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
from datetime import datetime, timezone
from typing import List, Dict
from loguru import logger

class CalendarConnector:
    def __init__(self):
        self.service = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("GOOGLE_CLIENT_ID"))
        
    async def connect(self):
        creds = None
        if os.path.exists("token_calendar.json"):
            creds = Credentials.from_authorized_user_file("token_calendar.json")
        if not creds or not creds.valid:
            logger.warning("Calendar requires OAuth, skipping")
            return
        self.service = build("calendar", "v3", credentials=creds)
        logger.info("Calendar connector initialized")
        
    async def get_events(self, max_results: int = 10) -> List[Dict]:
        if not self.service:
            return []
        now = datetime.now(timezone.utc).isoformat()
        events_result = self.service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
        
    async def create_event(self, summary: str, start: str, end: str) -> Dict:
        if not self.service:
            return {}
        event = {
            'summary': summary,
            'start': {'dateTime': start, 'timeZone': 'America/Santiago'},
            'end': {'dateTime': end, 'timeZone': 'America/Santiago'},
        }
        return self.service.events().insert(calendarId='primary', body=event).execute()
        
    async def disconnect(self):
        pass
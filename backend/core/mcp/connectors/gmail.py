import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64
from loguru import logger

class GmailConnector:
    def __init__(self):
        self.service = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("GOOGLE_CLIENT_ID"))
        
    async def connect(self):
        creds = None
        if os.path.exists("token_gmail.json"):
            creds = Credentials.from_authorized_user_file("token_gmail.json")
        if not creds or not creds.valid:
            logger.warning("Gmail requires OAuth, skipping")
            return
        self.service = build("gmail", "v1", credentials=creds)
        logger.info("Gmail connector initialized")
        
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        if not self.service:
            return False
        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["Subject"] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        try:
            self.service.users().messages().send(userId="me", body=create_message).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
            
    async def list_inbox(self, max_results: int = 10) -> list:
        if not self.service:
            return []
        results = self.service.users().messages().list(userId="me", maxResults=max_results).execute()
        return results.get('messages', [])
        
    async def disconnect(self):
        pass
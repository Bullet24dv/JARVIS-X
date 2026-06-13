from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from loguru import logger

class GoogleDriveConnector:
    def __init__(self):
        self.service = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("GOOGLE_CLIENT_ID"))
        
    async def connect(self):
        creds = None
        if os.path.exists("token_drive.json"):
            creds = Credentials.from_authorized_user_file("token_drive.json")
        if not creds or not creds.valid:
            logger.warning("Google Drive requires OAuth, skipping")
            return
        self.service = build("drive", "v3", credentials=creds)
        logger.info("Google Drive connector initialized")
        
    async def upload_file(self, file_path: str, mime_type: str = None) -> str:
        if not self.service:
            return ""
        file_name = os.path.basename(file_path)
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file_metadata = {'name': file_name}
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
        
    async def list_files(self, page_size: int = 10) -> list:
        if not self.service:
            return []
        results = self.service.files().list(pageSize=page_size, fields="files(id, name)").execute()
        return results.get('files', [])
        
    async def disconnect(self):
        pass
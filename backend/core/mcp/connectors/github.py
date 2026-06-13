import os
from github import Github, GithubException
from typing import List, Dict, Any
from loguru import logger

class GitHubConnector:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.client = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("GITHUB_TOKEN"))
        
    async def connect(self):
        if self.token:
            self.client = Github(self.token)
            logger.info("GitHub connector initialized")
        
    async def get_repo(self, repo_name: str):
        return self.client.get_repo(repo_name)
        
    async def create_issue(self, repo_name: str, title: str, body: str) -> Dict:
        if not self.client:
            return {"error": "GitHub not configured"}
        repo = self.client.get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body)
        return {"number": issue.number, "url": issue.html_url}
        
    async def disconnect(self):
        pass
import aiofiles
import os
import shutil
from pathlib import Path
from typing import List, Dict
from loguru import logger

class LocalFSConnector:
    def __init__(self):
        self.base_path = Path.home() / "JARVIS_DATA"
        self.base_path.mkdir(exist_ok=True)
        
    async def connect(self):
        logger.info("LocalFS connector ready")
        
    async def list_directory(self, path: str = ".") -> List[Dict]:
        full_path = self.base_path / path
        items = []
        for item in full_path.iterdir():
            items.append({
                "name": item.name,
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else 0,
                "modified": item.stat().st_mtime
            })
        return items
        
    async def read_file(self, file_path: str) -> str:
        full_path = self.base_path / file_path
        async with aiofiles.open(full_path, "r", encoding="utf-8") as f:
            return await f.read()
            
    async def write_file(self, file_path: str, content: str):
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(full_path, "w", encoding="utf-8") as f:
            await f.write(content)
            
    async def delete_file(self, file_path: str):
        full_path = self.base_path / file_path
        if full_path.exists():
            if full_path.is_file():
                full_path.unlink()
            else:
                shutil.rmtree(full_path)
                
    async def move_file(self, source: str, dest: str):
        src_path = self.base_path / source
        dst_path = self.base_path / dest
        shutil.move(str(src_path), str(dst_path))
        
    async def disconnect(self):
        pass
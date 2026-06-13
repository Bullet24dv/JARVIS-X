import os
import shutil
import aiofiles
from pathlib import Path
from typing import List, Dict

class FileManager:
    @staticmethod
    async def list_directory(path: str) -> List[Dict]:
        items = []
        for item in Path(path).iterdir():
            items.append({
                "name": item.name,
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else 0,
                "modified": item.stat().st_mtime
            })
        return items
        
    @staticmethod
    async def read_file(file_path: str) -> str:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            return await f.read()
            
    @staticmethod
    async def write_file(file_path: str, content: str):
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(content)
            
    @staticmethod
    async def delete_file(file_path: str):
        path = Path(file_path)
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
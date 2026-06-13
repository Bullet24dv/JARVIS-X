import sqlite3
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
import os
from loguru import logger

DB_PATH = os.getenv("DATABASE_PATH", "jarvis.db")

class AsyncSQLiteWrapper:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
    
    def _get_conn(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    class Collection:
        def __init__(self, conn, name: str):
            self.conn = conn
            self.name = name
            self._ensure_table()
        
        def _ensure_table(self):
            cursor = self.conn.cursor()
            if self.name == "users":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT,
                        name TEXT,
                        email TEXT,
                        created_at TIMESTAMP,
                        updated_at TIMESTAMP
                    )
                ''')
            elif self.name == "conversations":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        role TEXT,
                        content TEXT,
                        timestamp TIMESTAMP,
                        metadata TEXT
                    )
                ''')
            elif self.name == "memories":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        text TEXT,
                        memory_type TEXT,
                        metadata TEXT,
                        timestamp TIMESTAMP,
                        access_count INTEGER DEFAULT 0
                    )
                ''')
            elif self.name == "tasks":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_data TEXT,
                        status TEXT,
                        created_at TIMESTAMP
                    )
                ''')
            elif self.name == "agents":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS agents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        capabilities TEXT,
                        status TEXT,
                        last_active TIMESTAMP,
                        created_at TIMESTAMP
                    )
                ''')
            self.conn.commit()
        
        async def find_one(self, filter: Dict) -> Optional[Dict]:
            cursor = self.conn.cursor()
            if "username" in filter:
                cursor.execute(f"SELECT * FROM {self.name} WHERE username = ?", (filter["username"],))
            elif "_id" in filter:
                cursor.execute(f"SELECT * FROM {self.name} WHERE id = ?", (filter["_id"],))
            else:
                return None
            row = cursor.fetchone()
            return dict(row) if row else None
        
        async def insert_one(self, document: Dict) -> Any:
            cursor = self.conn.cursor()
            columns = ", ".join(document.keys())
            placeholders = ", ".join(["?" for _ in document])
            cursor.execute(
                f"INSERT INTO {self.name} ({columns}) VALUES ({placeholders})",
                list(document.values())
            )
            self.conn.commit()
            return cursor.lastrowid
        
        async def find(self, filter: Dict = None) -> List[Dict]:
            cursor = self.conn.cursor()
            if filter:
                conditions = " AND ".join([f"{k} = ?" for k in filter.keys()])
                cursor.execute(f"SELECT * FROM {self.name} WHERE {conditions}", list(filter.values()))
            else:
                cursor.execute(f"SELECT * FROM {self.name}")
            return [dict(row) for row in cursor.fetchall()]
    
    def __getattr__(self, name):
        return self.Collection(self._get_conn(), name)

db = None

async def init_db() -> None:
    global db
    db = AsyncSQLiteWrapper(DB_PATH)
    logger.info(f"SQLite database initialized at {DB_PATH}")

async def get_db():
    return db
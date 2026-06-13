import asyncpg
import os
from typing import List, Dict
from loguru import logger

class PostgreSQLConnector:
    def __init__(self):
        self.pool = None
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = int(os.getenv("POSTGRES_PORT", 5432))
        self.user = os.getenv("POSTGRES_USER", "jarvis")
        self.password = os.getenv("POSTGRES_PASSWORD", "securepassword")
        self.database = os.getenv("POSTGRES_DB", "jarvis")
        self.dsn = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        
    @classmethod
    def is_available(cls):
        return True
        
    async def connect(self):
        try:
            logger.info(f"Connecting to PostgreSQL at {self.host}:{self.port}...")
            self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=5, timeout=30)
            # Verificar conexión
            async with self.pool.acquire() as conn:
                await conn.execute("SELECT 1")
            logger.info("PostgreSQL connected successfully")
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            raise
        
    async def query(self, sql: str, *args) -> List[Dict]:
        if not self.pool:
            raise Exception("PostgreSQL not connected")
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *args)
            return [dict(row) for row in rows]
        
    async def execute(self, sql: str, *args) -> str:
        if not self.pool:
            raise Exception("PostgreSQL not connected")
        async with self.pool.acquire() as conn:
            return await conn.execute(sql, *args)
        
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL disconnected")
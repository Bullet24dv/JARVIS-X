import aiomysql
import os
from typing import List, Dict, Any
from loguru import logger

class MySQLConnector:
    def __init__(self):
        self.pool = None
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", 3306))
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.db = os.getenv("MYSQL_DB", "jarvis")
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("MYSQL_HOST"))
        
    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host, port=self.port,
            user=self.user, password=self.password,
            db=self.db, minsize=1, maxsize=5
        )
        logger.info("MySQL connector initialized")
        
    async def query(self, sql: str, args: tuple = None) -> List[Dict]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, args)
                return await cur.fetchall()
                
    async def disconnect(self):
        self.pool.close()
        await self.pool.wait_closed()
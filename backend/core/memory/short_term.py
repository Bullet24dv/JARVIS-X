from collections import deque
from typing import List, Dict, Any
from datetime import datetime, timedelta

class ShortTermMemory:
    """Memoria de corto plazo (contexto inmediato)"""
    
    def __init__(self, max_size: int = 20, ttl_seconds: int = 300):
        self.buffer = deque(maxlen=max_size)
        self.ttl = ttl_seconds
        
    def add(self, item: Dict[str, Any]):
        item["timestamp"] = datetime.utcnow()
        self.buffer.append(item)
        
    def get_recent(self, limit: int = 10) -> List[Dict]:
        now = datetime.utcnow()
        recent = []
        for item in reversed(self.buffer):
            if (now - item["timestamp"]).total_seconds() < self.ttl:
                recent.append(item)
            if len(recent) >= limit:
                break
        return recent
        
    def clear(self):
        self.buffer.clear()
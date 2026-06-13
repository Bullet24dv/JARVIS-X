import pytest
from backend.core.memory.short_term import ShortTermMemory

def test_short_term_memory():
    mem = ShortTermMemory(max_size=2)
    mem.add({"text": "hello"})
    mem.add({"text": "world"})
    assert len(mem.get_recent()) == 2
    mem.add({"text": "third"})
    assert len(mem.get_recent()) == 2
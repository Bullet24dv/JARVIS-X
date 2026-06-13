import pytest
from backend.core.agents.programmer import ProgrammerAgent

@pytest.mark.asyncio
async def test_programmer():
    agent = ProgrammerAgent("Test", "Developer", None, None)
    result = await agent.process({"action": "analyze_repo", "repo_path": "."})
    assert "files" in result
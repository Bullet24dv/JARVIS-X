"""Agents module for distributed execution"""
from .agent_manager import AgentManager
from .agent_runners import run_programmer_agent, run_researcher_agent

__all__ = ["AgentManager", "run_programmer_agent", "run_researcher_agent"]
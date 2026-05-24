#!/usr/bin/env python3
"""
Coding Agents - Multi-Agent Project Builder

Build complete projects from prompts using specialized agents for:
- Planning & Architecture
- Frontend Development
- Backend Development
- Database Design
- DevOps Setup

Usage:
    python main.py
    
Environment Variables:
    LLM_MODEL       - Model to use (default: gpt-4o)
    LLM_API_KEY     - API key for LLM
    LLM_BASE_URL    - Base URL for LLM API (optional)
    WORKSPACE_DIR   - Directory for generated projects
"""

from orchestrator import OrchestratorAgent
from config import CodingAgentsConfig


def main():
    """Main entry point."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗   ║
║   ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║   ║
║   ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║   ║
║   ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║   ║
║   ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║   ║
║   ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝   ║
║                                                           ║
║   Multi-Agent Project Builder                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    config = CodingAgentsConfig.from_env()
    orchestrator = OrchestratorAgent(config)
    orchestrator.start()


if __name__ == "__main__":
    main()
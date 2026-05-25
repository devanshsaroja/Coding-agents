"""
Backend Agent - Builds server-side logic and APIs.
"""

from pathlib import Path
from typing import Dict, Any
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

from config import CodingAgentsConfig
from utils import Colors


class BackendAgent:
    """Agent responsible for building backend services."""
    
    def __init__(self, config: CodingAgentsConfig):
        self.config = config
        llm_config = config.llm
        
        self.llm = LLM(
            model=llm_config.model,
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
        )
        
        self.agent = Agent(
            llm=self.llm,
            tools=[
                Tool(name=FileEditorTool.name),
                Tool(name=TerminalTool.name),
            ],
        )
        
    def build(self, architecture: Dict[str, Any], project_dir: Path):
        """Build backend based on architecture spec."""
        backend_stack = architecture.get("stack", {}).get("backend", "fastapi")
        components = [c for c in architecture.get("components", []) 
                      if c.get("layer") in ["backend", "server", "api", None]]
        api_endpoints = architecture.get("api", [])
        
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        build_prompt = f"""You are the Backend Agent. Build the server-side logic for this project.

Backend Stack: {backend_stack}
Project Name: {architecture.get('name', 'project')}
Description: {architecture.get('description', '')}

Components to build:
{self._format_components(components)}

API Endpoints to implement:
{self._format_api(api_endpoints)}

Tasks:
1. Set up backend project structure
2. Create requirements.txt or pyproject.toml
3. Implement all API endpoints
4. Add business logic layer
5. Create data models/schemas
6. Implement authentication if needed
7. Add error handling and validation

Project directory: {project_dir}

Create actual working code. Do not use placeholders or TODO comments.
Generate complete, production-ready backend code."""
        
        conversation.send_message(build_prompt)
        conversation.run()
        
        print(f"  {Colors.success('✓')} Backend build complete")
        
    def _format_components(self, components: list) -> str:
        """Format component list for prompt."""
        if not components:
            return "No specific components - create a basic API structure"
        lines = []
        for c in components:
            lines.append(f"- {c.get('name')}: {c.get('description', '')}")
        return "\n".join(lines)
        
    def _format_api(self, endpoints: list) -> str:
        """Format API endpoints for prompt."""
        if not endpoints:
            return "No specific endpoints - create RESTful CRUD endpoints"
        lines = []
        for e in endpoints:
            method = e.get("method", "GET")
            path = e.get("path", "/")
            desc = e.get("description", "")
            lines.append(f"- {method} {path}: {desc}")
        return "\n".join(lines)
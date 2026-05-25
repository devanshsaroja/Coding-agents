"""
Frontend Agent - Builds user interface components.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

from config import CodingAgentsConfig
from utils import Colors


class FrontendAgent:
    """Agent responsible for building frontend components."""
    
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
        """Build frontend based on architecture spec."""
        frontend_stack = architecture.get("stack", {}).get("frontend", "react")
        components = [c for c in architecture.get("components", []) 
                      if c.get("layer") in ["frontend", "ui", "client", None]]
        
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        build_prompt = f"""You are the Frontend Agent. Build the user interface for this project.

Frontend Stack: {frontend_stack}
Project Name: {architecture.get('name', 'project')}
Description: {architecture.get('description', '')}

Components to build:
{self._format_components(components)}

Tasks:
1. Set up frontend project structure (src/, components/, pages/, etc.)
2. Create package.json with all dependencies
3. Build all UI components with proper TypeScript/JavaScript
4. Set up routing (React Router, Vue Router, etc.)
5. Create API service layer for backend communication
6. Add styling (CSS/SCSS/Tailwind/styled-components)
7. Create App entry point

Project directory: {project_dir}

Create actual working code. Do not use placeholders or TODO comments.
Generate complete, production-ready frontend code."""
        
        conversation.send_message(build_prompt)
        conversation.run()
        
        print(f"  {Colors.success('✓')} Frontend build complete")
        
    def _format_components(self, components: list) -> str:
        """Format component list for prompt."""
        if not components:
            return "No specific components - create a basic project structure"
        lines = []
        for c in components:
            lines.append(f"- {c.get('name')}: {c.get('description', '')}")
        return "\n".join(lines)
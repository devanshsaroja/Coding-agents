"""
DevOps Agent - Sets up infrastructure and deployment.
"""

from pathlib import Path
from typing import Dict, Any
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

from config import CodingAgentsConfig
from utils import Colors


class DevOpsAgent:
    """Agent responsible for deployment and infrastructure."""
    
    def __init__(self, config: CodingAgentsConfig):
        self.config = config
        self.llm = LLM(
            model=config.llm.model,
            api_key=config.llm.api_key,
            base_url=config.llm.base_url,
        )
        self.agent = Agent(
            llm=self.llm,
            tools=[
                Tool(name=FileEditorTool.name),
                Tool(name=TerminalTool.name),
            ],
        )
        
    def build(self, architecture: Dict[str, Any], project_dir: Path):
        """Build DevOps configuration based on architecture spec."""
        frontend = architecture.get("stack", {}).get("frontend", "react")
        backend = architecture.get("stack", {}).get("backend", "fastapi")
        database = architecture.get("stack", {}).get("database", "postgresql")
        
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        build_prompt = f"""You are the DevOps Agent. Set up infrastructure and deployment for this project.

Stack:
- Frontend: {frontend}
- Backend: {backend}
- Database: {database}

Project Name: {architecture.get('name', 'project')}

Tasks:
1. Create Docker Compose file with all services
2. Create Dockerfile(s) for each component
3. Set up environment variables (.env.example)
4. Create docker-compose.yml with proper networking
5. Add nginx configuration for reverse proxy (optional)
6. Create CI/CD configuration (.github/workflows/, .gitlab-ci.yml)
7. Add README with setup instructions

Project directory: {project_dir}

Create actual working configurations. Do not use placeholders.
Include proper health checks, restart policies, and resource limits."""
        
        conversation.send_message(build_prompt)
        conversation.run()
        
        print(f"  {Colors.success('✓')} DevOps setup complete")
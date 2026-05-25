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
        """Build DevOps configuration (optional, for Docker deployments)."""
        frontend = architecture.get("stack", {}).get("frontend", "react")
        backend = architecture.get("stack", {}).get("backend", "fastapi")
        database = architecture.get("stack", {}).get("database", "postgresql")
        
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        build_prompt = f"""You are the DevOps Agent. Create deployment files (OPTIONAL - Docker is not required to run this project).

Stack:
- Frontend: {frontend}
- Backend: {backend}
- Database: {database}

Project Name: {architecture.get('name', 'project')}

Create these files ONLY IF user wants Docker deployment:
1. docker-compose.yml - For running with Docker (optional)
2. Dockerfile - For containerizing (optional)
3. .env.example - Environment variables template

IMPORTANT: This project can run WITHOUT Docker. Create a README.md in the project root 
with clear instructions for running directly without Docker:

```markdown
# Running Without Docker

## Backend Setup
1. cd backend
2. python -m venv venv
3. source venv/bin/activate  # Windows: venv\Scripts\activate
4. pip install -r requirements.txt
5. Set DATABASE_URL in .env or environment
6. uvicorn main:app --reload --port 8000

## Frontend Setup
1. cd frontend
2. npm install
3. npm run dev

## Database
- SQLite: Works out of the box (for development)
- PostgreSQL: Install locally and run `createdb myproject`
- MongoDB: Install locally and run `mongod`
```

Project directory: {project_dir}"""
        
        conversation.send_message(build_prompt)
        conversation.run()
        
        print(f"  {Colors.success('✓')} DevOps setup complete (includes non-Docker instructions)")
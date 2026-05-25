"""
Database Agent - Designs and creates database layer.
"""

from pathlib import Path
from typing import Dict, Any, List
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

from config import CodingAgentsConfig
from utils import Colors


class DatabaseAgent:
    """Agent responsible for database schema and migrations."""
    
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
        """Build database layer based on architecture spec."""
        db_stack = architecture.get("stack", {}).get("database", "postgresql")
        db_schema = architecture.get("database", {})
        tables = db_schema.get("tables", [])
        
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        build_prompt = f"""You are the Database Agent. Set up the database layer for this project.

Database: {db_stack}
Project Name: {architecture.get('name', 'project')}

Tables to create:
{self._format_tables(tables)}

Tasks:
1. Set up database configuration
2. Create migration files
3. Define table schemas with proper fields and relationships
4. Add indexes for performance
5. Create seed data if needed
6. Set up ORM models/schemas

For SQL databases (PostgreSQL, MySQL, SQLite):
- Create SQL migration files (.sql)
- Include CREATE TABLE statements
- Add proper foreign keys and indexes

For NoSQL (MongoDB):
- Create schema definitions
- Set up collections structure

Project directory: {project_dir}

Create actual working database code. Do not use placeholders."""
        
        conversation.send_message(build_prompt)
        conversation.run()
        
        print(f"  {Colors.success('✓')} Database layer complete")
        
    def _format_tables(self, tables: list) -> str:
        """Format table list for prompt."""
        if not tables:
            return "No specific tables - create basic user/content tables"
        lines = []
        for t in tables:
            name = t.get("name", "unknown")
            fields = t.get("fields", [])
            lines.append(f"\nTable: {name}")
            for f in fields:
                fname = f.get("name", "field")
                ftype = f.get("type", "TEXT")
                lines.append(f"  - {fname}: {ftype}")
        return "\n".join(lines)
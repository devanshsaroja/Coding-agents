"""
Orchestrator Agent - Coordinates the entire coding agent workflow.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

from config import CodingAgentsConfig, LLMConfig
from utils import Colors, sanitize_project_name, ensure_directory, save_architecture


class OrchestratorAgent:
    """Main orchestrator that coordinates the multi-agent workflow."""
    
    def __init__(self, config: Optional[CodingAgentsConfig] = None):
        self.config = config or CodingAgentsConfig.from_env()
        self.llm = LLM(
            model=self.config.llm.model,
            api_key=self.config.llm.api_key,
            base_url=self.config.llm.base_url,
        )
        self.agent = Agent(
            llm=self.llm,
            tools=[
                Tool(name=FileEditorTool.name),
                Tool(name=TerminalTool.name),
            ],
        )
        self.workspace = Path(ensure_directory(Path(self.config.project.workspace_dir)))
        
    def start(self):
        """Start the orchestrator CLI."""
        print(Colors.bold("\n🧙 Welcome to Coding Agents!\n"))
        print("Describe the project you want to build...\n")
        
        prompt = input("📝 Your project idea: ").strip()
        if not prompt:
            print(Colors.error("Please provide a project description."))
            return
        
        self.run_workflow(prompt)
        
    def run_workflow(self, prompt: str):
        """Run the complete workflow from prompt to running project."""
        project_name = sanitize_project_name(prompt)
        project_dir = self.workspace / project_name
        
        print(f"\n{Colors.info('📁 Project directory:')} {project_dir}\n")
        
        # Step 1: Create Architecture Plan
        print(Colors.bold("🔨 Step 1: Creating Architecture Plan..."))
        architecture = self._create_architecture(prompt, project_dir)
        
        # Step 2: Review and Iterate
        approved = self._review_loop(architecture, project_dir)
        
        if not approved:
            print(Colors.warning("\n⏸️ Project setup cancelled."))
            return
            
        # Step 3: Build with Agents
        print(Colors.bold("\n🚀 Step 2: Building Project..."))
        self._build_project(architecture, project_dir)
        
        # Step 4: Run Project
        print(Colors.bold("\n🎉 Step 3: Starting Project..."))
        self._run_project(architecture, project_dir)
        
    def _create_architecture(self, prompt: str, project_dir: Path) -> Dict[str, Any]:
        """Use the orchestrator agent to create architecture plan."""
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        arch_prompt = f"""You are the Architect Agent. Create a comprehensive architecture plan for this project:

Project Description: {prompt}

Create a detailed architecture document with:
1. **Project Overview** - Name, type, core features
2. **Tech Stack** - Frontend, Backend, Database choices
3. **Project Structure** - Full directory tree
4. **Component Specifications** - For each component:
   - Purpose
   - Props/Parameters
   - Dependencies
   - API endpoints (if applicable)
5. **Database Schema** - Tables, relationships, fields
6. **API Design** - Endpoints, request/response formats
7. **Implementation Order** - Phased approach

Format as a structured JSON document with these keys:
- name
- description
- stack (frontend, backend, database)
- structure (nested directory tree)
- components (list of component specs)
- database (schema info)
- api (endpoints list)
- phases (implementation order)

Save this as ARCHITECTURE.json in {project_dir}"""
        
        conversation.send_message(arch_prompt)
        conversation.run()
        
        # Load the created architecture
        arch_file = project_dir / "ARCHITECTURE.json"
        if arch_file.exists():
            import json
            with open(arch_file) as f:
                return json.load(f)
        return {"name": "project", "description": prompt, "components": []}
        
    def _review_loop(self, architecture: Dict[str, Any], project_dir: Path) -> bool:
        """Review architecture and allow modifications."""
        print(Colors.bold("\n📋 Architecture Plan Created!\n"))
        self._print_architecture(architecture)
        
        while True:
            print("\n" + "="*50)
            response = input(
                f"{Colors.bold('Actions:')}\n"
                f"  {Colors.info('[1]')} Proceed to build\n"
                f"  {Colors.info('[2]')} Request changes\n"
                f"  {Colors.info('[3]')} Show full details\n"
                f"  {Colors.info('[q]')} Quit\n"
                f"Choice: "
            ).strip().lower()
            
            if response == "1":
                return True
            elif response == "2":
                self._request_changes(architecture, project_dir)
            elif response == "3":
                self._print_architecture(architecture, detailed=True)
            elif response == "q":
                return False
                
    def _request_changes(self, architecture: Dict[str, Any], project_dir: Path):
        """Handle user change requests."""
        print("\n" + Colors.bold("✏️ What would you like to change?"))
        print("Examples:")
        print("  - 'Use Vue.js instead of React'")
        print("  - 'Add user authentication'")
        print("  - 'Change database to MongoDB'")
        print("  - 'Add admin panel'")
        print()
        
        changes = input("Your changes: ").strip()
        if not changes:
            return
            
        print(f"\n{Colors.info('🔄 Updating architecture...')}")
        
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        update_prompt = f"""Update the ARCHITECTURE.json file based on these change requests:

{changes}

Current architecture is in ARCHITECTURE.json. Modify it to incorporate the changes
while maintaining the overall structure. Save the updated version."""
        
        conversation.send_message(update_prompt)
        conversation.run()
        
        # Reload architecture
        arch_file = project_dir / "ARCHITECTURE.json"
        if arch_file.exists():
            import json
            with open(arch_file) as f:
                architecture.clear()
                architecture.update(json.load(f))
        
        print(Colors.success("✅ Architecture updated!"))
        self._print_architecture(architecture)
        
    def _build_project(self, architecture: Dict[str, Any], project_dir: Path):
        """Build project using specialized agents."""
        from agents.frontend import FrontendAgent
        from agents.backend import BackendAgent
        from agents.database import DatabaseAgent
        from agents.devops import DevOpsAgent
        
        print("\n🎯 Launching build agents...\n")
        
        # Create specialized agents
        frontend = FrontendAgent(self.config)
        backend = BackendAgent(self.config)
        database = DatabaseAgent(self.config)
        devops = DevOpsAgent(self.config)
        
        # Phase 1: Database first
        print(Colors.info("📊 Building Database Layer..."))
        database.build(architecture, project_dir)
        
        # Phase 2: Backend
        print(Colors.info("⚙️ Building Backend..."))
        backend.build(architecture, project_dir)
        
        # Phase 3: Frontend
        print(Colors.info("🎨 Building Frontend..."))
        frontend.build(architecture, project_dir)
        
        # Phase 4: DevOps
        print(Colors.info("🚢 Setting up DevOps..."))
        devops.build(architecture, project_dir)
        
        print(Colors.success("\n✅ All agents completed!"))
        
    def _run_project(self, architecture: Dict[str, Any], project_dir: Path):
        """Start the built project without Docker."""
        stack = architecture.get("stack", {})
        frontend = stack.get("frontend", "react")
        backend = stack.get("backend", "fastapi")
        database = stack.get("database", "postgresql")
        
        print(f"\n{Colors.bold('🎬 Starting the project (no Docker)...')}\n")
        
        cwd = str(project_dir)
        conversation = Conversation(agent=self.agent, workspace=cwd)
        
        run_prompt = f"""The project has been built! Here are instructions to run it WITHOUT Docker:

FOR {backend.upper()} BACKEND:
1. Create virtual environment: python -m venv venv
2. Activate: source venv/bin/activate  (Linux/Mac) or venv\\Scripts\\activate (Windows)
3. Install dependencies: pip install -r requirements.txt
4. Setup database: 
   - PostgreSQL: createdb myproject or use DATABASE_URL env var
   - SQLite: already included, no setup needed
   - MongoDB: ensure mongod is running
5. Run migrations if any: python manage.py migrate OR alembic upgrade head
6. Start server:
   - FastAPI: uvicorn main:app --reload --port 8000
   - Django: python manage.py runserver 0.0.0.0:8000
   - Express: npm install && npm start (port 3000)
   - NestJS: npm install && npm run start:dev

FOR {frontend.upper()} FRONTEND:
1. cd into frontend folder: cd frontend OR cd client
2. npm install
3. npm run dev OR npm start

STARTING BOTH:
- Open two terminal windows
- Terminal 1: Start backend first
- Terminal 2: Start frontend

IMPORTANT: Set environment variables first!
  - DATABASE_URL (your database connection string)
  - API_URL (backend URL, e.g., http://localhost:8000)
  - SECRET_KEY (for authentication)

Do NOT use docker-compose. Install and run everything directly on your machine.
If backend needs CORS setup for frontend, update the CORS middleware config.
Print clear instructions for starting both frontend and backend."""
        
        conversation.send_message(run_prompt)
        conversation.run()
        
        print(Colors.success("\n✅ Instructions provided!"))
        print(f"\nCheck {project_dir} for the generated code.")
        print("\nTo run without Docker:")
        print(f"  1. Backend: cd {project_dir} && pip install -r requirements.txt && uvicorn main:app --reload")
        print(f"  2. Frontend: cd {project_dir}/frontend && npm install && npm run dev")
        
    def _print_architecture(self, architecture: Dict[str, Any], detailed: bool = False):
        """Print architecture summary."""
        print(Colors.bold("\n📐 Architecture Summary"))
        print("="*50)
        print(f"{Colors.info('Name:')} {architecture.get('name', 'Unnamed')}")
        print(f"{Colors.info('Description:')} {architecture.get('description', '')}")
        
        stack = architecture.get("stack", {})
        if stack:
            print(f"\n{Colors.bold('Tech Stack:')}")
            print(f"  Frontend: {stack.get('frontend', 'N/A')}")
            print(f"  Backend: {stack.get('backend', 'N/A')}")
            print(f"  Database: {stack.get('database', 'N/A')}")
        
        components = architecture.get("components", [])
        if components:
            print(f"\n{Colors.bold(f'Components ({len(components)}):')}")
            for comp in components[:5]:  # Show first 5
                name = comp.get("name", "Unnamed")
                desc = comp.get("description", "")[:60]
                print(f"  • {name}: {desc}...")
        
        api = architecture.get("api", [])
        if api:
            print(f"\n{Colors.bold(f'API Endpoints ({len(api)}):')}")
            for endpoint in api[:3]:
                method = endpoint.get("method", "GET")
                path = endpoint.get("path", "/")
                print(f"  {method} {path}")
                
        if detailed:
            phases = architecture.get("phases", [])
            if phases:
                print(f"\n{Colors.bold('Implementation Phases:')}")
                for i, phase in enumerate(phases, 1):
                    print(f"  {i}. {phase}")
                    
    def save_architecture(self, architecture: Dict[str, Any], project_dir: Path):
        """Persist architecture to file."""
        save_architecture(architecture, project_dir / "ARCHITECTURE.json")


def main():
    """Entry point for the orchestrator."""
    config = CodingAgentsConfig.from_env()
    orchestrator = OrchestratorAgent(config)
    orchestrator.start()


if __name__ == "__main__":
    main()
# Coding Agents System

A multi-agent system for building complete projects from prompts through planning, review, and parallel execution using OpenHands SDK.

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER PROMPT                                │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                            │
│  • Receives user input                                           │
│  • Coordinates workflow                                          │
│  • Manages review loop                                           │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   ARCHITECT AGENT                                 │
│  • Creates project plan                                          │
│  • Designs system architecture                                   │
│  • Defines components & specs                                    │
│  • Generates ARCHITECTURE.json                                   │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    REVIEW LOOP                                   │
│  • Display plan to user                                          │
│  • Accept change requests                                        │
│  • Update architecture                                           │
│  • Repeat until approved                                         │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │    APPROVED?         │
                   └──────────┬───────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   ┌────────────┐     ┌────────────┐     ┌────────────┐
   │  FRONTEND  │     │   BACKEND  │     │  DATABASE  │
   │   AGENT    │     │   AGENT    │     │   AGENT    │
   └─────┬──────┘     └──────┬─────┘     └──────┬─────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                   ┌──────────────────────┐
                   │      DEVOPS AGENT     │
                   │  Docker, CI/CD, etc   │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │     INTEGRATION       │
                   │   & RUN PROJECT       │
                   └───────────────────────┘
```

## 🤖 Available Agents

| Agent | Responsibility |
|-------|----------------|
| **Orchestrator** | Main coordinator, manages workflow |
| **Architect** | Creates architecture plan from prompt |
| **Frontend** | Builds UI components, routing, styling |
| **Backend** | Creates APIs, business logic |
| **Database** | Designs schemas, migrations |
| **DevOps** | Docker, CI/CD, deployment configs |

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export LLM_API_KEY="your-api-key"

# Run the system
python main.py
```

## 📋 Workflow

1. **Enter Project Prompt** - Describe what you want to build
2. **View Architecture** - Review the generated plan
3. **Request Changes** - Modify any aspect (stack, components, etc.)
4. **Approve** - Lock in the final architecture
5. **Build** - Watch parallel agents construct your project
6. **Run** - Project is automatically started

## ⚙️ Configuration

Set these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODEL` | `gpt-4o` | LLM model to use |
| `LLM_API_KEY` | - | API key for LLM |
| `LLM_BASE_URL` | - | Base URL (for custom endpoints) |
| `WORKSPACE_DIR` | `./generated_projects` | Output directory |

## 📁 Project Structure

```
Coding-agents/
├── main.py              # Entry point
├── orchestrator.py      # Main orchestration
├── config.py            # Configuration
├── utils.py             # Utilities
├── agents/              # Specialized agents
│   ├── frontend.py
│   ├── backend.py
│   ├── database.py
│   └── devops.py
└── generated_projects/  # Output directory
```

## 🛠️ Tech Stacks Supported

- React + FastAPI + PostgreSQL
- Vue + Django + MongoDB
- Next.js + Express + SQLite
- Angular + Node.js + MySQL
- Svelte + NestJS + PostgreSQL

## 🐳 Docker (Optional)

Docker is **NOT required** to run the coding system or generated projects. However, Docker files are created for convenience.

**Without Docker (Recommended for development):**
```bash
# Backend
cd project_dir
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd project_dir/frontend
npm install
npm run dev
```

**With Docker (Optional):**
```bash
docker-compose up
```

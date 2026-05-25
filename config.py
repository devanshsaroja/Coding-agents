"""Configuration for the Coding Agents system."""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional


def load_env_file():
    """Load .env file if it exists."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


# Load .env file on module import
load_env_file()


@dataclass
class LLMConfig:
    """LLM Configuration."""
    model: str = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")
    api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    base_url: Optional[str] = os.getenv("LLM_BASE_URL", "https://api.anthropic.com/v1")
    provider: str = "anthropic"  # 'anthropic' or 'openai'
    
    def __post_init__(self):
        # Detect provider from available API keys
        if os.getenv("ANTHROPIC_API_KEY"):
            self.provider = "anthropic"
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            self.base_url = "https://api.anthropic.com/v1"
        elif os.getenv("OPENAI_API_KEY"):
            self.provider = "openai"
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    name: str
    instructions: str
    tools: List[str] = field(default_factory=list)


@dataclass
class ProjectConfig:
    """Project generation configuration."""
    workspace_dir: str = "./generated_projects"
    default_stack: str = "react-fastapi-postgresql"
    supported_stacks: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.supported_stacks = [
            "react-fastapi-postgresql",
            "vue-django-mongodb",
            "angular-nodejs-mysql",
            "nextjs-express-sqlite",
            "svelte-nestjs-postgresql",
        ]


@dataclass
class CodingAgentsConfig:
    """Main configuration for the coding agents system."""
    llm: LLMConfig = field(default_factory=LLMConfig)
    project: ProjectConfig = field(default_factory=ProjectConfig)
    
    @classmethod
    def from_env(cls) -> "CodingAgentsConfig":
        """Load configuration from environment variables."""
        return cls(
            llm=LLMConfig(),
            project=ProjectConfig(
                workspace_dir=os.getenv("WORKSPACE_DIR", "./generated_projects"),
                default_stack=os.getenv("DEFAULT_STACK", "react-fastapi-postgresql"),
            )
        )
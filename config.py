"""Configuration for the Coding Agents system."""

import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LLMConfig:
    """LLM Configuration."""
    model: str = os.getenv("LLM_MODEL", "gpt-4o")
    api_key: Optional[str] = os.getenv("LLM_API_KEY")
    base_url: Optional[str] = os.getenv("LLM_BASE_URL")


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
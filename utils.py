"""Shared utilities for the coding agents system."""

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import asdict


def sanitize_project_name(prompt: str) -> str:
    """Generate a safe project name from a prompt."""
    # Take first 5 words, lowercase, alphanumeric only
    words = prompt.lower().split()[:5]
    name = "_".join(w for w in words if w.isalnum())
    if not name:
        name = "project"
    # Add short hash for uniqueness
    hash_suffix = hashlib.md5(prompt.encode()).hexdigest()[:6]
    return f"{name}_{hash_suffix}"


def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists, create if needed."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_architecture(architecture: Dict[str, Any], path: Path) -> None:
    """Save architecture document to file."""
    with open(path, "w") as f:
        json.dump(architecture, f, indent=2)


def load_architecture(path: Path) -> Dict[str, Any]:
    """Load architecture document from file."""
    with open(path, "r") as f:
        return json.load(f)


def format_file_tree(structure: Dict[str, Any], prefix: str = "") -> str:
    """Format project structure as a tree string."""
    lines = []
    for name, content in structure.items():
        lines.append(f"{prefix}{name}/" if isinstance(content, dict) else f"{prefix}{name}")
        if isinstance(content, dict):
            lines.append(format_file_tree(content, prefix + "  "))
    return "\n".join(lines)


def parse_stack(stack_name: str) -> Dict[str, str]:
    """Parse stack name into components."""
    parts = stack_name.split("-")
    if len(parts) >= 3:
        return {
            "frontend": parts[0],
            "backend": parts[1],
            "database": "-".join(parts[2:])
        }
    return {"frontend": "react", "backend": "fastapi", "database": "postgresql"}


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    
    @classmethod
    def bold(cls, text: str) -> str:
        return f"{cls.BOLD}{text}{cls.ENDC}"
    
    @classmethod
    def success(cls, text: str) -> str:
        return f"{cls.GREEN}{text}{cls.ENDC}"
    
    @classmethod
    def error(cls, text: str) -> str:
        return f"{cls.RED}{text}{cls.ENDC}"
    
    @classmethod
    def info(cls, text: str) -> str:
        return f"{cls.CYAN}{text}{cls.ENDC}"
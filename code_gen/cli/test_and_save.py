"""CLI entrypoint for orchestration."""

from pathlib import Path
import sys

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    from code_gen.core.orchestrator import test_solution, test_system, main
else:
    from ..core.orchestrator import test_solution, test_system, main

__all__ = [
    "test_solution",
    "test_system",
    "main",
]

if __name__ == "__main__":
    main()

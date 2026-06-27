"""Fast CLI entrypoint without compile/run validation."""

from pathlib import Path
import sys

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    from code_gen.core.orchestrator import generate_solution, generate_system, main_fast
else:
    from ..core.orchestrator import generate_solution, generate_system, main_fast

__all__ = [
    "generate_solution",
    "generate_system",
    "main_fast",
]


if __name__ == "__main__":
    main_fast()

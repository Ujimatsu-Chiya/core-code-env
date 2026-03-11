"""Orchestration entrypoint."""

from pathlib import Path
import sys

if __package__ in (None, ""):
    script_dir = Path(__file__).resolve().parent
    script_dir_str = str(script_dir)
    if script_dir_str in sys.path:
        sys.path.remove(script_dir_str)

    project_root = script_dir.parent
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

from code_gen.core.orchestrator import test_solution, test_system, main

__all__ = [
    "test_solution",
    "test_system",
    "main",
]


if __name__ == "__main__":
    main()

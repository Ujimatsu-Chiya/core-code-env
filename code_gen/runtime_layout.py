"""Runtime directory/layout resolution for generators.

Phase-2 goal:
- Keep current legacy runtime folders working.
- Prepare migration to `runtimes/<lang>` without touching generator callers.
"""

from pathlib import Path
import os
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parent.parent

# Language key -> current legacy runtime folder name under repo root.
_LEGACY_RUNTIME_DIR: Dict[str, str] = {
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "py": "python3",
    "ts": "typescript",
    "js": "javascript",
    "go": "go",
}


def _candidate_runtime_dirs(lang: str) -> List[Path]:
    if lang not in _LEGACY_RUNTIME_DIR:
        raise ValueError(f"Unsupported runtime language: {lang}")

    candidates: List[Path] = []

    # Highest priority: per-language explicit override.
    explicit_env = os.getenv(f"CODE_GEN_RUNTIME_{lang.upper()}_PATH")
    if explicit_env:
        candidates.append(Path(explicit_env))

    # Optional shared runtime root override.
    runtime_root = os.getenv("CODE_GEN_RUNTIME_ROOT")
    if runtime_root:
        runtime_root_path = Path(runtime_root)
        candidates.append(runtime_root_path / lang)
        candidates.append(runtime_root_path / _LEGACY_RUNTIME_DIR[lang])

    # New target layout (future migration destination).
    candidates.append(REPO_ROOT / "runtimes" / lang)

    # Current legacy layout.
    candidates.append(REPO_ROOT / _LEGACY_RUNTIME_DIR[lang])
    return candidates


def get_runtime_path(lang: str) -> str:
    """Return resolved runtime directory for a language as an absolute path."""
    for candidate in _candidate_runtime_dirs(lang):
        if candidate.is_dir():
            return str(candidate)

    candidates = ", ".join(str(p) for p in _candidate_runtime_dirs(lang))
    raise FileNotFoundError(
        f"Runtime directory for `{lang}` not found. Checked: {candidates}. "
        "You can set CODE_GEN_RUNTIME_ROOT or CODE_GEN_RUNTIME_<LANG>_PATH."
    )


def get_rapidjson_helper_cpp() -> str:
    return str(REPO_ROOT / "rapidjson_helper.cpp")


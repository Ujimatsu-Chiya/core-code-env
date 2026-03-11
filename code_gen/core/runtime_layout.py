"""Runtime directory/layout resolution for generators."""

from pathlib import Path
import os
from typing import List


REPO_ROOT = Path(__file__).resolve().parents[2]

SUPPORTED_LANGS = {"c", "cpp", "java", "py", "ts", "js", "go"}


def _candidate_runtime_dirs(lang: str) -> List[Path]:
    if lang not in SUPPORTED_LANGS:
        raise ValueError(f"Unsupported runtime language: {lang}")

    candidates: List[Path] = []

    explicit_env = os.getenv(f"CODE_GEN_RUNTIME_{lang.upper()}_PATH")
    if explicit_env:
        candidates.append(Path(explicit_env))

    runtime_root = os.getenv("CODE_GEN_RUNTIME_ROOT")
    if runtime_root:
        candidates.append(Path(runtime_root) / lang)

    candidates.append(REPO_ROOT / "runtimes" / lang)
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


__all__ = ["get_runtime_path", "get_rapidjson_helper_cpp"]

"""Runtime directory/layout resolution for generators."""

from pathlib import Path
import os
from importlib import resources
from typing import List


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

    core_root = os.getenv("CODE_GEN_CORE_ROOT")
    if core_root:
        candidates.append(Path(core_root) / "runtimes" / lang)

    try:
        packaged_runtime = resources.files("runtimes").joinpath(lang)
        if packaged_runtime.is_dir():
            candidates.append(Path(str(packaged_runtime)))
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    return candidates


def get_runtime_path(lang: str) -> str:
    """Return resolved runtime directory for a language as an absolute path."""
    for candidate in _candidate_runtime_dirs(lang):
        if candidate.is_dir():
            return str(candidate)

    candidates = ", ".join(str(p) for p in _candidate_runtime_dirs(lang))
    raise FileNotFoundError(
        f"Runtime directory for `{lang}` not found. Checked: {candidates}. "
        "You can set CODE_GEN_RUNTIME_ROOT, CODE_GEN_CORE_ROOT, "
        "or CODE_GEN_RUNTIME_<LANG>_PATH."
    )


def _candidate_core_roots() -> List[Path]:
    candidates: List[Path] = []

    core_root = os.getenv("CODE_GEN_CORE_ROOT")
    if core_root:
        candidates.append(Path(core_root))

    runtime_root = os.getenv("CODE_GEN_RUNTIME_ROOT")
    if runtime_root:
        rr = Path(runtime_root)
        candidates.append(rr.parent if rr.name == "runtimes" else rr)

    try:
        asset_root = resources.files("code_gen.assets")
        if asset_root.is_dir():
            candidates.append(Path(str(asset_root)))
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    return candidates


def get_rapidjson_helper_cpp() -> str:
    explicit = os.getenv("CODE_GEN_RAPIDJSON_HELPER_CPP")
    if explicit:
        p = Path(explicit)
        if p.is_file():
            return str(p)

    for root in _candidate_core_roots():
        candidate = root / "rapidjson_helper.cpp"
        if candidate.is_file():
            return str(candidate)

    candidates = ", ".join(str(root / "rapidjson_helper.cpp") for root in _candidate_core_roots())
    raise FileNotFoundError(
        f"rapidjson_helper.cpp not found. Checked: {candidates}. "
        "You can set CODE_GEN_CORE_ROOT or CODE_GEN_RAPIDJSON_HELPER_CPP."
    )


def get_rapidjson_helper_include_dir() -> str:
    explicit = os.getenv("CODE_GEN_RAPIDJSON_HELPER_INCLUDE_DIR")
    if explicit:
        p = Path(explicit)
        if p.is_dir():
            return str(p)

    helper = Path(get_rapidjson_helper_cpp())
    return str(helper.parent)


__all__ = [
    "get_runtime_path",
    "get_rapidjson_helper_cpp",
    "get_rapidjson_helper_include_dir",
]

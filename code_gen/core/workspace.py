"""Temporary workspace helpers for generator test runs."""

import os
import shutil
import tempfile
from pathlib import Path


def create_tmp_workspace(prefix: str = "code_gen_") -> str:
    base_dir = os.getenv("CODE_GEN_TMP_ROOT")
    if not base_dir:
        repo_root = Path(__file__).resolve().parents[2]
        base_dir = str(repo_root / ".tmp")
    os.makedirs(base_dir, exist_ok=True)
    return tempfile.mkdtemp(prefix=prefix, dir=base_dir)


def cleanup_tmp_workspace(tmp_dir: str) -> None:
    shutil.rmtree(tmp_dir, ignore_errors=True)

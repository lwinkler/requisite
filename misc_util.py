"""General utilities for Python"""

import sys
import subprocess
from pathlib import Path
from typing import List


def get_python_executable() -> Path:
    """Return the path to the Python executable"""
    return Path(sys.executable)


def generate_all_git_files_command(path: Path, extensions: List[str]) -> str:
    """Generate a command to list all files with git+grep"""
    grep = (
        " | grep "
        + " ".join(['-e "\\.' + extension + '$"' for extension in extensions])
        if extensions
        else ""
    )
    return "git ls-files " + path.as_posix() + grep


def list_all_git_files(path: Path, extensions: List[str]) -> List[Path]:
    """List all files with git ls-files and grep"""
    command = generate_all_git_files_command(path, extensions)
    ret = subprocess.run(
        command, capture_output=True, encoding="utf-8", check=True, shell=True
    )
    return [Path(path) for path in ret.stdout.splitlines()]


def run_on_all_git_files(
    command: str, path: Path, extensions: List[str], check=True
) -> int:
    """Execute a command on all files using git and xargs"""

    full_command = (
        generate_all_git_files_command(path, extensions) + " | xargs " + command
    )
    ret = subprocess.run(full_command, check=check, shell=True)
    return ret.returncode

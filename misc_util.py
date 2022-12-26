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


def contain(path: Path, parent_paths: List[Path]) -> bool:
    """Check if a path is contained by a list of potential parents"""
    for parent_path in parent_paths:
        if parent_path in path.parents:
            return True
    return False


def list_all_files(
    path: Path, extensions: List[str], excluded_paths: List[Path], check: bool = True
) -> List[Path]:
    """List all files with one extension"""
    if contain(path, excluded_paths):
        return []

    if path.is_file():
        return [path] if not extensions or path.suffix[1:] in extensions else []

    results: List[Path] = []
    if path.is_dir():
        for child_path in path.iterdir():
            results += list_all_files(child_path, extensions, excluded_paths, check)
        return results
    raise Exception(f"Unknown file type {path.as_posix()}")


def run_on_all_files(
    command: str,
    path: Path,
    extensions: List[str],
    excluded_paths: List[Path],
    check: bool = True,
) -> int:
    """Execute a command on all files. With this function we still have the issue
    of max command length (although it is higher that by using the shell, on Windows)"""

    files = list_all_files(path, extensions, excluded_paths, check)
    full_command = command + " " + " ".join([file1.as_posix() for file1 in files])
    # print("run:", full_command)
    ret = subprocess.run(full_command, check=check, shell=False)
    return ret.returncode


def run_on_all_git_files(
    command: str, path: Path, extensions: List[str], check: bool = True
) -> int:
    """Execute a command on all files using git and xargs"""

    full_command = (
        generate_all_git_files_command(path, extensions) + " | xargs " + command
    )
    ret = subprocess.run(full_command, check=check, shell=True)
    return ret.returncode

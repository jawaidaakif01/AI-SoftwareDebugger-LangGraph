import os
from langchain_core.tools import tool


def get_python_files(folder):
    python_files = []
    for root, dirs, files in os.walk(folder):
        if "venv" in root or "__pycache__" in root:
            continue
        for name in files:
            if name.endswith(".py"):
                python_files.append(os.path.join(root, name))
    return python_files


@tool
def list_files(folder: str) -> str:
    """List all Python files inside a folder, including subfolders."""
    python_files = get_python_files(folder)
    if len(python_files) == 0:
        return "No Python files found."
    return "\n".join(python_files)


@tool
def read_file(file_path: str) -> str:
    """Read a Python file and return its content."""
    if not file_path.endswith(".py"):
        return "Error: only .py files can be read."
    if not os.path.exists(file_path):
        return f"Error: file not found: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()[:8000]


@tool
def search_in_repo(folder: str, text: str) -> str:
    """Search all Python files in a folder for some text. Returns file, line number and the line."""
    matches = []
    for path in get_python_files(folder):
        with open(path, "r", encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                if text in line:
                    matches.append(f"{path}:{number}: {line.strip()}")

    if len(matches) == 0:
        return "No matches found. This text does not appear in any Python file in the repository."
    return "\n".join(matches[:30])


gatherer_tools = [list_files, read_file, search_in_repo]
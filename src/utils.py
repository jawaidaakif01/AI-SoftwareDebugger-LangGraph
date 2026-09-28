import subprocess
import sys


def run_python_file(path, timeout=30):
    """Runs a Python file. Returns (passed, error_output)."""
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return True, ""
        return False, result.stderr[-1500:]
    except subprocess.TimeoutExpired:
        return False, "The file ran for more than 30 seconds."

def files_as_text(file_contents):
    """Turns {path: content} into one text block with line numbers."""
    text = ""
    for path, content in file_contents.items():
        text += f"### File: {path}\n"
        for number, line in enumerate(content.split("\n"), start=1):
            text += f"{number}: {line}\n"
        text += "\n"
    return text
import ast
import os
from importlib.util import find_spec

from state import State
from llm import get_llm
from utils import files_as_text

llm = get_llm(temperature=0)

def dependency_check_node(state: State) -> dict:
    """Branch 1: finds imported modules that are not installed and not in the repo."""
    print("\n[Branch 1] Dependency check...")

    missing = []

    for path, content in state["file_contents"].items():
        for line in content.split("\n"):
            line = line.strip()

            # only look at lines like "import x" or "from x import y"
            if line.startswith("import ") or line.startswith("from "):
                module = line.split()[1].replace(",", "")
                module = module.split(".")[0]

                if module == "":
                    continue

                local_file = os.path.join(state["repo_path"], module + ".py")
                if find_spec(module) is None and not os.path.exists(local_file):
                    missing.append(f"{module} (imported in {path})")

    if len(missing) > 0:
        result = "Missing modules: " + ", ".join(missing)
    else:
        result = "All imported modules are installed or exist in the repo."

    print(f"  -> {result}")
    return {"diagnostics": {"dependency_check": result}}

def static_check_node(state: State) -> dict:
    """Branch 2: The LLM reads the code (without running it) and finds the suspicious lines."""
    print("\n[Branch 2] Static code review...")

    prompt = (
        "You are reviewing Python code WITHOUT running it. Find the exact file and "
        "line number(s) most likely responsible for the error below, and explain why "
        "in 2-3 sentences.\n\n"
        f"Error\n{state["error"]}\n\n"
        f"Code:\n{files_as_text(state['file_contents'])}"
    )

    response = llm.invoke(prompt)
    result = response.content.strip()

    print(f" -> {result}")
    return {"diagnostics": {"static_check": result}}

def pattern_check_node(state: State) -> dict:
    """Branch 3: the LLM uses general knowledge about this kind of error (no code)."""
    print("\n[Branch 3] known-pattern check...")

    prompt = (
        "Using only general knowledge(do not guess about any specific code), describe "
        "the most common causes of this kind of Python error and the standard ways to "
        "fix it.Keep it to 3-4 sentences.\n\n"
        f"Error category: {state["error_category"]}\n"
        f"Error: \n {state['error']}"
    )

    response = llm.invoke(prompt)
    result = response.content.strip()


    print(f" -> {result}")
    return {"diagnostics": {"pattern_check": result}}
    
from state import State
from utils import run_python_file

def apply_fix_node(state: State) -> dict:
    """Phase 8: Writes the approved fix to the real file, then re-runs it for real."""

    print("\n--- Apply Fix ---")

    target = state["target_file"]
    code = state["draft_corrected_code"]

    with open(target, "w", encoding="utf-8") as f:
        f.write(code)
    print(f" -> wrote fix to {target}")

    passed, error_output = run_python_file(target)

    if passed:
        print(" -> confirmed: file runs cleanly")
    else:
        print(f" -> WARNING: still fails after being written:\n{error_output}")

    return {"verification_passed": passed, "last_failure_reason": error_output}



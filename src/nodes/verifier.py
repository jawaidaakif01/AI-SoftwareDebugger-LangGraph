import os
import subprocess
import sys

from state import State


def verifier_node(state: State) -> dict:
    """Phase 6: runs the proposed fix and checks whether it works."""
    print("\n--- Verifier ---")

    code = state["draft_corrected_code"]
    target = state["target_file"]

    # the fix must exist and must be for a file we actually gathered
    if code == "" or target not in state["file_contents"]:
        reason = "The fix was empty, or the file path was not one of the gathered files."
        print(f"  -> FAILED: {reason}")
        return {"verification_passed": False, "last_failure_reason": reason}

    # save the fix in a temporary file next to the original, so local imports still work
    temp_path = os.path.join(os.path.dirname(target), "_fix_test.py")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        passed = result.returncode == 0
        reason = "" if passed else result.stderr[-1500:]
    except subprocess.TimeoutExpired:
        passed = False
        reason = "The fixed code ran for more than 30 seconds."

    os.remove(temp_path)

    if passed:
        print("  -> PASSED")
    else:
        print(f"  -> FAILED:\n{reason}")

    return {"verification_passed": passed, "last_failure_reason": reason}
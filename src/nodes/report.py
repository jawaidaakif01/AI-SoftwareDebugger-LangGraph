from state import State

def report_node(state: State) -> dict:
    """Phase 8: builds the final human-readable report."""
    print("\n--- Report Generator ---")

    lines = []
    lines.append(f"Error category: {state.get("error_category", 'unknown')}")
    lines.append(f"Files investigated: {list(state.get('file_contents', {}).keys())}")
    lines.append("")
    lines.append("Root cause:")
    lines.append(state.get("diagnostics", {}).get("root_cause", "not determined"))
    lines.append("")
    lines.append(f"Fix attempts: {state.get('fix_attempt', 0)}")
    lines.append(F"Human approved: {state.get('human_approved', False)}")
    lines.append(f"Verified working: {state.get('verification_passed', False)}")

    if state.get("human_approved"):
        lines.append(f"Fix was applied to: {state.get('target_file', '')}")
    else:
        lines.append("No fix was applied (not approved, or attempts were exhausted).")

    report = "\n".join(lines)
    print("\n" + report)
    return{"final_report": report}
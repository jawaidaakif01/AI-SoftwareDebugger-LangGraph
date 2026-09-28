from langgraph.types import interrupt
from state import State

def human_review_node(state: State) -> dict:
    """Phase 7: pauses the graph and waits for a human decision."""
    print("\n--- [Phase 7] Human Review ---")

    human_response = interrupt({
        "target_file": state["target_file"],
        "proposed_fix": state["draft_corrected_code"],
        "instruction": "Type 'approved' to apply this fix, or type feedback to request a retry.",
    })

    response = human_response.strip()

    if response.lower() in ["approved", "approve", "yes", "ok"]:
        print(" -> approved")
        return {"human_approved": True, "human_feedback": ""}

    print(" -> rejected, feedback recorded")
    return {"human_approved": False, "human_feedback": response}
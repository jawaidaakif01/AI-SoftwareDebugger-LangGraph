from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from reducers import merge_diagnostics

class State(TypedDict):
    repo_path: str      # Path to the repo being debugged
    error: str      # raw error/traceback reported (or discovered)
    messages: Annotated[list, add_messages]     # LLM tool conversation history
    file_contents: dict[str, str]           # {filepath: content} gathered from the repo
    error_category: str        # "import", "logic", "langgraph"
    diagnostics: Annotated[dict, merge_diagnostics]     # each parallel node writes one sub-key, eg, {"dependency_check": {...}}
    draft_corrected_code: str       # current fix attempt
    fix_attempt: int        # attempt counter (loop guard)
    last_failure_reason: str        # why the previous attempt failed
    verification_passed: bool       # did the last test/run succeed?
    human_approved: bool        # human's approve/reject decision
    human_feedback: str         # any comments/edits the human gave
    final_report: str          # human-readable summary
    target_file: str         

    



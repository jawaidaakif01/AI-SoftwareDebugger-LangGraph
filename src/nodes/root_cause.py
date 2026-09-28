from state import State
from llm import get_llm

llm = get_llm(temperature=0)

def root_cause_node(state: State) -> dict:
    """Fan-in: combines the three diagnostic reports into one root cause."""
    print("\n--- Root Cause Analyzer ---")

    diagnostics = state["diagnostics"]

    prompt = (
        "You are a senior debugger. Three checks were run on a Python error. "
        "Combine them into one root cause.\n\n"
        f"Error:\n{state["error"]}\n\n"
        f"Dependency check:\n{diagnostics['dependency_check']}\n\n"
        f"Static code review:\n{diagnostics['static_check']}\n\n"
        f"Known patterns:\n{diagnostics['pattern_check']}\n\n"
        "In 2-4 sentences, state the root cause, the file and line it is in, and what "
        "needs to change to fix it. Do not write the fixed code."
    )

    response = llm.invoke(prompt)
    root_cause = response.content.strip()

    print(f" -> {root_cause}")
    return {"diagnostics": {"root_cause": root_cause}}


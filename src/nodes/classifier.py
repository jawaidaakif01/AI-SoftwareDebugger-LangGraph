from state import State
from llm import get_llm

llm = get_llm(temperature=0)

VALID_CATEGORIES = ["langgraph", "import", "logic"]

def classifier_node(state: State) -> dict:
    """
    Reads the raw error and decides which category is belongs to.
    """

    print("\n--- [Phase 3] Classifier ---")

    prompt = (
        "Classify the following Python error into exactly one category: "
        "'import', 'logic', 'langgraph', or 'unknown'.\n\n"
        "Use 'import' for ModuleNotFoundError, ImportError, missing packages, "
        "version conflicts, or wrong import paths.\n"
        "Use 'logic' for wrong output, AssertionError, off-by-one bugs, or any "
        "runtime error (TypeError, ValueError, IndexError, KeyError) in plain Python code.\n"
        "Use 'langgraph' for errors raised by LangGraph itself, such as "
        "InvalidUpdateError, GraphRecursionError, or invalid state/graph configuration.\n"
        "Use 'unknown' if the error fits none of these.\n\n"
        f"Error:\n{state['error']}\n\n"
        "Return only one word: import, logic, langgraph, or unknown."
    )

    response = llm.invoke(prompt)
    text = response.content.strip().lower()

    category = "unknown"
    for candidate in VALID_CATEGORIES:
        if candidate in text:
            category = candidate
            break

    print(f"Error classified as: {category}")
    return {"error_category": category}
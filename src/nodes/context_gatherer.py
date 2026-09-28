import os
from state import State
from llm import get_llm
from tools import gatherer_tools, read_file

llm = get_llm(temperature=0)
llm_with_tools = llm.bind_tools(gatherer_tools)

GATHERER_SYSTEM_PROMPT = (
    "You are a debugging assistant gathering context from a code repository. "
    "You are given the repository folder, an error and its category. Use your tools "
    "to find the code needed to understand the root cause: the file named in the error, "
    "plus any file it imports. Always use the repository folder given in the message "
    "when calling tools. Read only what is relevant, usually 1 to 4 files. "
    "Never repeat a tool call with the same arguments. If a search finds nothing, that "
    "name is not defined anywhere in the repository, so stop searching for it. "
    "Use at most 5 tool calls in total. "
    "When you have enough context, stop calling tools and reply with a 2-3 sentence "
    "summary of what you found. Do NOT try to fix the error."
)


def context_gatherer_node(state: State) -> dict:
    """
    The LLM decides which tools to call to explore the repo.
    This node runs again after every round of tool results.
    """
    print("\n--- [Phase 4] Context Gatherer ---")

    first_call = len(state["messages"]) == 0

    if first_call:
        first_message = (
            "human",
            f"Repository folder: {state['repo_path']}\n"
            f"Error category: {state['error_category']}\n\n"
            f"Error:\n{state['error']}\n\n"
            "Gather the relevant code from the repository."
        )
        history = [first_message]
    else:
        history = state["messages"]

    response = llm_with_tools.invoke([("system", GATHERER_SYSTEM_PROMPT)] + history)

    for call in response.tool_calls:
        print(f"  tool call -> {call['name']}({call['args']})")

    if first_call:
        return {"messages": [first_message, response]}
    return {"messages": [response]}


def extract_context_node(state: State) -> dict:
    """
    After the tool loop ends, collect every file the agent read
    into file_contents = {path: content}.
    """
    file_contents = {}

    for message in state["messages"]:
        for call in getattr(message, "tool_calls", []):
            if call["name"] == "read_file":
                path = call["args"]["file_path"]
                content = read_file.invoke({"file_path": path})
                if not content.startswith("Error:"):
                    file_contents[path] = content

    print(f"Collected {len(file_contents)} file(s): {list(file_contents)}")
    return {"file_contents": file_contents}
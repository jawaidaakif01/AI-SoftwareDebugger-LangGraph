from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from state import State
from nodes.classifier import classifier_node
from tools import gatherer_tools
from nodes.context_gatherer import context_gatherer_node, extract_context_node
from nodes.diagnostics import dependency_check_node, static_check_node, pattern_check_node
from nodes.root_cause import root_cause_node
from nodes.fix_generator import fix_generator_node
from nodes.verifier import verifier_node
from nodes.human_review import human_review_node
from nodes.apply_fix import apply_fix_node
from nodes.report import report_node



MAX_FIX_ATTEMPTS = 3
MAX_TOOL_ROUNDS = 5

# def classifier_node(state: State) -> dict:
#     print("\n--- [Phase 3] Classifier ---")
#     return {"error_category":"import"}

# def context_gatherer_node(state: State) -> dict:
#     print("\n--- [Phase 4] Context Gatherer ---")
#     return {"file_contents": {"stub.py": "print('hello')"}}

# def dependency_check_node(state: State) -> dict:
#     print("\n--- [Branch 1] Depenedency check...")
#     return {"diagnostics" : {"dependency_check": "stub result"}}

# def static_check_node(state: State) -> dict:
#     print("\n[Branch 2] Static / AST check...")
#     return {"diagnostics": {"static_check":"stub result"}}

# def pattern_check_node(state: State) -> dict:
#     print("\n[Branch 3] known-pattern check...")
#     return{"diagnostics": {"Pattern_check":"stub result"}}

# def root_cause_node(state: State) -> dict:
#     print("\n--- Root Cause Ananlyzer ---")
#     return {"diagnostics": {"root_cause": "stub root cause"}}

# def fix_generator_node(state: State) -> dict:
#     attempt = state.get("fix_attempt", 0) + 1
#     print(f"\n--- [Phase 6] fix generator (attempt {attempt}) ---")
#     return {"draft_corrected_code": f"# fix attempt {attempt}", "fix_attempt": attempt}

# def verifier_node(state: State) -> dict:
#     passed = state['fix_attempt'] >= 2
#     print(f"\n--- Verifier: {'PASSED' if passed else 'FAILED'} ---")
#     return{
#         "verification_passed": passed,
#         "last_failure_reason": "" if passed else "stub failure reason"
#     }

# def human_review_node(state: State) -> dict:
#     print("\n--- [Phase 7] Human Review (auto-approved stub) ---")
#     return {"human_approved": True, "human_feedback": ""}

# def apply_fix_node(state: State) -> dict:
#     print("\n--- Apply fix ---")
#     return {}

# def report_node(state: State) -> dict:
#     print("\n--- Report Generator ---")
#     report = (
#         f"Category: {state.get('error_category', 'unknown')}\n"
#         f"Attempts: {state.get('fix_attempt', 0)}\n"
#         f"Verified: {state.get("verification_passed", False)}\n"
#         f"Approved: {state.get('human_approved', False)}"
#     )

#     return {"final_report": report}

def route_by_category(state: State):
    if state['error_category'] == 'unknown':
        return "report"
    return "context_gatherer"

def route_after_verify(state: State):
    if state["verification_passed"]:
        return "human_review"
    if state["fix_attempt"] >= MAX_FIX_ATTEMPTS:
        print("reached max fix attempts")
        return "report"
    return "fix_generator"

def route_after_review(state: State):
    if state['human_approved']:
        return "apply_fix"
    if state['fix_attempt'] >= MAX_FIX_ATTEMPTS:
        return "report"
    return "fix_generator"

def should_use_tool(state: State):
    tool_rounds = 0
    for message in state["messages"]:
        if getattr(message, "tool_calls", None):
            tool_rounds += 1

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        if tool_rounds > MAX_TOOL_ROUNDS:
            print("  tool budget reached, moving on")
            return "extract_context"
        return "tools"
    return "extract_context"


graph = StateGraph(State)

graph.add_node("classifier", classifier_node)
graph.add_node("context_gatherer", context_gatherer_node)
graph.add_node("dependency_check", dependency_check_node)
graph.add_node("static_check", static_check_node)
graph.add_node("pattern_check", pattern_check_node)
graph.add_node("root_cause", root_cause_node)
graph.add_node("fix_generator", fix_generator_node)
graph.add_node("verifier", verifier_node)
graph.add_node("human_review", human_review_node)
graph.add_node("apply_fix", apply_fix_node)
graph.add_node("report", report_node)
graph.add_node("tools", ToolNode(gatherer_tools))
graph.add_node("extract_context", extract_context_node)

graph.add_edge(START, "classifier")
graph.add_conditional_edges(
    "classifier",
    route_by_category,
    {"context_gatherer": "context_gatherer", "report": "report"},
)

graph.add_conditional_edges(
    "context_gatherer",
    should_use_tool,
    {"tools":"tools", "extract_context":"extract_context"}
)
graph.add_edge("tools", "context_gatherer")
graph.add_edge("extract_context", "dependency_check")
graph.add_edge("extract_context", "static_check")
graph.add_edge("extract_context", "pattern_check")

graph.add_edge("dependency_check", "root_cause")
graph.add_edge("static_check", "root_cause")
graph.add_edge("pattern_check", "root_cause")

graph.add_edge("root_cause", "fix_generator")
graph.add_edge("fix_generator", "verifier")
graph.add_conditional_edges(
    "verifier",
    route_after_verify,
    {"human_review": "human_review", "fix_generator": "fix_generator", "report": "report"},
)
graph.add_conditional_edges(
    "human_review",
    route_after_review,
    {"apply_fix": "apply_fix", "fix_generator": "fix_generator", "report": "report"},
)

graph.add_edge("apply_fix", "report")
graph.add_edge("report", END)

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

png_bytes = app.get_graph().draw_mermaid_png()
with open("langgraph.png", "wb") as f:
    f.write(png_bytes)
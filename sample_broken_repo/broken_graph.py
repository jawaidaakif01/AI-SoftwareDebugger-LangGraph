from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    result: str # no reducer - but two parallel branches both write here

def node_a(state: State) -> dict:
    return {"result": "from node A"}

def node_b(state: State) -> dict:
    return {"result": "from node B"}

graph = StateGraph(State)

graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)

graph.add_edge(START, "node_a")
graph.add_edge("node_b", node_b)

graph.add_edge(START, "node_a")
graph.add_edge(START, "node_b")
graph.add_edge("node_a", END)
graph.add_edge("node_b", END)

app = graph.compile()

if __name__=="__main__":
    result = app.invoke({"result": ""})
    print(result)



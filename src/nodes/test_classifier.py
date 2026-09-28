from classifier import classifier_node

test_cases = {
    "import": "ModuleNotFoundError: No module named 'nonexistent_utils'",
    "logic": "AssertionError: Expected 15, got 10",
    "langgraph": (
        "langgraph.errors.InvalidUpdateError: At key 'result': Can receive "
        "only one value per step. Use an Annotated key to handle multiple values."
    ),
    "unknown": "The weather is nice today",
}

for expected, error in test_cases.items():
    result = classifier_node({"error": error})
    status = "PASS" if result["error_category"] == expected else "FAIL"
    print(f"[{status}] expected={expected}, got={result['error_category']}\n") 
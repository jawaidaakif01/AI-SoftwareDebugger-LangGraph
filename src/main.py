from graph import app

initial_state = {
    "repo_path": "sample_broken_repo",
    "error": "ModuleNotFoundError: No module named 'nonexistent_utils'",
    "messages": [],
    "diagnostics": {},
    "fix_attempt": 0
}

result = app.invoke(initial_state)

print("\n" + "=" * 55)
for name, text in result["diagnostics"].items():
    print(f"\n[{name}]\n{text}")
print("FINAL REPORT")
print("=" * 55)
print(result['final_report'])
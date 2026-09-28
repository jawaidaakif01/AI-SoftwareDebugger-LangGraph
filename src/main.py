import sys
from langgraph.types import Command
from graph import app
from utils import run_python_file

print("=" * 55)
print("AI Software Debugger")
print("=" * 55)

repo_path = input("\nEnter the path to the repository you want to debug: ").strip()

print("\nHow do you want to provide the error?")
print("1. Run a file in the repo and capture the error")
print("2. Paste the error message myself")
choice = input("\nEnter 1 or 2: ").strip()

if choice == "1":
    file_to_run = input("Enter the file to run (e.g. broken_imports.py): ").strip()
    file_path = repo_path.rstrip("/\\") + "/" + file_to_run

    passed, error_output = run_python_file(file_path)

    if passed:
        print("\nThat file ran without any error. Nothing to debug.")
        sys.exit()

    error = error_output
    print(f"\nCaptured error:\n{error}")

else:
    error = input("Paste the error message: ").strip()

initial_state = {
    "repo_path": repo_path,
    "error": error,
    "messages": [],
    "diagnostics": {},
    "fix_attempt": 0,
}

config = {"configurable": {"thread_id": "debug_session_1"}}

print("\nStarting investigation...\n")

result = app.invoke(initial_state, config=config)

while "__interrupt__" in result:
    interrupt_data = result["__interrupt__"][0].value

    print("\n" + "=" * 55)
    print("PROPOSED FIX FOR YOUR REVIEW")
    print("=" * 55)
    print(f"File: {interrupt_data['target_file']}")
    print("-" * 55)
    print(interrupt_data["proposed_fix"])
    print("-" * 55)
    print(interrupt_data["instruction"])

    human_input = input("\nYour response: ").strip()
    result = app.invoke(Command(resume=human_input), config=config)

print("\n" + "=" * 55)
print("FINAL REPORT")
print("=" * 55)
print(result["final_report"])
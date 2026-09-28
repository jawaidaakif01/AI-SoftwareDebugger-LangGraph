from state import State
from llm import get_llm
from utils import files_as_text

llm = get_llm(temperature=0)


def clean_code(text):
    """Removes ``` lines in case the LLM wraps its code in markdown."""
    kept_lines = []
    for line in text.strip().split("\n"):
        if not line.strip().startswith("```"):
            kept_lines.append(line)
    return "\n".join(kept_lines)


def fix_generator_node(state: State) -> dict:
    """Phase 6: asks the LLM for a fixed version of one file."""
    attempt = state.get("fix_attempt", 0) + 1
    print(f"\n--- [Phase 6] Fix Generator (attempt {attempt}) ---")

    prompt = (
         "You are fixing a bug in a Python repository.\n\n"
        f"Error:\n{state['error']}\n\n"
        f"Root cause:\n{state['diagnostics']['root_cause']}\n\n"
        f"Code (line numbers are shown only for reference):\n{files_as_text(state['file_contents'])}\n"
        f"The FILE you choose must be exactly one of: {list(state['file_contents'].keys())}\n\n"
    )

    # on a retry, show the LLM what it tried before and why it failed
    if attempt > 1:
        prompt += (
            "Your previous fix did not work.\n"
            f"Previous fix:\n{state['draft_corrected_code']}\n\n"
            f"It failed with:\n{state['last_failure_reason']}\n\n"
        )

    prompt += (
        "Fix ONE file. Reply in exactly this format:\n"
        "FILE: <path of the file, exactly as shown above>\n"
        "CODE:\n"
        "<the complete corrected file, without line numbers and without explanations>"
    )

    reply = llm.invoke(prompt).content.strip()

    if "FILE:" not in reply or "CODE:" not in reply:
        print("  -> reply was not in the expected format")
        return {"draft_corrected_code": "", "target_file": "", "fix_attempt": attempt}

    first_part, code = reply.split("CODE:", 1)
    target_file = first_part.replace("FILE:", "").strip()
    code = clean_code(code)

    print(f"  -> proposed a fix for {target_file}")
    return {
        "draft_corrected_code": code,
        "target_file": target_file,
        "fix_attempt": attempt,
    }
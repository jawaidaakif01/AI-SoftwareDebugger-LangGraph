import uuid
import streamlit as st

from langgraph.types import Command
from graph import app
from utils import run_python_file
from ui_theme import CUSTOM_CSS, status_chip, section

st.set_page_config(page_title="Case Debugger", page_icon="🔍", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "result" not in st.session_state:
    st.session_state.result = None
if "started" not in st.session_state:
    st.session_state.started = False

config = {"configurable": {"thread_id": st.session_state.thread_id}}
case_id = st.session_state.thread_id[:8]


def start_new_session():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.result = None
    st.session_state.started = False


def current_status():
    if not st.session_state.started:
        return "pending", "Not started"
    result = st.session_state.result
    if "__interrupt__" in result:
        return "active", "Awaiting review"
    if result.get("human_approved"):
        return "passed", "Resolved"
    return "failed", "Closed, unresolved"


kind, label = current_status()
st.markdown(
    f'<div class="case-header"><div><div class="id">case #{case_id}</div>'
    f'<h1>Investigation</h1></div>{status_chip(label, kind)}</div>',
    unsafe_allow_html=True,
)


def show_diagnostics(result):
    diagnostics = result.get("diagnostics", {})
    if not diagnostics:
        return
    section("evidence", "Diagnostic findings")
    for name, text in diagnostics.items():
        if name == "root_cause":
            continue
        st.markdown(f'<div class="evidence">{name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="evidence-body">{text}</div>', unsafe_allow_html=True)
    if "root_cause" in diagnostics:
        section("conclusion", "Root cause", kind="active")
        st.markdown(f'<div class="evidence-body">{diagnostics["root_cause"]}</div>', unsafe_allow_html=True)


if not st.session_state.started:
    section("intake", "Repository")
    repo_path = st.text_input("Repository folder", value="sample_broken_repo", label_visibility="collapsed")

    mode = st.radio("Error source", ["Run a file", "Paste an error"], label_visibility="collapsed")

    file_to_run, pasted_error = "", ""
    if mode == "Run a file":
        file_to_run = st.text_input("File to run", placeholder="buggy_math.py", label_visibility="collapsed")
    else:
        pasted_error = st.text_area("Paste error", label_visibility="collapsed")

    if st.button("Begin investigation"):
        if mode == "Run a file":
            passed, error_output = run_python_file(repo_path.rstrip("/\\") + "/" + file_to_run)
            if passed:
                st.success("That file ran cleanly. No case to open.")
                st.stop()
            error = error_output
        else:
            error = pasted_error

        initial_state = {
            "repo_path": repo_path,
            "error": error,
            "messages": [],
            "diagnostics": {},
            "fix_attempt": 0,
        }
        with st.spinner("Investigating..."):
            result = app.invoke(initial_state, config=config)

        st.session_state.result = result
        st.session_state.started = True
        st.rerun()

elif "__interrupt__" in st.session_state.result:
    show_diagnostics(st.session_state.result)
    interrupt_data = st.session_state.result["__interrupt__"][0].value

    section("proposal", f"Fix — {interrupt_data['target_file']}", kind="active")
    st.markdown('<div class="fix-panel">', unsafe_allow_html=True)
    st.code(interrupt_data["proposed_fix"], language="python")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Approve & apply"):
            with st.spinner("Applying..."):
                result = app.invoke(Command(resume="approved"), config=config)
            st.session_state.result = result
            st.rerun()
    with col2:
        feedback = st.text_input("Feedback", placeholder="Or leave blank to reject and retry", label_visibility="collapsed")
        if st.button("Reject"):
            with st.spinner("Retrying..."):
                result = app.invoke(Command(resume=feedback or "rejected"), config=config)
            st.session_state.result = result
            st.rerun()

else:
    show_diagnostics(st.session_state.result)
    section("outcome", "Final report", kind="passed" if st.session_state.result.get("human_approved") else "failed")
    st.markdown(
        f'<div class="evidence-body">{st.session_state.result["final_report"]}</div>',
        unsafe_allow_html=True,
    )
    if st.button("Open new case"):
        start_new_session()
        st.rerun()
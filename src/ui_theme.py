CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap');

:root {
    --bg: #0E1116;
    --panel: #161A21;
    --line: #262B35;
    --text: #ECE9E2;
    --muted: #8890A0;
    --amber: #E8B339;
    --teal: #4FD1A5;
    --red: #E2574C;
}

/* hide Streamlit's own chrome */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer {
    display: none !important;
}
[data-testid="stHeader"] {
    background: transparent;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    font-family: 'IBM Plex Sans', sans-serif;
}

.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
}

/* case header */
.case-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1px solid var(--line);
    padding-bottom: 1rem;
    margin-bottom: 1.75rem;
}
.case-header .id {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 0.02em;
}
.case-header h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    margin: 0.15rem 0 0 0;
}

/* status chip */
.chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    padding: 0.25rem 0.7rem;
    border-radius: 3px;
    border: 1px solid var(--line);
}
.chip.pending { color: var(--muted); }
.chip.active  { color: var(--amber); border-color: var(--amber); }
.chip.passed  { color: var(--teal);  border-color: var(--teal); }
.chip.failed  { color: var(--red);   border-color: var(--red); }

/* section tab (replaces st.subheader) */
.section {
    border-left: 3px solid var(--line);
    padding-left: 0.9rem;
    margin: 1.6rem 0 0.8rem 0;
}
.section.active { border-left-color: var(--amber); }
.section.passed { border-left-color: var(--teal); }
.section.failed { border-left-color: var(--red); }
.section .label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    margin: 0;
}
.section .title {
    font-size: 1rem;
    font-weight: 500;
    margin: 0.1rem 0 0 0;
}

/* evidence entries */
.evidence {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 0.2rem;
}
.evidence-body {
    font-size: 0.92rem;
    line-height: 1.5;
    color: var(--text);
    margin-bottom: 1.1rem;
}

/* widgets */
.stTextInput input, .stTextArea textarea {
    background: var(--panel) !important;
    border: 1px solid var(--line) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    border-radius: 3px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--amber) !important;
    box-shadow: none !important;
}

.stButton button {
    background: transparent !important;
    border: 1px solid var(--amber) !important;
    color: var(--amber) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    border-radius: 3px !important;
    padding: 0.4rem 1.1rem !important;
    transition: background 0.15s ease;
}
.stButton button:hover {
    background: rgba(232, 179, 57, 0.1) !important;
    color: var(--amber) !important;
}

[data-testid="stRadio"] label {
    font-family: 'IBM Plex Sans', sans-serif !important;
}

pre, code {
    background: #0A0C10 !important;
    border: 1px solid var(--line) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

@keyframes reveal {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fix-panel { animation: reveal 0.35s ease; }
</style>
"""


def status_chip(label, kind):
    return f'<span class="chip {kind}">{label}</span>'


def section(label, title, kind="pending"):
    import streamlit as st
    st.markdown(
        f'<div class="section {kind}"><p class="label">{label}</p>'
        f'<p class="title">{title}</p></div>',
        unsafe_allow_html=True,
    )
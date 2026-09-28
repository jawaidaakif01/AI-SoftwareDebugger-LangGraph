"""
Custom reducers for State fields that multiple paralle nodes write to.
"""

def merge_diagnostics(existing: dict, new_update: dict) -> dict:
    """
    Reduce for the 'diagnostics' field in State.

    Phase 5 runs three parallel nodes (dependency check, static/AST check,
    known-error-pattern check). Each one returns its own diagnosis under a
    distinct sub-key. Without a reducer, LangGraph sees three nodes writing
    to the same `diagnostics` key in the same step and raises
    InvalidUpdateError.
    """

    if existing is None:
        return new_update
    return {**existing, **new_update}